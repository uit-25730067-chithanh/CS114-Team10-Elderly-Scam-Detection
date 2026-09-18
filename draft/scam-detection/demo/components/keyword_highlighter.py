"""
Keyword Highlighter Component for Elderly Scam Detection App.
Author: Hoàng Cao Sơn (MSSV: 25730061)
"""

import re
from typing import List, Tuple

# Danh mục các từ khóa thao túng tâm lý điển hình nhắm vào người cao tuổi
RISK_PATTERNS = [
    # Nhóm 1: Đe dọa quyền lực (Pháp luật / Công an)
    ("công an", "#e74c3c"),
    ("cong an", "#e74c3c"),
    ("viện kiểm sát", "#e74c3c"),
    ("vien kiem sat", "#e74c3c"),
    ("tòa án", "#e74c3c"),
    ("toa an", "#e74c3c"),
    ("bắt tạm giam", "#c0392b"),
    ("bat tam giam", "#c0392b"),
    ("lệnh bắt", "#c0392b"),
    ("lenh bat", "#c0392b"),
    ("phạt nguội", "#e74c3c"),
    ("phat nguoi", "#e74c3c"),
    ("khởi tố", "#c0392b"),
    ("khoi to", "#c0392b"),
    ("phong tỏa tài khoản", "#c0392b"),
    ("phong toa tai khoan", "#c0392b"),
    ("hồ sơ vụ án", "#e74c3c"),
    ("ho so vu an", "#e74c3c"),
    ("điều tra", "#e74c3c"),
    ("dieu tra", "#e74c3c"),
    ("vi phạm", "#e67e22"),
    ("vi pham", "#e67e22"),
    ("truy nã", "#c0392b"),
    ("truy na", "#c0392b"),

    # Nhóm 2: Cấp cứu / Tai nạn người thân
    ("tai nạn", "#e74c3c"),
    ("tai nan", "#e74c3c"),
    ("cấp cứu", "#c0392b"),
    ("cap cuu", "#c0392b"),
    ("bệnh viện", "#e74c3c"),
    ("benh vien", "#e74c3c"),
    ("viện phí", "#c0392b"),
    ("vien phi", "#c0392b"),
    ("chuyển tiền gấp", "#c0392b"),
    ("chuyen tien gap", "#c0392b"),
    ("chuyển khoản ngay", "#c0392b"),
    ("chuyen khoan ngay", "#c0392b"),
    ("đừng gọi", "#d35400"),
    ("dung goi", "#d35400"),
    ("gấp lắm", "#e67e22"),
    ("gap lam", "#e67e22"),
    ("nguy kịch", "#c0392b"),
    ("nguy kich", "#c0392b"),
    ("mổ gấp", "#c0392b"),
    ("mo gap", "#c0392b"),

    # Nhóm 3: Giả mạo Dịch vụ công / VNeID
    ("vneid", "#d35400"),
    ("định danh", "#d35400"),
    ("dinh danh", "#d35400"),
    ("mức 2", "#d35400"),
    ("muc 2", "#d35400"),
    ("bảo hiểm xã hội", "#d35400"),
    ("bao hiem xa hoi", "#d35400"),
    ("nâng cấp sim", "#e67e22"),
    ("nang cap sim", "#e67e22"),
    ("đồng bộ dữ liệu", "#d35400"),
    ("dong bo du lieu", "#d35400"),
    ("cập nhật cccd", "#d35400"),
    ("cap nhat cccd", "#d35400"),
    ("thuế", "#e67e22"),
    ("thue", "#e67e22"),
    ("khóa sim", "#c0392b"),
    ("khoa sim", "#c0392b"),

    # Nhóm 4: Quà tặng / Sức khỏe / Trúng thưởng
    ("trúng thưởng", "#8e44ad"),
    ("trung thuong", "#8e44ad"),
    ("quà tri ân", "#8e44ad"),
    ("qua tri an", "#8e44ad"),
    ("miễn phí", "#8e44ad"),
    ("mien phi", "#8e44ad"),
    ("thuốc đặc trị", "#8e44ad"),
    ("thuoc dac tri", "#8e44ad"),
    ("bài thuốc gia truyền", "#8e44ad"),
    ("bai thuoc gia truyen", "#8e44ad"),
    ("trị dứt điểm", "#8e44ad"),
    ("tri dut diem", "#8e44ad"),
    ("nhận quà", "#8e44ad"),
    ("nhan qua", "#8e44ad"),
    ("tặng xe", "#8e44ad"),
    ("tang xe", "#8e44ad"),

    # Nhóm 5: Đòi thông tin bảo mật & đường dẫn lạ
    ("mã otp", "#c0392b"),
    ("ma otp", "#c0392b"),
    ("mật khẩu", "#c0392b"),
    ("mat khau", "#c0392b"),
    ("số tài khoản", "#d35400"),
    ("so tai khoan", "#d35400"),
    ("đăng nhập", "#d35400"),
    ("dang nhap", "#d35400"),
    ("bấm vào link", "#c0392b"),
    ("bam vao link", "#c0392b"),
    ("nhấp vào", "#c0392b"),
    ("nhap vao", "#c0392b"),
    ("truy cập ngay", "#c0392b"),
    ("truy cap ngay", "#c0392b"),
    ("[đường_dẫn]", "#c0392b"),
    ("[duong_dan]", "#c0392b"),
    ("http", "#c0392b"),
    ("https", "#c0392b"),
]


def extract_found_keywords(text: str) -> List[str]:
    """Tìm tất cả các từ khóa cảnh báo xuất hiện trong tin nhắn."""
    found = []
    text_lower = text.lower()
    for kw, _ in RISK_PATTERNS:
        if kw in text_lower:
            found.append(kw)
    return list(dict.fromkeys(found))


def highlight_text_html(text: str, font_multiplier: float = 1.0) -> str:
    """Tạo chuỗi HTML bôi đỏ nổi bật các từ khóa nguy hiểm cho người già dễ đọc."""
    highlighted = text
    # Sắp xếp từ khóa theo độ dài giảm dần để tránh replace trùng lặp
    sorted_patterns = sorted(RISK_PATTERNS, key=lambda x: len(x[0]), reverse=True)

    for kw, color in sorted_patterns:
        # Regex case-insensitive
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        replacement = (
            f'<mark style="background-color: {color}; color: #ffffff; '
            f'font-weight: 800; padding: 2px 8px; border-radius: 6px; '
            f'display: inline-block; margin: 1px 2px;">{kw.upper()}</mark>'
        )
        highlighted = pattern.sub(replacement, highlighted)

    # Thay thế xuống dòng thành <br>
    highlighted = highlighted.replace("\n", "<br>")

    font_size = int(20 * font_multiplier)
    line_height = 1.8

    return f"""
    <div style="
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        padding: 20px;
        font-size: {font_size}px;
        line-height: {line_height};
        color: #1e293b;
        font-family: 'Segoe UI', Roboto, sans-serif;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.03);
    ">
        {highlighted}
    </div>
    """
