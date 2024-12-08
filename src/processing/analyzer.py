from collections import Counter
from typing import Dict

from config import MAX_WORD_LENGTH, MIN_WORD_LENGTH
from core.statistics import WordStats
from processing.tokenizer import tokenize


def analyze_text(text: str) -> Dict[str, WordStats]:
    """Main analysis function for text content."""
    # Preprocess text
    tokens = tokenize(text.lower())
    words = [word for word in tokens if _is_valid_word(word)]

    # Calculate statistics
    word_counts = Counter(words)
    stats = {}

    for word, count in word_counts.items():
        stats[word] = WordStats(original_word=word, count=count)

    return stats


def _is_valid_word(word: str) -> bool:
    """Validate word based on configuration rules."""
    return word.isalpha() and MIN_WORD_LENGTH <= len(word) <= MAX_WORD_LENGTH
