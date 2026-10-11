"""
Risk Meter Component for Elderly Scam Detection App.
Author: Hoàng Cao Sơn (MSSV: 25730061)
"""

import streamlit as st


def render_risk_meter(probability: float, font_multiplier: float = 1.0) -> None:
    """Hiển thị thước đo mức độ nguy cơ lừa đảo với cỡ chữ lớn và màu sắc tương phản cao."""
    pct = probability * 100

    base_title_size = int(26 * font_multiplier)
    base_sub_size = int(18 * font_multiplier)
    base_score_size = int(36 * font_multiplier)

    if probability < 0.35:
        bg_color = "#e8f8f5"
        border_color = "#27ae60"
        text_color = "#1e8449"
        status_icon = "🛡️"
        status_title = "TIN NHẮN AN TOÀN"
        sub_title = "Không phát hiện dấu hiệu lừa đảo nguy hiểm. Ông/Bà có thể an tâm."
        badge_label = "Mức độ rủi ro: THẤP"
    elif probability < 0.70:
        bg_color = "#fef9e7"
        border_color = "#f39c12"
        text_color = "#b7950b"
        status_icon = "⚠️"
        status_title = "CHÚ Ý: TIN NHẮN NGHI VẤN"
        sub_title = "Tin nhắn có chứa một số từ ngữ bất thường. Xin hỏi ý kiến người thân trước khi làm theo."
        badge_label = "Mức độ rủi ro: TRUNG BÌNH"
    else:
        bg_color = "#fdedec"
        border_color = "#e74c3c"
        text_color = "#c0392b"
        status_icon = "🚨"
        status_title = "CẢNH BÁO: TIN NHẮN LỪA ĐẢO NGUY HIỂM!"
        sub_title = "Phát hiện chiêu trò thao túng tâm lý chiếm đoạt tài sản. TUYỆT ĐỐI KHÔNG làm theo!"
        badge_label = "Mức độ rủi ro: CỰC KỲ NGUY HIỂM"

    html_card = f"""
    <div style="
        background-color: {bg_color};
        border: 3px solid {border_color};
        border-radius: 16px;
        padding: clamp(14px, 3.5vw, 24px);
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        animation: smoothFadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    ">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 12px;">
            <div style="font-size: clamp(19px, 4.5vw, {base_title_size}px); font-weight: 800; color: {text_color}; line-height: 1.35; flex: 1 1 220px; min-width: 0;">
                {status_icon} {status_title}
            </div>
            <div style="
                background-color: {border_color};
                color: #ffffff;
                font-weight: 700;
                font-size: 13px;
                padding: 6px 14px;
                border-radius: 20px;
                white-space: nowrap;
                margin-top: 2px;
            ">
                {badge_label}
            </div>
        </div>
        <p style="font-size: clamp(15px, 3.5vw, {base_sub_size}px); color: #2c3e50; margin: 8px 0 16px 0; font-weight: 500; line-height: 1.55;">
            {sub_title}
        </p>
        <div style="
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 8px 14px;
            background: #ffffff;
            border-radius: 12px;
            padding: 12px 18px;
            border: 1px solid #e2e8f0;
        ">
            <span style="font-size: 16px; color: #555555; font-weight: 600;">Độ nguy hiểm ước tính:</span>
            <span style="font-size: clamp(28px, 6vw, {base_score_size}px); font-weight: 900; color: {text_color}; font-family: monospace;">
                {pct:.1f}%
            </span>
            <div style="width: 100%; font-size: 13px; color: #7f8c8d; margin-top: -2px;">
                (Đánh giá bởi Trí tuệ Nhân tạo AI)
            </div>
        </div>
    </div>
    """
    st.markdown(html_card, unsafe_allow_html=True)
    st.progress(min(max(probability, 0.0), 1.0))
