"""Map vague symptom descriptions into structured evidence."""

from __future__ import annotations

from src.common.types import EvidenceDict


def parse_free_text(text: str) -> EvidenceDict:
    """Convert a symptom description into the reduced evidence schema."""
    if not text.strip():
        return {}

    raise NotImplementedError("Parser implementation pending.")
