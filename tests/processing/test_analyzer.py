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
    # Arrange
    text = ""

    # Act
    result = analyze_text(text)

    # Assert
    assert result == {}


def test_single_word_returns_correct_count():
    """
    Given: A text with a single word
    When: Analyzing the text
    Then: Should return statistics with count 1 for that word
    """
    # Arrange
    text = "hello"
    expected_stats = {"hello": WordStats(original_word="hello", count=1)}

    # Act
    result = analyze_text(text)

    # Assert
    assert len(result) == 1
    assert result["hello"].count == expected_stats["hello"].count
    assert (
        result["hello"].original_word == expected_stats["hello"].original_word
    )


def test_repeated_word_counts_correctly():
    """
    Given: A text with repeated words
    When: Analyzing the text
    Then: Should return correct count for repeated word
    """
    # Arrange
    text = "hello hello hello"
    expected_count = 3

    # Act
    result = analyze_text(text)

    # Assert
    assert result["hello"].count == expected_count


def test_case_insensitive_counting():
    """
    Given: A text with same word in different cases
    When: Analyzing the text
    Then: Should count them as the same word (case insensitive)
    """
    # Arrange
    text = "Hello HELLO hello"
    expected_count = 3

    # Act
    result = analyze_text(text)

    # Assert
    assert result["hello"].count == expected_count


def test_tokenized_words_handled_correctly():
    """
    Given: A text with punctuation and multiple words
    When: Analyzing the text
    Then: Should correctly tokenize and count words
    """
    # Arrange
    text = "Hello, world! Hello."
    expected_tokens = ["hello", ",", "world", "!", "hello", "."]

    with patch(
        "processing.analyzer.tokenize"
    ) as mock_tokenize:  # Updated patch path
        # Configure mock to return predefined tokens
        mock_tokenize.return_value = expected_tokens

        # Act
        result = analyze_text(text)

        # Assert
        assert result["hello"].count == 2
        assert result["world"].count == 1
        assert result[","].count == 1
        mock_tokenize.assert_called_once_with(text.lower())


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
