"""Unit tests for farmer_service helpers (DB-independent functions)."""
from app.services.farmer_service import detect_isixhosa, is_stop_message


# --- is_stop_message ---

def test_stop_english_uppercase():
    assert is_stop_message("STOP") is True


def test_stop_english_lowercase():
    assert is_stop_message("stop") is True


def test_stop_with_whitespace():
    assert is_stop_message("  STOP  ") is True


def test_stop_xhosa_cima():
    assert is_stop_message("cima") is True


def test_stop_xhosa_yima():
    assert is_stop_message("yima") is True


def test_stop_does_not_match_substring():
    """'stop please help' is not an opt-out — only exact matches count."""
    assert is_stop_message("stop please help me") is False


def test_stop_empty_string():
    assert is_stop_message("") is False


def test_stop_none():
    assert is_stop_message(None) is False


# --- detect_isixhosa ---

def test_xhosa_greeting_detected():
    assert detect_isixhosa("Molo, ndicela uncedo") is True


def test_xhosa_pig_word_detected():
    assert detect_isixhosa("Iihagu zam ziyagula") is True


def test_xhosa_thanks_detected():
    assert detect_isixhosa("Enkosi kakhulu") is True


def test_pure_english_not_detected():
    assert detect_isixhosa("My pigs have a fever") is False


def test_code_switched_message_detected_as_xhosa():
    """A single Xhosa token in mixed text should detect as Xhosa."""
    assert detect_isixhosa("Molo my pigs are sick") is True


def test_xhosa_empty_string():
    assert detect_isixhosa("") is False


def test_xhosa_none():
    assert detect_isixhosa(None) is False


def test_xhosa_punctuation_stripped():
    """Punctuation around Xhosa tokens should not prevent detection."""
    assert detect_isixhosa("Molo!!! Ndicela uncedo.") is True
