"""Risk Meter Component designed for elderly accessibility with large indicators and high contrast."""

import streamlit as st

def render_risk_meter(risk_score: float, is_elderly_mode: bool = False):
    """
    Renders an accessible, 3-tier risk gauge with prominent visual cues.
    - Low (< 0.35): Green - Safe
    - Medium (0.35 - 0.69): Amber - Suspicious
    - High (>= 0.70): Crimson Red - Scam Alert
    """
    pct = int(round(risk_score * 100))

    if risk_score < 0.35:
        level_title = "🟢 TIN NHẮN AN TOÀN"
        subtitle = "Không phát hiện yếu tố đe dọa hoặc bẫy lừa đảo"
        theme_color = "#15803D"      # Xanh lá đậm chuẩn WCAG AAA
        bg_color = "#DCFCE7"         # Nền xanh nhạt
        border_color = "#86EFAC"
        advice = "Nội dung mang tính chất sinh hoạt bình thường. Tuy nhiên, vẫn nên cẩn trọng nếu có yêu cầu bất thường về sau."
    elif risk_score < 0.70:
        level_title = "🟡 CẢNH BÁO: TIN NHẮN NGHI VẤN"
        subtitle = "Có dấu hiệu hối thúc hoặc chứa thông tin bất thường"
        theme_color = "#B45309"      # Vàng cam sẫm
        bg_color = "#FEF3C7"         # Nền vàng nhạt
        border_color = "#FCD34D"
        advice = "Tin nhắn có dấu hiệu bất thường. TUYỆT ĐỐI KHÔNG chuyển tiền hoặc bấm link khi chưa gọi điện xác nhận lại với người thân."
    else:
        level_title = "🔴 NGUY HIỂM: KỊCH BẢN LỪA ĐẢO CAO!"
        subtitle = "Phát hiện dấu hiệu thao túng tâm lý và lừa đảo chiếm đoạt tài sản"
        theme_color = "#B91C1C"      # Đỏ sẫm
        bg_color = "#FEE2E2"         # Nền đỏ nhạt
        border_color = "#FCA5A5"
        advice = "ĐÂY LÀ KỊCH BẢN LỪA ĐẢO! Bác hãy BÌNH TĨNH, KHÔNG LÀM THEO và KHÔNG CHUYỂN TIỀN cho bất kỳ ai!"

    title_size = "28px" if is_elderly_mode else "22px"
    body_size = "20px" if is_elderly_mode else "16px"

    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            border: 3px solid {border_color};
            border-left: 10px solid {theme_color};
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        ">
            <div style="color: {theme_color}; font-size: {title_size}; font-weight: 800; line-height: 1.3;">
                {level_title}
            </div>
            <div style="color: #334155; font-size: {body_size}; margin-top: 6px; font-weight: 600;">
                {subtitle}
            </div>
            <div style="margin-top: 14px; background-color: rgba(255,255,255,0.7); padding: 10px 14px; border-radius: 8px; border: 1px dashed {border_color};">
                <span style="font-size: {body_size}; color: #0F172A; font-weight: 500;">
                    💡 <strong>Lời khuyên nhanh:</strong> {advice}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Visual Progress Bar
    st.progress(min(max(risk_score, 0.0), 1.0))
    st.caption(f"Mức độ rủi ro hệ thống ước tính: **{pct}%** (Dựa trên mô hình học máy phân tích 5.015 đặc trưng)")
