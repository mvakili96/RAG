import argparse
import csv
import json
import os
import re
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import yaml

from main import RAGPipeline, find_explicit_sources


CONFIG_PATH = Path("config.yml")


def evidence_words_with_spans(text):
    words = []
    for match in re.finditer(r"\w+(?:['\u2019]\w+)*", text):
        word = unicodedata.normalize("NFKC", match.group()).casefold()
        if words and re.fullmatch(
            r"[\-\u00ad\u2010\u2011][\t ]*\r?\n[\t ]*",
            text[words[-1]["raw_end"] : match.start()],
        ):
            words[-1]["word"] += word
            words[-1]["raw_end"] = match.end()
        else:
            words.append(
                {
                    "word": word,
                    "raw_start": match.start(),
                    "raw_end": match.end(),
                }
            )
    return words


def words_for_evidence_mapping(text):
    return [word["word"] for word in evidence_words_with_spans(text)]


def map_passage_to_page(passage, source, page, passage_id, page_texts):
    page_key = (source, page)
    details = {
        "passage_id": passage_id,
        "source": source,
        "page": page,
    }
    if page_key not in page_texts:
        details.update({"mapping_status": "failed", "mapping_error": "Source/page was not loaded."})
        return details, set()

    page_words = words_for_evidence_mapping(page_texts[page_key])
    passage_words = words_for_evidence_mapping(passage)
    details["word_count"] = len(passage_words)
    if not passage_words:
        details.update({"mapping_status": "failed", "mapping_error": "Passage has no words."})
        return details, set()

    length = len(passage_words)
    starts = [
        start
        for start in range(len(page_words) - length + 1)
        if page_words[start : start + length] == passage_words
    ]
    if not starts:
        details.update(
            {"mapping_status": "failed", "mapping_error": "No consecutive normalized match."}
        )
        return details, set()
    if len(starts) > 1:
        details.update(
            {
                "mapping_status": "ambiguous",
                "mapping_error": f"Found {len(starts)} consecutive normalized matches.",
                "candidate_page_word_starts": [start + 1 for start in starts],
            }
        )
        return details, set()

    start = starts[0]
    details.update(
        {
            "mapping_status": "mapped",
            "page_word_start": start + 1,
            "page_word_end": start + length,
        }
    )
    positions = {(source, page, position) for position in range(start, start + length)}
    return details, positions


def map_chunk_to_page(chunk, page_texts):
    source = chunk.get("source")
    page = chunk.get("page")
    chunk_id = chunk.get("chunk_id", "<missing chunk_id>")
    start = chunk.get("start_index")
    text = chunk.get("text")
    details = {
        "chunk_id": chunk_id,
        "source": source,
        "page": page,
        "character_start": start,
    }
    page_key = (source, page)
    if page_key not in page_texts:
        details.update({"mapping_status": "failed", "mapping_error": "Source/page was not loaded."})
        return details, set()
    if not isinstance(start, int) or not isinstance(text, str):
        details.update(
            {
                "mapping_status": "failed",
                "mapping_error": "Chunk has no valid start_index or text.",
            }
        )
        return details, set()

    page_text = page_texts[page_key]
    end = start + len(text)
    details["character_end_exclusive"] = end
    if start < 0 or end > len(page_text) or page_text[start:end] != text:
        details.update(
            {
                "mapping_status": "failed",
                "mapping_error": "Chunk text does not equal its declared PDF-page character slice.",
            }
        )
        return details, set()

    page_words = evidence_words_with_spans(page_text)
    contained_positions = [
        position
        for position, word in enumerate(page_words)
        if word["raw_start"] >= start and word["raw_end"] <= end
    ]
    if not contained_positions:
        details.update(
            {
                "mapping_status": "failed",
                "mapping_error": "Chunk contains no complete normalized page words.",
            }
        )
        return details, set()

    boundary_fragments = []
    for position, word in enumerate(page_words):
        intersects_chunk = word["raw_end"] > start and word["raw_start"] < end
        fully_contained = word["raw_start"] >= start and word["raw_end"] <= end
        if intersects_chunk and not fully_contained:
            fragment_start = max(start, word["raw_start"])
            fragment_end = min(end, word["raw_end"])
            boundary_fragments.append(
                {
                    "page_word_position": position + 1,
                    "normalized_page_word": word["word"],
                    "chunk_fragment": page_text[fragment_start:fragment_end],
                }
            )

    details.update(
        {
            "word_count": len(contained_positions),
            "mapping_status": "mapped",
            "mapping_method": "verified_character_offsets",
            "page_word_start": contained_positions[0] + 1,
            "page_word_end": contained_positions[-1] + 1,
            "excluded_boundary_fragments": boundary_fragments,
        }
    )
    positions = {(source, page, position) for position in contained_positions}
    return details, positions


