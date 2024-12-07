from dataclasses import dataclass


@dataclass
class WordStats:
    """Class to hold word statistics."""

    original_word: str
    stem: str
    count: int
