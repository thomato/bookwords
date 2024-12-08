from unittest.mock import patch

import pytest

from processing.tokenizer import ensure_nltk_data, tokenize

# Test data
MOCK_REQUIRED_PACKAGES = ["punkt", "averaged_perceptron_tagger"]


@pytest.fixture
def mock_config():
    with patch(
        "processing.tokenizer.REQUIRED_NLTK_PACKAGES", MOCK_REQUIRED_PACKAGES
    ):
        yield


def test_ensure_nltk_data_downloads_missing_packages(mock_config):
    """Test that ensure_nltk_data downloads packages that aren't found"""
    with patch("nltk.data.find") as mock_find, patch(
        "nltk.download"
    ) as mock_download:
        # Make nltk.data.find raise LookupError for all packages
        mock_find.side_effect = LookupError()

        ensure_nltk_data()

        # Verify download was called for each required package
        assert mock_download.call_count == len(MOCK_REQUIRED_PACKAGES)
        for package in MOCK_REQUIRED_PACKAGES:
            mock_download.assert_any_call(package)


def test_ensure_nltk_data_skips_existing_packages(mock_config):
    """Test that ensure_nltk_data doesn't download already present packages"""
    with patch("nltk.data.find") as mock_find, patch(
        "nltk.download"
    ) as mock_download:
        # Make nltk.data.find succeed (no LookupError)
        mock_find.return_value = True

        ensure_nltk_data()

        # Verify download was not called
        mock_download.assert_not_called()


def test_tokenize_basic_text():
    """Test basic tokenization functionality"""
    test_text = "Hello, world! This is a test."
    expected_tokens = [
        "Hello",
        ",",
        "world",
        "!",
        "This",
        "is",
        "a",
        "test",
        ".",
    ]

    with patch("processing.tokenizer.ensure_nltk_data") as mock_ensure_data:
        result = tokenize(test_text)

        # Verify ensure_nltk_data was called
        mock_ensure_data.assert_called_once()

        # Verify tokenization result
        assert result == expected_tokens


def test_tokenize_empty_string():
    """Test tokenization with empty string"""
    with patch("processing.tokenizer.ensure_nltk_data"):
        result = tokenize("")
        assert result == []


def test_tokenize_special_characters():
    """Test tokenization with special characters"""
    test_text = "Don't @ me!! 😊 #hashtag"
    expected_tokens = ["Do", "n't", "@", "me", "!", "!", "😊", "#", "hashtag"]

    with patch("processing.tokenizer.ensure_nltk_data"):
        result = tokenize(test_text)
        assert result == expected_tokens


@pytest.mark.parametrize(
    "invalid_input", [None, 123, ["not", "a", "string"], {"key": "value"}]
)
def test_tokenize_invalid_input(invalid_input):
    """Test tokenization with invalid input types"""
    with patch("processing.tokenizer.ensure_nltk_data"), pytest.raises(
        TypeError
    ):
        tokenize(invalid_input)
