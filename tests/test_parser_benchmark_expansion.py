"""Tests for benchmark-driven parser refinements."""

from src.parser import parse_free_text


def test_parser_maps_feeling_sick_into_existing_schema() -> None:
    evidence = parse_free_text("I am feeling sick and have chills.")

    assert evidence["fatigue"] == "yes"
    assert evidence["mild_fever"] == "yes"


def test_parser_maps_lost_appetite_into_existing_schema() -> None:
    evidence = parse_free_text("I feel ill and have lost appetite.")

    assert evidence["fatigue"] == "yes"


def test_parser_maps_decreased_appetite_variant() -> None:
    evidence = parse_free_text("I have decreased appetite and feel tired.")

    assert evidence["fatigue"] == "yes"
