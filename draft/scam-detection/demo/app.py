"""
Civic Safety Web Portal: Scam SMS Verification for Elderly Citizens.
Designed in accordance with GOV.UK / NHS Civic Service Standards.
Zero AI Slop • Single-Column Linear Flow • High-Contrast Large Typography.
"""

import streamlit as st
from components.sample_data import SAMPLE_MESSAGES
from components.model_adapter import get_detector
from components.risk_meter import render_civic_alert
from components.keyword_highlighter import highlight_scam_keywords, extract_indicators
from components.safety_advisor import render_safety_actions


# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cổng Kiểm Tra Tin Nhắn Nghi Vấn — Phòng Chống Lừa Đảo",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ─── Civic Design System CSS ──────────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Ẩn hoàn toàn header và footer mặc định của Streamlit */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}

        /* Thiết lập khối nội dung chính ở giữa màn hình (Max-width 780px) */
        .block-container {
            max-width: 780px !important;
            padding-top: 2.5rem !important;
            padding-bottom: 4rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }

        /* Phông chữ toàn trang to rõ, tương phản cao theo chuẩn Trợ năng */
        body, p, span, div, label {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
            color: #0F172A;
            -webkit-font-smoothing: antialiased;
        }

        /* Tùy chỉnh ô Textarea */
        .stTextArea textarea {
            font-size: 19px !important;
            line-height: 1.6 !important;
            padding: 16px !important;
            border-radius: 8px !important;
            border: 2px solid #CBD5E1 !important;
            background-color: #FFFFFF !important;
            color: #0F172A !important;
        }
        .stTextArea textarea:focus {
            border-color: #0F172A !important;
            box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.15) !important;
        }

        /* Nút hành động chính to bản (Height >= 58px, Chữ trắng rõ ràng) */
        .stButton button[kind="primary"] {
            width: 100% !important;
            height: 58px !important;
            background-color: #0F172A !important;
            border: none !important;
            border-radius: 8px !important;
            transition: background-color 0.2s ease;
        }
        .stButton button[kind="primary"] p {
            color: #FFFFFF !important;
            font-size: 19px !important;
            font-weight: 700 !important;
            letter-spacing: 0.5px !important;
            margin: 0 !important;
        }
        .stButton button[kind="primary"]:hover {
            background-color: #1E293B !important;
        }

        /* Nút mẫu thử nghiệm */
        .sample-btn button {
            width: 100% !important;
            min-height: 50px !important;
            border-radius: 6px !important;
            border: 1px solid #CBD5E1 !important;
            background-color: #F8FAFC !important;
            padding: 10px 14px !important;
            text-align: left !important;
        }
        .sample-btn button p {
            color: #1E293B !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }
        .sample-btn button:hover {
            border-color: #0F172A !important;
            background-color: #F1F5F9 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ─── Civic Portal Header ──────────────────────────────────────────────────────
st.markdown(
    """
    <div style="text-align: left; margin-bottom: 24px;">
        <div style="
            font-size: 13px;
            font-weight: 700;
            color: #475569;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 8px;
        ">
            Hệ Thống Trợ Giúp An Toàn Số • Đại Học Công Nghệ Thông Tin (UIT)
        </div>
        <h1 style="
            font-size: 32px;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.25;
            margin: 0 0 12px 0;
            letter-spacing: -0.5px;
        ">
            Kiểm Tra Tin Nhắn Nghi Vấn
        </h1>
        <p style="
            font-size: 18px;
            color: #475569;
            line-height: 1.5;
            margin: 0;
        ">
            Công cụ hỗ trợ Bác và Gia đình nhận diện nhanh các tin nhắn dọa bắt giữ từ Công an, tin nhắn cấp cứu viện phí, hoặc lừa chuyển tiền.
        </p>
    </div>
    <hr style="border: none; border-top: 1px solid #E2E8F0; margin-bottom: 28px;">
    """,
    unsafe_allow_html=True
)


# ─── Session State Callback ───────────────────────────────────────────────────
if "text_area_content" not in st.session_state:
    st.session_state["text_area_content"] = ""

def set_sample_text(content: str):
    st.session_state["text_area_content"] = content


# ─── Input Form ───────────────────────────────────────────────────────────────
st.markdown(
    "<label style='font-size: 19px; font-weight: 700; color: #0F172A; margin-bottom: 8px; display: block;'>"
    "1. Dán hoặc nhập nội dung tin nhắn cần kiểm tra:"
    "</label>",
    unsafe_allow_html=True
)

user_text = st.text_area(
    label="sms_area_hidden_label",
    label_visibility="collapsed",
    height=150,
    placeholder="Dán nội dung tin nhắn nhận được (từ SMS, Zalo hoặc mạng xã hội) vào đây...",
    key="text_area_content"
)

# Nút kiểm tra chính
btn_check = st.button("KIỂM TRA TIN NHẮN NÀY", type="primary")


# ─── Quick Preset Chips (1-Touch Testing) ─────────────────────────────────────
st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-size: 15px; font-weight: 600; color: #64748B; margin-bottom: 8px;'>"
    "Hoặc bấm thử các mẫu tin nhắn thực tế có sẵn:"
    "</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
    st.button(
        "Mẫu 1: Mạo danh Công an dọa bắt giữ",
        key="chip_police",
        on_click=set_sample_text,
        args=(SAMPLE_MESSAGES["police"]["content"],)
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
    st.button(
        "Mẫu 3: Tặng thuốc bổ / Máy đo huyết áp",
        key="chip_gift",
        on_click=set_sample_text,
        args=(SAMPLE_MESSAGES["gift"]["content"],)
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
    st.button(
        "Mẫu 2: Báo con tai nạn cấp cứu gấp",
        key="chip_hospital",
        on_click=set_sample_text,
        args=(SAMPLE_MESSAGES["hospital"]["content"],)
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
    st.button(
        "Mẫu 4: Tin nhắn con cái hỏi thăm",
        key="chip_family",
        on_click=set_sample_text,
        args=(SAMPLE_MESSAGES["family"]["content"],)
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Analysis & Verification Logic ────────────────────────────────────────────
target_message = st.session_state.get("text_area_content", "").strip()

if target_message:
    st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 32px 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<h2 style='font-size: 24px; font-weight: 800; color: #0F172A; margin-bottom: 20px;'>"
        "2. Kết quả đánh giá tin nhắn:"
        "</h2>",
        unsafe_allow_html=True
    )

    detector = get_detector()
    prediction = detector.predict(target_message)
    risk_score = prediction["risk_score"]
    is_scam = prediction["is_scam"]

    # 1. Authoritative Civic Alert Banner
    render_civic_alert(risk_score)

    # 2. Text with Highlighter for Suspicious Phrases
    st.markdown(
        "<div style='font-size: 17px; font-weight: 700; color: #1E293B; margin: 20px 0 8px 0;'>"
        "Từ khóa và chi tiết tin nhắn:"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown(highlight_scam_keywords(target_message), unsafe_allow_html=True)

    # 3. Direct Safety Actions & Hotline
    render_safety_actions(is_scam)


# ─── Portal Footer ────────────────────────────────────────────────────────────
st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 14px; line-height: 1.6; padding-top: 8px;">
        Đề tài Nghiên cứu Máy học phục vụ cộng đồng (CS114) — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM.<br>
        Nhóm 10: Đặng Chí Thanh • Bùi Thị Mỷ Cẩm • Hoàng Cao Sơn.<br>
        Toàn bộ dữ liệu huấn luyện thu thập từ các vụ lừa đảo thực tế tại Việt Nam (Zero Synthetic Text).
    </div>
    """,
    unsafe_allow_html=True
)
