#########################################################################################################################################
# 1- Load the document
#########################################################################################################################################
import json
import re
from pathlib import Path

import pypdf
from langchain_core.documents import Document

PDF_PATHS = sorted(Path(".").glob("*.pdf"))

if not PDF_PATHS:
    raise FileNotFoundError("No PDF files were found in the current directory.")

query = "What is Hough transform in the context of computer vision?"


def find_explicit_sources(question, available_sources):
    # Example: according to "Probabilistic Machine Learning.pdf", what is ...?
    mentioned_names = re.findall(
        r"\baccording to\s+(?:the\s+(?:file|document)\s+)?[\"\u201c']([^\"\u201d']+)[\"\u201d']",
        question,
        flags=re.IGNORECASE
    )

    matched_sources = []

    for mentioned_name in mentioned_names:
        for source in available_sources:
            if mentioned_name == source:
                if source not in matched_sources:
                    matched_sources.append(source)

    return matched_sources



selected_sources = find_explicit_sources(
    query,
    [pdf_path.name for pdf_path in PDF_PATHS]
)

if selected_sources:
    print("Source explicitly selected:", ", ".join(selected_sources))
    pdf_paths_to_load = [
        pdf_path
        for pdf_path in PDF_PATHS
        if pdf_path.name in selected_sources
    ]
else:
    print("No source explicitly selected; searching all sources.")
    pdf_paths_to_load = PDF_PATHS

documents = []

for pdf_path in pdf_paths_to_load:
    reader = pypdf.PdfReader(pdf_path)

    for page_number, page in enumerate(reader.pages):

        # the following text totally ignores figures. Object type is a string.
        text = page.extract_text() or ""

        doc = Document(
            page_content=text,
            metadata={
                "source": pdf_path.name,
                "page": page_number + 1
            }
        )

        documents.append(doc)

print(200*"#")
print("DONE with parsing the reference files!")
print(200*"#")
#########################################################################################################################################
# 2- Chunk the document
#########################################################################################################################################
from langchain_text_splitters import RecursiveCharacterTextSplitter

# LangChain's recursive splitter tries paragraph boundaries first, then progressively smaller separators instead of blindly cutting every N characters.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=200,
    add_start_index=True
)

# chunks is a list of chunks. Each chunk has metadata such as page_content, source, page, start_index, and so on.
# Here, start_index means the index of the first character of this chunk corresponds to character start_index of the original pagetext.
chunks = splitter.split_documents(documents)

# This ID is stored in both retrieval systems so the same chunk can be
# recognized and deduplicated after dense and sparse retrieval.
for chunk in chunks:
    chunk.metadata["chunk_id"] = (
        f"{chunk.metadata['source']}::"
        f"page={chunk.metadata['page']}::"
        f"start={chunk.metadata['start_index']}"
    )

#########################################################################################################################################
# 3- Turn chunks into embeddings
#########################################################################################################################################
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={
        "normalize_embeddings": True
    }
)

"""
Analyze and diagnose embeddings:
text = chunks[50].page_content
vector = embedding_model.embed_query(text)

print(type(vector))
print("Embedding dimensions:", len(vector))
print(vector[:10])
"""
#########################################################################################################################################
# 4- Build the dense and sparse retrieval indexes
#########################################################################################################################################
from langchain_community.vectorstores import FAISS
from rank_bm25 import BM25Okapi


def tokenize_for_bm25(text):
    return re.findall(r"[a-z0-9]+", text.lower())

# LangChain's vector-store abstraction exists to associate embeddings with their original documents and perform similarity search over them.
# When a source was named, chunks contains only that source. Otherwise, it
# contains all chunks from all sources in one global FAISS index.
vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)

# Unlike a vector store, BM25 indexes tokenized words(so here, by token, we mean a word) rather than embeddings.
# It is built once during ingestion and reused for every query.
# bm25_corpus is a list of all chunks, each chunk represented with a list of its words as strings
bm25_corpus = [tokenize_for_bm25(chunk.page_content) for chunk in chunks]  
bm25_index = BM25Okapi(bm25_corpus)


