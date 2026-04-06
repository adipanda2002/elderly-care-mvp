"""Bayesian inference entrypoints."""

from __future__ import annotations

import math

from src.common.config import (
    load_condition_priors_config,
    load_evidence_likelihoods_config,
    load_variables_config,
)
from src.common.types import EvidenceDict, PosteriorDict

EPSILON = 1e-6


def rank_conditions(evidence: EvidenceDict) -> PosteriorDict:
    """Return posterior probabilities for the modeled conditions."""
    if not evidence:
        return _normalized_priors()

    priors = _normalized_priors()
    likelihoods = load_evidence_likelihoods_config()
    modeled_variables = _modeled_evidence_variables()

    log_scores: dict[str, float] = {}

    for condition, prior in priors.items():
        log_score = math.log(_clamp_probability(prior))
        condition_likelihoods = likelihoods.get(condition, {})

        for variable_name in modeled_variables:
            evidence_value = evidence.get(variable_name, "unknown")
            if evidence_value == "unknown":
                continue

            yes_likelihood = _clamp_probability(float(condition_likelihoods.get(variable_name, 0.5)))

            if evidence_value == "yes":
                log_score += math.log(yes_likelihood)
            elif evidence_value == "no":
                log_score += math.log(_clamp_probability(1.0 - yes_likelihood))

        log_scores[condition] = log_score

    return _softmax_normalize(log_scores)


def _normalized_priors() -> PosteriorDict:
    priors = {
        str(condition): float(value)
        for condition, value in load_condition_priors_config().items()
    }

    total = sum(priors.values())
    if total <= 0:
        raise ValueError("Condition priors must sum to a positive value.")

    return {condition: value / total for condition, value in priors.items()}


def _modeled_evidence_variables() -> tuple[str, ...]:
    variables = load_variables_config()
    names: list[str] = []

    for section_name in ("context_variables", "symptoms"):
        section = variables.get(section_name, {})
        if isinstance(section, dict):
            names.extend(section.keys())

    return tuple(names)


def _softmax_normalize(log_scores: dict[str, float]) -> PosteriorDict:
    max_log_score = max(log_scores.values())
    exp_scores = {
        condition: math.exp(score - max_log_score)
        for condition, score in log_scores.items()
    }
    total = sum(exp_scores.values())

    if total <= 0:
        raise ValueError("Posterior normalization failed.")

    normalized = {
        condition: score / total
        for condition, score in exp_scores.items()
    }

    return dict(
        sorted(
            normalized.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


def _clamp_probability(value: float) -> float:
    return min(max(value, EPSILON), 1.0 - EPSILON)
