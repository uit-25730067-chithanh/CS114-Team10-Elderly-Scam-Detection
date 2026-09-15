"""Full Vietnamese NLP preprocessing pipeline and auxiliary feature extraction."""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Tuple

import pandas as pd

from .stopwords import remove_stopwords
from .text_cleaner import clean_text
from .tokenizer import segment_vietnamese

# Regex patterns for auxiliary feature extraction
PHONE_PATTERN = re.compile(r"\b(0|\+?84)\d{9,10}\b")
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
MONEY_PATTERN = re.compile(
    r"\d+[\.,]?\d*\s*(triệu|tỷ|nghìn|ngàn|k|tr|đ|vnd|vnđ|đồng)\b",
    re.IGNORECASE,
)
URGENT_PATTERN = re.compile(
    r"(gấp|khẩn|ngay lập tức|hạn chót|trong ngày|ngay hôm nay|trong vòng \d+ phút|"
    r"phong tỏa|bắt giam|truy nã|khóa thẻ|khóa tài khoản|tạm giữ)",
    re.IGNORECASE,
)
AUTHORITY_PATTERN = re.compile(
    r"(công an|cảnh sát|viện kiểm sát|tòa án|bộ công an|bộ y tế|cục thuế|"
    r"bảo hiểm xã hội|vneid|điều tra viên)",
    re.IGNORECASE,
)


def extract_auxiliary_features(text: str) -> Dict[str, Any]:
    """Extract metadata and domain-specific features prior to text cleaning."""
    if not isinstance(text, str):
        text = ""

    words = text.split()
    return {
        "num_phone_numbers": len(PHONE_PATTERN.findall(text)),
        "num_urls": len(URL_PATTERN.findall(text)),
        "num_money_mentions": len(MONEY_PATTERN.findall(text)),
        "has_urgent_words": int(bool(URGENT_PATTERN.search(text))),
        "num_authority_words": len(AUTHORITY_PATTERN.findall(text)),
        "text_length": len(text),
        "num_words": len(words),
        "num_exclamation": text.count("!"),
        "num_question": text.count("?"),
        "num_uppercase_words": sum(1 for w in words if w.isupper() and len(w) > 1),
    }


def preprocess_pipeline(text: str) -> Tuple[str, Dict[str, Any]]:
    """Execute end-to-end preprocessing on raw text. Returns (cleaned_text, features)."""
    # 1. Extract auxiliary features from raw text
    aux_features = extract_auxiliary_features(text)

    # 2. Clean text (Unicode NFC, lowercase, teencode, noise removal)
    cleaned = clean_text(text)

    # 3. Vietnamese compound word segmentation (pyvi)
    segmented = segment_vietnamese(cleaned)

    # 4. Filter grammatical stopwords while guarding domain indicators
    final_text = remove_stopwords(segmented)

    # 5. Fallback check: Ensure result is not empty string
    if not final_text.strip() and cleaned.strip():
        final_text = cleaned.strip()

    return final_text, aux_features


class TextPreprocessor:
    """Scikit-learn compatible and DataFrame batch text preprocessor."""

    def __init__(self, apply_stopwords: bool = True) -> None:
        self.apply_stopwords = apply_stopwords

    def fit(self, X: Any = None, y: Any = None) -> TextPreprocessor:
        """Fit preprocessor parameters (stateless)."""
        return self

    def transform(self, texts: Iterable[str]) -> List[Tuple[str, Dict[str, Any]]]:
        """Transform an iterable of texts into preprocessed tuples."""
        return [preprocess_pipeline(str(t)) for t in texts]

    def process_dataframe(
        self,
        df: pd.DataFrame,
        text_column: str = "text",
    ) -> pd.DataFrame:
        """Transform a pandas DataFrame, adding text_cleaned and auxiliary columns."""
        df_copy = df.copy()
        pipeline_results = df_copy[text_column].apply(preprocess_pipeline)

        df_copy["text_cleaned"] = pipeline_results.apply(lambda item: item[0])
        aux_df = pd.DataFrame(pipeline_results.apply(lambda item: item[1]).tolist(), index=df_copy.index)

        return pd.concat([df_copy, aux_df], axis=1)
