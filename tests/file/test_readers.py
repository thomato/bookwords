from pathlib import Path
from unittest.mock import MagicMock

import pytest
from ebooklib import ITEM_DOCUMENT, epub

from core.book import Book
from file.reader import read_book
from utils.exceptions import BookProcessingError


def mock_parse_html(html: str) -> str:
    return "Test content"


def create_mock_epub():
    mock_epub = MagicMock(spec=epub.EpubBook)
    mock_epub.get_metadata.side_effect = lambda dc, field: [[f"Test {field}"]]
    mock_item = MagicMock()
    mock_item.get_type.return_value = ITEM_DOCUMENT
    mock_item.get_content.return_value = (
        b"<html><body>Test content</body></html>"
    )
    mock_epub.get_items.return_value = [mock_item]
    return mock_epub


def test_unsupported_format():
    with pytest.raises(ValueError) as exc_info:
        read_book(Path("test.pdf"))
    assert "Unsupported format: .pdf" in str(exc_info.value)


@pytest.mark.usefixtures("monkeypatch")
class TestBookReader:
    def test_successful_epub_read(self, monkeypatch):
        # Arrange
        monkeypatch.setattr("file.reader.parse_html", mock_parse_html)
        monkeypatch.setattr(epub, "read_epub", lambda _: create_mock_epub())

        # Act
        book = read_book(Path("test.epub"))

        # Assert
        assert isinstance(book, Book)
        assert book.title == "Test title"
        assert book.author == "Test creator"
        assert book.content == "Test content"

    def test_missing_metadata(self, monkeypatch):
        # Arrange
        mock_epub = create_mock_epub()
        mock_epub.get_metadata.side_effect = IndexError
        monkeypatch.setattr("file.reader.parse_html", mock_parse_html)
        monkeypatch.setattr(epub, "read_epub", lambda _: mock_epub)

        # Act
        book = read_book(Path("test.epub"))

        # Assert
        assert book.title == "Unknown Title"
        assert book.author == "Unknown Author"
        assert book.content == "Test content"

    def test_epub_processing_error(self, monkeypatch):
        # Arrange
        def mock_parse_html_error(html: str) -> str:
            raise ValueError("Parse error")

        monkeypatch.setattr("file.reader.parse_html", mock_parse_html_error)
        monkeypatch.setattr(epub, "read_epub", lambda _: create_mock_epub())

        # Act & Assert
        with pytest.raises(BookProcessingError) as exc_info:
            read_book(Path("test.epub"))

        assert "Failed to read book: Parse error" in str(exc_info.value)

    def test_epub_read_error(self, monkeypatch):
        # Arrange
        class MockEpubException(Exception):
            def __init__(self, msg):
                self.msg = msg
                super().__init__(msg)

        def mock_read_epub_error(path: str):
            raise MockEpubException("Failed to read EPUB")

        monkeypatch.setattr(epub, "read_epub", mock_read_epub_error)
        monkeypatch.setattr(epub, "EpubException", MockEpubException)

        # Act & Assert
        with pytest.raises(BookProcessingError) as exc_info:
            read_book(Path("test.epub"))

        assert "Failed to read book: Failed to read EPUB" in str(exc_info.value)

    def test_multiple_content_items(self, monkeypatch):
        # Arrange
        mock_epub = create_mock_epub()
        mock_item2 = MagicMock()
        mock_item2.get_type.return_value = ITEM_DOCUMENT
        mock_item2.get_content.return_value = (
            b"<html><body>More content</body></html>"
        )
        mock_epub.get_items.return_value = [
            mock_epub.get_items.return_value[0],
            mock_item2,
        ]

        monkeypatch.setattr("file.reader.parse_html", mock_parse_html)
        monkeypatch.setattr(epub, "read_epub", lambda _: mock_epub)

        # Act
        book = read_book(Path("test.epub"))

        # Assert
        assert book.content == "Test content Test content"
