import pytest

from functions.normalizing import normalize


def test_normalize_lowercases_string():
    assert normalize("HeLLo") == "hello"


def test_normalize_strips_leading_and_trailing_whitespace():
    assert normalize("   hello   ") == "hello"


def test_normalize_collapses_multiple_spaces():
    assert normalize("hello    world") == "hello world"


def test_normalize_handles_tabs_and_newlines():
    input_str = "hello\t\tworld\n\nagain"
    assert normalize(input_str) == "hello world again"


def test_normalize_mixed_whitespace():
    input_str = "  hello \t world \n again  "
    assert normalize(input_str) == "hello world again"


def test_normalize_empty_string():
    assert normalize("") == ""


def test_normalize_only_whitespace():
    assert normalize("   \t\n  ") == ""


def test_normalize_keeps_special_characters():
    assert normalize("Hello!  How ARE you?") == "hello! how are you?"
