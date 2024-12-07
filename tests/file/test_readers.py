from pathlib import Path
from unittest.mock import MagicMock

import ebooklib
import pytest
from ebooklib import epub

from src.file.parsers import HTMLParser
from src.file.reader import EPUBReader
from src.utils.exceptions import BookProcessingError


class MockHTMLParser(HTMLParser):
    def __init__(self, text: str):
        self._text = text

    def extract_text(self, html: str) -> str:
        return self._text


def create_mock_epub():
    mock_epub = MagicMock(spec=epub.EpubBook)
    mock_epub.get_metadata.side_effect = lambda dc, field: [[f"Test {field}"]]
    mock_item = MagicMock()
    mock_item.get_type.return_value = ebooklib.ITEM_DOCUMENT
    mock_item.get_content.return_value = (
        b"<html><body>Test content</body></html>"
    )
    mock_epub.get_items.return_value = [mock_item]
    return mock_epub


def test_supported_formats():
    reader = EPUBReader()
    assert ".epub" in reader.supported_formats()


@pytest.mark.usefixtures("monkeypatch")
class TestEPUBReader:
    def test_successful_read(self, monkeypatch):
        # Arrange
        mock_html_parser = MockHTMLParser("Parsed content")
        reader = EPUBReader(html_parser=mock_html_parser)

        # Act
        monkeypatch.setattr(epub, "read_epub", lambda _: create_mock_epub())
        book = reader.read(Path("test.epub"))

        # Assert
        assert book.title == "Test title"
        assert book.author == "Test creator"
        assert "Parsed content" in book.content

    def test_missing_metadata(self, monkeypatch):
        # Arrange
        mock_epub = create_mock_epub()
        mock_epub.get_metadata.side_effect = IndexError

        reader = EPUBReader(html_parser=MockHTMLParser("test"))

        # Act
        monkeypatch.setattr(epub, "read_epub", lambda _: mock_epub)
        book = reader.read(Path("test.epub"))

        # Assert
        assert book.title == "Unknown title"
        assert book.author == "Unknown creator"

    def test_html_parsing_error(self, monkeypatch):
        # Arrange
        class ErrorHTMLParser(HTMLParser):
            def extract_text(self, html: str) -> str:
                raise ValueError("Parse error")

        reader = EPUBReader(html_parser=ErrorHTMLParser())
        monkeypatch.setattr(epub, "read_epub", lambda _: create_mock_epub())

        # Assert that the original ValueError is caught and wrapped
        # in a BookProcessingError with the correct message
        expected_error = None
        try:
            reader.read(Path("test.epub"))
        except Exception as e:
            expected_error = e

        assert expected_error is not None
        assert isinstance(expected_error, BookProcessingError)
        assert str(expected_error) == "Failed to process EPUB file: Parse error"
