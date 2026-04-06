"""Basic repository-structure smoke tests."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_expected_directories_exist() -> None:
    expected_paths = [
        "app",
        "config",
        "data/raw",
        "data/processed",
        "docs",
        "notebooks",
        "src",
        "src/parser",
        "src/bn",
        "src/rules",
        "src/explain",
        "src/eval",
        "tests",
    ]

    for relative_path in expected_paths:
        assert (ROOT / relative_path).exists()
