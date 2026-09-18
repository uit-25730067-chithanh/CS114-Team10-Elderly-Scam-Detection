"""Ứng dụng Web Demo Phát hiện Tin nhắn Lừa đảo Người cao tuổi (CS114 - Nhóm 10).

Thiết kế giao diện chuẩn hóa theo đặc tả PRODUCT.md và kỹ năng uit:ux-research.
Chuyên biệt hóa khả năng tiếp cận cho người cao tuổi (Elderly Accessibility).
"""

import os
import sys
import streamlit as st

# Setup import path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from demo.components.sample_data import SAMPLE_MESSAGES
from demo.components.model_adapter import get_detector
from demo.components.risk_meter import render_risk_meter
from demo.components.keyword_highlighter import highlight_scam_keywords, extract_psychological_flags
from demo.components.safety_advisor import render_safety_advisor


# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="🛡️ Kiểm Tra Tin Nhắn Lừa Đảo Người Cao Tuổi",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ─── Custom CSS for Elderly Accessibility ─────────────────────────────────────
def apply_custom_styles(is_elderly_mode: bool):
    base_font = "20px" if is_elderly_mode else "16px"
    h1_size = "34px" if is_elderly_mode else "28px"
    h2_size = "26px" if is_elderly_mode else "22px"
    btn_padding = "16px 28px" if is_elderly_mode else "12px 20px"
    btn_font = "22px" if is_elderly_mode else "16px"

    st.markdown(
        f"""
        <style>
            html, body, [class*="css"] {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                font-size: {base_font};
            }}
            h1 {{
                font-size: {h1_size} !important;
                font-weight: 800 !important;
                color: #0F172A !important;
            }}
            h2, h3 {{
                font-size: {h2_size} !important;
                font-weight: 700 !important;
                color: #1E293B !important;
            }}
            .stButton > button {{
                width: 100%;
                font-size: {btn_font} !important;
                font-weight: 700 !important;
                padding: {btn_padding} !important;
                border-radius: 10px !important;
                background-color: #0284C7 !important;
                color: #FFFFFF !important;
                border: none !important;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}
            .stButton > button:hover {{
                background-color: #0369A1 !important;
            }}
            .sample-box {{
                border: 2px solid #E2E8F0;
                border-radius: 10px;
                padding: 14px;
                margin-bottom: 12px;
                background-color: #FFFFFF;
                transition: all 0.2s ease;
            }}
            .sample-box:hover {{
                border-color: #0284C7;
                background-color: #F0F9FF;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ─── Sidebar Settings ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Cài Đặt Trợ Năng")
    elderly_mode = st.toggle(
        "👵 **Chế độ Chữ Lớn (Người cao tuổi)**",
        value=True,
        help="Phóng to toàn bộ cỡ chữ lên 20–24px, tăng độ tương phản và mở rộng nút bấm để mắt kém dễ đọc."
    )

    st.markdown("---")
    st.markdown("### ℹ️ Về Đồ Án")
    st.markdown(
        """
        - **Môn học:** Máy học (CS114) — UIT
        - **Đề tài:** Phát hiện Tin nhắn Lừa đảo nhắm vào Người cao tuổi tại Việt Nam
        - **Nhóm 10:** Đặng Chí Thanh, Bùi Thị Mỷ Cẩm, Hoàng Cao Sơn
        - **Dữ liệu:** 2.193 mẫu thực tế (100% Zero Synthetic Text)
        - **Mô hình:** XGBoost / Random Forest (5.015 đặc trưng)
        """
    )
    st.markdown("---")
    detector = get_detector()
    if detector.is_ready:
        st.success(f"🤖 **Mô hình sẵn sàng:**\n\n{detector.model_name}")
    else:
        st.warning("⚠️ **Đang chạy chế độ:**\n\nQuy tắc Chuyên gia Dự phòng")


apply_custom_styles(elderly_mode)


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("<h1>🛡️ Hệ Thống Kiểm Tra & Cảnh Báo Tin Nhắn Lừa Đảo</h1>", unsafe_allow_html=True)
subtitle_size = "22px" if elderly_mode else "17px"
st.markdown(
    f"<p style='font-size:{subtitle_size}; color:#475569; margin-top:-10px; font-weight:500;'>"
    f"Công cụ hỗ trợ Người cao tuổi và Gia đình phát hiện bẫy tâm lý mạo danh Công an, cấp cứu viện phí, trúng thưởng giả mạo."
    f"</p>",
    unsafe_allow_html=True
)

st.divider()


# ─── Session State Initialization ─────────────────────────────────────────────
if "current_message" not in st.session_state:
    st.session_state["current_message"] = ""


# ─── Main Columns Layout ──────────────────────────────────────────────────────
col_input, col_result = st.columns([1, 1], gap="large")


# ─── Column 1: Input & Sample Presets ──────────────────────────────────────────
with col_input:
    st.markdown("### 📩 Bước 1: Nhập hoặc Dán Tin Nhắn Cần Kiểm Tra")

    user_input = st.text_area(
        label="Nội dung tin nhắn nhận được (SMS, Zalo, Telegram):",
        value=st.session_state["current_message"],
        height=180,
        placeholder="Dán nội dung tin nhắn đáng ngờ vào đây...",
        key="text_input_area"
    )

    btn_check = st.button("🔍 KIỂM TRA TIN NHẮN NGAY", type="primary")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚡ Hoặc Bấm Thử Các Kịch Bản Mẫu Thực Tế:")

    for key, sample in SAMPLE_MESSAGES.items():
        with st.expander(f"{sample['title']}"):
            st.markdown(f"**Phân loại:** `{sample['tag']}`")
            st.markdown(f"*{sample['content']}*")
            st.caption(f"💡 {sample['explanation']}")
            if st.button(f"👉 Nạp kịch bản này vào kiểm tra", key=f"btn_{key}"):
                st.session_state["current_message"] = sample["content"]
                st.rerun()


# ─── Column 2: Result & Safety Actions ─────────────────────────────────────────
with col_result:
    st.markdown("### 📊 Bước 2: Kết Quả Đánh Giá & Hướng Dẫn An Toàn")

    target_text = user_input.strip()

    if not target_text:
        # Empty State
        empty_font = "20px" if elderly_mode else "16px"
        st.markdown(
            f"""
            <div style="background-color: #F8FAFC; border: 2px dashed #CBD5E1; border-radius: 12px; padding: 40px 20px; text-align: center; margin-top: 20px;">
                <div style="font-size: 48px;">🛡️</div>
                <div style="font-size: {empty_font}; color: #475569; font-weight: 600; margin-top: 12px;">
                    Chưa có nội dung để kiểm tra
                </div>
                <div style="font-size: {empty_font}; color: #64748B; margin-top: 6px;">
                    Bác hoặc người thân hãy dán tin nhắn vào ô bên trái, hoặc bấm chọn các kịch bản mẫu có sẵn để xem kết quả đánh giá ngay lập tức.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Perform Inference
        prediction = detector.predict(target_text)
        risk_score = prediction["risk_score"]
        is_scam = prediction["is_scam"]

        # 1. Render Risk Meter
        render_risk_meter(risk_score, is_elderly_mode=elderly_mode)

        # 2. Highlight Scam Keywords
        st.markdown("#### 🔍 Chi Tiết Tin Nhắn & Từ Khóa Cảnh Báo:")
        st.markdown(highlight_scam_keywords(target_text, is_elderly_mode=elderly_mode), unsafe_allow_html=True)

        # 3. Psychological Flags Detected
        flags = extract_psychological_flags(target_text)
        if flags:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🧠 Nhận Diện Bẫy Tâm Lý Đang Được Sử Dụng:")
            flag_cols = st.columns(len(flags))
            for i, f in enumerate(flags):
                with flag_cols[i]:
                    st.markdown(
                        f"""
                        <div style="background-color:{f['bg']}; border-left:4px solid {f['color']}; padding:8px 12px; border-radius:6px; margin-bottom:8px;">
                            <div style="color:{f['color']}; font-weight:700; font-size:15px;">{f['label']}</div>
                            <div style="color:#334155; font-size:13px; margin-top:2px;">{", ".join(f['matches'])}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.divider()

        # 4. Emergency Safety Advisor
        render_safety_advisor(is_scam, is_elderly_mode=elderly_mode)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 14px;">
        Đồ án Môn học Máy học (CS114) — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM<br>
        <strong>Nhóm 10:</strong> Đặng Chí Thanh (25730067) • Bùi Thị Mỷ Cẩm (25730013) • Hoàng Cao Sơn (25730061)<br>
        <em>Hệ thống cam kết tuân thủ chính sách Zero Synthetic Text — 100% dữ liệu huấn luyện thu thập từ đời thực.</em>
    </div>
    """,
    unsafe_allow_html=True
)
