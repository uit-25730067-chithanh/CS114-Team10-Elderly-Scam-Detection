"""
HỆ THỐNG PHÁT HIỆN TIN NHẮN & KỊCH BẢN THAO TÚNG TÂM LÝ LỪA ĐẢO NHẮM VÀO NGƯỜI CAO TUỔI
Học phần: CS114 — Machine Learning (ĐH Công Nghệ Thông Tin - ĐHQG TP.HCM)
Nhóm 10: Hoàng Cao Sơn (Demo Lead), Đặng Chí Thanh, Bùi Thị Mỷ Cẩm
Giảng viên hướng dẫn: ThS. Cáp Phạm Đình Thăng
"""

from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, hstack
import streamlit as st

# Thiết lập đường dẫn hệ thống chuẩn hóa
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
from src.preprocessing.pipeline import extract_auxiliary_features, preprocess_pipeline

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Phát Hiện Tin Nhắn Lừa Đảo Cho Người Cao Tuổi — CS114",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Danh mục thông số 4 mô hình học máy (CS114 Model Benchmark Catalog)
MODEL_CATALOG: Dict[str, Dict[str, Any]] = {
    "random_forest": {
        "name": "🌲 Random Forest (Mặc định)",
        "file": "random_forest.pkl",
        "dims": 5015,
        "type": "ensemble",
        "desc": "Ensemble Bagging 200 cây quyết định, tối ưu hóa chống Overfitting",
        "accuracy": "97.72%",
        "f1": "94.25%",
        "recall": "97.62%",
        "roc_auc": "0.9976",
        "author": "Hoàng Cao Sơn (MSSV: 25730061)",
    },
    "xgboost": {
        "name": "⚡ XGBoost (F1 Tối ưu)",
        "file": "xgboost.pkl",
        "dims": 5015,
        "type": "boosting",
        "desc": "Gradient Boosting với scale_pos_weight=4.22 xử lý mất cân bằng nhãn",
        "accuracy": "98.18%",
        "f1": "95.35%",
        "recall": "97.62%",
        "roc_auc": "0.9984",
        "author": "Bùi Thị Mỷ Cẩm (MSSV: 25730013)",
    },
    "svm_linear": {
        "name": "🎯 Linear SVM (Calibrated CV)",
        "file": "svm_linear.pkl",
        "dims": 5015,
        "type": "svm",
        "desc": "LinearSVC kết hợp hiệu chỉnh xác suất CalibratedClassifierCV (Sigmoid)",
        "accuracy": "98.41%",
        "f1": "95.81%",
        "recall": "96.43%",
        "roc_auc": "0.9986",
        "author": "Bùi Thị Mỷ Cẩm (MSSV: 25730013)",
    },
    "naive_bayes": {
        "name": "📊 Naive Bayes (Baseline)",
        "file": "naive_bayes.pkl",
        "dims": 5000,
        "type": "nb",
        "desc": "Mô hình xác suất Bayes cơ sở (TF-IDF non-negative, alpha=0.01)",
        "accuracy": "95.44%",
        "f1": "88.64%",
        "recall": "92.86%",
        "roc_auc": "0.9911",
        "author": "Bùi Thị Mỷ Cẩm (MSSV: 25730013)",
    },
}

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

