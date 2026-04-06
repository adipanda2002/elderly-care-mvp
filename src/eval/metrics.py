"""Evaluation helpers and placeholders."""

from __future__ import annotations


def load_benchmark_summary() -> dict[str, float]:
    """Return placeholder benchmark targets until evaluations are implemented."""
    return {
        "parser_f1_target": 0.75,
        "top1_accuracy_target": 0.75,
        "top2_recall_target": 0.90,
        "safety_recall_target": 1.00,
    }
