from pathlib import Path
from typing import Dict, Tuple

from core.book import Book
from core.statistics import WordStats
from file.reader import read_book
from processing.analyzer import analyze_text
from utils.exceptions import BookProcessingError


def process_book(file_path: Path) -> Tuple[Book, Dict[str, WordStats]]:
    """
    Process a book file through the complete pipeline:

    1. Read the book file
    2. Analyze text content
    3. Return processed book with statistics
    """
    try:
        # Read book
        book = read_book(file_path)

        # Analyze content
        stats = analyze_text(book.content)

        return book, stats

    except Exception as e:
        raise BookProcessingError(
            message="Failed to process book",
            file_path=file_path,
            original_error=e,
        )
