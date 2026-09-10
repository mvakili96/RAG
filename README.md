# Exploring RAG

A compact, local pipeline for progressively exploring production RAG concepts over PDF documents.

The pipeline extracts text with pypdf, recursively chunks it with LangChain, and performs hybrid retrieval using MiniLM embeddings with FAISS plus BM25 with Qwen-based query expansion. It merges and deduplicates candidates, reranks them with a cross-encoder, then uses Qwen to generate an answer with source filenames and page numbers. An exactly named PDF restricts retrieval to that source; otherwise, all documents are searched.

Documents belong in `documents/`. Models, prompts, the query, chunking, and retrieval parameters are defined in `config.yml`. Install dependencies with `pip install -r requirements.txt`, then run `python main.py`.

## Retrieval Sources

- *Computer Vision: Algorithms and Applications* — computer vision methods and applications.
- *Designing Data-Intensive Applications* — scalable and distributed data systems.
- *Grokking the System Design Interview* — practical system-design case studies.
- *LeetCode 4000 Problem Reference* — coding problems, algorithms, and data structures.
- *Probabilistic Machine Learning* — advanced probabilistic modeling and inference.
- *Speech and Language Processing* — NLP, speech, and language models.

## Evaluation Dataset

`evaluation/rag_benchmark_v1.jsonl` is a fixed, source-grounded benchmark of 50 answerable and controlled-unanswerable questions. It includes reference answers, atomic facts, exact PDF evidence with physical page numbers, source restrictions, terminology variants, and distractors. It exists to compare retrieval, query-expansion, reranking, and context-coverage changes consistently across experiments.

Run the complete automated evaluation with `python evaluate.py`, or use `python evaluate.py --limit 1` for a small execution check. Evidence text precision and recall deterministically measure normalized word-position overlap with the annotated passages; they do not measure semantic correctness and can miss valid alternative evidence. This repository evaluates RAG retrieval and reranking rather than the final language model response. Generated answers are retained, and answers to the three unanswerable questions are shown in the summary for manual inspection. Each run replaces `summary.md`, `per_question.csv`, and `details.json` in `evaluation-results/`.

## Current limitations

- Figures, table structure, page layout, and scanned text are not parsed.
- Indexes are rebuilt on every run and are not persisted.
- FAISS uses exact search rather than an approximate nearest-neighbor index.
- `rank_bm25` scores every chunk rather than using a scalable inverted index.
- No serving API or conversational memory yet.
