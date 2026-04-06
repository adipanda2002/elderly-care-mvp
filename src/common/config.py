"""Helpers for loading cached project configuration."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT_DIR / "config"


def project_root() -> Path:
    """Return the repository root."""
    return ROOT_DIR


def config_path(*parts: str) -> Path:
    """Build a path inside the config directory."""
    return CONFIG_DIR.joinpath(*parts)


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in config file: {path}")

    return data


@lru_cache(maxsize=1)
def load_variables_config() -> dict[str, Any]:
    """Load the canonical variable schema."""
    return _read_yaml(config_path("variables.yaml"))


@lru_cache(maxsize=1)
def load_lexicon_config() -> dict[str, Any]:
    """Load parser phrase mappings and negation terms."""
    return _read_yaml(config_path("symptom_lexicon.yaml"))


@lru_cache(maxsize=1)
def load_safety_rules_config() -> dict[str, Any]:
    """Load symbolic safety override rules."""
    return _read_yaml(config_path("safety_rules.yaml"))


@lru_cache(maxsize=1)
def load_condition_priors_config() -> dict[str, Any]:
    """Load condition priors for Bayesian ranking."""
    return _read_yaml(config_path("cpts", "condition_priors.yaml"))


@lru_cache(maxsize=1)
def load_evidence_likelihoods_config() -> dict[str, Any]:
    """Load reduced evidence likelihoods for Bayesian ranking."""
    return _read_yaml(config_path("cpts", "symptom_likelihoods.yaml"))


@lru_cache(maxsize=1)
def load_benchmark_cases_config() -> dict[str, Any]:
    """Load benchmark cases for parser, ranking, and safety evaluation."""
    return _read_yaml(config_path("benchmark_cases.yaml"))
