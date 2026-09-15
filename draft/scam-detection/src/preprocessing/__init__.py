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
from .text_cleaner import (
    TEENCODE_DICT,
    clean_text,
    normalize_unicode,
    teencode_normalize,
)
from .tokenizer import (
    ViTextTokenizer,
    segment_vietnamese,
    tokenize_words,
)

__all__ = [
    "normalize_unicode",
    "teencode_normalize",
    "clean_text",
    "TEENCODE_DICT",
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
