from pathlib import Path
from typing import List

from ebooklib import ITEM_DOCUMENT, epub

from file import parse_html
from src.core.book import Book
from src.utils.exceptions import BookProcessingError


class EPUBReader:
    @staticmethod
    def supported_formats() -> List[str]:
        return [".epub"]

    def read(self, file_path: Path) -> Book:
        try:
            book = epub.read_epub(str(file_path))

            # Extract and parse content
            content = []
            for item in book.get_items():
                if item.get_type() == ITEM_DOCUMENT:
                    html_content = item.get_content().decode("utf-8")
                    text = parse_html(html_content)
                    content.append(text)

            # Extract metadata
            title = self._get_metadata_safely(book, "title")
            author = self._get_metadata_safely(book, "creator")

            return Book(title=title, author=author, content=" ".join(content))

        except Exception as e:
            raise BookProcessingError(f"Failed to process EPUB file: {str(e)}")

    @staticmethod
    def _get_metadata_safely(book: epub.EpubBook, field: str) -> str:
        """Safely extract metadata with fallback values."""
        try:
            return book.get_metadata("DC", field)[0][0]
        except (IndexError, KeyError, AttributeError):
            return f"Unknown {field}"
