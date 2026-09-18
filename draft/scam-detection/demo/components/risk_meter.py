"""Accessible Civic Alert Banner conforming to public safety and healthcare standards with production animations."""

import streamlit as st

def render_civic_alert(risk_score: float):
    """
    Renders a clear, authoritative civic alert card modeled after GOV.UK / NHS alert standards.
    Features GPU-accelerated transition animations for production feel.
    """
    if risk_score >= 0.70:
        badge_text = "MỨC ĐỘ NGUY HIỂM CAO"
        title = "CẢNH BÁO: ĐÂY LÀ TIN NHẮN LỪA ĐẢO"
        lead_text = "Bác hoặc người thân tuyệt đối KHÔNG làm theo, KHÔNG chuyển tiền và KHÔNG bấm vào bất kỳ đường dẫn nào."
        theme_border = "#DC2626"
        theme_bg = "#FEF2F2"
        theme_title = "#991B1B"
        theme_text = "#7F1D1D"
        pulse_class = "civic-pulse-danger"
        status_code = "danger"
    elif risk_score >= 0.35:
        badge_text = "CẦN LƯU Ý XÁC MINH"
        title = "CHÚ Ý: TIN NHẮN CÓ YẾU TỐ BẤT THƯỜNG"
        lead_text = "Tin nhắn có dấu hiệu hối thúc hoặc mạo danh. Bác hãy gọi điện thoại cho con cháu hoặc người thân để kiểm tra trước khi phản hồi."
        theme_border = "#D97706"
        theme_bg = "#FFFBEB"
        theme_title = "#92400E"
        theme_text = "#78350F"
        pulse_class = "civic-pulse-warning"
        status_code = "warning"
    else:
        badge_text = "AN TÂM"
        title = "TIN NHẮN BÌNH THƯỜNG (KHÔNG PHÁT HIỆN LỪA ĐẢO)"
        lead_text = "Nội dung mang tính chất trao đổi thông thường. Bác có thể yên tâm tiếp tục sinh hoạt."
        theme_border = "#16A34A"
        theme_bg = "#F0FDF4"
        theme_title = "#166534"
        theme_text = "#14532D"
        pulse_class = "civic-pulse-safe"
        status_code = "safe"

    html = (
        f'<div class="civic-animate-up {pulse_class}" style="'
        f'background-color: {theme_bg}; '
        f'border-left: 6px solid {theme_border}; '
        f'border-radius: 8px; '
        f'padding: 24px 24px; '
        f'margin-bottom: 24px; '
        f'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); '
        f'font-family: -apple-system, BlinkMacSystemFont, sans-serif;">'
        f'<div style="display: inline-block; background-color: {theme_border}; color: #FFFFFF; font-size: 13px; font-weight: 700; letter-spacing: 0.5px; padding: 4px 10px; border-radius: 4px; margin-bottom: 12px;">{badge_text}</div>'
        f'<div style="color: {theme_title}; font-size: 24px; font-weight: 800; line-height: 1.35; margin-bottom: 10px;">{title}</div>'
        f'<div style="color: {theme_text}; font-size: 19px; line-height: 1.6; font-weight: 500;">{lead_text}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    return status_code
