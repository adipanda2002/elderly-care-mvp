"""Benchmark-driven evaluation helpers for the MVP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.bn import rank_conditions
from src.common.config import load_benchmark_cases_config
from src.parser import parse_free_text
from src.rules import evaluate_overrides

TARGETS = {
    "parser_f1_target": 0.75,
    "top1_accuracy_target": 0.75,
    "top2_recall_target": 0.90,
    "safety_recall_target": 1.00,
}


@dataclass(frozen=True)
class ParserCaseResult:
    id: str
    expected: set[str]
    predicted: set[str]

    @property
    def true_positives(self) -> int:
        return len(self.expected & self.predicted)

    @property
    def false_positives(self) -> int:
        return len(self.predicted - self.expected)

    @property
    def false_negatives(self) -> int:
        return len(self.expected - self.predicted)


def load_benchmark_summary() -> dict[str, Any]:
    """Return computed benchmark metrics alongside target thresholds."""
    parser_summary = evaluate_parser_cases()
    ranking_summary = evaluate_ranking_cases()
    safety_summary = evaluate_safety_cases()

    return {
        "targets": TARGETS,
        "parser": parser_summary,
        "ranking": ranking_summary,
        "safety": safety_summary,
    }


def evaluate_parser_cases() -> dict[str, Any]:
    cases = load_benchmark_cases_config().get("parser_cases", [])
    results: list[ParserCaseResult] = []

    for case in cases:
        parsed = parse_free_text(str(case.get("text", "")))
        predicted = _labeled_pairs(parsed)
        expected = _expected_pairs(case.get("expected", {}))
        results.append(
            ParserCaseResult(
                id=str(case.get("id", "")),
                expected=expected,
                predicted=predicted,
            )
        )

    true_positives = sum(item.true_positives for item in results)
    false_positives = sum(item.false_positives for item in results)
    false_negatives = sum(item.false_negatives for item in results)

    precision = _safe_divide(true_positives, true_positives + false_positives)
    recall = _safe_divide(true_positives, true_positives + false_negatives)
    f1 = _f1(precision, recall)

    return {
        "num_cases": len(results),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "details": [
            {
                "id": item.id,
                "expected": sorted(item.expected),
                "predicted": sorted(item.predicted),
                "true_positives": item.true_positives,
                "false_positives": item.false_positives,
                "false_negatives": item.false_negatives,
            }
            for item in results
        ],
    }


def evaluate_ranking_cases() -> dict[str, Any]:
    cases = load_benchmark_cases_config().get("ranking_cases", [])
    details: list[dict[str, Any]] = []
    top1_hits = 0
    top2_hits = 0

    for case in cases:
        evidence = {
            str(key): _normalize_label_value(value)
            for key, value in dict(case.get("evidence", {})).items()
        }
        scores = rank_conditions(evidence)
        predicted_order = list(scores.keys())
        predicted_top1 = predicted_order[0]
        predicted_top2 = predicted_order[:2]
        expected_top1 = str(case.get("expected_top1", ""))
        acceptable_top2 = [str(item) for item in case.get("acceptable_top2", [])]

        top1_hit = predicted_top1 == expected_top1
        top2_hit = bool(set(predicted_top2) & set(acceptable_top2))

        top1_hits += int(top1_hit)
        top2_hits += int(top2_hit)

        details.append(
            {
                "id": str(case.get("id", "")),
                "expected_top1": expected_top1,
                "acceptable_top2": acceptable_top2,
                "predicted_top1": predicted_top1,
                "predicted_top2": predicted_top2,
                "top1_hit": top1_hit,
                "top2_hit": top2_hit,
                "scores": scores,
            }
        )

    num_cases = len(cases)
    return {
        "num_cases": num_cases,
        "top1_accuracy": _safe_divide(top1_hits, num_cases),
        "top2_recall": _safe_divide(top2_hits, num_cases),
        "details": details,
    }


def evaluate_safety_cases() -> dict[str, Any]:
    cases = load_benchmark_cases_config().get("safety_cases", [])
    details: list[dict[str, Any]] = []
    positives = 0
    true_positive_hits = 0
    correct_predictions = 0

    for case in cases:
        text = str(case.get("text", ""))
        expected_trigger = bool(case.get("expected_trigger", False))
        expected_rule_id = str(case.get("expected_rule_id", ""))
        parsed = parse_free_text(text)
        override = evaluate_overrides(parsed)
        predicted_trigger = bool(override.get("triggered"))
        predicted_rule_id = str(override.get("rule_id", ""))

        if expected_trigger:
            positives += 1
            true_positive_hits += int(predicted_trigger)

        if predicted_trigger == expected_trigger and (
            not expected_trigger or predicted_rule_id == expected_rule_id
        ):
            correct_predictions += 1

        details.append(
            {
                "id": str(case.get("id", "")),
                "expected_trigger": expected_trigger,
                "predicted_trigger": predicted_trigger,
                "expected_rule_id": expected_rule_id,
                "predicted_rule_id": predicted_rule_id,
            }
        )

    num_cases = len(cases)
    return {
        "num_cases": num_cases,
        "recall": _safe_divide(true_positive_hits, positives),
        "accuracy": _safe_divide(correct_predictions, num_cases),
        "details": details,
    }


def _expected_pairs(expected_mapping: dict[str, Any]) -> set[str]:
    return {
        f"{key}={_normalize_label_value(value)}"
        for key, value in expected_mapping.items()
    }


def _labeled_pairs(evidence: dict[str, str]) -> set[str]:
    return {
        f"{key}={value}"
        for key, value in evidence.items()
        if value in {"yes", "no"}
    }


def _normalize_label_value(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"

    return str(value).casefold()


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
