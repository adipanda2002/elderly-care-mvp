"""Generate report-ready evaluation artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.common.config import project_root
from src.eval.metrics import load_benchmark_summary


def write_evaluation_artifacts(output_dir: Path | None = None) -> dict[str, Any]:
    """Write JSON and Markdown benchmark summaries to the docs directory."""
    summary = load_benchmark_summary()
    docs_dir = output_dir or (project_root() / "docs")
    docs_dir.mkdir(parents=True, exist_ok=True)

    json_path = docs_dir / "evaluation_summary.json"
    markdown_path = docs_dir / "evaluation_summary.md"

    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    markdown_path.write_text(_build_markdown(summary), encoding="utf-8")

    return {
        "summary": summary,
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }


def _build_markdown(summary: dict[str, Any]) -> str:
    parser = summary["parser"]
    ranking = summary["ranking"]
    safety = summary["safety"]
    targets = summary["targets"]

    return f"""# Evaluation Summary

## Headline Metrics

| Metric | Value | Target |
| --- | ---: | ---: |
| Parser F1 | {parser['f1']:.3f} | {targets['parser_f1_target']:.2f} |
| Parser Precision | {parser['precision']:.3f} | - |
| Parser Recall | {parser['recall']:.3f} | - |
| Ranking Top-1 Accuracy | {ranking['top1_accuracy']:.3f} | {targets['top1_accuracy_target']:.2f} |
| Ranking Top-2 Recall | {ranking['top2_recall']:.3f} | {targets['top2_recall_target']:.2f} |
| Safety Recall | {safety['recall']:.3f} | {targets['safety_recall_target']:.2f} |
| Safety Accuracy | {safety['accuracy']:.3f} | - |

## Notes

- Benchmarks are synthetic or hand-authored for the reduced MVP scope.
- Ranking evaluation uses structured evidence cases.
- Safety evaluation uses free-text inputs passed through the parser and rule engine.
- These numbers should be refreshed after future parser or CPT changes.
"""
