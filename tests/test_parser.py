"""Tests for the phrase-based symptom parser."""

from src.parser import empty_evidence, parse_free_text


def test_empty_evidence_contains_full_schema() -> None:
    evidence = empty_evidence()

    assert evidence == {
        "skipped_meal": "unknown",
        "low_water_intake": "unknown",
        "poor_sleep": "unknown",
        "chronic_condition_flag": "unknown",
        "dizziness": "unknown",
        "fatigue": "unknown",
        "dry_mouth": "unknown",
        "headache": "unknown",
        "mild_fever": "unknown",
        "nausea": "unknown",
        "sweating": "unknown",
        "confusion": "unknown",
        "chest_pain": "unknown",
        "severe_confusion": "unknown",
        "fainting": "unknown",
        "recent_fall": "unknown",
    }


def test_empty_input_returns_unknown_schema() -> None:
    assert parse_free_text("") == empty_evidence()


def test_parser_extracts_multiple_symptoms() -> None:
    evidence = parse_free_text("I feel tired, slightly dizzy, and have a dry mouth.")

    assert evidence["fatigue"] == "yes"
    assert evidence["dizziness"] == "yes"
    assert evidence["dry_mouth"] == "yes"
    assert evidence["mild_fever"] == "unknown"


def test_parser_handles_simple_negation() -> None:
    evidence = parse_free_text("I am dizzy but no fever and not nauseous.")

    assert evidence["dizziness"] == "yes"
    assert evidence["mild_fever"] == "no"
    assert evidence["nausea"] == "no"


def test_parser_extracts_context_variables() -> None:
    evidence = parse_free_text(
        "I skipped breakfast, have not had much water, and didn't sleep well."
    )

    assert evidence["skipped_meal"] == "yes"
    assert evidence["low_water_intake"] == "yes"
    assert evidence["poor_sleep"] == "yes"


def test_parser_extracts_red_flags_and_negated_red_flags() -> None:
    positive = parse_free_text("I fainted and have chest tightness.")
    negative = parse_free_text("I have no chest pain after the walk.")

    assert positive["fainting"] == "yes"
    assert positive["chest_pain"] == "yes"
    assert negative["chest_pain"] == "no"
