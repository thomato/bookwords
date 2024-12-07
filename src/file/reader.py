from pathlib import Path
from typing import Protocol

from ebooklib import ITEM_DOCUMENT, epub

from config import ENCODING, SUPPORTED_FORMATS
from core.book import Book
from file import parse_html
from utils.exceptions import BookProcessingError


class BookReader(Protocol):
    """Protocol for book readers."""

    def read(self, path: Path) -> Book:
        """Read book from file."""


def read_book(path: Path) -> Book:
    """Read book from file using appropriate reader."""
    if path.suffix not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {path.suffix}")

    try:
        if path.suffix == ".epub":
            return _read_epub(path)

    except Exception as e:
        raise BookProcessingError(f"Failed to read book: {str(e)}", path, e)


def _read_epub(path: Path) -> Book:
    """Read EPUB format book."""
    book = epub.read_epub(str(path))
    content = []

    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            html_content = item.get_content().decode(ENCODING)
            text = parse_html(html_content)
            content.append(text)

    return Book(
        title=_get_metadata(book, "title", "Unknown Title"),
        author=_get_metadata(book, "creator", "Unknown Author"),
        content=" ".join(content),
    )


def _get_metadata(book: epub.EpubBook, field: str, default: str) -> str:
    """Safely extract metadata with fallback."""
    try:
        return book.get_metadata("DC", field)[0][0]
    except (IndexError, KeyError, AttributeError):
        return default
