"""Run benchmark evaluation and write report-ready artifacts."""

from __future__ import annotations

from src.eval.report import write_evaluation_artifacts


def main() -> None:
    result = write_evaluation_artifacts()
    print("Wrote evaluation artifacts:")
    print(f"- {result['json_path']}")
    print(f"- {result['markdown_path']}")


if __name__ == "__main__":
    main()
