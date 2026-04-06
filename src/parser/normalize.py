"""Map vague symptom descriptions into structured evidence."""

from __future__ import annotations

import re
from functools import lru_cache

from src.common.config import load_lexicon_config, load_variables_config
from src.common.types import EvidenceDict


SECTION_NAMES = ("context_variables", "symptoms", "red_flags")
NEGATION_WINDOW_WORDS = 3


def empty_evidence() -> EvidenceDict:
    """Return the full evidence schema initialized to unknown."""
    return {key: "unknown" for key in _ordered_evidence_keys()}


def parse_free_text(text: str) -> EvidenceDict:
    """Convert a symptom description into the reduced evidence schema."""
    evidence = empty_evidence()
    normalized_text = _normalize_text(text)

    if not normalized_text:
        return evidence

    lexicon = load_lexicon_config()
    negations = {term.casefold() for term in lexicon.get("negations", [])}

    for section_name in SECTION_NAMES:
        section_lexicon = lexicon.get(section_name, {})

        for variable_name, phrases in section_lexicon.items():
            if variable_name not in evidence:
                continue

            detected_value = _detect_value(
                text=normalized_text,
                phrases=phrases.get("positive", []),
                negations=negations,
            )

            if detected_value != "unknown":
                evidence[variable_name] = detected_value

    return evidence


@lru_cache(maxsize=1)
def _ordered_evidence_keys() -> tuple[str, ...]:
    variables_config = load_variables_config()
    keys: list[str] = []

    for section_name in SECTION_NAMES:
        section = variables_config.get(section_name, {})
        if isinstance(section, dict):
            keys.extend(section.keys())

    return tuple(keys)


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()


def _detect_value(text: str, phrases: list[str], negations: set[str]) -> str:
    saw_positive = False
    saw_negative = False

    for phrase in phrases:
        for match in _phrase_pattern(phrase).finditer(text):
            if _is_negated(text, match.start(), negations):
                saw_negative = True
            else:
                saw_positive = True

    if saw_positive:
        return "yes"

    if saw_negative:
        return "no"

    return "unknown"


@lru_cache(maxsize=None)
def _phrase_pattern(phrase: str) -> re.Pattern[str]:
    escaped_phrase = re.escape(phrase.casefold()).replace(r"\ ", r"\s+")
    return re.compile(rf"\b{escaped_phrase}\b")


def _is_negated(text: str, match_start: int, negations: set[str]) -> bool:
    prefix = text[:match_start]
    prefix_tokens = re.findall(r"[a-z']+", prefix)

    if not prefix_tokens:
        return False

    return any(token in negations for token in prefix_tokens[-NEGATION_WINDOW_WORDS:])
