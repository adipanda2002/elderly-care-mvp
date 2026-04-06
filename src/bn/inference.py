"""Bayesian inference entrypoints."""

from __future__ import annotations

from src.common.types import EvidenceDict, PosteriorDict


def rank_conditions(evidence: EvidenceDict) -> PosteriorDict:
    """Return posterior probabilities for the modeled conditions."""
    if not evidence:
        return {}

    raise NotImplementedError("Bayesian network implementation pending.")
