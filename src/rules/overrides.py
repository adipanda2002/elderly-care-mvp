"""Urgent escalation rule checks."""

from __future__ import annotations

from src.common.types import EvidenceDict


def evaluate_overrides(evidence: EvidenceDict) -> dict[str, str | bool]:
    """Return override status and message for urgent cases."""
    if not evidence:
        return {"triggered": False, "message": ""}

    raise NotImplementedError("Safety override implementation pending.")
