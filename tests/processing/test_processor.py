from pathlib import Path
from unittest.mock import patch

import pytest

from core.book import Book
from core.statistics import WordStats
from processing.processor import process_book
from utils.exceptions import BookProcessingError


def test_successful_book_processing():
    """
    Given: A valid book file path
    When: Processing the book
    Then: Should return book and statistics
    """
    # Arrange
    file_path = Path("test.epub")
    mock_book = Book(
        title="Test Book", author="Test Author", content="hello world"
    )
    mock_stats = {
        "hello": WordStats(original_word="hello", count=1),
        "world": WordStats(original_word="world", count=1),
    }

    with patch("processing.processor.read_book") as mock_read, patch(
        "processing.processor.analyze_text"
    ) as mock_analyze:
        # Configure mocks
        mock_read.return_value = mock_book
        mock_analyze.return_value = mock_stats

        # Act
        book, stats = process_book(file_path)

        # Assert
        assert book == mock_book
        assert stats == mock_stats
        mock_read.assert_called_once_with(file_path)
        mock_analyze.assert_called_once_with(mock_book.content)


def test_file_reading_error_handling():
    """
    Given: A book file that fails to read
    When: Processing the book
    Then: Should raise BookProcessingError with appropriate context
    """
    # Arrange
    file_path = Path("error.epub")
    original_error = IOError("Failed to read file")

    with patch("processing.processor.read_book") as mock_read:
        # Configure mock to raise error
        mock_read.side_effect = original_error

        # Act & Assert
        with pytest.raises(BookProcessingError) as exc_info:
            process_book(file_path)

        # Verify error details
        assert exc_info.value.file_path == file_path
        assert exc_info.value.message == "Failed to process book"
        assert exc_info.value.original_error == original_error


def test_analysis_error_handling():
    """
    Given: A book with content that fails analysis
    When: Processing the book
    Then: Should raise BookProcessingError with appropriate context
    """
    # Arrange
    file_path = Path("bad_content.epub")
    mock_book = Book(
        title="Test Book", author="Test Author", content="test content"
    )
    original_error = ValueError("Analysis failed")

    with patch("processing.processor.read_book") as mock_read, patch(
        "processing.processor.analyze_text"
    ) as mock_analyze:
        # Configure mocks
        mock_read.return_value = mock_book
        mock_analyze.side_effect = original_error

        # Act & Assert
        with pytest.raises(BookProcessingError) as exc_info:
            process_book(file_path)

        # Verify error details
        assert exc_info.value.file_path == file_path
        assert exc_info.value.message == "Failed to process book"
        assert exc_info.value.original_error == original_error


def test_invalid_file_path_type():
    """
    Given: An invalid file path type
    When: Processing the book
    Then: Should raise BookProcessingError
    """
    # Arrange
    invalid_path = "not/a/path/object"

    # Act & Assert
    with pytest.raises(BookProcessingError) as exc_info:
        process_book(invalid_path)

    assert isinstance(exc_info.value.original_error, AttributeError)