# Diễn giải 15 đặc trưng phụ tâm lý cho Hội đồng Giảng viên
AUX_FEATURE_DESCRIPTIONS = {
    "num_urls": ("Số liên kết đường dẫn (URL/Domain)", "Dẫn dụ nạn nhân vào trang web lừa đảo/cài mã độc"),
    "num_phone_numbers": ("Số điện thoại lạ xuất hiện", "Cung cấp hotline giả mạo để thao túng trực tiếp"),
    "num_money_mentions": ("Đề cập số tiền/giao dịch", "Ép chuyển khoản viện phí, phạt nguội hoặc hứa thưởng lớn"),
    "has_urgent_words": ("Từ ngữ hối thúc khẩn cấp (gấp, ngay)", "Tạo áp lực thời gian khiến nạn nhân hoảng sợ mất bình tĩnh"),
    "num_authority_words": ("Từ ngữ mạo danh cơ quan công quyền", "Mượn danh Công an, Viện KS, Tòa án, VNeID để gây sợ hãi"),
    "has_emergency_words": ("Từ ngữ cấp cứu/tai nạn người thân", "Khai thác tình mẫu tử, lòng trắc ẩn của người già"),
    "has_gift_words": ("Từ ngữ trúng thưởng/quà tri ân", "Kích thích lòng tham quà tặng miễn phí hoặc bài thuốc tiên"),
    "has_otp_request": ("Yêu cầu mã OTP/Mật khẩu tài khoản", "Chiếm đoạt quyền kiểm soát tài khoản ngân hàng"),
    "has_leet_speak": ("Ký tự lách luật (th0ng ba0, t1en)", "Cố tình biến dạng chữ để né bộ lọc spam của nhà mạng"),
    "is_unaccented": ("Tin nhắn không dấu tiếng Việt", "Thủ thuật thường thấy của các đối tượng gửi tin nhắn rác quốc tế"),
    "text_length": ("Tổng độ dài ký tự tin nhắn", "Kịch bản lừa đảo thường dài hơn tin nhắn sinh hoạt"),
    "num_words": ("Tổng số từ trong tin nhắn", "Phản ánh dung lượng thông tin truyền tải"),
    "num_exclamation": ("Dấu chấm than (!) đe dọa", "Tăng cường độ cảm xúc giật gân, đe dọa"),
    "num_question": ("Dấu chấm hỏi (?) nghi vấn", "Thăm dò, đặt câu hỏi thao túng"),
    "num_uppercase_words": ("Từ viết IN HOA toàn bộ", "Nhấn mạnh, quát nạt hoặc giả danh thương hiệu chính thống"),
}


@st.cache_resource
def load_all_detection_engines():
    """Tải toàn bộ bộ trích xuất đặc trưng và 4 mô hình học máy phục vụ benchmark."""
    engines: Dict[str, Any] = {}
    vec_path = PROJECT_ROOT / "data" / "processed" / "tfidf_vectorizer.pkl"
    scaler_path = PROJECT_ROOT / "data" / "processed" / "aux_scaler.pkl"

    if not vec_path.exists() or not scaler_path.exists():
        logging.error("Thiếu tfidf_vectorizer.pkl hoặc aux_scaler.pkl trong data/processed/")
        return None, "Lỗi: Không tìm thấy bộ trích xuất đặc trưng!"

    try:
        vectorizer = joblib.load(vec_path)
        scaler = joblib.load(scaler_path)
        engines["vectorizer"] = vectorizer
        engines["aux_scaler"] = scaler
    except Exception as e:
        logging.error(f"Lỗi khi nạp vectorizer/scaler: {e}")
        return None, f"Lỗi nạp vectorizer: {e}"

    # Nạp từng mô hình từ thư mục models/
    for key, info in MODEL_CATALOG.items():
        model_path = PROJECT_ROOT / "models" / info["file"]
        if model_path.exists():
            try:
                model = joblib.load(model_path)
                engines[key] = model
            except Exception as e:
                logging.error(f"Lỗi khi nạp mô hình {key} ({info['file']}): {e}")

    # Kiểm tra bundle tổng hợp nếu thiếu các file lẻ
    if "random_forest" not in engines:
        bundle_path = PROJECT_ROOT / "models" / "best_model_bundle.pkl"
        if bundle_path.exists():
            try:
                bundle = joblib.load(bundle_path)
                engines["random_forest"] = bundle["model"]
            except Exception as e:
                logging.error(f"Lỗi nạp bundle fallback: {e}")

    loaded_count = sum(1 for k in MODEL_CATALOG if k in engines)
    status_msg = f"Đã sẵn sàng {loaded_count}/4 Mô hình Học Máy (Random Forest, XGBoost, SVM, Naive Bayes)"
    return engines, status_msg


