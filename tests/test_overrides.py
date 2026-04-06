"""Tests for deterministic safety override rules."""

from src.rules import evaluate_overrides


def test_no_override_for_empty_evidence() -> None:
    result = evaluate_overrides({})

    assert result["triggered"] is False
    assert result["action"] == "none"
    assert result["message"] == ""


def test_chest_pain_triggers_override() -> None:
    evidence = {"chest_pain": "yes", "dizziness": "unknown", "recent_fall": "unknown"}

    result = evaluate_overrides(evidence)

    assert result["triggered"] is True
    assert result["action"] == "urgent_escalation"
    assert result["rule_id"] == "chest_pain_emergency"


def test_dizziness_after_fall_requires_both_signals() -> None:
    partial = evaluate_overrides({"dizziness": "yes", "recent_fall": "unknown"})
    full = evaluate_overrides({"dizziness": "yes", "recent_fall": "yes"})

    assert partial["triggered"] is False
    assert full["triggered"] is True
    assert full["rule_id"] == "dizziness_after_fall"


def test_negated_red_flag_does_not_trigger_override() -> None:
    result = evaluate_overrides({"chest_pain": "no"})

    assert result["triggered"] is False


def test_first_matching_rule_is_used_as_primary() -> None:
    result = evaluate_overrides(
        {
            "chest_pain": "yes",
            "fainting": "yes",
        }
    )

    assert result["triggered"] is True
    assert result["rule_id"] == "chest_pain_emergency"
    assert "fainting_emergency" in str(result["matched_rules"])
