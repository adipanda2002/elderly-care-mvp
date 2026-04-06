"""Tests for Bayesian condition ranking."""

from src.bn import rank_conditions


def test_rank_conditions_returns_normalized_probabilities() -> None:
    scores = rank_conditions({})

    assert set(scores) == {
        "dehydration",
        "hypoglycemia",
        "mild_viral_infection",
        "medication_side_effect",
    }
    assert abs(sum(scores.values()) - 1.0) < 1e-9


def test_dehydration_case_ranks_dehydration_first() -> None:
    scores = rank_conditions(
        {
            "low_water_intake": "yes",
            "dry_mouth": "yes",
            "dizziness": "yes",
            "mild_fever": "no",
        }
    )

    assert next(iter(scores)) == "dehydration"


def test_hypoglycemia_case_ranks_hypoglycemia_first() -> None:
    scores = rank_conditions(
        {
            "skipped_meal": "yes",
            "sweating": "yes",
            "dizziness": "yes",
            "mild_fever": "no",
        }
    )

    assert next(iter(scores)) == "hypoglycemia"


def test_viral_case_ranks_viral_infection_first() -> None:
    scores = rank_conditions(
        {
            "mild_fever": "yes",
            "fatigue": "yes",
            "headache": "yes",
            "dry_mouth": "no",
        }
    )

    assert next(iter(scores)) == "mild_viral_infection"


def test_medication_case_ranks_side_effect_first() -> None:
    scores = rank_conditions(
        {
            "chronic_condition_flag": "yes",
            "nausea": "yes",
            "dry_mouth": "yes",
            "mild_fever": "no",
        }
    )

    assert next(iter(scores)) == "medication_side_effect"
