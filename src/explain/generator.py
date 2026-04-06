"""Generate user-facing explanations and safe next-step guidance."""

from __future__ import annotations

from collections.abc import Iterable

from src.common.config import load_evidence_likelihoods_config
from src.common.types import EvidenceDict, PosteriorDict

DISCLAIMER = (
    "This tool provides limited educational decision support only and is not a medical diagnosis. "
    "Seek professional care if symptoms persist, worsen, or you are concerned."
)

NON_URGENT_RECOMMENDATIONS = {
    "dehydration": (
        "Drink water, rest, and monitor symptoms closely over the next few hours. "
        "Seek medical care if symptoms continue or worsen."
    ),
    "hypoglycemia": (
        "If it is safe to do so, have food or a quick source of sugar and monitor symptoms. "
        "Seek medical care if symptoms continue, recur, or you feel worse."
    ),
    "mild_viral_infection": (
        "Rest, stay hydrated, and monitor temperature and energy levels. "
        "Seek medical care if symptoms worsen or do not improve."
    ),
    "medication_side_effect": (
        "Monitor the symptoms and review any recent medication changes. "
        "Contact a clinician or pharmacist if the symptoms continue or become more concerning."
    ),
}


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
            "disclaimer": DISCLAIMER,
            "evidence_used": [],
        }

    ranked_conditions = _ranked_condition_rows(condition_scores)
    positive_evidence = _evidence_with_value(evidence, "yes")
    known_evidence = _evidence_with_any_known_value(evidence)
    urgent_warning = bool(override.get("triggered"))

    if urgent_warning:
        explanation = _build_urgent_explanation(
            override_message=str(override.get("message", "")),
            positive_evidence=positive_evidence,
            ranked_conditions=ranked_conditions,
        )
        recommendation = (
            f"{override.get('message', 'Seek urgent medical attention immediately.')} "
            "Do not rely on the ranked conditions alone when a red-flag rule is triggered."
        )
    else:
        explanation = _build_non_urgent_explanation(
            ranked_conditions=ranked_conditions,
            positive_evidence=positive_evidence,
        )
        recommendation = _build_non_urgent_recommendation(ranked_conditions)

    return {
        "conditions": ranked_conditions,
        "urgent_warning": urgent_warning,
        "recommendation": recommendation,
        "explanation": explanation,
        "disclaimer": DISCLAIMER,
        "evidence_used": [_humanize(item) for item in known_evidence],
    }


def _ranked_condition_rows(condition_scores: PosteriorDict) -> list[dict[str, object]]:
    return [
        {
            "id": condition,
            "label": _humanize(condition),
            "probability": score,
        }
        for condition, score in condition_scores.items()
    ]


def _evidence_with_any_known_value(evidence: EvidenceDict) -> list[str]:
    return [
        key
        for key, value in evidence.items()
        if value in {"yes", "no"}
    ]


def _evidence_with_value(evidence: EvidenceDict, target_value: str) -> list[str]:
    return [
        key
        for key, value in evidence.items()
        if value == target_value
    ]


def _build_urgent_explanation(
    override_message: str,
    positive_evidence: list[str],
    ranked_conditions: list[dict[str, object]],
) -> str:
    evidence_text = _join_humanized(positive_evidence[:3]) or "the recognized red-flag evidence"
    top_condition = ranked_conditions[0]["label"] if ranked_conditions else "the current top-ranked condition"

    return (
        f"Urgent escalation was triggered because of {evidence_text}. "
        f"{override_message} The current top-ranked modeled condition is {top_condition}, "
        "but the emergency rule takes priority over the ranking."
    )


def _build_non_urgent_explanation(
    ranked_conditions: list[dict[str, object]],
    positive_evidence: list[str],
) -> str:
    if not ranked_conditions:
        return "No ranked conditions are available yet."

    top_condition = ranked_conditions[0]["label"]
    supporting_evidence = _top_supporting_evidence(
        condition_id=str(ranked_conditions[0]["id"]),
        positive_evidence=positive_evidence,
    )
    evidence_text = _join_humanized(supporting_evidence)

    if evidence_text:
        return (
            f"Based on {evidence_text}, {top_condition} is ranked highest among the limited conditions modeled in this MVP."
        )

    return (
        f"{top_condition} is currently ranked highest among the limited conditions modeled in this MVP."
    )


def _build_non_urgent_recommendation(ranked_conditions: list[dict[str, object]]) -> str:
    if not ranked_conditions:
        return "Please describe the symptoms in more detail."

    top_condition_id = str(ranked_conditions[0]["id"])
    recommendation = NON_URGENT_RECOMMENDATIONS.get(
        top_condition_id,
        "Monitor the symptoms closely and seek medical advice if they persist or worsen.",
    )

    return (
        f"{recommendation} Seek urgent medical attention if chest pain, fainting, or worsening confusion occurs."
    )


def _top_supporting_evidence(condition_id: str, positive_evidence: list[str]) -> list[str]:
    likelihoods = load_evidence_likelihoods_config().get(condition_id, {})
    scored: list[tuple[str, float]] = []

    for evidence_name in positive_evidence:
        if evidence_name not in likelihoods:
            continue
        scored.append((evidence_name, float(likelihoods[evidence_name])))

    scored.sort(key=lambda item: item[1], reverse=True)
    return [name for name, _ in scored[:3]]


def _join_humanized(values: Iterable[str]) -> str:
    items = [_humanize(value) for value in values if value]

    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"

    return f"{', '.join(items[:-1])}, and {items[-1]}"


def _humanize(value: str) -> str:
    return value.replace("_", " ")
