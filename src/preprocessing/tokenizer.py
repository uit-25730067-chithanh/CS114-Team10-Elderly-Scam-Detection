"""Vietnamese word segmentation and tokenization module using pyvi and unaccented adaptations."""

from __future__ import annotations

import logging
import re
from typing import List

from .teencode_dictionary import UNACCENTED_COMPOUNDS

try:
    from pyvi import ViTokenizer
except ImportError:  # pragma: no cover
    ViTokenizer = None
    logging.warning("pyvi library not installed. Falling back to basic whitespace tokenizer.")


def join_unaccented_compounds(text: str) -> str:
    """Join common unaccented Vietnamese compound words with underscores."""
    if not isinstance(text, str) or not text.strip():
        return ""
    joined = text
    for phrase, replacement in UNACCENTED_COMPOUNDS.items():
        pattern = r"\b" + re.escape(phrase) + r"\b"
        joined = re.sub(pattern, replacement, joined, flags=re.IGNORECASE)
    return joined


def segment_vietnamese(text: str, join_unaccented: bool = True) -> str:
    """Segment Vietnamese compound words with pyvi and adaptive unaccented joining."""
    if not isinstance(text, str) or not text.strip():
        return ""

    # Phase 1: Join common unaccented compound phrases
    if join_unaccented:
        text = join_unaccented_compounds(text)

    # Phase 2: PyVi tokenization for accented Vietnamese compound words
    if ViTokenizer is not None:
        try:
            return ViTokenizer.tokenize(text)
        except Exception as exc:  # pragma: no cover
            logging.error("ViTokenizer error: %s. Returning partially joined text.", exc)
            return text
    return text


def tokenize_words(text: str) -> List[str]:
    """Tokenize Vietnamese text into a list of word tokens."""
    segmented = segment_vietnamese(text)
    return segmented.split()


class ViTextTokenizer:
    """Configurable Vietnamese text tokenizer class with adaptive unaccented joining."""

    def __init__(self, join_char: str = "_", join_unaccented: bool = True) -> None:
        self.join_char = join_char
        self.join_unaccented = join_unaccented

    def tokenize(self, text: str) -> str:
        """Tokenize text into compound words joined by configured join_char."""
        segmented = segment_vietnamese(text, join_unaccented=self.join_unaccented)
        if self.join_char != "_":
            segmented = segmented.replace("_", self.join_char)
        return segmented

    def __call__(self, text: str) -> str:
        """Allow class instance to be called as a callable."""
        return self.tokenize(text)
