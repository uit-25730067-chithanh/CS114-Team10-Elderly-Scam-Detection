"""Clean, high-contrast keyword highlighting and indicator extraction with animation."""

import re

SCAM_KEYWORDS = [
    # Cơ quan chức năng & đe dọa
    "bộ công an", "công an", "cảnh sát", "viện kiểm sát", "tòa án",
    "lệnh bắt", "lệnh tạm giam", "bắt tạm giam", "khởi tố", "truy nã",
    "rửa tiền", "buôn ma túy", "án hình sự", "thanh tra",
    
    # Tài chính & Chuyển tiền
    "chuyển tiền", "chuyển ngay", "tài khoản", "số tài khoản",
    "nộp tiền", "tạm ứng", "kho bạc", "phí vận chuyển", "bảo hiểm",
    "ngân hàng", "techcombank", "vietcombank", "mã otp", "mật khẩu",
    
    # Cấp bách & Hối thúc
    "khẩn cấp", "ngay lập tức", "trong vòng", "hôn mê sâu", "cấp cứu",
    "tai nạn", "phẫu thuật gấp", "tính mạng", "bất tuân lệnh", "cưỡng chế",
    
    # Cô lập nạn nhân
    "giữ bí mật", "tuyệt đối không", "không được nói", "không báo cho",
    "người nhà", "con cái"
]


def highlight_scam_keywords(text: str) -> str:
    """Highlights suspicious words with an animated soft yellow marker effect."""
    if not text:
        return ""

    escaped_keywords = [re.escape(k) for k in sorted(SCAM_KEYWORDS, key=len, reverse=True)]
    pattern = re.compile(r"(" + "|".join(escaped_keywords) + r")", re.IGNORECASE)

    def _replace(match):
        word = match.group(0)
        return (
            f'<mark class="marker-glow" style="background-color: #FEF08A; color: #854D0E; font-weight: 700; '
            f'padding: 2px 6px; border-radius: 4px; border-bottom: 2px solid #EAB308;">{word}</mark>'
        )

    highlighted = pattern.sub(_replace, text)
    formatted_html = (
        f'<div class="civic-animate-up" style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; '
        f'padding: 18px 20px; font-size: 19px; line-height: 1.7; color: #1E293B; font-family: -apple-system, BlinkMacSystemFont, sans-serif; '
        f'box-shadow: 0 1px 3px rgba(0,0,0,0.05);">'
        f'{highlighted}'
        f'</div>'
    )
    return formatted_html