def load_dataset(path):
    records = []
    seen_ids = set()

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid dataset JSON on line {line_number}: {error}") from error

            question_id = record.get("id")
            if not isinstance(question_id, str) or not question_id:
                raise ValueError(f"Dataset line {line_number} has no valid ID.")
            if question_id in seen_ids:
                raise ValueError(f"Duplicate dataset ID: {question_id}")

            seen_ids.add(question_id)
            records.append(record)

    return records


def record_is_quarantined(record):
    statuses = [
        record.get("evaluation_eligibility", ""),
        record.get("review_status", ""),
        record.get("review", {}).get("status", ""),
    ]
    return any("quarantin" in str(status).lower() for status in statuses)


def record_is_eligible(record):
    review_status = record.get("review_status") or record.get("review", {}).get("status")
    review_method = (
        record.get("review_method")
        or record.get("review", {}).get("review_method")
        or record.get("review", {}).get("method")
    )
    eligibility = record.get("evaluation_eligibility", "eligible")

    return (
        review_status == "reviewed_and_verified"
        and review_method == "codex_source_audit"
        and eligibility == "eligible"
        and not record_is_quarantined(record)
    )


def unscored_metric(reason, attempts=None):
    result = {"status": "unscored", "score": None, "explanation": reason}
    if attempts is not None:
        result["attempts"] = attempts
    return result


def evidence_text_metrics(record, final_chunks, page_texts):
    evidence_records = record.get("evidence_records", [])
    answerability = record.get("answerability", {}).get("label")
    if answerability == "unanswerable_within_allowed_sources" and not evidence_records:
        reason = "N/A for an unanswerable question without positive reference evidence."
        metric = {
            "status": "not_applicable",
            "score": None,
            "matched_word_count": None,
            "total_word_count": None,
            "explanation": reason,
        }
        return dict(metric), dict(metric)

    if not isinstance(evidence_records, list) or not evidence_records:
        reason = "No positive reference-evidence passages are available for text-overlap mapping."
        metric = {
            "status": "unscored",
            "score": None,
            "matched_word_count": None,
            "total_word_count": None,
            "explanation": reason,
            "mapping_failures": [{"mapping_error": reason}],
        }
        return dict(metric), dict(metric)

    allowed_sources = set(record.get("allowed_sources", []))
    reference_mappings = []
    reference_positions = []
    mapping_failures = []
    for evidence in evidence_records:
        evidence_id = evidence.get("evidence_id", "<missing evidence_id>")
        source = evidence.get("source")
        page = evidence.get("pdf_page")
        quote = evidence.get("exact_quote")
        if source not in allowed_sources:
            details = {
                "evidence_id": evidence_id,
                "source": source,
                "page": page,
                "mapping_status": "failed",
                "mapping_error": "Reference evidence source is outside allowed_sources.",
            }
            positions = set()
        elif not isinstance(quote, str) or not isinstance(source, str) or not isinstance(page, int):
            details = {
                "evidence_id": evidence_id,
                "source": source,
                "page": page,
                "mapping_status": "failed",
                "mapping_error": "Reference evidence has invalid source, page, or quote fields.",
            }
            positions = set()
        else:
            details, positions = map_passage_to_page(
                quote,
                source,
                page,
                evidence_id,
                page_texts,
            )
            details["evidence_id"] = details.pop("passage_id")
        reference_mappings.append(details)
        reference_positions.append((evidence_id, positions))
        if details["mapping_status"] != "mapped":
            mapping_failures.append(details)

    if mapping_failures:
        reason = "Reference-evidence mapping failed or was ambiguous; overlap metrics were not scored."
        metric = {
            "status": "unscored",
            "score": None,
            "matched_word_count": None,
            "total_word_count": None,
            "explanation": reason,
            "mapping_failures": mapping_failures,
        }
        precision = dict(metric)
        recall = dict(metric)
        recall["mapped_reference_passages"] = reference_mappings
        return precision, recall

    reference_union = set().union(*(positions for _, positions in reference_positions))
    if not final_chunks:
        precision = {
            "status": "not_applicable",
            "score": None,
            "matched_word_count": 0,
            "total_word_count": 0,
            "explanation": "N/A because the final context contains no chunk body text.",
            "mapped_context_chunks": [],
        }
        recall = {
            "status": "scored",
            "score": 0.0,
            "matched_word_count": 0,
            "total_word_count": len(reference_union),
            "explanation": (
                f"0 of {len(reference_union)} unique reference-evidence word positions were covered."
            ),
            "mapped_reference_passages": reference_mappings,
        }
        return precision, recall

    context_mappings = []
    context_positions = []
    for chunk in final_chunks:
        details, positions = map_chunk_to_page(chunk, page_texts)
        context_mappings.append(details)
        context_positions.append((details["chunk_id"], positions))
        if details["mapping_status"] != "mapped":
            mapping_failures.append(details)

    if mapping_failures:
        reason = "Final-context mapping failed or was ambiguous; overlap metrics were not scored."
        metric = {
            "status": "unscored",
            "score": None,
            "matched_word_count": None,
            "total_word_count": None,
            "explanation": reason,
            "mapping_failures": mapping_failures,
        }
        precision = dict(metric)
        recall = dict(metric)
        precision["mapped_context_chunks"] = context_mappings
        recall["mapped_reference_passages"] = reference_mappings
        return precision, recall

    context_union = set().union(*(positions for _, positions in context_positions))
    overlap = reference_union & context_union

    for details, (_, positions) in zip(context_mappings, context_positions):
        details["reference_overlap_word_count"] = len(positions & reference_union)
        details["overlapping_evidence_ids"] = [
            evidence_id
            for evidence_id, evidence_position_set in reference_positions
            if positions & evidence_position_set
        ]
    for details, (_, positions) in zip(reference_mappings, reference_positions):
        details["covered_word_count"] = len(positions & context_union)
        details["overlapping_chunk_ids"] = [
            chunk_id
            for chunk_id, chunk_position_set in context_positions
            if positions & chunk_position_set
        ]

    precision = {
        "status": "scored",
        "score": len(overlap) / len(context_union),
        "matched_word_count": len(overlap),
        "total_word_count": len(context_union),
        "explanation": (
            f"{len(overlap)} of {len(context_union)} unique final-context body-word positions "
            "overlapped the annotated reference evidence."
        ),
        "mapped_context_chunks": context_mappings,
    }
    recall = {
        "status": "scored",
        "score": len(overlap) / len(reference_union),
        "matched_word_count": len(overlap),
        "total_word_count": len(reference_union),
        "explanation": (
            f"{len(overlap)} of {len(reference_union)} unique reference-evidence word positions "
            "were covered by the final context."
        ),
        "mapped_reference_passages": reference_mappings,
    }
    return precision, recall


