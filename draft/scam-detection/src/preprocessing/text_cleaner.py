"""Text cleaning and normalization module for Vietnamese scam text."""

from __future__ import annotations

import logging
import re
import unicodedata

from .teencode_dictionary import LEET_SPEAK_PATTERNS, TEENCODE_DICT

try:
    from underthesea import text_normalize
except ImportError:  # pragma: no cover
    text_normalize = None
    logging.warning("underthesea not available. Using fallback unicode NFC normalization.")

# Regex pattern for retaining valid Vietnamese characters, alphanumeric tokens, and spaces
VIETNAMESE_CHARS_PATTERN = re.compile(
    r"[^\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]",
    re.IGNORECASE | re.UNICODE,
)

# Regex for repeated characters (e.g. 'nhaaaaa' -> 'nha', 'gấpppp' -> 'gấp')
REPEATED_CHARS_PATTERN = re.compile(
    r"([a-zA-Zàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ])\1{2,}",
    re.IGNORECASE,
)


def normalize_unicode(text: str) -> str:
    """Normalize text into Unicode NFC standard for Vietnamese."""
    if not isinstance(text, str):
        return ""
    return unicodedata.normalize("NFC", text)


def normalize_tone_marks(text: str) -> str:
    """Normalize Vietnamese tone mark placement (quy tắc đặt dấu mới) using underthesea."""
    if not isinstance(text, str) or not text.strip():
        return ""
    normalized = normalize_unicode(text)
    if text_normalize is not None:
        try:
            return text_normalize(normalized)
        except Exception:  # pragma: no cover
            return normalized
    return normalized


def deobfuscate_leetspeak(text: str) -> str:
    """De-obfuscate deliberate character/number substitutions used in scam messages."""
    if not text:
        return ""
    # Separate bracketed tokens that are glued to adjacent words (e.g. '[ĐƯỜNG_DẪN]de' -> '[ĐƯỜNG_DẪN] de')
    text = re.sub(r"(\[[A-Z0-9_ÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ]+\])([a-zA-Zà-ỹ0-9])", r"\1 \2", text)
    text = re.sub(r"([a-zA-Zà-ỹ0-9])(\[[A-Z0-9_ÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ]+\])", r"\1 \2", text)

    # Apply leet-speak regex substitutions
    for pattern, replacement in LEET_SPEAK_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Collapse elongated repeated characters
    text = REPEATED_CHARS_PATTERN.sub(r"\1", text)
    return text


def teencode_normalize(text: str) -> str:
    """Normalize abbreviations and teencode words according to comprehensive dictionary."""
    if not text:
        return ""
    words = text.split()
    normalized_words = [TEENCODE_DICT.get(w.lower(), w) for w in words]
    return " ".join(normalized_words)


def clean_text(text: str, apply_teencode: bool = True, apply_deobfuscation: bool = True) -> str:
    """Execute deep text cleaning pipeline on raw Vietnamese text."""
    if not isinstance(text, str) or not text.strip():
        return ""

    # Step 1: De-obfuscate leet-speak & separate glued entity tags
    if apply_deobfuscation:
        cleaned = deobfuscate_leetspeak(text)
    else:
        cleaned = text

    # Step 2: Tone mark placement normalization (underthesea) & Unicode NFC
    cleaned = normalize_tone_marks(cleaned)

    # Step 3: Lowercase conversion
    cleaned = cleaned.lower()

    # Step 4: Remove raw URLs (http, https, www) and normalize bracketed URLs
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)
    cleaned = re.sub(r"\[đường_dẫn\]|\[url\]", " link_truy_cap ", cleaned)

    # Step 5: Remove raw phone numbers and normalize bracketed phone tags
    cleaned = re.sub(r"\b(0|\+?84)\d{8,10}\b", " ", cleaned)
    cleaned = re.sub(r"\[số_điện_thoại\]|\[hotline\]", " so_dien_thoai ", cleaned)

    # Step 6: Remove email addresses
    cleaned = re.sub(r"\S+@\S+", " ", cleaned)

    # Step 7: Normalize money and OTP tags to meaningful semantic tokens
    cleaned = re.sub(r"\[money\]|\[số_tiền\]", " so_tien ", cleaned)
    cleaned = re.sub(r"\[mã_otp\]", " ma_otp ", cleaned)
    cleaned = re.sub(r"\[thương_hiệu\]", " thuong_hieu ", cleaned)

    # Step 8: Normalize teencode and abbreviations
    if apply_teencode:
        cleaned = teencode_normalize(cleaned)

    # Step 9: Filter special characters while preserving Vietnamese diacritics
    cleaned = VIETNAMESE_CHARS_PATTERN.sub(" ", cleaned)

    # Step 10: Collapse multiple spaces and strip
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Fallback: If cleaning completely wiped out text, preserve alphanumeric base
    if not cleaned and text.strip():
        cleaned = re.sub(r"\s+", " ", text).strip().lower()

    return cleaned
