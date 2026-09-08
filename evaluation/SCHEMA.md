# RAG Benchmark Schema Guide

Schema version: `1.1.0`

`rag_benchmark_v1.jsonl` contains one JSON object per question. All 50 stable IDs form one fixed benchmark for component comparisons and ablations; there are no development, validation, or held-out splits. Results on it must not be described as held-out generalization.

## Record fields

- `schema_version`: Semantic version of the record structure.
- `id`: Stable question ID. The v1.1 source audit preserved `ragbench-v1-001` through `ragbench-v1-050`.
- `question`, `primary_category`, `tags`, `difficulty`: Query text and descriptive labels.
- `allowed_sources`: Exact PDF filenames admissible for answering. Explicit filenames match the exact-name routing behavior in `main.py`.
- `answerability`: `answerable` or `unanswerable_within_allowed_sources`, the expected behavior, rationale, and residual uncertainty.
- `reference_answer`: Gold response containing only claims supported by admissible evidence. For an unanswerable item, it is the required abstention.
- `atomic_required_facts`: Individually scoreable claims with stable fact IDs and supporting evidence IDs.
- `evidence_records`: Admissible passages with stable evidence IDs, exact source filename, one-based physical PDF page, optional printed label, exact `pypdf` quote, fact links, and quote-verification metadata.
- `required_evidence_groups`: Context-coverage logic. Every group is required. Within a group, `any_alternative` means any listed evidence set is sufficient; `within_set_policy: all` means every passage in the chosen set is jointly necessary.
- `terminology_variants`: Source-supported examples for query-expansion analysis, not an exhaustive set of acceptable expansions.
- `verified_distractor_passages`: Optional exact passages that are topically plausible but inadmissible or insufficient, with explanations.
- `unanswerable_audit`: For controlled abstention items, records the allowed-source search scope, terms, reviewed near hits, result, and residual uncertainty.
- `automated_checks`: Exact-quote, mapping, semantic-support, admissibility, answerability, and eligibility results from the source audit.
- `review_status`: `reviewed_and_verified` for records that passed the Codex source audit.
- `review_method`: `codex_source_audit` for this release.
- `evaluation_eligibility`: `eligible` for included records; quarantined records must not be evaluated.
- `review`: Audit date, verifier, available model identification, verification notes, and a separate human-review status.
- `corpus_manifest`: Manifest that pins source bytes, page counts, extractor, and page-number policy.

`reviewed_and_verified` means an AI-performed source audit verified the extracted evidence, mappings, and semantic support. It is not human approval and does not guarantee correctness. Human approval remains a distinct optional field and is `false` in this release; it is not required for evaluation eligibility.

Evidence is anchored to source passages rather than current RAG chunk IDs, so chunk-size experiments do not change the gold labels. Labeled passages are sufficient evidence examples, not a claim that every relevant passage in a book has been enumerated.

## Evaluation mapping

### Query expansion

Use `question`, `tags`, and `terminology_variants` to inspect whether conservative expansions recover source language without retrieval drift. Variants are examples, so an unlisted but valid expansion is not automatically wrong.

### Retrieval and candidate merging

Map chunks by `source` and `pdf_page`, then test whether the merged candidate set covers at least one alternative in every `required_evidence_group`. For explicitly restricted questions, evidence outside `allowed_sources` is inadmissible even if it contains the answer.

### Reranking

Measure whether evidence-bearing chunks survive and move above labeled distractors. Report candidate recall before reranking and evidence-group recall after final top-k separately.

### Context coverage

The assembled context succeeds only when every required evidence group is satisfied. Multiple required groups are jointly necessary for the complete answer; alternatives within a group are interchangeable support.

### Answer quality

Score coverage of `atomic_required_facts`, reject unsupported claims, and verify citations against exact source names and one-based physical `pdf_page` values. For `unanswerable_within_allowed_sources`, success is an explicit insufficiency statement; using a disallowed distractor is a grounding failure.

## Versioning and quarantine

Question IDs remain stable across experiments. Corrections to v1 labels are documented in `CHANGELOG.md`. Future meaning-changing additions should increment the benchmark version rather than silently repurpose an ID. Any unresolved item must be excluded from the main JSONL, recorded as quarantined with a reason, and remain ineligible until it passes a new audit. This release has no quarantined items.

## Corpus manifest

`corpus_manifest_v1.json` records SHA-256, byte size, physical page count, PDF metadata title, extractor version, and page-number policy for each original PDF. A hash mismatch means the run is not using the audited corpus bytes.
