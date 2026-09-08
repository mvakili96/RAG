# Exploring RAG

A compact, local pipeline for progressively exploring production RAG concepts over PDF documents.

The pipeline extracts text with pypdf, recursively chunks it with LangChain, and performs hybrid retrieval using MiniLM embeddings with FAISS plus BM25 with Qwen-based query expansion. It merges and deduplicates candidates, reranks them with a cross-encoder, then uses Qwen to generate an answer with source filenames and page numbers. An exactly named PDF restricts retrieval to that source; otherwise, all documents are searched.

Documents belong in `documents/`. Models, prompts, the query, chunking, and retrieval parameters are defined in `config.yml`. Install dependencies with `pip install -r requirements.txt`, then run `python main.py`.

## Current limitations

- Figures, table structure, page layout, and scanned text are not parsed.
- Indexes are rebuilt on every run and are not persisted.
- FAISS uses exact search rather than an approximate nearest-neighbor index.
- `rank_bm25` scores every chunk rather than using a scalable inverted index.
- No retrieval evaluation, serving API, or conversational memory yet.

