#########################################################################################################################################
# 1- Load the document
#########################################################################################################################################
import pypdf
from langchain_core.documents import Document

PDF_PATH = "Grokking-the-system-design-interview-free.pdf"

reader = pypdf.PdfReader(PDF_PATH)

documents = []

for page_number, page in enumerate(reader.pages):

    # the following text totally ignores figures. Object type is a string.
    text = page.extract_text() or ""                           

    doc = Document(
        page_content=text,
        metadata={
            "source": PDF_PATH,
            "page": page_number + 1
        }
    )

    documents.append(doc)

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
vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)

"""
For a huge document, save it: vector_store.save_local("rag_index"). Then next time you don't embed thousands of chunks again:
vector_store = FAISS.load_local(
    "rag_index",
    embedding_model,
    allow_dangerous_deserialization=True
)

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
query = "This is my first time hearing about twitter. Tell me about it and its functionaly and the way people use it."
query_vector = embedding_model.embed_query(query)

# Under the hood, with LangChain's default FAISS setup, following is a nearest-neighbor search using Euclidean distance.
results = vector_store.similarity_search_by_vector(
    query_vector,
    k=10
)

"""
Now you can print the retrieved results using:

for i, doc in enumerate(results):

    print("=" * 80)

    print("RESULT:", i + 1)
    print("PAGE:", doc.metadata["page"])

    print(doc.page_content[:500])

    
You can do the following to get the score/distance of each chunk too:

results = vector_store.similarity_search_with_score(
    query,
    k=10
)

for i, (doc, score) in enumerate(results):

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

candidate_docs = vector_store.similarity_search(
    query,
    k=10
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
for rank, (doc, score) in enumerate(reranked_docs, start=1):

    print("=" * 80)

    print("Reranked position:", rank)
    print("Reranker score:", score)
    print("Page:", doc.metadata["page"])

    print(doc.page_content[:500])
"""

