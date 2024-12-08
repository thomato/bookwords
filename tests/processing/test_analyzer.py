from unittest.mock import patch

import pytest

from core.statistics import WordStats
from processing.analyzer import analyze_text


def test_empty_text_returns_empty_stats():
    """
    Given: An empty text string
    When: Analyzing the text
    Then: Should return empty statistics dictionary
    """
    text = ""
    result = analyze_text(text)
    assert result == {}


def test_single_word_returns_correct_count():
    """
    Given: A text with a single valid word
    When: Analyzing the text
    Then: Should return statistics with count 1 for that word
    """
    text = "hello"
    expected_stats = {"hello": WordStats(original_word="hello", count=1)}

    result = analyze_text(text)

    assert len(result) == 1
    assert result["hello"].count == expected_stats["hello"].count
    assert (
        result["hello"].original_word == expected_stats["hello"].original_word
    )


def test_repeated_word_counts_correctly():
    """
    Given: A text with repeated valid words
    When: Analyzing the text
    Then: Should return correct count for repeated word
    """
    text = "hello hello hello"
    expected_count = 3

    result = analyze_text(text)

    assert result["hello"].count == expected_count


def test_case_insensitive_counting():
    """
    Given: A text with same word in different cases
    When: Analyzing the text
    Then: Should count them as the same word (case insensitive)
    """
    text = "Hello HELLO hello"
    expected_count = 3

    result = analyze_text(text)

    assert result["hello"].count == expected_count


def test_tokenized_words_handled_correctly():
    """
    Given: A text with punctuation and multiple words
    When: Analyzing the text
    Then: Should correctly filter and count only valid words
    """
    text = "Hello, world! Hello."
    mock_tokens = ["hello", ",", "world", "!", "hello", "."]
    expected_valid_words = ["hello", "world", "hello"]  # Only alpha words

    with patch("processing.analyzer.tokenize") as mock_tokenize:
        mock_tokenize.return_value = mock_tokens

        result = analyze_text(text)

        assert result["hello"].count == 2
        assert result["world"].count == 1
        assert "," not in result  # Punctuation should be filtered out
        assert "!" not in result
        assert "." not in result
        mock_tokenize.assert_called_once_with(text.lower())


def test_word_length_validation():
    """
    Given: Words of various lengths
    When: Analyzing the text
    Then: Should only include words within the configured length limits
    """
    text = "a ok long anextremelyveryveryverylongwordthatexceedsmaxlength"
    mock_tokens = [
        "a",
        "ok",
        "long",
        "anextremelyveryveryverylongwordthatexceedsmaxlength",
    ]

    with patch("processing.analyzer.tokenize") as mock_tokenize:
        mock_tokenize.return_value = mock_tokens

        result = analyze_text(text)

        assert "a" not in result  # Too short (< MIN_WORD_LENGTH)
        assert "ok" in result  # Valid length
        assert "long" in result  # Valid length
        assert (
            "anextremelyveryveryverylongwordthatexceedsmaxlength" not in result
        )  # Too long (> MAX_WORD_LENGTH)


def test_non_alphabetic_words_filtered():
    """
    Given: A mix of alphabetic and non-alphabetic words
    When: Analyzing the text
    Then: Should only include purely alphabetic words
    """
    text = "hello123 world h3llo w0rld"
    mock_tokens = ["hello123", "world", "h3llo", "w0rld"]

    with patch("processing.analyzer.tokenize") as mock_tokenize:
        mock_tokenize.return_value = mock_tokens

        result = analyze_text(text)

        assert "hello123" not in result  # Contains numbers
        assert "world" in result  # Pure alphabetic
        assert "h3llo" not in result  # Contains numbers
        assert "w0rld" not in result  # Contains numbers


@pytest.mark.parametrize(
    "invalid_input", [None, 123, ["not", "a", "string"], {"key": "value"}]
)
def test_invalid_input_types_raise_error(invalid_input):
    """
    Given: Invalid input types
    When: Attempting to analyze them
    Then: Should raise appropriate error
    """
    with pytest.raises((AttributeError, TypeError)):
        analyze_text(invalid_input)
