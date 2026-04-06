"""Tests for dataset-driven parser phrase expansions."""

from src.parser import parse_free_text


def test_parser_recognizes_figshare_dizziness_and_thirst_variants() -> None:
    evidence = parse_free_text("I have a sensation of spinning and increased thirst.")

    assert evidence["dizziness"] == "yes"
    assert evidence["dry_mouth"] == "yes"


def test_parser_recognizes_figshare_fatigue_variant() -> None:
    evidence = parse_free_text("I am dealing with extreme tiredness and muscle weakness.")

    assert evidence["fatigue"] == "yes"


def test_parser_recognizes_headache_and_sweating_variants() -> None:
    evidence = parse_free_text("I woke up with a morning headache and profuse sweating.")

    assert evidence["headache"] == "yes"
    assert evidence["sweating"] == "yes"


def test_parser_recognizes_confusion_variant() -> None:
    evidence = parse_free_text("I am having confused thinking and feel a bit off.")

    assert evidence["confusion"] == "yes"


def test_parser_recognizes_red_flag_dataset_variants() -> None:
    evidence = parse_free_text("I had loss of consciousness and burning chest pain.")

    assert evidence["fainting"] == "yes"
    assert evidence["chest_pain"] == "yes"
