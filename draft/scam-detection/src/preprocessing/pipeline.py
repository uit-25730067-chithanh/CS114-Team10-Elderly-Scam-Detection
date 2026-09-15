"""Full Vietnamese NLP preprocessing pipeline and 14-dimension auxiliary feature extraction."""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Tuple

import pandas as pd

from .stopwords import remove_stopwords
from .text_cleaner import clean_text
from .tokenizer import segment_vietnamese

# Regex patterns for auxiliary feature extraction (including masked entity tokens)
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+|\[đường_dẫn\]|\[url\]", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"\b(0|\+?84)\d{8,10}\b|\[số_điện_thoại\]|\[hotline\]", re.IGNORECASE)
MONEY_PATTERN = re.compile(
    r"\d+[\.,]?\d*\s*(triệu|tỷ|nghìn|ngàn|k|tr|đ|vnd|vnđ|đồng)\b|\[money\]|\[số_tiền\]",
    re.IGNORECASE,
)
URGENT_PATTERN = re.compile(
    r"(gấp|khẩn|ngay lập tức|hạn chót|trong ngày|ngay hôm nay|trong vòng \d+ phút|"
    r"phong tỏa|bắt giam|truy nã|khóa thẻ|khóa tài khoản|tạm khóa|tạm giữ|hết hạn|mổ gấp)",
    re.IGNORECASE,
)
AUTHORITY_PATTERN = re.compile(
    r"(công an|cảnh sát|viện kiểm sát|tòa án|bộ công an|bộ y tế|cục thuế|"
    r"bảo hiểm xã hội|vneid|điều tra viên|phòng pháp lý|bộ kh&cn|ubnd)",
    re.IGNORECASE,
)
EMERGENCY_PATTERN = re.compile(
    r"(cấp cứu|tai nạn|bệnh viện|viện phí|nguy kịch|mất máu|chấn thương|bác sĩ|chợ rẫy|bạch mai)",
    re.IGNORECASE,
)
GIFT_PATTERN = re.compile(
    r"(trúng thưởng|tri ân|tặng quà|miễn phí|lì xì|quay số|quà tết|liệu trình|khuyến mại|may mắn)",
    re.IGNORECASE,
)
OTP_PATTERN = re.compile(
    r"(mã otp|mã xác thực|mật khẩu|mã gd|xác thực ngay|\[mã_otp\])",
    re.IGNORECASE,
)
LEET_PATTERN = re.compile(
    r"\b(th0ng|ba0|kh0ng|kh0a|l0ng|d[!1]eu|t[!1]en|h0 tro|bhtn)\b",
    re.IGNORECASE,
)
ACCENT_PATTERN = re.compile(
    r"[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]",
    re.IGNORECASE,
)


def extract_auxiliary_features(text: str) -> Dict[str, Any]:
    """Extract 14 metadata, psychological manipulation, and domain features prior to cleaning."""
    if not isinstance(text, str):
        text = ""

    words = text.split()
    return {
        "num_urls": len(URL_PATTERN.findall(text)),
        "num_phone_numbers": len(PHONE_PATTERN.findall(text)),
        "num_money_mentions": len(MONEY_PATTERN.findall(text)),
        "has_urgent_words": int(bool(URGENT_PATTERN.search(text))),
        "num_authority_words": len(AUTHORITY_PATTERN.findall(text)),
        "has_emergency_words": int(bool(EMERGENCY_PATTERN.search(text))),
        "has_gift_words": int(bool(GIFT_PATTERN.search(text))),
        "has_otp_request": int(bool(OTP_PATTERN.search(text))),
        "has_leet_speak": int(bool(LEET_PATTERN.search(text))),
        "is_unaccented": int(not bool(ACCENT_PATTERN.search(text))),
        "text_length": len(text),
        "num_words": len(words),
        "num_exclamation": text.count("!"),
        "num_question": text.count("?"),
        "num_uppercase_words": sum(1 for w in words if w.isupper() and len(w) > 1),
    }


def preprocess_pipeline(text: str) -> Tuple[str, Dict[str, Any]]:
    """Execute end-to-end preprocessing on raw text. Returns (cleaned_text, features)."""
    # 1. Extract 14 auxiliary features from raw text before cleaning
    aux_features = extract_auxiliary_features(text)

    # 2. Deep text cleaning (leet-speak deobfuscation, tone normalization, teencode, noise removal)
    cleaned = clean_text(text)

    # 3. Vietnamese compound word segmentation (pyvi + unaccented adaptive joining)
    segmented = segment_vietnamese(cleaned)

    # 4. Filter grammatical stopwords while strictly guarding domain indicators
    final_text = remove_stopwords(segmented)

    # 5. Fallback check: Ensure result is never an empty string
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
        """Transform a pandas DataFrame, adding text_cleaned and 14 auxiliary columns."""
        df_copy = df.copy()
        pipeline_results = df_copy[text_column].apply(preprocess_pipeline)

        df_copy["text_cleaned"] = pipeline_results.apply(lambda item: item[0])
        aux_df = pd.DataFrame(pipeline_results.apply(lambda item: item[1]).tolist(), index=df_copy.index)

        return pd.concat([df_copy, aux_df], axis=1)