"""
For huge documents, the index can be saved with vector_store.save_local(...),
then loaded on later runs so the chunks do not need to be embedded again.

LangChain’s FAISS vector store is like this:
FAISS Vector Store
│
├── index
│   ├── vector 0  → [0.12, -0.43, 0.08, ...]
│   ├── vector 1  → [0.31,  0.17, -0.22, ...]
│   └── vector 2  → [-0.14, 0.52, 0.09, ...]
│
├── index_to_docstore_id
│   ├── 0 → "abc123"
│   ├── 1 → "def456"
│   └── 2 → "ghi789"
│
└── docstore
    ├── "abc123"
    │    ├── page_content: "Machine learning is..."
    │    └── metadata: {page: 1, start_index: 0}
    │
    ├── "def456"
    │    ├── page_content: "Neural networks are..."
    │    └── metadata: {page: 1, start_index: 850}
    │
    └── "ghi789"
         ├── page_content: "Transformers use..."
         └── metadata: {page: 2, start_index: 0}

         
To inspect vector store:

vector = vector_store.index.reconstruct(0)
print(vector)  
index_to_docstore_id = vector_store.index_to_docstore_id[0]
print(index_to_docstore_id)
doc = vector_store.docstore.search(index_to_docstore_id)
print(doc)

To inspect bm25_index:

Following shows all available attributes/methods you can access with bm25_index.something.
print(dir(bm25_index))

Following shows a dict for each chunk, with key being the word inside the chunk and value being the frequency of the word inside the chunk
for freq_dict in bm25_index.doc_freqs:
    print(freq_dict)

bm25_index.idf["draft"] measures each token’s importance across all chunks.
idf = Inverse Document Frequency. It measures how rare a word is across your chunks.
In rank_bm25, roughly:
IDF(t)= log[(N-df(t)+0.5)/(df(t)+0.5)]
where:
N = total number of chunks
df(t) = number of chunks containing that word
So:
word appears in few chunks → high IDF → more informative
word appears in many chunks → low IDF → less informative

bm25_index.get_scores(query_tokens) → BM25 score for every chunk for a query.
rank_bm25.get_scores() effectively scores every chunk in doc_freqs. So it is brute-force over the corpus rather than using an inverted index.
For each query word and each chunk, BM25 combines:
score = IDF(q) * TF(q,d)*(k_1+1) / (TF(q,d)+k_1(1-b+b*|d|/avgdl))
where:
IDF(q) = how rare the query word is across chunks
TF(q,d) = how many times it occurs in that chunk
|d| = chunk length
avgdl = average chunk length
Then it adds the scores for all query words. So for a query, it's key/important/rare words already contribute a lot
to the aggregate score, whereas the common words add only a bit. 
Therefore, LLM for matching is mainly used for extracting synonyms, rather than localizing keywords
One limitation of BM25 is its unawareness about a combo of keywords like "neural radiance field", even though it
handles all its rare words.
"""

#########################################################################################################################################
# 5- Load a local LLM and expand the query for BM25
#########################################################################################################################################
from langchain_huggingface import HuggingFacePipeline
from transformers import GenerationConfig


generation_config = GenerationConfig.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct"
)

generation_config.max_new_tokens = 400
generation_config.do_sample = False

# These only matter when sampling is enabled
generation_config.temperature = None
generation_config.top_p = None
generation_config.top_k = None

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",

    pipeline_kwargs={
        "generation_config": generation_config,
        "return_full_text": False,
    },

    device_map="auto",
)

expansion_prompt = f"""
Extract conservative search terms for BM25 retrieval from the user query.

Return ONLY valid JSON with this exact structure:
{{
  "key_terms": ["up to 6 main technical terms"],
  "acronyms": ["up to 4 relevant acronyms"],
  "variations": ["2 to 4 close synonyms or common wording variations"]
}}

Do not answer the query. Do not add broader or merely related topics.

USER QUERY:
{query}
"""

expansion_response = llm.invoke(
    expansion_prompt,
    pipeline_kwargs={"max_new_tokens": 120}
)
json_start = expansion_response.find("{")

try:
    # raw_decode reads the first complete JSON object and ignores any text the
    # LLM may have generated after it.
    parsed_expansion, _ = json.JSONDecoder().raw_decode(
        expansion_response[json_start:]
    ) if json_start != -1 else ({}, 0)
except json.JSONDecodeError:
    parsed_expansion = {}

if not isinstance(parsed_expansion, dict):
    parsed_expansion = {}


def keep_conservative_terms(values, maximum):
    kept_terms = []
    seen_terms = set()

    if not isinstance(values, list):
        return kept_terms

    for value in values:
        if not isinstance(value, str):
            continue

        term = value.strip()
        normalized_term = term.lower()

        if term and len(term) <= 80 and normalized_term not in seen_terms:
            kept_terms.append(term)
            seen_terms.add(normalized_term)

    return kept_terms[:maximum]


query_expansion = {
    "key_terms": keep_conservative_terms(parsed_expansion.get("key_terms"), 6),
    "acronyms": keep_conservative_terms(parsed_expansion.get("acronyms"), 4),
    "variations": keep_conservative_terms(parsed_expansion.get("variations"), 4)
}

expanded_terms = (
    query_expansion["key_terms"]
    + query_expansion["acronyms"]
    + query_expansion["variations"]
)
expanded_query = " ".join([query, *expanded_terms])


# print("\nEXPANDED QUERY TERMS")
# print(json.dumps(query_expansion, indent=2, ensure_ascii=False))
# print("BM25 query:", expanded_query)

#########################################################################################################################################
# 6- Retrieve dense and sparse candidates, then merge them
#########################################################################################################################################
query_vector = embedding_model.embed_query(query)

# If a source was explicitly named, this searches only its chunks. Otherwise,
# this searches all chunks from all sources.
dense_results_with_scores = vector_store.similarity_search_with_score_by_vector(
    query_vector,
    k=10
)
dense_results_with_scores.sort(key=lambda item: item[1])
dense_candidate_docs = [doc for doc, _ in dense_results_with_scores]

