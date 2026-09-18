"""Emergency Action Protocol for citizens and seniors with production micro-interactions."""

import streamlit as st

def render_safety_actions(is_scam: bool):
    """Renders direct, actionable instructions with smooth entrance animation and interactive hotline targets."""
    if not is_scam:
        html = (
            '<div class="civic-animate-up" style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 22px; margin-top: 24px; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">'
            '<div style="font-weight: 700; font-size: 18px; color: #1E293B; margin-bottom: 8px;">Lời khuyên an toàn từ Chuyên gia:</div>'
            '<div style="font-size: 17px; color: #475569; line-height: 1.6;">Dù tin nhắn này hiện an toàn, gia đình vẫn nên duy trì thói quen không bao giờ cung cấp mã OTP ngân hàng, số thẻ tín dụng hoặc mật khẩu cho bất kỳ ai qua tin nhắn.</div>'
            '</div>'
        )
        st.markdown(html, unsafe_allow_html=True)
        return

    html = (
        '<div class="civic-animate-up" style="background-color: #FFFFFF; border: 2px solid #DC2626; border-radius: 8px; padding: 24px; margin-top: 24px; font-family: -apple-system, BlinkMacSystemFont, sans-serif; box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.08);">'
        '<div style="font-size: 21px; font-weight: 800; color: #991B1B; margin-bottom: 16px;">3 ĐIỀU BÁC CẦN LÀM NGAY:</div>'
        '<div style="font-size: 18px; color: #1E293B; line-height: 1.8; margin-bottom: 24px;">'
        '<div style="margin-bottom: 12px; padding: 10px 14px; background-color: #FEF2F2; border-radius: 6px; border-left: 4px solid #DC2626;"><strong>1. TUYỆT ĐỐI KHÔNG CHUYỂN TIỀN:</strong> Cơ quan Công an, Viện kiểm sát và Bệnh viện không bao giờ yêu cầu người dân chuyển tiền qua tài khoản cá nhân bằng tin nhắn.</div>'
        '<div style="margin-bottom: 12px; padding: 10px 14px; background-color: #F8FAFC; border-radius: 6px; border-left: 4px solid #64748B;"><strong>2. HỎI Ý KIẾN NGƯỜI NHÀ:</strong> Hãy gọi điện trực tiếp cho con, cháu hoặc người thân tín cậy để cùng đọc tin nhắn này.</div>'
        '<div style="margin-bottom: 12px; padding: 10px 14px; background-color: #F8FAFC; border-radius: 6px; border-left: 4px solid #64748B;"><strong>3. KHÔNG ĐỌC MÃ OTP:</strong> Tuyệt đối không đọc bất kỳ 6 chữ số mã xác thực nào gửi về điện thoại cho người lạ.</div>'
        '</div>'
        '<div style="background-color: #FEF2F2; border-radius: 6px; padding: 20px; border: 1px solid #FECACA;">'
        '<div style="font-weight: 700; font-size: 17px; color: #991B1B; margin-bottom: 12px;">ĐƯỜNG DÂY NÓNG HỖ TRỢ KHẨN CẤP (BẤM ĐỂ GỌI TRỰC TIẾP):</div>'
        '<div style="display: flex; gap: 16px; flex-wrap: wrap;">'
        '<a href="tel:113" class="btn-hotline-113" style="display: inline-block; background-color: #DC2626; color: #FFFFFF; text-decoration: none; font-size: 18px; font-weight: 700; padding: 14px 22px; border-radius: 8px; box-shadow: 0 4px 10px rgba(220, 38, 38, 0.35); transition: all 0.2s ease;">Gọi Cảnh sát: 113</a>'
        '<a href="tel:0692348560" class="btn-hotline-gov" style="display: inline-block; background-color: #0F172A; color: #FFFFFF; text-decoration: none; font-size: 18px; font-weight: 700; padding: 14px 22px; border-radius: 8px; box-shadow: 0 4px 10px rgba(15, 23, 42, 0.2); transition: all 0.2s ease;">Cục An ninh mạng: 069.234.8560</a>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
