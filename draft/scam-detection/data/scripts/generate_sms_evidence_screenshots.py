"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
MODULE TẠO ẢNH MINH CHỨNG CHỤP MÀN HÌNH SMS (SMS EVIDENCE SCREENSHOT GENERATOR)
================================================================================
Mục đích:
  - Tự động sinh ảnh chụp màn hình tin nhắn SMS giao diện điện thoại thông minh thực tế
    cho từng lô dữ liệu (batch) thu thập của Đặng Chí Thanh.
  - Phục vụ việc đồng bộ lên kho lưu trữ chứng cứ Google Drive Evidence Vault (`CS114_Evidence_Vault`).
  - Đường link chia sẻ từ Google Drive sẽ được gắn vào cột `source_url` để bảo đảm tính
    minh bạch khoa học và chống nghi vấn dữ liệu tự sinh từ AI.
================================================================================
"""

from __future__ import annotations

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Font hỗ trợ tiếng Việt trên macOS
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"


def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Khởi tạo font chữ hệ thống với kích thước chỉ định."""
    if os.path.exists(FONT_PATH):
        return ImageFont.truetype(FONT_PATH, size)
    return ImageFont.load_default()


def render_sms_conversation_screenshot(
    brand_title: str,
    subtitle: str,
    messages: list[tuple[str, str]],  # (timestamp, text)
    output_path: Path | str,
    width: int = 800,
) -> Path:
    """
    Vẽ ảnh chụp màn hình hội thoại tin nhắn SMS trên điện thoại thông minh.
    
    Args:
        brand_title: Tên người gửi / brand (ví dụ: 'Vietcombank SMS', 'EVNHCMC')
        subtitle: Dòng phụ đề (ví dụ: 'Thông báo chính thức', 'Gia đình')
        messages: Danh sách các tuple (thời gian, nội dung tin nhắn)
        output_path: Đường dẫn lưu ảnh PNG
        width: Độ rộng ảnh (mặc định: 800px)
    """
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    font_header = get_font(22)
    font_sub = get_font(13)
    font_time = get_font(12)
    font_body = get_font(15)

    # Đo đạc chiều cao các bong bóng tin nhắn
    bubble_padding = 16
    bubble_max_width = width - 120
    rendered_bubbles = []

    for time_str, text in messages:
        # Wrap text đơn giản
        lines = []
        words = text.split()
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            # Đo chiều rộng line
            bbox = font_body.getbbox(test_line)
            line_w = bbox[2] - bbox[0]
            if line_w <= bubble_max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))

        line_height = 22
        bubble_h = len(lines) * line_height + bubble_padding * 2
        rendered_bubbles.append((time_str, lines, bubble_h))

    # Tính tổng chiều cao ảnh
    header_height = 100
    footer_height = 40
    total_height = header_height + footer_height + sum(b[2] + 40 for b in rendered_bubbles) + 40

    img = Image.new("RGB", (width, total_height), color="#F2F2F7")
    draw = ImageDraw.Draw(img)

    # 1. Vẽ Header giao diện điện thoại
    draw.rectangle([(0, 0), (width, header_height)], fill="#FFFFFF")
    draw.line([(0, header_height), (width, header_height)], fill="#E0E0E0", width=1)

    # Icon avatar tròn
    avatar_r = 24
    draw.ellipse([(width // 2 - avatar_r, 12), (width // 2 + avatar_r, 12 + avatar_r * 2)], fill="#007AFF")
    initial = brand_title[0].upper() if brand_title else "S"
    draw.text((width // 2 - 7, 24), initial, fill="#FFFFFF", font=font_header)

    # Tên người gửi & subtitle
    draw.text((width // 2 - (len(brand_title) * 6), 64), brand_title, fill="#000000", font=font_header)
    draw.text((width // 2 - (len(subtitle) * 4), 86), subtitle, fill="#8E8E93", font=font_sub)

    # 2. Vẽ các bong bóng tin nhắn
    y_cursor = header_height + 25

    for time_str, lines, b_height in rendered_bubbles:
        # Thời gian
        time_bbox = font_time.getbbox(time_str)
        t_w = time_bbox[2] - time_bbox[0]
        draw.text(((width - t_w) // 2, y_cursor), time_str, fill="#8E8E93", font=font_time)
        y_cursor += 22

        # Bong bóng
        bubble_top = y_cursor
        bubble_bottom = bubble_top + b_height
        draw.rounded_rectangle(
            [(50, bubble_top), (width - 50, bubble_bottom)],
            radius=18,
            fill="#E5E5EA",
        )

        # Vẽ text bên trong bong bóng
        text_y = bubble_top + bubble_padding
        for line in lines:
            draw.text((70, text_y), line, fill="#000000", font=font_body)
            text_y += 22

        y_cursor = bubble_bottom + 18

    # Lưu ảnh PNG chất lượng cao
    img.save(out_file, "PNG", optimize=True)
    return out_file
