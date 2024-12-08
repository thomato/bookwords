from collections import Counter
from typing import Dict

from core.statistics import WordStats
from processing.tokenizer import tokenize


def analyze_text(text: str) -> Dict[str, WordStats]:
    """Main analysis function for text content."""
    # Preprocess text
    tokens = tokenize(text.lower())

    # Calculate statistics
    word_counts = Counter(tokens)
    stats = {}

    for word, count in word_counts.items():
        stats[word] = WordStats(original_word=word, count=count)

    return stats
