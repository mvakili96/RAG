# Benchmark Changelog

## 1.1.0 — 2026-09-08

- Re-read all 50 examples against the original PDFs and verified source filenames, one-based physical pages, exact extracted quotes, semantic support, fact mappings, evidence groups, source restrictions, answerability, and terminology annotations.
- Reverified 76 admissible evidence passages and 10 distractor passages; rechecked all six corpus hashes and page counts.
- Corrected and reverified 19 stable-ID records: `ragbench-v1-004`, `005`, `007`, `012`, `016`, `032`, `033`, `034`, `037`, `038`, `040`, `042`, `044`, `045`, `046`, `047`, `048`, `049`, and `050`.
- Corrections narrowed evidence to extractable prose, removed reliance on nearby figures, tables, captions, or displayed formulas, made required facts more atomic, repaired evidence-group mappings, and constrained several answers to exactly what their prose evidence states.
- Audited every physical page of each allowed PDF for the three controlled unanswerable records. One apparent `WER` hit in the computer-vision source was the line-broken surname “Wer-man,” not word error rate; the other recorded searches produced no relevant hits.
- Marked all passing records `reviewed_and_verified` via `codex_source_audit` and eligible for evaluation. Human approval remains separately recorded as not performed.
- Quarantined 0 records. All question IDs were preserved.

## 1.0.0 — 2026-09-08

- Created the 50-question draft benchmark, corpus manifest, schema guide, readable review, and coverage summary.
- Marked all examples as draft pending human review after initial exact-quote verification.
