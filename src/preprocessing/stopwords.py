"""Vietnamese stopword removal module with scam-domain preservation safeguards."""

from __future__ import annotations

from typing import Iterable, Set

# Curated Vietnamese grammatical stopwords (conjunctions, prepositions, copulas)
VIETNAMESE_STOPWORDS: Set[str] = {
    "và", "là", "của", "được", "cho", "với", "trong", "này", "đó", "để",
    "từ", "theo", "về", "trên", "đã", "những", "các", "một", "cũng", "như",
    "nhưng", "hay", "thì", "mà", "rằng", "nếu", "khi", "tại", "rồi", "rất",
    "lại", "ra", "vào", "ở", "qua", "nữa", "bởi", "vì", "nên", "do_đó",
    "ngoài_ra", "tuy_nhiên", "tất_cả", "mỗi", "từng", "họ", "chúng_tôi", "tôi",
    "ai", "gì", "sao", "thế", "nào", "đâu", "bao_giờ", "vậy", "dường_như",
    "chỉ", "chỉ_là", "chính_là", "thật_ra", "thực_sự", "hầu_như", "dù_sao",
    "cho_nên", "do_vậy", "ngay_cả", "thậm_chí", "phải_chăng", "thay_vì",
    "tuy_thế", "nếu_như", "giá_như", "bởi_vì", "bởi_thế", "vì_thế", "cho_dù",
    "dẫu_cho", "dẫu_sao", "bấy_lâu", "tự_nhiên", "tức_thì", "thế_nên"
}

# Domain words that MUST NEVER be eliminated because they indicate scam/urgency
DOMAIN_PROTECTED_WORDS: Set[str] = {
    "công_an", "cảnh_sát", "viện_kiểm_sát", "tòa_án", "bộ_công_an",
    "phong_tỏa", "bắt_giam", "truy_nã", "lệnh_bắt", "điều_tra",
    "khẩn_cấp", "khẩn", "gấp", "ngay_lập_tức", "nguy_kịch", "cấp_cứu", "tai_nạn",
    "tiền", "triệu", "tỷ", "nghìn", "tài_khoản", "ngân_hàng", "chuyển_khoản",
    "mã_xác_thực", "mật_khẩu", "otp", "stk", "sdt", "điện_thoại",
    "quà", "trúng_thưởng", "miễn_phí", "tri_ân", "trợ_cấp", "bảo_hiểm",
    "căn_cước", "cccd", "vneid", "con", "cháu", "bố", "mẹ", "viện_phí",
}

# Clean effective stopwords by removing protected keywords
EFFECTIVE_STOPWORDS: Set[str] = VIETNAMESE_STOPWORDS - DOMAIN_PROTECTED_WORDS


def get_stopwords() -> Set[str]:
    """Return the set of active Vietnamese stopwords."""
    return set(EFFECTIVE_STOPWORDS)


def remove_stopwords(text: str, custom_stopwords: Iterable[str] | None = None) -> str:
    """Remove stopwords from tokenized Vietnamese text."""
    if not isinstance(text, str) or not text.strip():
        return ""

    stopwords = EFFECTIVE_STOPWORDS if custom_stopwords is None else set(custom_stopwords)
    words = text.split()
    filtered_words = [w for w in words if w not in stopwords or w in DOMAIN_PROTECTED_WORDS]

    # Fallback: if stopword removal results in an empty text, keep the original words
    if not filtered_words:
        return text.strip()

    return " ".join(filtered_words)
