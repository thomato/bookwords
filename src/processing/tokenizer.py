from typing import List

import nltk

from src.config import REQUIRED_NLTK_PACKAGES


def ensure_nltk_data() -> None:
    """Ensure required NLTK data is available."""
    for package in REQUIRED_NLTK_PACKAGES:
        try:
            nltk.data.find(f"corpora/{package}")
        except LookupError:
            nltk.download(package)


def tokenize(text: str) -> List[str]:
    """Tokenize text into words."""
    ensure_nltk_data()
    return nltk.word_tokenize(text)