def evaluate_question(record, pipeline_output, page_texts):
    final_chunks = pipeline_output["final_chunks"]
    precision, recall = evidence_text_metrics(record, final_chunks, page_texts)

    return {
        "evidence_text_precision": precision,
        "evidence_text_recall": recall,
    }


def metric_summary(question_results, metric):
    results = [result["metrics"][metric] for result in question_results]
    scores = [result["score"] for result in results if result["status"] == "scored"]
    return {
        "average": sum(scores) / len(scores) if scores else None,
        "scored": len(scores),
        "not_applicable": sum(result["status"] == "not_applicable" for result in results),
        "unscored": sum(result["status"] == "unscored" for result in results),
    }


def metric_cell(metric):
    if metric["status"] == "scored":
        return f"{metric['score']:.6f}"
    if metric["status"] == "not_applicable":
        return "N/A"
    return "UNSCORED"


def write_outputs_safely(results_dir, details, summary_text, question_results):
    results_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=".evaluation-results-", dir=results_dir.parent))

    try:
        (temporary_dir / "summary.md").write_text(summary_text, encoding="utf-8")
        (temporary_dir / "details.json").write_text(
            json.dumps(details, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        with (temporary_dir / "per_question.csv").open("w", encoding="utf-8", newline="") as file:
            fieldnames = ["question_id", "question", "reference_answer", "generated_answer"]
            for metric in (
                "evidence_text_precision",
                "evidence_text_recall",
            ):
                fieldnames.extend([f"{metric}_score", f"{metric}_status", f"{metric}_explanation"])
                if metric.startswith("evidence_text_"):
                    fieldnames.extend(
                        [f"{metric}_matched_words", f"{metric}_total_words"]
                    )

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for result in question_results:
                row = {
                    "question_id": result["id"],
                    "question": result["question"],
                    "reference_answer": result["reference_answer"],
                    "generated_answer": result.get("generated_answer", ""),
                }
                for metric_name, metric in result["metrics"].items():
                    row[f"{metric_name}_score"] = metric_cell(metric)
                    row[f"{metric_name}_status"] = metric["status"]
                    row[f"{metric_name}_explanation"] = metric["explanation"]
                    if metric_name.startswith("evidence_text_"):
                        row[f"{metric_name}_matched_words"] = metric.get("matched_word_count")
                        row[f"{metric_name}_total_words"] = metric.get("total_word_count")
                writer.writerow(row)

        results_dir.mkdir(parents=True, exist_ok=True)
        for filename in ("summary.md", "per_question.csv", "details.json"):
            os.replace(temporary_dir / filename, results_dir / filename)
        temporary_dir.rmdir()
    except Exception:
        print(
            f"Evaluation aborted before all result files were replaced. Any existing files in "
            f"{results_dir} may belong to the previous completed run.",
            file=sys.stderr,
        )
        raise


def build_summary(run, dataset_counts, metric_summaries, question_results):
    lines = [
        "# RAG Evaluation Summary",
        "",
        "Evidence text precision and recall are deterministic normalized word-position overlap "
        "against annotated passages. This project evaluates RAG retrieval and reranking rather "
        "than the quality of the final language model, so generated answers are not assigned "
        "correctness or faithfulness scores. Dataset eligibility is based on automatic source "
        "verification, not human review.",
        "",
        f"- Run timestamp: {run['timestamp_utc']}",
        f"- Coverage: {'full verified dataset' if run['full_dataset'] else 'subset'}",
        f"- Evaluated questions: {run['evaluated_questions']}",
        f"- Eligible dataset questions: {dataset_counts['eligible']}",
        f"- Excluded questions: {dataset_counts['excluded']} "
        f"({dataset_counts['quarantined']} quarantined, {dataset_counts['unresolved']} unresolved)",
        f"- Answer model: `{run['model_id']}`",
        f"- Dataset: `{run['dataset_path']}`",
        f"- Config: `{run['config_path']}`",
        "",
        "| Metric | Average | Scored denominator | N/A | Failed/unscored |",
        "|---|---:|---:|---:|---:|",
    ]

    labels = {
        "evidence_text_precision": "Evidence text precision",
        "evidence_text_recall": "Evidence text recall",
    }
    for metric, values in metric_summaries.items():
        average = f"{values['average']:.4f}" if values["average"] is not None else "N/A"
        lines.append(
            f"| {labels[metric]} | {average} | {values['scored']} | "
            f"{values['not_applicable']} | {values['unscored']} |"
        )

    lines.extend([
        "",
        "Averages include scored examples only. N/A and failed/unscored judgments are excluded from each denominator.",
        "Evidence text overlap measures coverage of the specifically annotated passages, not semantic "
        "correctness, and may miss valid alternative evidence.",
        "",
        "## Pipeline configuration",
        "",
        f"- Chunk size/overlap: {run['chunk_size']} / {run['chunk_overlap']} characters",
        f"- Dense FAISS index: `{run['dense_index_type']}`",
        f"- Dense top-k / BM25 top-k: {run['dense_top_k']} / {run['bm25_top_k']}",
        f"- Final reranked top-k: {run['final_top_k']}",
        f"- Embedding model: `{run['embedding_model']}`",
        f"- Reranker model: `{run['reranker_model']}`",
        "",
    ])

    unanswerable_results = [
        result
        for result in question_results
        if result.get("answerability", {}).get("label")
        == "unanswerable_within_allowed_sources"
    ]
    if unanswerable_results:
        lines.extend([
            "## Generated answers for unanswerable questions",
            "",
            "These outputs are included for manual inspection of whether the answer model "
            "recognized that the retrieved context was insufficient; they are not scored.",
            "",
        ])
        for result in unanswerable_results:
            lines.extend([
                f"### `{result['id']}`",
                "",
                f"Question: {result['question']}",
                "",
                "Generated answer:",
                "",
            ])
            answer = result.get("generated_answer", "").strip() or "(No answer was generated.)"
            lines.extend(f"> {line}" if line else ">" for line in answer.splitlines())
            lines.append("")

    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate the local RAG pipeline.")
    parser.add_argument(
        "--limit",
        type=int,
        help="Evaluate only the first N eligible examples for a small execution check.",
    )
    args = parser.parse_args()
    if args.limit is not None and args.limit <= 0:
        parser.error("--limit must be a positive integer")
    return args


def main():
    args = parse_args()
    with CONFIG_PATH.open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    evaluation_config = config["evaluation"]
    dataset_path = Path(evaluation_config["dataset_path"])
    results_dir = Path(evaluation_config["results_dir"])
    all_records = load_dataset(dataset_path)
    eligible_records = [record for record in all_records if record_is_eligible(record)]
    quarantined_count = sum(record_is_quarantined(record) for record in all_records)
    excluded_count = len(all_records) - len(eligible_records)
    dataset_counts = {
        "total": len(all_records),
        "eligible": len(eligible_records),
        "excluded": excluded_count,
        "quarantined": quarantined_count,
        "unresolved": excluded_count - quarantined_count,
    }

    selected_records = eligible_records[: args.limit] if args.limit else eligible_records
    if not selected_records:
        raise ValueError("No eligible evaluation examples were selected.")

    all_pdf_paths = sorted(Path(".").glob(config["documents"]["pdf_glob"]))
    if not all_pdf_paths:
        raise FileNotFoundError("No PDF files were found.")
    all_source_names = [path.name for path in all_pdf_paths]

    required_source_names = set()
    for record in selected_records:
        explicit = find_explicit_sources(record["question"], all_source_names)
        if explicit:
            required_source_names.update(explicit)
        else:
            required_source_names.update(all_source_names)
    pdf_paths = [path for path in all_pdf_paths if path.name in required_source_names]

    print(
        f"Loading the pipeline for {len(selected_records)} "
        f"{'subset' if args.limit else 'full-dataset'} question(s)...",
        flush=True,
    )
    pipeline = RAGPipeline(config, pdf_paths)

    question_results = []
    for index, record in enumerate(selected_records, start=1):
        print(f"[{index}/{len(selected_records)}] {record['id']}", flush=True)
        result = {
            "id": record["id"],
            "question": record["question"],
            "reference_answer": record["reference_answer"],
            "required_facts": record.get("atomic_required_facts", []),
            "reference_evidence": record.get("evidence_records", []),
            "required_evidence_groups": record.get("required_evidence_groups", []),
            "answerability": record.get("answerability"),
            "allowed_sources": record.get("allowed_sources", []),
            "errors": [],
        }
        try:
            pipeline_output = pipeline.run(record["question"])
            result.update(pipeline_output)
            result["metrics"] = evaluate_question(
                record,
                pipeline_output,
                pipeline.page_texts,
            )
        except Exception as error:
            reason = f"Pipeline call failed: {type(error).__name__}: {error}"
            result["errors"].append(reason)
            result["generated_answer"] = ""
            result["final_context"] = ""
            result["final_chunks"] = []
            result["metrics"] = {
                metric: unscored_metric(reason)
                for metric in (
                    "evidence_text_precision",
                    "evidence_text_recall",
                )
            }
            for metric in ("evidence_text_precision", "evidence_text_recall"):
                result["metrics"][metric]["matched_word_count"] = None
                result["metrics"][metric]["total_word_count"] = None
        question_results.append(result)

    metric_names = (
        "evidence_text_precision",
        "evidence_text_recall",
    )
    metric_summaries = {
        metric: metric_summary(question_results, metric) for metric in metric_names
    }
    run = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "full_dataset": args.limit is None,
        "requested_limit": args.limit,
        "evaluated_questions": len(selected_records),
        "model_id": config["llm"]["model_id"],
        "dataset_path": str(dataset_path),
        "config_path": str(CONFIG_PATH),
        "embedding_model": config["embedding"]["model_name"],
        "reranker_model": config["reranking"]["model_name"],
        "chunk_size": config["chunking"]["chunk_size"],
        "chunk_overlap": config["chunking"]["chunk_overlap"],
        "dense_index_type": config["retrieval"]["dense_index_type"],
        "dense_top_k": config["retrieval"]["dense_top_k"],
        "bm25_top_k": config["retrieval"]["bm25_top_k"],
        "final_top_k": config["reranking"]["final_top_k"],
        "answer_max_new_tokens": config["llm"]["generation"]["max_new_tokens"],
        "evidence_text_mapping": (
            "Verified chunk character offsets plus NFKC Unicode normalization, line-break "
            "dehyphenation, case folding, and exact consecutive reference-passage mapping "
            "within source/page"
        ),
    }
    details = {
        "run": run,
        "dataset_counts": dataset_counts,
        "metric_summaries": metric_summaries,
        "questions": question_results,
    }
    summary = build_summary(run, dataset_counts, metric_summaries, question_results)
    write_outputs_safely(results_dir, details, summary, question_results)
    print(f"Wrote {results_dir / 'summary.md'}")
    print(f"Wrote {results_dir / 'per_question.csv'}")
    print(f"Wrote {results_dir / 'details.json'}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(
            "Evaluation aborted before output replacement. Any existing evaluation result files "
            "belong to the previous completed run.",
            file=sys.stderr,
        )
        raise
