"""Vietnamese word segmentation and tokenization module using pyvi."""

from __future__ import annotations

import logging
from typing import List

try:
    from pyvi import ViTokenizer
except ImportError:  # pragma: no cover
    ViTokenizer = None
    logging.warning("pyvi library not installed. Falling back to basic whitespace tokenizer.")


def segment_vietnamese(text: str) -> str:
    """Segment Vietnamese compound words using pyvi (e.g. 'công an' -> 'công_an')."""
    if not isinstance(text, str) or not text.strip():
        return ""
    if ViTokenizer is not None:
        try:
            return ViTokenizer.tokenize(text)
        except Exception as exc:  # pragma: no cover
            logging.error("ViTokenizer error: %s. Returning raw text.", exc)
            return text
    return text


def tokenize_words(text: str) -> List[str]:
    """Tokenize Vietnamese text into a list of word tokens."""
    segmented = segment_vietnamese(text)
    return segmented.split()


class ViTextTokenizer:
    """Configurable Vietnamese text tokenizer class."""

    def __init__(self, join_char: str = "_") -> None:
        self.join_char = join_char

    def tokenize(self, text: str) -> str:
        """Tokenize text into compound words joined by underscore."""
        segmented = segment_vietnamese(text)
        if self.join_char != "_":
            segmented = segmented.replace("_", self.join_char)
        return segmented

    def __call__(self, text: str) -> str:
        """Allow class instance to be called as a callable."""
        return self.tokenize(text)
