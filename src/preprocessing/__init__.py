"""Vietnamese NLP text preprocessing and feature engineering package."""

from __future__ import annotations

from .pipeline import (
    TextPreprocessor,
    extract_auxiliary_features,
    preprocess_pipeline,
)
from .stopwords import (
    DOMAIN_PROTECTED_WORDS,
    EFFECTIVE_STOPWORDS,
    VIETNAMESE_STOPWORDS,
    get_stopwords,
    remove_stopwords,
)
from .teencode_dictionary import (
    LEET_SPEAK_PATTERNS,
    TEENCODE_DICT,
    UNACCENTED_COMPOUNDS,
)
from .text_cleaner import (
    clean_text,
    deobfuscate_leetspeak,
    normalize_tone_marks,
    normalize_unicode,
    teencode_normalize,
)
from .tokenizer import (
    ViTextTokenizer,
    join_unaccented_compounds,
    segment_vietnamese,
    tokenize_words,
)

__all__ = [
    "normalize_unicode",
    "normalize_tone_marks",
    "deobfuscate_leetspeak",
    "teencode_normalize",
    "clean_text",
    "TEENCODE_DICT",
    "LEET_SPEAK_PATTERNS",
    "UNACCENTED_COMPOUNDS",
    "join_unaccented_compounds",
    "segment_vietnamese",
    "tokenize_words",
    "ViTextTokenizer",
    "VIETNAMESE_STOPWORDS",
    "DOMAIN_PROTECTED_WORDS",
    "EFFECTIVE_STOPWORDS",
    "get_stopwords",
    "remove_stopwords",
    "extract_auxiliary_features",
    "preprocess_pipeline",
    "TextPreprocessor",
]