def predict_text(
    raw_text: str,
    model_key: str,
    engines: Optional[Dict[str, Any]],
) -> Tuple[float, bool, Dict[str, Any], Dict[str, Any]]:
    """
    Suy luận xác suất lừa đảo trên văn bản người dùng nhập với chuyển đổi linh hoạt mô hình.
    Trả về: (xác suất, là_lừa_đảo, từ_điển_15_đặc_trưng, thông_tin_mô_hình)
    """
    model_info = MODEL_CATALOG.get(model_key, MODEL_CATALOG["random_forest"])

    # 1. Tiền xử lý NLP tiếng Việt toàn diện bằng pipeline chuẩn hóa
    cleaned_text, aux_dict = preprocess_pipeline(raw_text)

    if engines is not None and model_key in engines:
        model = engines[model_key]
        vectorizer = engines["vectorizer"]
        scaler = engines["aux_scaler"]

        # Biến đổi TF-IDF (5.000 n-grams)
        tfidf_vec = vectorizer.transform([cleaned_text])

        # Phân nhánh theo không gian đặc trưng của từng mô hình
        if model_info["dims"] == 5000:
            # Naive Bayes: Chỉ dùng 5.000 chiều TF-IDF
            full_input = tfidf_vec
        else:
            # Random Forest, XGBoost, Linear SVM: Ghép 5.000 TF-IDF + 15 đặc trưng phụ = 5.015 chiều
            aux_df = pd.DataFrame([aux_dict])[AUX_FEATURE_COLS]
            aux_scaled = scaler.transform(aux_df.values.astype(float))
            full_input = hstack([tfidf_vec, csr_matrix(aux_scaled)], format="csr")

        # Dự đoán xác suất từ mô hình
        if hasattr(model, "predict_proba"):
            proba = float(model.predict_proba(full_input)[0][1])
        else:
            proba = 0.5

        threshold = 0.5
        return proba, bool(proba >= threshold), aux_dict, model_info

    # Heuristic Rule fallback nếu chưa có file weights
    keywords = extract_found_keywords(raw_text)
    score = min(len(keywords) * 0.25, 0.95)
    return score, bool(score >= 0.5), aux_dict, model_info