bm25_query_tokens = list(dict.fromkeys(tokenize_for_bm25(expanded_query)))
bm25_scores = bm25_index.get_scores(bm25_query_tokens)
top_bm25_indices = bm25_scores.argsort()[::-1][:10]
bm25_results_with_scores = [
    (chunks[index], float(bm25_scores[index]))
    for index in top_bm25_indices
    if bm25_scores[index] > 0
]
bm25_candidate_docs = [doc for doc, _ in bm25_results_with_scores]

"""
print("\nBM25 CANDIDATES")
for rank, (doc, score) in enumerate(bm25_results_with_scores, start=1):
    print(
        f"{rank}. score={score:.4f} | {doc.metadata['chunk_id']} | "
        f"{doc.page_content[:200].replace(chr(10), ' ')}"
    )

print("\nDENSE CANDIDATES")
for rank, (doc, score) in enumerate(dense_results_with_scores, start=1):
    print(
        f"{rank}. distance={score:.4f} | {doc.metadata['chunk_id']} | "
        f"{doc.page_content[:200].replace(chr(10), ' ')}"
    )
"""

candidate_docs = []
candidate_methods = {}

for retrieval_method, retrieved_docs in (
    ("dense", dense_candidate_docs),
    ("BM25", bm25_candidate_docs)
):
    for doc in retrieved_docs:
        chunk_id = doc.metadata["chunk_id"]

        if chunk_id not in candidate_methods:
            candidate_docs.append(doc)
            candidate_methods[chunk_id] = []

        candidate_methods[chunk_id].append(retrieval_method)

"""
print("\nMERGED CANDIDATES")
for rank, doc in enumerate(candidate_docs, start=1):
    methods = ", ".join(candidate_methods[doc.metadata["chunk_id"]])
    print(
        f"{rank}. retrieved_by={methods} | {doc.metadata['chunk_id']} | "
        f"{doc.page_content[:200].replace(chr(10), ' ')}"
    )


Now you can print the retrieved results using:

for i, doc in enumerate(dense_candidate_docs):

    print("=" * 80)

    print("RESULT:", i + 1)
    print("PAGE:", doc.metadata["page"])

    print(doc.page_content[:500])

    
You can use dense_results_with_scores to get the score/distance of each chunk too:

for i, (doc, score) in enumerate(dense_results_with_scores):

    print("=" * 80)

    print("Rank:", i + 1)
    print("FAISS distance:", score)
    print("Page:", doc.metadata["page"])
    print(doc.page_content[:300])

"""

#########################################################################################################################################
# 7- Rerank the n candidates
#########################################################################################################################################

"""
the previous retrieval step is optimized for speed, not perfect relevance. FAISS quickly finds chunks whose embeddings are close to the query, but embedding similarity can still return chunks that are only loosely related.

Reranking takes those top candidates and uses a stronger/more expensive model to score them more carefully against the actual query.
"""

from langchain_community.cross_encoders import HuggingFaceCrossEncoder

reranker = HuggingFaceCrossEncoder(
    model_name="cross-encoder/ms-marco-MiniLM-L6-v2"
)

pairs = [
    (query, doc.page_content)
    for doc in candidate_docs
]

rerank_scores = reranker.score(pairs)

scored_docs = list(
    zip(candidate_docs, rerank_scores)
)

scored_docs.sort(
    key=lambda x: x[1],
    reverse=True
)

reranked_docs = scored_docs[:4]

"""
print("\nRERANKED RESULTS")
for rank, (doc, score) in enumerate(reranked_docs, start=1):
    print(
        f"{rank}. score={score:.4f} | {doc.metadata['chunk_id']} | "
        f"{doc.page_content[:500].replace(chr(10), ' ')}"
    )
"""

"""
for rank, (doc, score) in enumerate(reranked_docs, start=1):

    print("=" * 80)

    print("Reranked position:", rank)
    print("Reranker score:", score)
    print("Page:", doc.metadata["page"])

    print(doc.page_content[:500])
"""

#########################################################################################################################################
# 8- Build the retrieved context
#########################################################################################################################################

context_parts = []

for doc, score in reranked_docs:

    source = doc.metadata["source"]
    page = doc.metadata["page"]

    context_parts.append(
        f"""
SOURCE: {source}, PAGE: {page}

{doc.page_content}
"""
    )

context = "\n\n---\n\n".join(context_parts)

# print(context)

#########################################################################################################################################
# 9- Construct the actual RAG prompt
#########################################################################################################################################

from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate.from_template(
"""
You are answering questions about a collection of documents.

Rules:
    - Use ONLY the provided context to answer the question.

    - If the answer cannot be determined from the context,
    say that the provided document context does not contain
    enough information. Otherwise, answer with explicitly naming the SOURCES and their PAGES from the CONTEXT.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
)

formatted_prompt = rag_prompt.format(
    context=context,
    question=query
)

# print(formatted_prompt)

#########################################################################################################################################
# 10- Generate the grounded response with the already-loaded LLM
#########################################################################################################################################
response = llm.invoke(formatted_prompt)

print(response)
