"""Generate user-facing explanations and safe next-step guidance."""

from __future__ import annotations

from src.common.types import EvidenceDict, PosteriorDict


def build_response(
    evidence: EvidenceDict,
    condition_scores: PosteriorDict,
    override: dict[str, str | bool],
) -> dict[str, object]:
    """Build the final structured response for the app."""
    if not evidence and not condition_scores:
        return {
            "conditions": [],
            "urgent_warning": False,
            "recommendation": "Please describe the symptoms in more detail.",
            "explanation": "No evidence was extracted from the input.",
        }

    raise NotImplementedError("Explanation generation pending.")
