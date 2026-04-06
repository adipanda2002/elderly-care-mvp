"""Tests for explanation and recommendation generation."""

from src.explain import build_response


def test_non_urgent_response_includes_top_condition_explanation() -> None:
    evidence = {
        "low_water_intake": "yes",
        "dry_mouth": "yes",
        "dizziness": "yes",
        "mild_fever": "no",
    }
    scores = {
        "dehydration": 0.80,
        "hypoglycemia": 0.10,
        "medication_side_effect": 0.06,
        "mild_viral_infection": 0.04,
    }
    override = {
        "triggered": False,
        "message": "",
        "rule_id": "",
    }

    response = build_response(evidence, scores, override)

    assert response["urgent_warning"] is False
    assert response["conditions"][0]["id"] == "dehydration"
    assert "dehydration" in str(response["explanation"])
    assert "dry mouth" in str(response["explanation"])
    assert "not a medical diagnosis" not in str(response["explanation"])
    assert "Drink water" in str(response["recommendation"])
    assert "not a medical diagnosis" in str(response["disclaimer"])


def test_urgent_response_prioritizes_override_message() -> None:
    evidence = {
        "chest_pain": "yes",
        "fainting": "yes",
    }
    scores = {
        "dehydration": 0.40,
        "hypoglycemia": 0.30,
        "mild_viral_infection": 0.20,
        "medication_side_effect": 0.10,
    }
    override = {
        "triggered": True,
        "message": "Seek urgent medical attention immediately.",
        "rule_id": "chest_pain_emergency",
    }

    response = build_response(evidence, scores, override)

    assert response["urgent_warning"] is True
    assert "Urgent escalation was triggered" in str(response["explanation"])
    assert "Seek urgent medical attention immediately." in str(response["recommendation"])
    assert "takes priority" in str(response["explanation"])


def test_empty_response_returns_prompt_for_more_detail() -> None:
    response = build_response({}, {}, {"triggered": False, "message": "", "rule_id": ""})

    assert response["conditions"] == []
    assert response["urgent_warning"] is False
    assert response["recommendation"] == "Please describe the symptoms in more detail."
