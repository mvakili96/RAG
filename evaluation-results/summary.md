# RAG Evaluation Summary

Evidence text precision and recall are deterministic normalized word-position overlap against annotated passages. This project evaluates RAG retrieval and reranking rather than the quality of the final language model, so generated answers are not assigned correctness or faithfulness scores. Dataset eligibility is based on automatic source verification, not human review.

- Run timestamp: 2026-09-26T00:23:06.958158+00:00
- Coverage: full verified dataset
- Evaluated questions: 50
- Eligible dataset questions: 50
- Excluded questions: 0 (0 quarantined, 0 unresolved)
- Answer model: `Qwen/Qwen2.5-7B-Instruct`
- Dataset: `evaluation-data/rag_benchmark_v1.jsonl`
- Config: `config.yml`

| Metric | Average | Scored denominator | N/A | Failed/unscored |
|---|---:|---:|---:|---:|
| Evidence text precision | 0.1655 | 47 | 3 | 0 |
| Evidence text recall | 0.6112 | 47 | 3 | 0 |

Averages include scored examples only. N/A and failed/unscored judgments are excluded from each denominator.
Evidence text overlap measures coverage of the specifically annotated passages, not semantic correctness, and may miss valid alternative evidence.

## Pipeline configuration

- Indexing mode: `load`
- Persisted index directory: `index-data`
- Dense retrieval enabled: `True`
- BM25 retrieval enabled: `False`
- Query expansion enabled: `True`
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

> The provided document context does not contain enough information to determine which word-level edit operations underlie word error rate or any range exception noted because insertions are included. The context mentions error rates like accuracy, false negatives, false positives, precision, recall, ROC curve, true negatives, and true positives but does not provide details on word error rate or its associated edit operations. Therefore, based solely on the given information, no specific answer can be provided. SOURCE: Computer Vision: Algorithms and Applications.pdf, PAGE: 1212. PAGE: 164. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE: 242. PAGE: 1212. PAGE: 1214. PAGE

### `ragbench-v1-049`

Question: According to "Designing Data-Intensive Applications.pdf", how does byte-pair encoding training grow its token vocabulary?

Generated answer:

> The provided document context does not contain enough information. The text discusses encoding methods like serialization, deserialization, and specific protocols such as Thrift's CompactProtocol and Protocol Buffers, but it does not mention anything about byte-pair encoding training or vocabulary growth. Therefore, I cannot determine how byte-pair encoding training grows its token vocabulary based on the given context. SOURCE: N/A, PAGE: N/A
> ```

### `ragbench-v1-050`

Question: According to "Grokking-the-system-design-interview-free.pdf", how do forward and reverse KL differ in mode-covering versus mode-seeking behavior?

Generated answer:

> The provided document context does not contain enough information to determine how forward and reverse proxies differ in mode-covering versus mode-seeking behavior. The context describes the basic functionalities of transparent, reverse, and open proxies, but does not provide details on their mode-covering or mode-seeking behaviors. Therefore, based solely on the given information, no specific answer can be provided regarding the difference in these behaviors between forward and reverse proxies. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE: 184-183
>
> The context provided does not include specific information about the mode-covering versus mode-seeking behavior of forward and reverse proxies. It describes the basic functionalities of different types of proxies, including reverse proxies which retrieve resources on behalf of a client from one or more servers and return them to the client as if they originated from the proxy server itself. However, it does not detail the operational modes or behaviors related to covering or seeking actions for these types of proxies. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE: 184-183
>
> The document does not specify the mode-covering or mode-seeking behaviors for either forward or reverse proxies. It provides definitions and descriptions of various proxy types, including reverse proxies which act on behalf of clients to retrieve resources from servers, but does not delve into the operational modes or behaviors related to covering or seeking actions for these proxies. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE: 184-183
>
> The context does not provide information on the mode-covering versus mode-seeking behavior of forward and reverse proxies. It explains that a reverse proxy retrieves resources on behalf of a client from one or more servers and returns them to the client as if they originated from the proxy server itself, but it does not discuss the operational modes or behaviors related to covering or seeking actions for these proxies. SOURCE: Grokking-the-system-design-interview-free.pdf, PAGE:
