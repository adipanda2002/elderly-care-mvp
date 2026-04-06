"""Tests for the benchmark evaluation pipeline."""

from src.eval import (
    evaluate_parser_cases,
    evaluate_ranking_cases,
    evaluate_safety_cases,
    load_benchmark_summary,
)


def test_parser_benchmark_metrics_are_computed() -> None:
    summary = evaluate_parser_cases()

    assert summary["num_cases"] >= 5
    assert 0.0 <= summary["precision"] <= 1.0
    assert 0.0 <= summary["recall"] <= 1.0
    assert 0.0 <= summary["f1"] <= 1.0


def test_ranking_benchmark_metrics_are_computed() -> None:
    summary = evaluate_ranking_cases()

    assert summary["num_cases"] >= 5
    assert summary["top1_accuracy"] >= 0.75
    assert summary["top2_recall"] >= 0.90


def test_safety_benchmark_metrics_are_computed() -> None:
    summary = evaluate_safety_cases()

    assert summary["num_cases"] >= 6
    assert summary["recall"] == 1.0
    assert 0.0 <= summary["accuracy"] <= 1.0


def test_benchmark_summary_contains_all_sections() -> None:
    summary = load_benchmark_summary()

    assert set(summary) == {"targets", "parser", "ranking", "safety"}
