"""Urgent escalation rule checks."""

from __future__ import annotations

from typing import Any

from src.common.config import load_safety_rules_config
from src.common.types import EvidenceDict


def evaluate_overrides(evidence: EvidenceDict) -> dict[str, str | bool]:
    """Return override status and message for urgent cases."""
    if not evidence:
        return _empty_override_result()

    matching_rules: list[dict[str, Any]] = []

    for rule in load_safety_rules_config().get("rules", []):
        conditions = rule.get("if_all", {})
        if _matches_all(evidence, conditions):
            matching_rules.append(rule)

    if not matching_rules:
        return _empty_override_result()

    primary_rule = matching_rules[0]

    return {
        "triggered": True,
        "action": str(primary_rule.get("action", "urgent_escalation")),
        "message": str(primary_rule.get("message", "Seek urgent medical attention immediately.")),
        "rule_id": str(primary_rule.get("id", "")),
        "matched_rules": ", ".join(str(rule.get("id", "")) for rule in matching_rules if rule.get("id")),
    }


def _empty_override_result() -> dict[str, str | bool]:
    return {
        "triggered": False,
        "action": "none",
        "message": "",
        "rule_id": "",
        "matched_rules": "",
    }


def _matches_all(evidence: EvidenceDict, conditions: dict[str, Any]) -> bool:
    return all(evidence.get(key, "unknown") == _normalize_expected_value(value) for key, value in conditions.items())


def _normalize_expected_value(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"

    return str(value).casefold()
