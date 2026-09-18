"""
HỆ THỐNG PHÁT HIỆN TIN NHẮN & KỊCH BẢN THAO TÚNG TÂM LÝ LỪA ĐẢO NHẮM VÀO NGƯỜI CAO TUỔI
Học phần: CS114 — Machine Learning (ĐH Công Nghệ Thông Tin - ĐHQG TP.HCM)
Nhóm 10: Hoàng Cao Sơn (Demo Lead), Đặng Chí Thanh, Bùi Thị Mỷ Cẩm
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, hstack
import streamlit as st

# Thiết lập đường dẫn hệ thống
DEMO_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DEMO_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))

from demo.components.keyword_highlighter import extract_found_keywords, highlight_text_html
from demo.components.risk_meter import render_risk_meter
from demo.components.safety_advisor import diagnose_scam_category, render_safety_advisor
from src.feature_engineering_config import AUX_FEATURE_COLS
from src.preprocessing.pipeline import extract_auxiliary_features
from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.tokenizer import segment_vietnamese

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Phát Hiện Tin Nhắn Lừa Đảo Cho Người Cao Tuổi — CS114",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)



# Danh mục tin nhắn mẫu (Presets) phục vụ Người cao tuổi & Thuyết trình Live Demo
PRESET_SAMPLES = {
    "fear": {
        "title": "⚖️ Phạt nguội dọa bắt",
        "text": (
            "CỤC CSGT THÔNG BÁO: Phương tiện của quý khách đã vi phạm luật giao thông đường bộ, "
            "bị phạt nguội 5.000.000đ. Hồ sơ vụ án đang được chuyển sang Viện Kiểm Sát để khởi tố. "
            "Yêu cầu quý khách truy cập ngay website: https://canhsat-phatnguoi-vn.com để nộp phạt "
            "nếu không sẽ bị bắt tạm giam và phong tỏa tài khoản ngân hàng."
        ),
    },
    "emergency": {
        "title": "🚨 Cấp cứu người thân",
        "text": (
            "Mẹ ơi con bị tai nạn giao thông gãy chân đang cấp cứu ở bệnh viện Chợ Rẫy nguy kịch lắm. "
            "Bác sĩ yêu cầu đóng viện phí gấp 30 triệu để mổ cấp cứu ngay. Con không tiện nghe máy vì đang cấp cứu, "
            "mẹ chuyển gấp vào STK 0912345678 chủ tài khoản BS NGUYEN VAN A nha mẹ, đừng gọi con nhé."
        ),
    },
    "vneid": {
        "title": "🏛️ Lỗi định danh VNeID",
        "text": (
            "Bộ Công An thông báo: Hồ sơ định danh điện tử VNeID mức 2 của quý khách bị lỗi đồng bộ dữ liệu dân cư. "
            "Vui lòng truy cập đường dẫn: http://vneid-dichvucong-gov.com để cập nhật thông tin căn cước công dân "
            "và kích hoạt lại trước 24h hôm nay nếu không tài khoản sẽ bị khóa vĩnh viễn."
        ),
    },
    "gift": {
        "title": "🎁 Trúng thưởng & Tặng thuốc",
        "text": (
            "TRUNG TÂM DƯỢC LIỆU TRI ÂN: Chúc mừng quý khách đã may mắn trúng thưởng 1 xe máy Honda SH "
            "và 1 liệu trình bài thuốc đông y gia truyền trị dứt điểm thoái hóa khớp trị giá 15 triệu miễn phí. "
            "Nhanh tay liên hệ hotline để nhận quà hoặc bấm vào link để xác nhận thông tin nhận xe."
        ),
    },
    "bank": {
        "title": "💳 Biến động số dư Vietcombank",
        "text": (
            "VCB: 17/09/2026 14:30. Số dư TK 0071000xxx thay đổi +2.000.000 VND. "
            "Số dư hiện tại: 15.450.000 VND. Nội dung: CON GUI TIEN THUOC CHO ME. "
            "Cảm ơn quý khách đã sử dụng dịch vụ của Vietcombank."
        ),
    },
}




@st.cache_resource
def load_detection_engine():
    """Tải gói mô hình (bundle) hoặc nạp fallback các thành phần riêng lẻ."""
    bundle_path = PROJECT_ROOT / "models" / "best_model_bundle.pkl"
    if bundle_path.exists():
        try:
            bundle = joblib.load(bundle_path)
            return bundle, "Bundle Model (Random Forest 5.015 Features)"
        except Exception as e:
            st.warning(f"Lưu ý nạp bundle: {e}")

    # Fallback nạp từng thành phần
    rf_path = PROJECT_ROOT / "models" / "random_forest.pkl"
    vec_path = PROJECT_ROOT / "data" / "processed" / "tfidf_vectorizer.pkl"
    scaler_path = PROJECT_ROOT / "data" / "processed" / "aux_scaler.pkl"

    if rf_path.exists() and vec_path.exists() and scaler_path.exists():
        rf = joblib.load(rf_path)
        vec = joblib.load(vec_path)
        scaler = joblib.load(scaler_path)
        bundle = {
            "model": rf,
            "vectorizer": vec,
            "aux_scaler": scaler,
            "model_name": "Random Forest Classifier",
            "threshold": 0.5,
        }
        return bundle, "Random Forest Standalone Engine"

    return None, "Chế độ Quét Quy Tắc Ngữ Nghĩa (Rule-Based Fallback)"


from data.scripts.anonymize_sms import mask_pii
import re


def predict_text(raw_text: str, engine_bundle: dict | None) -> tuple[float, bool]:
    """Hàm suy luận xác suất lừa đảo trên văn bản người dùng nhập với chuẩn hóa PII & 5.015 chiều."""
    if engine_bundle is not None and "model" in engine_bundle:
        # 1. Chuẩn hóa & Ẩn danh hóa thông tin PII/URL để khớp với phân phối dữ liệu huấn luyện
        masked = mask_pii(raw_text)
        masked = re.sub(r"https?://\S+|www\.\S+", "[ĐƯỜNG_DẪN]", masked)

        # 2. Tiền xử lý NLP tiếng Việt toàn diện (làm sạch + tách từ + loại từ dừng có kiểm soát)
        from src.preprocessing.pipeline import preprocess_pipeline
        cleaned_text, aux_dict = preprocess_pipeline(masked)

        # 3. Chuẩn hóa 15 đặc trưng phụ
        aux_df = pd.DataFrame([aux_dict])[AUX_FEATURE_COLS]
        if "aux_scaler" in engine_bundle:
            aux_scaled = engine_bundle["aux_scaler"].transform(aux_df.values.astype(float))
        else:
            aux_scaled = aux_df.values.astype(float)

        # 4. Biến đổi TF-IDF (5.000 n-grams)
        tfidf_vec = engine_bundle["vectorizer"].transform([cleaned_text])

        # 5. Hợp nhất thành ma trận thưa 5.015 chiều
        full_vec = hstack([tfidf_vec, csr_matrix(aux_scaled)], format="csr")

        # 6. Dự đoán xác suất từ Random Forest Ensemble
        clf = engine_bundle["model"]
        if hasattr(clf, "predict_proba"):
            proba = float(clf.predict_proba(full_vec)[0][1])
        else:
            proba = 0.5

        threshold = engine_bundle.get("threshold", 0.5)
        return proba, bool(proba >= threshold)

    # Heuristic Rule fallback nếu chưa có file weights
    keywords = extract_found_keywords(raw_text)
    score = min(len(keywords) * 0.25, 0.95)
    return score, bool(score >= 0.5)


# ================= GIAO DIỆN CHÍNH (STREAMLIT APP) =================
def main():
    bundle, engine_info = load_detection_engine()

    # --- Thanh điều khiển bên Sidebar ---
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/shield.png", width=70)
        st.markdown("### ⚙️ CÀI ĐẶT HỆ THỐNG")
        font_choice = st.radio(
            "🔎 Cỡ chữ hiển thị:",
            ["Chữ Vừa (100%)", "Chữ To (125% - Dễ đọc)", "Chữ Rất To (150% - Cho người lớn tuổi)"],
            index=1,
            help="Tăng cỡ chữ để Ông/Bà nhìn rõ ràng hơn mà không bị mỏi mắt.",
        )
        multiplier_map = {
            "Chữ Vừa (100%)": 1.0,
            "Chữ To (125% - Dễ đọc)": 1.25,
            "Chữ Rất To (150% - Cho người lớn tuổi)": 1.5,
        }
        font_mult = multiplier_map[font_choice]

        st.markdown("---")
        st.markdown("#### ℹ️ THÔNG TIN HỆ THỐNG")
        st.info(f"**Động cơ AI:** {engine_info}\n\n**Học phần:** CS114 — Machine Learning\n\n**Phụ trách Demo:** Hoàng Cao Sơn (MSSV: 25730061)")

        st.markdown("---")
        st.markdown("#### 🚨 HOTLINE HỖ TRỢ KHẨN CẤP")
        st.error("**📞 Cục An Toàn Thông Tin:**\n# 156 (Miễn phí)")
        st.warning("**📞 Khẩn Cấp Công An:**\n# 113")

    # CSS Tùy biến Cỡ Chữ Lớn & Thân Thiện Người Cao Tuổi
    custom_css = f"""
    <style>
        html, body, [class*="css"] {{
            font-size: {int(18 * font_mult)}px !important;
            font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
        }}
        .stTextArea textarea {{
            font-size: {int(20 * font_mult)}px !important;
            line-height: 1.6 !important;
            border: 2px solid #3b82f6 !important;
            border-radius: 12px !important;
        }}
        /* Nút phụ / Nút chọn mẫu tin nhắn nhanh */
        .stButton button[kind="secondary"], .stButton button:not([kind="primary"]) {{
            font-size: {int(15 * font_mult)}px !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 8px 12px !important;
            background: #f8fafc !important;
            color: #1e3a8a !important;
            border: 1.5px solid #cbd5e1 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
        }}
        .stButton button[kind="secondary"]:hover, .stButton button:not([kind="primary"]):hover {{
            background: #e0f2fe !important;
            border-color: #0284c7 !important;
            color: #0369a1 !important;
        }}
        /* Nút chính KIỂM TRA TIN NHẮN NGAY */
        .stButton button[kind="primary"] {{
            font-size: {int(22 * font_mult)}px !important;
            font-weight: 800 !important;
            border-radius: 12px !important;
            padding: 14px 24px !important;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(30, 64, 175, 0.35) !important;
            width: 100% !important;
        }}
        .stButton button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
            box-shadow: 0 6px 18px rgba(30, 64, 175, 0.45) !important;
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # --- Banner Tiêu Đề Chính ---
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.25);
    ">
        <h1 style="color: white; margin: 0; font-size: {int(30 * font_mult)}px; font-weight: 900; display: flex; align-items: center; gap: 12px;">
            🛡️ HỆ THỐNG PHÁT HIỆN TIN NHẮN LỪA ĐẢO
        </h1>
        <p style="margin: 8px 0 0 0; font-size: {int(19 * font_mult)}px; opacity: 0.95; font-weight: 500;">
            Chuyên sâu nhận diện các chiêu trò thao túng tâm lý nhắm vào Người cao tuổi (CS114 - Nhóm 10)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Bố cục 2 cột chính
    col_left, col_right = st.columns([1.1, 1.2], gap="large")

    with col_left:
        st.markdown(f"<h3 style='font-size: {int(24 * font_mult)}px; color: #1e3a8a; margin-bottom: 4px;'>📩 NHẬP TIN NHẮN CẦN KIỂM TRA</h3>", unsafe_allow_html=True)

        if "sms_input" not in st.session_state:
            st.session_state["sms_input"] = ""

        def select_preset(key: str):
            if key in PRESET_SAMPLES:
                st.session_state["sms_input"] = PRESET_SAMPLES[key]["text"]
            else:
                st.session_state["sms_input"] = ""

        # Dòng hướng dẫn và nút xóa trắng gọn gàng
        col_lbl, col_clr = st.columns([3.2, 1.2])
        with col_lbl:
            st.markdown(f"<p style='font-size: {int(17 * font_mult)}px; color: #475569; margin-top: 6px;'>Dán tin nhắn SMS, Zalo lạ vào ô dưới đây:</p>", unsafe_allow_html=True)
        with col_clr:
            st.button("🗑️ Xóa trắng", key="btn_clear_top", on_click=select_preset, args=("clear",), use_container_width=True)

        # Ô nhập tin nhắn to, rộng rãi, nằm ngay trên đầu
        user_input = st.text_area(
            "Nội dung tin nhắn:",
            key="sms_input",
            height=180,
            placeholder="Ví dụ: CUC CSGT THONG BAO: Ban bi phat nguoi 5 trieu, nop phat gap neu khong se bi bat tam giam...",
            label_visibility="collapsed",
        )

        # Nút Kiểm tra chính
        btn_check = st.button("🔍 KIỂM TRA TIN NHẮN NGAY", type="primary", use_container_width=True)

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        # Khối kịch bản mẫu thu gọn lịch sự
        with st.expander("💡 Hoặc bấm vào đây để thử nhanh các kịch bản lừa đảo thực tế", expanded=True):
            st.markdown(f"<p style='font-size: {int(16 * font_mult)}px; color: #64748b; margin-bottom: 8px;'>Bấm 1 chạm để nạp kịch bản mẫu vào ô kiểm tra bên trên:</p>", unsafe_allow_html=True)
            sc_c1, sc_c2 = st.columns(2, gap="small")
            with sc_c1:
                st.button("⚖️ CSGT phạt nguội dọa bắt", key="btn_fear", on_click=select_preset, args=("fear",), use_container_width=True)
                st.button("🏛️ Giả VNeID dọa khóa định danh", key="btn_vneid", on_click=select_preset, args=("vneid",), use_container_width=True)
                st.button("💳 Tin nhắn biến động số dư (An toàn)", key="btn_bank", on_click=select_preset, args=("bank",), use_container_width=True)
            with sc_c2:
                st.button("🚨 Báo người thân tai nạn cấp cứu", key="btn_emergency", on_click=select_preset, args=("emergency",), use_container_width=True)
                st.button("🎁 Báo trúng thưởng xe & thuốc bổ", key="btn_gift", on_click=select_preset, args=("gift",), use_container_width=True)

    with col_right:
        st.markdown(f"<h3 style='font-size: {int(24 * font_mult)}px; color: #1e3a8a;'>📊 KẾT QUẢ ĐÁNH GIÁ TỪ TRÍ TUỆ NHÂN TẠO</h3>", unsafe_allow_html=True)

        if btn_check and user_input.strip():
            with st.spinner("🤖 Trí tuệ nhân tạo đang phân tích các bẫy thao túng tâm lý..."):
                proba, is_scam = predict_text(user_input, bundle)
                category = diagnose_scam_category(user_input)

            # 1. Thước đo rủi ro
            render_risk_meter(proba, font_multiplier=font_mult)

            # 2. Bôi đỏ từ khóa cảnh báo
            st.markdown(f"<div style='font-size: {int(20 * font_mult)}px; font-weight: 700; color: #1e293b; margin-top: 18px; margin-bottom: 8px;'>🔍 Phân tích các từ khóa nghi vấn trong tin nhắn:</div>", unsafe_allow_html=True)
            highlighted_html = highlight_text_html(user_input, font_multiplier=font_mult)
            st.markdown(highlighted_html, unsafe_allow_html=True)

            # 3. Lời khuyên an toàn chuyên biệt
            render_safety_advisor(category, is_scam, font_multiplier=font_mult)

            # 4. Chi tiết kỹ thuật cho Hội đồng chấm thi / Giảng viên
            with st.expander("🛠️ Xem chi tiết kỹ thuật mô hình (Dành cho Giảng viên CS114)"):
                st.markdown(f"""
                - **Thuật toán sử dụng:** Random Forest Classifier (Ensemble Bagging)
                - **Kích thước không gian đặc trưng:** 5.015 chiều (5.000 TF-IDF N-gram 1-2 + 15 đặc trưng bẫy tâm lý)
                - **Chỉ số kiểm định Test Set:** Accuracy = 97.72%, Recall = 97.62%, F1-Score = 94.25%, ROC-AUC = 0.9976
                - **Xác suất mô hình dự đoán:** `{proba:.4f}`
                - **Nhóm bẫy tâm lý nhận diện:** `{category}`
                """)

        elif btn_check and not user_input.strip():
            st.warning("⚠️ Ông/Bà vui lòng dán hoặc nhập nội dung tin nhắn vào ô bên trái trước khi bấm kiểm tra nhé!")
        else:
            # Ảnh ông bà lớn tuổi kiểm tra tin nhắn và hướng dẫn sử dụng
            elderly_img_file = DEMO_DIR / "assets" / "elderly_check_sms.jpg"
            if elderly_img_file.exists():
                st.image(
                    str(elderly_img_file),
                    caption="Hệ thống hỗ trợ bảo vệ Người cao tuổi trước các thủ đoạn thao túng tâm lý qua điện thoại",
                    use_container_width=True,
                )

            st.markdown(f"""
            <div style="
                background: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 14px;
                padding: 20px;
                margin-top: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            ">
                <h4 style="font-size: {int(22 * font_mult)}px; font-weight: 800; color: #1e3a8a; margin-bottom: 10px;">
                    🛡️ HỆ THỐNG SẴN SÀNG BẢO VỆ ÔNG/BÀ
                </h4>
                <p style="font-size: {int(18 * font_mult)}px; line-height: 1.6; color: #334155; margin-bottom: 14px;">
                    Khi nhận được tin nhắn lạ yêu cầu chuyển tiền, đe dọa phạt nguội, hoặc báo người thân cấp cứu:
                </p>
                <div style="background: #ffffff; padding: 14px 18px; border-radius: 10px; border-left: 5px solid #0284c7; font-size: {int(17 * font_mult)}px; line-height: 1.8; color: #1e293b;">
                    ✅ <b>Bước 1:</b> Dán hoặc nhập nội dung tin nhắn vào ô bên trái.<br>
                    ✅ <b>Bước 2:</b> Bấm nút màu xanh <b>"KIỂM TRA TIN NHẮN NGAY"</b>.<br>
                    ✅ <b>Bước 3:</b> Xem ngay mức độ nguy hiểm, từ khóa nghi vấn và lời khuyên phòng tránh.
                </div>
            </div>
            """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