# ================= GIAO DIỆN CHÍNH (STREAMLIT APP) =================
def main():
    engines, engine_status = load_all_detection_engines()

    # --- Thanh điều khiển bên Sidebar ---
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/shield.png", width=70)
        st.markdown("### ⚙️ CÀI ĐẶT HỆ THỐNG")

        # 1. Bộ chọn cỡ chữ người cao tuổi
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

        # 2. Bộ chuyển đổi mô hình học máy (CS114 Model Switcher)
        st.markdown("### 🤖 BỘ CHỌN MÔ HÌNH HỌC MÁY")
        available_model_keys = [k for k in MODEL_CATALOG.keys() if engines and k in engines] or list(MODEL_CATALOG.keys())
        selected_model_key = st.selectbox(
            "Mô hình thực thi dự đoán:",
            options=available_model_keys,
            format_func=lambda k: MODEL_CATALOG[k]["name"],
            index=0,
            help="Cho phép Hội đồng Giảng viên CS114 đối chứng trực tiếp phản ứng giữa các thuật toán trên cùng một tin nhắn.",
        )
        current_model_meta = MODEL_CATALOG[selected_model_key]

        # Thẻ thông số tóm tắt của mô hình đang chọn
        st.markdown(f"""
        <div style="
            background: #f1f5f9;
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            padding: 10px 14px;
            margin-top: 8px;
            font-size: 13px;
        ">
            <b>Đặc tả:</b> {current_model_meta['desc']}<br>
            <b>Không gian:</b> {current_model_meta['dims']:,} chiều<br>
            <b>F1-Score:</b> <span style="color: #1e40af; font-weight: 700;">{current_model_meta['f1']}</span> | 
            <b>Recall:</b> <span style="color: #b91c1c; font-weight: 700;">{current_model_meta['recall']}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### ℹ️ THÔNG TIN DỰ ÁN")
        st.info(
            f"**Trạng thái:** {engine_status}\n\n"
            f"**Học phần:** CS114 — Machine Learning (UIT)\n\n"
            f"**Giảng viên:** ThS. Cáp Phạm Đình Thăng\n\n"
            f"**Nhóm 10:** Hoàng Cao Sơn, Đặng Chí Thanh, Bùi Thị Mỷ Cẩm"
        )

        st.markdown("---")
        st.markdown("#### 🚨 HOTLINE HỖ TRỢ KHẨN CẤP")
        st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <a href="tel:156" style="
                background: #ef4444; color: white !important; text-decoration: none;
                padding: 10px 12px; border-radius: 8px; font-weight: 700; text-align: center;
                display: block; font-size: 14px;
            ">📞 Tổng đài An Toàn Thông Tin: 156</a>
            <a href="tel:113" style="
                background: #f97316; color: white !important; text-decoration: none;
                padding: 10px 12px; border-radius: 8px; font-weight: 700; text-align: center;
                display: block; font-size: 14px;
            ">🚨 Khẩn Cấp Công An: 113</a>
        </div>
        """, unsafe_allow_html=True)

    # CSS Tùy biến Cỡ Chữ Lớn & Thân Thiện Người Cao Tuổi (Tối ưu Responsive Đa Thiết Bị)
    custom_css = f"""
    <style>
        /* Mặc định cho màn hình máy tính (Desktop / Laptop) */
        @media (min-width: 769px) {{
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
            }}
        }}

        /* Tối ưu hóa đặc biệt cho màn hình Điện thoại / Tablet (Mobile Responsive <= 768px, 360px-450px) */
        @media (max-width: 768px) {{
            html, body, [class*="css"] {{
                font-size: 15px !important;
                font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
            }}
            .main .block-container {{
                padding: 1rem 0.6rem 2rem 0.6rem !important;
            }}
            .stTextArea textarea {{
                font-size: 16px !important;
                line-height: 1.5 !important;
                border: 2px solid #3b82f6 !important;
                border-radius: 10px !important;
            }}
            .stButton button[kind="primary"] {{
                font-size: 17px !important;
                font-weight: 800 !important;
                border-radius: 10px !important;
                padding: 12px 16px !important;
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
                color: white !important;
                border: none !important;
                box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3) !important;
                width: 100% !important;
            }}
            .stButton button[kind="secondary"], .stButton button:not([kind="primary"]) {{
                font-size: 13px !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                padding: 6px 8px !important;
                background: #f8fafc !important;
                color: #1e3a8a !important;
                border: 1px solid #cbd5e1 !important;
                width: 100% !important;
            }}
        }}

        .stButton button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
            box-shadow: 0 6px 18px rgba(30, 64, 175, 0.45) !important;
        }}
        .stButton button[kind="secondary"]:hover, .stButton button:not([kind="primary"]):hover {{
            background: #e0f2fe !important;
            border-color: #0284c7 !important;
            color: #0369a1 !important;
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # --- Banner Tiêu Đề Chính (Tự thích ứng độ phân giải) ---
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%);
        padding: clamp(14px, 3.5vw, 24px) clamp(16px, 4vw, 30px);
        border-radius: 16px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.25);
    ">
        <h1 style="color: white; margin: 0; font-size: clamp(20px, 5.2vw, {int(30 * font_mult)}px); font-weight: 900; display: flex; align-items: center; gap: 10px; line-height: 1.3;">
            🛡️ HỆ THỐNG PHÁT HIỆN TIN NHẮN LỪA ĐẢO
        </h1>
        <p style="margin: 6px 0 0 0; font-size: clamp(14px, 3.5vw, {int(18 * font_mult)}px); opacity: 0.95; font-weight: 500; line-height: 1.45;">
            Chuyên sâu nhận diện các chiêu trò thao túng tâm lý nhắm vào Người cao tuổi (CS114 — Nhóm 10)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Bố cục 2 cột chính (Split-View Workbench Archetype)
    col_left, col_right = st.columns([1.1, 1.2], gap="large")

    with col_left:
        st.markdown(f"<h3 style='font-size: clamp(18px, 4.5vw, {int(24 * font_mult)}px); color: #1e3a8a; margin-bottom: 4px; line-height: 1.35;'>📩 NHẬP TIN NHẮN CẦN KIỂM TRA</h3>", unsafe_allow_html=True)

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
            st.markdown(f"<p style='font-size: clamp(14px, 3.4vw, {int(17 * font_mult)}px); color: #475569; margin-top: 6px;'>Dán tin nhắn SMS, Zalo lạ vào ô dưới đây:</p>", unsafe_allow_html=True)
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
            st.markdown(f"<p style='font-size: clamp(13px, 3.2vw, {int(16 * font_mult)}px); color: #64748b; margin-bottom: 8px;'>Bấm 1 chạm để nạp kịch bản mẫu vào ô kiểm tra bên trên:</p>", unsafe_allow_html=True)
            sc_c1, sc_c2 = st.columns(2, gap="small")
            with sc_c1:
                st.button("⚖️ CSGT phạt nguội dọa bắt", key="btn_fear", on_click=select_preset, args=("fear",), use_container_width=True)
                st.button("🏛️ Giả VNeID dọa khóa định danh", key="btn_vneid", on_click=select_preset, args=("vneid",), use_container_width=True)
                st.button("💳 Tin nhắn biến động số dư (An toàn)", key="btn_bank", on_click=select_preset, args=("bank",), use_container_width=True)
            with sc_c2:
                st.button("🚨 Báo người thân tai nạn cấp cứu", key="btn_emergency", on_click=select_preset, args=("emergency",), use_container_width=True)
                st.button("🎁 Báo trúng thưởng xe & thuốc bổ", key="btn_gift", on_click=select_preset, args=("gift",), use_container_width=True)

    with col_right:
        st.markdown(f"<h3 style='font-size: clamp(18px, 4.5vw, {int(24 * font_mult)}px); color: #1e3a8a; margin-bottom: 4px; line-height: 1.35;'>📊 KẾT QUẢ ĐÁNH GIÁ TỪ TRÍ TUỆ NHÂN TẠO</h3>", unsafe_allow_html=True)

        input_valid = bool(user_input.strip() and len(user_input.strip()) >= 10)

        if btn_check and input_valid:
            # Script cuộn trang mượt mà trên thiết bị di động
            st.components.v1.html(
                """
                <script>
                    setTimeout(function() {
                        const target = window.parent.document.getElementById('verdict-anchor');
                        if (target) {
                            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    }, 150);
                </script>
                """,
                height=0,
            )

            with st.spinner(f"🤖 Đang kích hoạt mô hình {current_model_meta['name']} phân tích bẫy tâm lý..."):
                proba, is_scam, aux_dict, model_info = predict_text(user_input, selected_model_key, engines)
                category = diagnose_scam_category(user_input)

            # 1. Thước đo rủi ro (Risk Meter)
            render_risk_meter(proba, font_multiplier=font_mult)

            # 2. Bôi đỏ từ khóa cảnh báo (Pre-compiled Keyword Highlighter)
            st.markdown(f"<div style='font-size: clamp(16px, 4vw, {int(20 * font_mult)}px); font-weight: 700; color: #1e293b; margin-top: 16px; margin-bottom: 8px;'>🔍 Phân tích các từ khóa nghi vấn trong tin nhắn:</div>", unsafe_allow_html=True)
            highlighted_html = highlight_text_html(user_input, font_multiplier=font_mult)
            st.markdown(highlighted_html, unsafe_allow_html=True)

            # 3. Lời khuyên an toàn chuyên biệt + Nút gọi khẩn cấp 1-chạm
            render_safety_advisor(category, is_scam, font_multiplier=font_mult)

            # 4. Bảng Thanh tra Kỹ thuật dành cho Hội đồng Chấm thi CS114 (Academic Inspector Panel)
            with st.expander("🛠️ Xem chi tiết kỹ thuật mô hình (Dành cho Giảng viên CS114)"):
                st.markdown(f"""
                #### 1. Thông số Kỹ thuật Mô hình Thực thi
                - **Thuật toán đang chạy:** `{model_info['name']}`
                - **Phương pháp / Cấu trúc:** {model_info['desc']}
                - **Không gian biểu diễn:** `{model_info['dims']:,} chiều`
                - **Chỉ số kiểm định Test Set (439 mẫu):**
                  - Accuracy = **{model_info['accuracy']}**
                  - Precision = **{model_info.get('precision', 'N/A')}**
                  - Recall (Phát hiện lừa đảo) = **{model_info['recall']}**
                  - F1-Score = **{model_info['f1']}**
                  - ROC-AUC = **{model_info['roc_auc']}**
                - **Xác suất mô hình dự đoán:** `{proba:.4f}` ({proba*100:.2f}%)
                - **Phân loại bẫy tâm lý chẩn đoán:** `{category}`
                - **Tác giả phụ trách:** `{model_info['author']}`
                """)

                st.markdown("#### 2. Bảng Phân tích 15 Đặc trưng Tâm lý Real-time (Extracted Auxiliary Features)")
                st.caption("Các đặc trưng phụ được bóc tách trực tiếp từ tin nhắn người dùng trước khi chuyển đổi số học:")

                feature_rows = []
                for feat_col in AUX_FEATURE_COLS:
                    val = aux_dict.get(feat_col, 0)
                    feat_title, feat_impact = AUX_FEATURE_DESCRIPTIONS.get(feat_col, (feat_col, "Đặc trưng ngôn ngữ"))
                    if isinstance(val, (int, float)) and val > 0:
                        status = f"🔴 Phát hiện ({val})"
                    else:
                        status = "🟢 Bình thường (0)"
                    feature_rows.append({
                        "Mã đặc trưng": feat_col,
                        "Tên đặc trưng tiếng Việt": feat_title,
                        "Giá trị trích xuất": val,
                        "Trạng thái kích hoạt": status,
                        "Ý nghĩa cảnh báo tâm lý": feat_impact,
                    })

                feat_df = pd.DataFrame(feature_rows)
                st.dataframe(feat_df, use_container_width=True, hide_index=True)

        elif btn_check and not user_input.strip():
            st.warning("⚠️ Ông/Bà vui lòng dán hoặc nhập nội dung tin nhắn vào ô bên trái trước khi bấm kiểm tra nhé!")
        elif btn_check and len(user_input.strip()) < 10:
            st.warning("⚠️ Tin nhắn quá ngắn để phân tích chính xác các thủ đoạn thao túng tâm lý. Ông/Bà vui lòng nhập đầy đủ câu văn của tin nhắn nhé!")
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
                padding: clamp(14px, 3.5vw, 20px);
                margin-top: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            ">
                <h4 style="font-size: clamp(17px, 4.2vw, {int(22 * font_mult)}px); font-weight: 800; color: #1e3a8a; margin-bottom: 10px;">
                    🛡️ HỆ THỐNG SẴN SÀNG BẢO VỆ ÔNG/BÀ
                </h4>
                <p style="font-size: clamp(14px, 3.5vw, {int(18 * font_mult)}px); line-height: 1.6; color: #334155; margin-bottom: 14px;">
                    Khi nhận được tin nhắn lạ yêu cầu chuyển tiền, đe dọa phạt nguội, hoặc báo người thân cấp cứu:
                </p>
                <div style="background: #ffffff; padding: 12px 16px; border-radius: 10px; border-left: 5px solid #0284c7; font-size: clamp(13px, 3.2vw, {int(17 * font_mult)}px); line-height: 1.7; color: #1e293b;">
                    ✅ <b>Bước 1:</b> Dán hoặc nhập nội dung tin nhắn vào ô bên trái.<br>
                    ✅ <b>Bước 2:</b> Bấm nút màu xanh <b>"KIỂM TRA TIN NHẮN NGAY"</b>.<br>
                    ✅ <b>Bước 3:</b> Xem ngay mức độ nguy hiểm, từ khóa nghi vấn và lời khuyên phòng tránh.
                </div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
