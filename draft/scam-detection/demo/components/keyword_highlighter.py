"""Component for highlighting psychological manipulation keywords and scam signals in text."""

import re
import html
from typing import Dict, List, Tuple

# Patterns for psychological scam categories
PATTERNS = {
    "authority": {
        "label": "Bẫy Quyền lực & Dọa nạt",
        "color": "#DC2626",      # Đỏ đậm
        "bg": "#FEE2E2",         # Nền đỏ nhạt
        "regex": re.compile(
            r"(công an|cảnh sát|viện kiểm sát|tòa án|bộ công an|bộ y tế|cục thuế|"
            r"lệnh bắt|tạm giam|truy nã|khởi tố|điều tra viên|áp giải|bắt giữ|phong tỏa|rửa tiền)",
            re.IGNORECASE
        )
    },
    "urgency": {
        "label": "Thúc ép Thời gian & Cấp cứu",
        "color": "#EA580C",      # Cam đậm
        "bg": "#FFEDD5",         # Nền cam nhạt
        "regex": re.compile(
            r"(cấp cứu|tai nạn|mổ gấp|nguy kịch|chấn thương|viện phí|bệnh viện|chợ rẫy|"
            r"trong vòng \d+ phút|ngay lập tức|khẩn cấp|gấp|trong 2 giờ|ngay hôm nay)",
            re.IGNORECASE
        )
    },
    "financial": {
        "label": "Đòi Chuyển tiền & Mã OTP",
        "color": "#B91C1C",      # Đỏ mận
        "bg": "#FDF2F8",         # Nền hồng nhạt
        "regex": re.compile(
            r"(chuyển tiền|chuyển khoản|số tài khoản|chủ tk|ngân hàng|techcombank|mb bank|"
            r"mã otp|mã xác thực|mật khẩu|tiết kiệm|phí bảo chứng|\d+[\.,]?\d*\s*(triệu|tỷ|nghìn|tr|đ|vnd))",
            re.IGNORECASE
        )
    },
    "fake_gift": {
        "label": "Bẫy Quà tặng & Thuốc tiên",
        "color": "#7C3AED",      # Tím
        "bg": "#F3E8FF",         # Nền tím nhạt
        "regex": re.compile(
            r"(trúng thưởng|tri ân|tặng quà|miễn phí|quà tết|lì xì|may mắn|"
            r"thuốc thảo dược|thuốc tiên|trị dứt điểm|sữa canxi|phí vận chuyển|phí giao hàng)",
            re.IGNORECASE
        )
    },
    "link": {
        "label": "Đường dẫn lạ (Link nghi vấn)",
        "color": "#2563EB",      # Xanh dương
        "bg": "#DBEAFE",         # Nền xanh nhạt
        "regex": re.compile(
            r"(https?://\S+|www\.\S+|\[đường_dẫn\]|\[url\])",
            re.IGNORECASE
        )
    }
}


def extract_psychological_flags(text: str) -> List[Dict[str, str]]:
    """Detect psychological manipulation triggers present in the message."""
    flags = []
    for cat, conf in PATTERNS.items():
        matches = conf["regex"].findall(text)
        if matches:
            unique_matches = list(set([m[0] if isinstance(m, tuple) else m for m in matches]))
            flags.append({
                "category": cat,
                "label": conf["label"],
                "color": conf["color"],
                "bg": conf["bg"],
                "matches": unique_matches[:4]
            })
    return flags


def highlight_scam_keywords(text: str, is_elderly_mode: bool = False) -> str:
    """Highlight scam trigger words in text with styled HTML badges for easy reading."""
    font_size = "22px" if is_elderly_mode else "17px"
    line_height = "1.8" if is_elderly_mode else "1.6"

    # Escape HTML to prevent injection
    safe_text = html.escape(text)

    # Collect all match spans
    spans = []
    for cat, conf in PATTERNS.items():
        for match in conf["regex"].finditer(safe_text):
            spans.append((match.start(), match.end(), cat, conf["color"], conf["bg"]))

    if not spans:
        return f'<div style="font-size:{font_size}; line-height:{line_height}; color:#1E293B;">{safe_text}</div>'

    # Sort spans by start index, avoiding overlaps
    spans.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    merged_spans = []
    last_end = 0
    for start, end, cat, color, bg in spans:
        if start >= last_end:
            merged_spans.append((start, end, cat, color, bg))
            last_end = end

    # Construct HTML with highlighted tags
    html_out = []
    curr = 0
    for start, end, cat, color, bg in merged_spans:
        if start > curr:
            html_out.append(safe_text[curr:start])
        matched_str = safe_text[start:end]
        html_out.append(
            f'<mark style="background-color:{bg}; color:{color}; font-weight:700; '
            f'padding:2px 6px; border-radius:4px; border-bottom:2px solid {color};">'
            f'{matched_str}</mark>'
        )
        curr = end
    if curr < len(safe_text):
        html_out.append(safe_text[curr:])

    result_content = "".join(html_out)
    return (
        f'<div style="font-size:{font_size}; line-height:{line_height}; color:#0F172A; '
        f'background-color:#F8FAFC; padding:18px; border-radius:10px; border:2px solid #E2E8F0; '
        f'word-break:break-word;">{result_content}</div>'
    )
