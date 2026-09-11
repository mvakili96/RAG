# Exploring RAG

A compact, local pipeline for progressively exploring production RAG concepts over PDF documents.

## Pipeline at a glance

| Component | Implementation |
|---|---|
| **PDF ingestion** | `pypdf` |
| **Chunking** | LangChain recursive text splitting |
| **Dense retrieval** | MiniLM embeddings + `FAISS` IndexFlat (exact k-NN) or HNSW (ANN) |
| **Sparse retrieval** | `BM25` with Qwen-based query expansion |
| **Candidate fusion** | Chunk-ID deduplication |
| **Reranking** | MiniLM cross-encoder |
| **Generation** | `Qwen2.5-7B-Instruct` with source and page citations |
| **Evaluation** | 50-question source-grounded benchmark with deterministic evidence-overlap metrics |

IndexFlat compares the query with every stored vector, while HNSW navigates a graph and trades a small chance of missing the exact nearest chunks for faster search on large indexes. Both return the requested top-k results. An exactly named PDF restricts retrieval to that source; otherwise, the entire corpus is searched.

Retrieval sources belong in `documents/` which is git-ignored. Models, prompts, the query, chunking, and retrieval parameters are defined in `config.yml`. Install dependencies with `pip install -r requirements.txt`, then run `python main.py`.

## Retrieval Sources

- *Computer Vision: Algorithms and Applications* — computer vision methods and applications.
- *Designing Data-Intensive Applications* — scalable and distributed data systems.
- *Grokking the System Design Interview* — practical system-design case studies.
- *LeetCode 4000 Problem Reference* — coding problems, algorithms, and data structures.
- *Probabilistic Machine Learning* — advanced probabilistic modeling and inference.
- *Speech and Language Processing* — NLP, speech, and language models.

## Evaluation Dataset

`evaluation-data/rag_benchmark_v1.jsonl` is a fixed, source-grounded benchmark of 50 answerable and controlled-unanswerable questions. It includes reference answers, atomic facts, exact PDF evidence with physical page numbers, source restrictions, terminology variants, and distractors. It exists to compare retrieval, query-expansion, reranking, and context-coverage changes consistently across experiments.

Run the complete automated evaluation with `python evaluate.py`, or use `python evaluate.py --limit 1` for a small execution check. Evidence text precision and recall deterministically measure normalized word-position overlap with the annotated passages; they do not measure semantic correctness and can miss valid alternative evidence. This repository evaluates RAG retrieval and reranking rather than the final language model response. Generated answers are retained, and answers to the three unanswerable questions are shown in the summary for manual inspection. Each run replaces `summary.md`, `per_question.csv`, and `details.json` in `evaluation-results/`.

## Current limitations

- Figures, table structure, page layout, and scanned text are not parsed.
- Indexes are rebuilt on every run and are not persisted.
- `rank_bm25` scores every chunk rather than using a scalable inverted index.
- No serving API or conversational memory yet.
