# RAG Evaluation Summary

Evidence text precision and recall are deterministic normalized word-position overlap against annotated passages. This project evaluates RAG retrieval and reranking rather than the quality of the final language model, so generated answers are not assigned correctness or faithfulness scores. Dataset eligibility is based on automatic source verification, not human review.

- Run timestamp: 2026-09-11T11:53:23.751080+00:00
- Coverage: full verified dataset
- Evaluated questions: 50
- Eligible dataset questions: 50
- Excluded questions: 0 (0 quarantined, 0 unresolved)
- Answer model: `Qwen/Qwen2.5-7B-Instruct`
- Dataset: `evaluation-data/rag_benchmark_v1.jsonl`
- Config: `config.yml`

| Metric | Average | Scored denominator | N/A | Failed/unscored |
|---|---:|---:|---:|---:|
| Evidence text precision | 0.1825 | 47 | 3 | 0 |
| Evidence text recall | 0.7435 | 47 | 3 | 0 |

Averages include scored examples only. N/A and failed/unscored judgments are excluded from each denominator.
Evidence text overlap measures coverage of the specifically annotated passages, not semantic correctness, and may miss valid alternative evidence.

## Pipeline configuration

- Chunk size/overlap: 900 / 200 characters
- Dense FAISS index: `hnsw`
- Dense top-k / BM25 top-k: 10 / 10
- Final reranked top-k: 4
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
- Reranker model: `cross-encoder/ms-marco-MiniLM-L6-v2`

## Generated answers for unanswerable questions

These outputs are included for manual inspection of whether the answer model recognized that the retrieved context was insufficient; they are not scored.

### `ragbench-v1-048`

Question: According to "Computer Vision: Algorithms and Applications.pdf", which word-level edit operations underlie word error rate, and what range exception is noted because insertions are included?

Generated answer:

> The provided document context does not contain enough information to determine which word-level edit operations underlie word error rate or any range exception noted due to insertions being included. The context discusses false positive rate, true positive rate, ROC curves, and document scanning but does not provide details on word error rate or its underlying edit operations. SOURCE: Computer Vision: Algorithms and Applications.pdf, PAGE: 470
>
> The relevant content from PAGE 470 is about ROC curves and their related rates, not word error rate or its underlying edit operations. Therefore, no answer can be given based on the provided context. SOURCE: Computer Vision: Algorithms and Applications.pdf, PAGE: 164
>
> The relevant content from PAGE 164 is about binary image morphology and processing, which is unrelated to word error rate. Thus, the context still does not provide the required information. SOURCE: Computer Vision: Algorithms and Applications.pdf, PAGE: 1206
>
> PAGE 1206 lists various applications of computer vision but does not mention word error rate or its underlying edit operations. Therefore, the context does not contain the necessary information. 
>
> In conclusion, the provided document context does not contain enough information to answer the question regarding word-level edit operations underlying word error rate and any range exception noted because insertions are included. SOURCE: Computer Vision: Algorithms and Applications.pdf, PAGE: 606
>
> PAGE 606 discusses motion estimation techniques like Horn and Schunck's method but does not address word error rate or its underlying edit operations. Hence, the context lacks the required information. 
>
> Therefore, the provided document context does not contain enough information to answer the question. SOURCE: Computer Vision: Algorithms and Applications.pdf, PAGE: 470
>
> The context from PAGE 470 focuses on ROC curves and their related rates, which do not pertain to word error rate or its underlying edit operations. Thus, the context does not provide the necessary information

### `ragbench-v1-049`

Question: According to "Designing Data-Intensive Applications.pdf", how does byte-pair encoding training grow its token vocabulary?

Generated answer:

> The provided document context does not contain enough information. The text discusses data-intensive applications, cloud services, and the concept of evolvability in data systems but does not mention byte-pair encoding or its training process. Therefore, there is no information available to answer the question regarding how byte-pair encoding training grows its token vocabulary. 
>
> SOURCES: Designing Data-Intensive Applications.pdf, PAGES: 1, 3, 15, 44 PAGE: 44 does not contain the required information. PAGE: 15 does not contain the required information. PAGE: 1 does not contain the required information. PAGE: 3 does not contain the required information. PAGE: 44 does not contain the required information. PAGE: 15 does not contain the required information. PAGE: 1 does not contain the required information. PAGE: 3 does not contain the required information. PAGE: 44 does not contain the required information. PAGE: 15 does not contain the required information. PAGE: 1 does not contain the required information. PAGE: 3 does not contain the required information. PAGE: 44 does not contain the required information. PAGE: 15 does not contain the required information. PAGE: 1 does not contain the required information. PAGE: 3 does not contain the required information. PAGE: 44 does not contain the required information. PAGE: 15 does not contain the required information. PAGE: 1 does not contain the required information. PAGE: 3 does not contain the required information. PAGE: 44 does not contain the required information. PAGE: 15 does not contain the required information. PAGE: 1 does not contain the required information. PAGE: 3 does not contain the required information. PAGE: 44 does not contain the required information. PAGE: 15 does not contain the required information. PAGE: 1 does

### `ragbench-v1-050`

Question: According to "Grokking-the-system-design-interview-free.pdf", how do forward and reverse KL differ in mode-covering versus mode-seeking behavior?

Generated answer:

> The provided document context does not contain enough information. The text discusses system design interview preparation and guidelines but does not mention forward and reverse KL or their differences in mode-covering versus mode-seeking behavior. Therefore, no answer can be given based on the provided context. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE: 49
>
> The context provided does not contain any information related to forward and reverse KL or their differences in mode-covering versus mode-seeking behavior. Therefore, the answer cannot be derived from the given sources. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE: 11
>
> The context provided does not contain any information related to forward and reverse KL or their differences in mode-covering versus mode-seeking behavior. Therefore, the answer cannot be derived from the given sources. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE: 8
>
> The context provided does not contain any information related to forward and reverse KL or their differences in mode-covering versus mode-seeking behavior. Therefore, the answer cannot be derived from the given sources. 
>
> In conclusion, the provided document context does not contain enough information to answer the question regarding forward and reverse KL and their differences in mode-covering versus mode-seeking behavior. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE: 11
>
> The provided document context does not contain enough information to answer the question regarding forward and reverse KL and their differences in mode-covering versus mode-seeking behavior. Therefore, the answer cannot be derived from the given sources. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE: 8
>
> The provided document context does not contain enough information to answer the question regarding forward and reverse KL and their differences in mode-covering versus mode-seeking behavior. Therefore, the answer cannot be derived from the given sources. 
>
> In summary, the provided document context does not contain the necessary information to address the question about forward and reverse KL
