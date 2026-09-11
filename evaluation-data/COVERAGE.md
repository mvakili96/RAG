# Coverage Summary and Limitations

All 50 stable-ID examples form one fixed, evaluation-eligible benchmark. There are no development, validation, or held-out splits.

## Audit result

- Reviewed and verified: 50
- Corrected and reverified: 19
- Quarantined: 0
- Answerable: 47
- Controlled unanswerable within allowed sources: 3
- Admissible evidence quotes reverified against original PDFs: 76
- Distractor quotes reverified against original PDFs: 10

All source filenames, one-based physical pages, exact quotes, fact links, evidence groups, source restrictions, answerability labels, and terminology annotations passed the Codex source audit. Corpus SHA-256 hashes and PDF page counts also passed.

## Coverage

- Difficulty: 14 easy, 24 medium, 12 hard.
- Answerable items by source: 8 computer vision, 9 data-intensive systems, 7 system design, 7 LeetCode reference, 9 probabilistic ML, and 7 speech/language processing.
- Primary categories: 8 direct factual lookup, 5 numerical factual lookup, 5 source-specific lookup, 5 technical distinction, 5 multi-fact lookup, 4 multi-passage synthesis, 4 method comparison, 4 limitations/exceptions, 3 method explanation, 3 controlled unanswerable, 2 causal explanation, and 2 conditional claim.
- 18 questions use multiple admissible evidence passages; 9 include verified distractors; 27 include terminology variants.

Coverage includes direct and paraphrased lookup, exact source routing, acronyms and terminology variants, numerical and conditional claims, multi-passage synthesis, misleading near-topic passages, limitations/exceptions, and controlled source-restricted abstention.

## Remaining limitations

- Source verification was performed by Codex, not a human, and does not guarantee correctness.
- The benchmark is intentionally small and cannot represent every topic, query phrasing, terminology variant, or relevant passage in the corpus.
- Evidence is verified against `pypdf` text extraction, not visual page rendering; extraction preserves some source ligatures, line breaks, and hyphenation.
- Figures, tables, diagrams, captions, scanned content, and layout-dependent claims are excluded, reducing coverage of visually presented results.
- Printed labels are advisory; the authoritative citation is the one-based physical PDF page.
- Controlled unanswerability passed complete allowed-source extracted-text audits, but absence of every conceivable paraphrase cannot be guaranteed; those records retain `uncertainty: true`.
- Some supplied material is itself a draft or study reference. The benchmark measures faithfulness to this fixed corpus, not external factual correctness.
- Repeated use of one fixed benchmark can cause benchmark-specific tuning, so reported comparisons must not claim held-out generalization.
