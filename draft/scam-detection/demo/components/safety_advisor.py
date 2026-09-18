"""Safety advisor component providing actionable emergency rules for elderly users."""

import streamlit as st

def render_safety_advisor(is_scam: bool, is_elderly_mode: bool = False):
    """Renders high-visibility safety checklist and emergency contacts."""
    body_size = "19px" if is_elderly_mode else "15px"
    heading_size = "24px" if is_elderly_mode else "18px"

    st.markdown(f"### 🛡️ 4 Điều Cần Nhớ Tuyệt Đối (Nguyên Tắc 4 KHÔNG)")

    st.markdown(
        f"""
        <div style="background-color: #FFFFFF; border: 2px solid #CBD5E1; border-radius: 12px; padding: 18px; margin-bottom: 20px;">
            <ul style="font-size: {body_size}; line-height: 1.8; color: #1E293B; margin: 0; padding-left: 24px;">
                <li><strong style="color: #DC2626;">1. KHÔNG CHUYỂN TIỀN:</strong> Tuyệt đối không ra ngân hàng hay dùng điện thoại chuyển tiền vào bất kỳ "tài khoản tạm giữ" nào.</li>
                <li><strong style="color: #EA580C;">2. KHÔNG BẤM ĐƯỜNG LINK:</strong> Không bấm vào bất kỳ liên kết lạ gửi qua tin nhắn SMS, Zalo để tránh mất tài khoản.</li>
                <li><strong style="color: #7C3AED;">3. KHÔNG ĐỌC MÃ OTP:</strong> Công an, Viện kiểm sát và Ngân hàng <em>KHÔNG BAO GIỜ</em> yêu cầu người dân đọc mã OTP hay mật khẩu.</li>
                <li><strong style="color: #0284C7;">4. KHÔNG GIỮ BÍ MẬT:</strong> Khi có người dọa nạt bắt bớ, hãy dừng lại ngay và kể cho con cháu trong nhà biết!</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📞 Đường Dây Nóng Khẩn Cấp Trợ Giúp")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🚨 **Cảnh sát 113 / Cục An ninh mạng (A05):**\n\n**Hotline:** `113` hoặc `069.234.3636`")
    with col2:
        st.success("👨‍👩‍👦 **Gia đình & Người thân:**\n\nBác hãy bấm gọi ngay cho con/cháu để nhờ kiểm tra trực tiếp!")
