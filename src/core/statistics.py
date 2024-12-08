from dataclasses import dataclass


@dataclass
class WordStats:
    """Class to hold word statistics."""

    original_word: str
    count: int
