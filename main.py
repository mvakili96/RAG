#########################################################################################################################################
# 1- Load the document
#########################################################################################################################################
import re
from pathlib import Path

import pypdf
from langchain_core.documents import Document

PDF_PATHS = sorted(Path(".").glob("*.pdf"))

if not PDF_PATHS:
    raise FileNotFoundError("No PDF files were found in the current directory.")

query = "What is Hough transform?"


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
# 4- Embed all chunks and create the vector store
#########################################################################################################################################
from langchain_community.vectorstores import FAISS

# LangChain's vector-store abstraction exists to associate embeddings with their original documents and perform similarity search over them.
# When a source was named, chunks contains only that source. Otherwise, it
# contains all chunks from all sources in one global FAISS index.
vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)

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

         
To inspect:

vector = vector_store.index.reconstruct(0)
print(vector)  
index_to_docstore_id = vector_store.index_to_docstore_id[0]
print(index_to_docstore_id)
doc = vector_store.docstore.search(index_to_docstore_id)
print(doc)          
"""

#########################################################################################################################################
# 5- Embed the user's question ourselves and retrieve relevant chunks
#########################################################################################################################################
query_vector = embedding_model.embed_query(query)

# If a source was explicitly named, this searches only its chunks. Otherwise,
# this searches all chunks from all sources.
results_with_scores = vector_store.similarity_search_with_score_by_vector(
    query_vector,
    k=10
)

results_with_scores.sort(key=lambda item: item[1])
results = [doc for doc, _ in results_with_scores[:10]]

"""
Now you can print the retrieved results using:

for i, doc in enumerate(results):

    print("=" * 80)

    print("RESULT:", i + 1)
    print("PAGE:", doc.metadata["page"])

    print(doc.page_content[:500])

    
You can use results_with_scores to get the score/distance of each chunk too:

for i, (doc, score) in enumerate(results_with_scores[:10]):

    print("=" * 80)

    print("Rank:", i + 1)
    print("FAISS distance:", score)
    print("Page:", doc.metadata["page"])
    print(doc.page_content[:300])

"""

#########################################################################################################################################
# 6- Rerank the n candidates
#########################################################################################################################################

"""
the previous retrieval step is optimized for speed, not perfect relevance. FAISS quickly finds chunks whose embeddings are close to the query, but embedding similarity can still return chunks that are only loosely related.

Reranking takes those top candidates and uses a stronger/more expensive model to score them more carefully against the actual query.
"""

from langchain_community.cross_encoders import HuggingFaceCrossEncoder

reranker = HuggingFaceCrossEncoder(
    model_name="cross-encoder/ms-marco-MiniLM-L6-v2"
)

candidate_docs = results

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
for rank, (doc, score) in enumerate(reranked_docs, start=1):

    print("=" * 80)

    print("Reranked position:", rank)
    print("Reranker score:", score)
    print("Page:", doc.metadata["page"])

    print(doc.page_content[:500])
"""

#########################################################################################################################################
# 7- Build the retrieved context
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
# 8- Construct the actual RAG prompt
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
# 9- Load a local LLM and generate the grounded response
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

response = llm.invoke(formatted_prompt)

print(response)
