"""Text cleaning and normalization module for Vietnamese scam text."""

from __future__ import annotations

import re
import unicodedata

# Dictionary of common Vietnamese SMS abbreviations, teencode, and domain terms
TEENCODE_DICT: dict[str, str] = {
    # Pronouns & Common slang
    "ko": "không",
    "k": "không",
    "kh": "không",
    "hok": "không",
    "hông": "không",
    "dc": "được",
    "đc": "được",
    "ng": "người",
    "vs": "với",
    "mk": "mình",
    "mik": "mình",
    "mềnh": "mình",
    "bn": "bạn",
    "mn": "mọi người",
    "r": "rồi",
    "ch": "chưa",
    "bt": "bình thường",
    "tks": "cảm ơn",
    "ty": "cảm ơn",
    "thks": "cảm ơn",
    "thanks": "cảm ơn",
    "nhug": "nhưng",
    # Communication & Interaction
    "ib": "nhắn tin",
    "inbox": "nhắn tin",
    "rep": "trả lời",
    "tl": "trả lời",
    "nt": "nhắn tin",
    "kb": "kết bạn",
    "dt": "điện thoại",
    "đt": "điện thoại",
    "sdt": "số điện thoại",
    "fb": "facebook",
    "zalo": "zalo",
    # Banking & Transaction terminology
    "ck": "chuyển khoản",
    "tk": "tài khoản",
    "stk": "số tài khoản",
    "acc": "tài khoản",
    "pass": "mật khẩu",
    "nh": "ngân hàng",
    "atm": "thẻ ngân hàng",
    "otp": "mã xác thực",
    "vnd": "đồng",
    "vnđ": "đồng",
    "tr": "triệu",
    "ngàn": "nghìn",
    "k": "nghìn",
    # Administrative & Public Authority abbreviations
    "cmnd": "chứng minh nhân dân",
    "cccd": "căn cước công dân",
    "bhyt": "bảo hiểm y tế",
    "bhxh": "bảo hiểm xã hội",
    "ca": "công an",
    "cs": "cảnh sát",
    "vks": "viện kiểm sát",
    "ta": "tòa án",
    "bca": "bộ công an",
    "byt": "bộ y tế",
    "bv": "bệnh viện",
    "vneid": "vneid",
    # Common banks
    "vcb": "vietcombank",
    "tcb": "techcombank",
    "bidv": "bidv",
    "ctg": "vietinbank",
    "acb": "acb",
    "mb": "mbbank",
    "vpb": "vpbank",
    "tpb": "tpbank",
    "shb": "shb",
    "hdb": "hdbank",
    "vib": "vib",
    "msb": "msb",
    "ocb": "ocb",
    "scb": "scb",
}

# Regex pattern for retaining valid Vietnamese characters, alphanumeric tokens, and spaces
VIETNAMESE_CHARS_PATTERN = re.compile(
    r"[^\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]",
    re.IGNORECASE | re.UNICODE,
)


def normalize_unicode(text: str) -> str:
    """Normalize text into Unicode NFC standard for Vietnamese."""
    if not isinstance(text, str):
        return ""
    return unicodedata.normalize("NFC", text)


def teencode_normalize(text: str) -> str:
    """Normalize abbreviations and teencode words according to dictionary."""
    if not text:
        return ""
    words = text.split()
    normalized_words = [TEENCODE_DICT.get(w.lower(), w) for w in words]
    return " ".join(normalized_words)


def clean_text(text: str, apply_teencode: bool = True) -> str:
    """Execute text cleaning pipeline on raw Vietnamese text."""
    if not isinstance(text, str) or not text.strip():
        return ""

    # Step 1: Unicode NFC normalization
    cleaned = normalize_unicode(text)

    # Step 2: Lowercase conversion
    cleaned = cleaned.lower()

    # Step 3: Remove URLs (http, https, www)
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)

    # Step 4: Remove phone numbers (10-11 digit Vietnamese prefixes)
    cleaned = re.sub(r"\b(0|\+?84)\d{9,10}\b", " ", cleaned)

    # Step 5: Remove email addresses
    cleaned = re.sub(r"\S+@\S+", " ", cleaned)

    # Step 6: Normalize teencode and abbreviations
    if apply_teencode:
        cleaned = teencode_normalize(cleaned)

    # Step 7: Filter special characters while preserving Vietnamese diacritics
    cleaned = VIETNAMESE_CHARS_PATTERN.sub(" ", cleaned)

    # Step 8: Collapse multiple spaces and strip
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Fallback: If cleaning completely wiped out text, preserve alphanumeric base
    if not cleaned and text.strip():
        cleaned = re.sub(r"\s+", " ", text).strip().lower()

    return cleaned
