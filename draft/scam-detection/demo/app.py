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
import time
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
    page_title="Hệ Thống Phát Hiện Tin Nhắn Lừa Đảo — CS114",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Danh mục thông số 4 mô hình học máy (CS114 Model Benchmark Catalog)
MODEL_CATALOG: Dict[str, Dict[str, Any]] = {
    "xgboost": {
        "name": "⚡ XGBoost (Mặc định — F1 Tối ưu 0.9535)",
        "file": "xgboost.pkl",
        "dims": 5015,
        "type": "boosting",
        "desc": "Gradient Boosting với scale_pos_weight=4.22 tối ưu F1 trên dữ liệu mất cân bằng",
        "accuracy": "98.18%",
        "precision": "93.18%",
        "recall": "97.62%",
        "f1": "95.35%",
        "roc_auc": "0.9984",
        "author": "Bùi Thị Mỷ Cẩm (MSSV: 25730013)",
    },
    "svm_linear": {
        "name": "🎯 Linear SVM (Á quân — Calibrated CV)",
        "file": "svm_linear.pkl",
        "dims": 5015,
        "type": "svm",
        "desc": "LinearSVC kết hợp hiệu chỉnh xác suất CalibratedClassifierCV (Sigmoid Platt Scaling)",
        "accuracy": "97.95%",
        "precision": "93.10%",
        "recall": "96.43%",
        "f1": "94.74%",
        "roc_auc": "0.9986",
        "author": "Bùi Thị Mỷ Cẩm (MSSV: 25730013)",
    },
    "random_forest": {
        "name": "🌲 Random Forest (Ensemble Bagging 200 cây)",
        "file": "random_forest.pkl",
        "dims": 5015,
        "type": "ensemble",
        "desc": "Ensemble Bagging 200 cây quyết định, độ ổn định cao, chống Overfitting",
        "accuracy": "97.72%",
        "precision": "91.11%",
        "recall": "97.62%",
        "f1": "94.25%",
        "roc_auc": "0.9976",
        "author": "Hoàng Cao Sơn (MSSV: 25730061)",
    },
    "naive_bayes": {
        "name": "📊 Naive Bayes (Baseline Đối chứng)",
        "file": "naive_bayes.pkl",
        "dims": 5000,
        "type": "nb",
        "desc": "Mô hình xác suất Bayes cơ sở (TF-IDF 5.000 từ khóa, alpha=0.5)",
        "accuracy": "95.44%",
        "precision": "84.78%",
        "recall": "92.86%",
        "f1": "88.64%",
        "roc_auc": "0.9911",
        "author": "Đặng Chí Thanh (MSSV: 25730067)",
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
    if not any(k in engines for k in ("xgboost", "svm_linear", "random_forest")):
        bundle_path = PROJECT_ROOT / "models" / "best_model_bundle.pkl"
        if bundle_path.exists():
            try:
                bundle = joblib.load(bundle_path)
                b_name = bundle.get("model_name", "")
                if "SVM" in b_name:
                    engines["svm_linear"] = bundle["model"]
                elif "XGB" in b_name:
                    engines["xgboost"] = bundle["model"]
                else:
                    engines["random_forest"] = bundle["model"]
            except Exception as e:
                logging.error(f"Lỗi nạp bundle fallback: {e}")

    loaded_count = sum(1 for k in MODEL_CATALOG if k in engines)
    status_msg = f"Đã sẵn sàng {loaded_count}/4 Mô hình Học Máy (XGBoost, SVM, Random Forest, Naive Bayes)"
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
    model_info = MODEL_CATALOG.get(model_key, MODEL_CATALOG["xgboost"])

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

    # --- Thanh điều khiển bên Sidebar (Mặc định ẩn - collapsed) ---
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 24px;">🛡️</span>
                <span style="font-size: 15px; font-weight: 800; color: #0f172a;">CÀI ĐẶT HỆ THỐNG</span>
            </div>
            <div style="
                font-size: 11px;
                font-weight: 700;
                color: #15803d;
                background-color: #dcfce7;
                border: 1px solid #86efac;
                padding: 2px 8px;
                border-radius: 20px;
            ">
                🟢 Trực tuyến
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 1. Bộ chọn cỡ chữ hiển thị trực quan kích thước thực tế (Visual Font-Size Preview)
        font_choice = st.radio(
            "🔎 Cỡ chữ hiển thị:",
            ["Chữ Vừa (100%)", "Chữ To (125%)", "Chữ Rất To (150%)"],
            index=1,
            help="Cỡ chữ trên giao diện sẽ thay đổi tương ứng theo lựa chọn của Ông/Bà.",
        )
        multiplier_map = {
            "Chữ Vừa (100%)": 1.0,
            "Chữ To (125%)": 1.25,
            "Chữ Rất To (150%)": 1.5,
        }
        font_mult = multiplier_map[font_choice]

        st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

        # 2. Hotline Hỗ Trợ Khẩn Cấp (Độ tương phản cao chuẩn WCAG AAA - Chữ Trắng nổi bật tuyệt đối)
        st.markdown("#### 🚨 Đường dây nóng")
        st.markdown("""
        <div class="hotline-card-sidebar">
            <a href="tel:156" class="hotline-link-red">
                <span>📞 Tổng đài Quốc gia: 156</span>
            </a>
            <a href="tel:113" class="hotline-link-orange">
                <span>🚨 Cảnh sát Khẩn cấp: 113</span>
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 3. Chế độ Chuyên sâu CS114 (Toggle cho Giảng viên / Nghiên cứu)
        academic_mode = st.toggle(
            "🎓 Chế độ giảng viên",
            value=False,
            help="Bật để Hội đồng Giảng viên xem chi tiết ma trận kiểm định, so sánh 4 mô hình học máy và đặc tả 5.015 chiều.",
        )

        available_model_keys = [k for k in MODEL_CATALOG.keys() if engines and k in engines] or list(MODEL_CATALOG.keys())

        if academic_mode:
            st.markdown("### 🤖 BỘ CHỌN MÔ HÌNH HỌC MÁY")
            selected_model_key = st.selectbox(
                "Mô hình thực thi dự đoán:",
                options=available_model_keys,
                format_func=lambda k: MODEL_CATALOG[k]["name"],
                index=0,
                help="Cho phép Hội đồng Giảng viên CS114 đối chứng trực tiếp phản ứng giữa các thuật toán trên cùng một tin nhắn.",
            )
            current_model_meta = MODEL_CATALOG[selected_model_key]

            # Thẻ thông số kỹ thuật tóm tắt gọn gàng
            st.markdown(f"""
            <div style="
                background: #f1f5f9;
                border-left: 4px solid #3b82f6;
                border-radius: 8px;
                padding: 8px 12px;
                margin-top: 6px;
                font-size: 13px;
                line-height: 1.45;
            ">
                <b>Đặc tả:</b> {current_model_meta['desc']}<br>
                <b>Không gian:</b> {current_model_meta['dims']:,} chiều<br>
                <b>F1-Score:</b> <span style="color: #1e40af; font-weight: 700;">{current_model_meta['f1']}</span> | 
                <b>Recall:</b> <span style="color: #b91c1c; font-weight: 700;">{current_model_meta['recall']}</span><br>
                <b>Độ chính xác:</b> <span style="color: #15803d; font-weight: 700;">{current_model_meta['accuracy']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Chế độ Người cao tuổi: Mặc định chọn mô hình tối ưu (XGBoost F1=0.9535)
            selected_model_key = available_model_keys[0] if available_model_keys else "xgboost"
            current_model_meta = MODEL_CATALOG[selected_model_key]
            st.markdown("""
            <div style="
                background: #f0fdf4;
                border: 1.5px solid #86efac;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                color: #166534;
                line-height: 1.45;
            ">
                🛡️ <b>Mô hình bảo vệ tối ưu (XGBoost):</b><br>
                Đang chạy bộ lọc Trí tuệ Nhân tạo đa tầng (Độ chính xác 98.18%, phát hiện 97.62% tin lừa đảo).
            </div>
            """, unsafe_allow_html=True)

    # CSS Tinh gọn Padding & Tối ưu Trợ Năng Người Cao Tuổi
    custom_css = f"""
    <style>
        /* Ẩn hoàn toàn các nút rác của Streamlit (Deploy, Manage App, MainMenu 3 chấm) */
        .stAppDeployButton, [data-testid="stAppDeployButton"] {{
            display: none !important;
        }}
        #MainMenu, [data-testid="stMainMenu"] {{
            display: none !important;
        }}

        /* Thanh Header trong suốt, không che chắn hay cản trở click lên Banner */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            pointer-events: none !important;
        }}
        header[data-testid="stHeader"] button {{
            pointer-events: auto !important;
        }}

        /* Nút mở Sidebar (>>) thẩm mỹ, nền trắng có viền và đổ bóng rõ ràng */
        button[data-testid="stExpandSidebarButton"] {{
            background: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
            pointer-events: auto !important;
            margin-top: 6px !important;
            margin-left: 6px !important;
        }}

        /* Đảm bảo Sidebar ẩn triệt để khi Collapsed, không để lọt phần thừa sang trang chính */
        section[data-testid="stSidebar"][aria-expanded="false"] {{
            display: none !important;
            width: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
            overflow: hidden !important;
        }}

        /* Thiết lập Sticky Footer & Khung trang toàn màn hình: */
        html, body {{
            height: 100% !important;
        }}

        section.stMain {{
            flex: 1 1 auto !important;
            display: flex !important;
            flex-direction: column !important;
            min-height: 100vh !important;
        }}

        /* Tinh gọn & Thích ứng Padding theo trạng thái Sidebar: */
        /* 1. Mặc định khi TẮT/ẨN Sidebar (Collapsed): Padding 2 bên rộng thoáng đãng, cân đối trên màn hình lớn */
        [data-testid="stAppViewContainer"]:has(section[data-testid="stSidebar"][aria-expanded="false"]) .block-container,
        section[data-testid="stSidebar"][aria-expanded="false"] ~ div .block-container,
        .main .block-container {{
            min-height: 100vh !important;
            flex: 1 0 auto !important;
            height: auto !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            padding-top: 3.2rem !important;
            padding-bottom: 8.5rem !important;
            padding-left: clamp(16px, 5vw, 4.5rem) !important;
            padding-right: clamp(16px, 5vw, 4.5rem) !important;
            max-width: 1400px !important;
            box-sizing: border-box !important;
            position: relative !important;
            transition: padding 0.3s ease !important;
        }}

        /* 2. Khi MỞ Sidebar (Expanded): Padding 2 bên co nhỏ lại tối đa (1rem) để nhường không gian cho 2 cột nội dung */
        [data-testid="stAppViewContainer"]:has(section[data-testid="stSidebar"][aria-expanded="true"]) .block-container,
        section[data-testid="stSidebar"][aria-expanded="true"] ~ div .block-container {{
            min-height: 100vh !important;
            flex: 1 0 auto !important;
            height: auto !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            padding-top: 3.2rem !important;
            padding-bottom: 8.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            position: relative !important;
            transition: padding 0.3s ease !important;
        }}

        .main .block-container > .stVerticalBlock,
        .main .block-container > div[data-testid="stVerticalBlock"],
        .main .block-container > div:first-child {{
            flex: 1 1 auto !important;
            display: flex !important;
            flex-direction: column !important;
        }}

        /* Loại bỏ relative trên container trực tiếp của footer để footer định vị tuyệt đối theo .block-container */
        div[data-testid="stElementContainer"]:has(.project-portal-footer),
        div.element-container:has(.project-portal-footer) {{
            position: static !important;
        }}

        /* Chân Trang Đồ Án (Absolute Footer) đặt ở đáy trang theo đúng position: absolute */
        .project-portal-footer {{
            position: absolute !important;
            bottom: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            box-sizing: border-box !important;
            z-index: 100 !important;
            background: rgba(255, 255, 255, 0.98) !important;
            border-top: 1px solid #cbd5e1 !important;
            padding: 10px 16px 8px 16px !important;
            text-align: center !important;
        }}

        /* Nút Hotline Đỏ - Tổng đài 156 (Sidebar & Banner) - Chống Streamlit khử style trên thẻ <a> */
        a.hotline-link-red, .hotline-link-red {{
            background: linear-gradient(135deg, #b91c1c 0%, #dc2626 100%) !important;
            border: 1.5px solid #ef4444 !important;
            color: #ffffff !important;
            text-decoration: none !important;
            padding: 7px 14px !important;
            border-radius: 8px !important;
            text-align: center !important;
            display: inline-block !important;
            font-size: 14px !important;
            font-weight: 800 !important;
            box-shadow: 0 3px 8px rgba(185, 28, 28, 0.4) !important;
            line-height: 1.3 !important;
            transition: all 0.2s ease !important;
        }}
        .hotline-card-sidebar a.hotline-link-red {{
            display: block !important;
            width: 100% !important;
            padding: 11px 14px !important;
            margin-bottom: 8px !important;
            box-sizing: border-box !important;
        }}
        a.hotline-link-red:hover {{
            background: #991b1b !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(185, 28, 28, 0.5) !important;
        }}
        a.hotline-link-red *, a.hotline-link-red span, a.hotline-link-red p {{
            color: #ffffff !important;
            font-weight: 800 !important;
        }}

        /* Nút Hotline Cam - Cảnh sát 113 (Sidebar & Banner) */
        a.hotline-link-orange, .hotline-link-orange {{
            background: linear-gradient(135deg, #c2410c 0%, #ea580c 100%) !important;
            border: 1.5px solid #f97316 !important;
            color: #ffffff !important;
            text-decoration: none !important;
            padding: 7px 14px !important;
            border-radius: 8px !important;
            text-align: center !important;
            display: inline-block !important;
            font-size: 14px !important;
            font-weight: 800 !important;
            box-shadow: 0 3px 8px rgba(194, 65, 12, 0.4) !important;
            line-height: 1.3 !important;
            transition: all 0.2s ease !important;
        }}
        .hotline-card-sidebar a.hotline-link-orange {{
            display: block !important;
            width: 100% !important;
            padding: 11px 14px !important;
            box-sizing: border-box !important;
        }}
        a.hotline-link-orange:hover {{
            background: #9a3412 !important;
            color: #ffffff !important;
            box-shadow: 0 4px 12px rgba(194, 65, 12, 0.5) !important;
        }}
        a.hotline-link-orange *, a.hotline-link-orange span, a.hotline-link-orange p {{
            color: #ffffff !important;
            font-weight: 800 !important;
        }}

        /* Nút Hotline Khẩn cấp trong Khối Hành Động Cần Làm Ngay */
        a.action-hotline-btn,
        a.action-hotline-btn:hover,
        a.action-hotline-btn:visited,
        a.action-hotline-btn:active,
        a.action-hotline-btn span {{
            color: #ffffff !important;
            text-decoration: none !important;
        }}

        /* Hiển thị trực quan kích thước cỡ chữ ngay trong Radio Selector */
        div[data-testid="stRadio"] div[role="radiogroup"] label:nth-of-type(1) p {{
            font-size: 14px !important;
            font-weight: 500 !important;
        }}
        div[data-testid="stRadio"] div[role="radiogroup"] label:nth-of-type(2) p {{
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #1e3a8a !important;
        }}
        div[data-testid="stRadio"] div[role="radiogroup"] label:nth-of-type(3) p {{
            font-size: 22px !important;
            font-weight: 800 !important;
            color: #0f172a !important;
        }}

        /* Chống cắt cụt chữ (anti-truncation) trên toàn bộ Button */
        .stButton button, .stButton button p, .stButton button div, .stButton button span {{
            white-space: normal !important;
            word-break: break-word !important;
            text-overflow: unset !important;
            overflow: visible !important;
            line-height: 1.4 !important;
        }}
        .stButton button {{
            height: auto !important;
            min-height: 42px !important;
        }}

        /* Màn hình máy tính (Desktop / Laptop) */
        @media (min-width: 769px) {{
            html, body, [class*="css"] {{
                font-size: {int(17 * font_mult)}px !important;
                font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
            }}
            .stTextArea textarea {{
                font-size: {int(18 * font_mult)}px !important;
                line-height: 1.55 !important;
                border: 2px solid #3b82f6 !important;
                border-radius: 10px !important;
            }}
            .stButton button[kind="primary"] {{
                font-size: {int(20 * font_mult)}px !important;
                font-weight: 800 !important;
                border-radius: 10px !important;
                padding: 11px 20px !important;
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
                color: white !important;
                border: none !important;
                box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3) !important;
                width: 100% !important;
            }}
            .stButton button[kind="secondary"], .stButton button:not([kind="primary"]) {{
                font-size: {int(15 * font_mult)}px !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                padding: 8px 14px !important;
                background: #f8fafc !important;
                color: #1e3a8a !important;
                border: 1.5px solid #cbd5e1 !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
                width: 100% !important;
                text-align: left !important;
                justify-content: flex-start !important;
            }}
        }}

        /* Màn hình Điện thoại / Tablet (Mobile Responsive <= 768px) */
        @media (max-width: 768px) {{
            html, body, [class*="css"] {{
                font-size: 15px !important;
                font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
            }}
            [data-testid="stAppViewContainer"] .block-container,
            [data-testid="stAppViewContainer"]:has(section[data-testid="stSidebar"]) .block-container,
            section[data-testid="stSidebar"] ~ div .block-container,
            .main .block-container {{
                padding-top: 2.8rem !important;
                padding-bottom: 6.5rem !important;
                padding-left: 32px !important;
                padding-right: 32px !important;
                position: relative !important;
            }}
            .project-portal-footer {{
                position: absolute !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                width: 100% !important;
                box-sizing: border-box !important;
                border-top: 1px solid #cbd5e1 !important;
                padding: 10px 8px 8px 8px !important;
            }}
            .stTextArea textarea {{
                font-size: 15px !important;
                line-height: 1.5 !important;
                border: 2px solid #3b82f6 !important;
                border-radius: 8px !important;
            }}
            .stButton button[kind="primary"] {{
                font-size: 16px !important;
                font-weight: 800 !important;
                border-radius: 8px !important;
                padding: 10px 14px !important;
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
                color: white !important;
                border: none !important;
                box-shadow: 0 3px 10px rgba(30, 64, 175, 0.25) !important;
                width: 100% !important;
            }}
            .stButton button[kind="secondary"], .stButton button:not([kind="primary"]) {{
                font-size: 14px !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                padding: 8px 10px !important;
                background: #f8fafc !important;
                color: #1e3a8a !important;
                border: 1px solid #cbd5e1 !important;
                width: 100% !important;
                text-align: left !important;
                justify-content: flex-start !important;
            }}
        }}

        .stButton button[kind="primary"]:hover {{
            background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
            box-shadow: 0 6px 16px rgba(30, 64, 175, 0.4) !important;
        }}
        .stButton button[kind="secondary"]:hover, .stButton button:not([kind="primary"]):hover {{
            background: #e0f2fe !important;
            border-color: #0284c7 !important;
            color: #0369a1 !important;
        }}

        /* Hiệu ứng thanh quét AI 60fps siêu mượt (GPU-accelerated) */
        @keyframes aiScanTrackGlow {{
            0% {{
                box-shadow: 0 0 6px rgba(59, 130, 246, 0.15);
            }}
            50% {{
                box-shadow: 0 0 16px rgba(59, 130, 246, 0.35);
            }}
            100% {{
                box-shadow: 0 0 6px rgba(59, 130, 246, 0.15);
            }}
        }}

        @keyframes aiScanBarFlow {{
            0% {{
                width: 0%;
            }}
            20% {{
                width: 35%;
            }}
            60% {{
                width: 80%;
            }}
            85% {{
                width: 95%;
            }}
            100% {{
                width: 100%;
            }}
        }}

        @keyframes aiScanBeam {{
            0% {{
                transform: translateX(-100%);
            }}
            100% {{
                transform: translateX(350%);
            }}
        }}

        @keyframes aiPulseDot {{
            0%, 100% {{
                transform: scale(1);
                opacity: 1;
            }}
            50% {{
                transform: scale(1.35);
                opacity: 0.45;
            }}
        }}

        @keyframes smoothFadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(12px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .ai-scan-card {{
            background: #ffffff !important;
            border: 1.5px solid #bfdbfe !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            margin-bottom: 14px !important;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.08) !important;
            animation: aiScanTrackGlow 2s ease-in-out infinite !important;
        }}

        .ai-scan-track {{
            height: 8px !important;
            background: #e2e8f0 !important;
            border-radius: 4px !important;
            overflow: hidden !important;
            position: relative !important;
            margin: 10px 0 8px 0 !important;
        }}

        .ai-scan-bar {{
            height: 100% !important;
            border-radius: 4px !important;
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 40%, #06b6d4 75%, #10b981 100%) !important;
            background-size: 200% 100% !important;
            animation: aiScanBarFlow 0.85s cubic-bezier(0.22, 1, 0.36, 1) forwards !important;
            position: relative !important;
        }}

        .ai-scan-bar::after {{
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 80px !important;
            height: 100% !important;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.75), transparent) !important;
            animation: aiScanBeam 1.1s ease-in-out infinite !important;
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # --- Banner Tiêu Đề Chính (Tinh gọn chiều cao & Hiện đại) ---
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
        padding: clamp(12px, 2.5vw, 18px) clamp(16px, 3vw, 24px);
        border-radius: 12px;
        color: white;
        margin-bottom: 10px;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.2);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <h1 style="color: white; margin: 0; font-size: clamp(18px, 4vw, {int(26 * font_mult)}px); font-weight: 900; display: flex; align-items: center; gap: 8px; line-height: 1.25;">
                🛡️ HỆ THỐNG PHÁT HIỆN TIN NHẮN LỪA ĐẢO
            </h1>
            <div style="
                font-size: 11px;
                font-weight: 700;
                color: #dcfce7;
                background: rgba(22, 101, 52, 0.4);
                border: 1px solid #86efac;
                padding: 3px 10px;
                border-radius: 20px;
            ">
                🟢 Trực tuyến 24/7
            </div>
        </div>
        <p style="margin: 4px 0 0 0; font-size: clamp(13px, 2.8vw, {int(16 * font_mult)}px); opacity: 0.95; font-weight: 500; line-height: 1.4;">
            Chuyên sâu nhận diện chiêu trò thao túng tâm lý nhắm vào Người cao tuổi (CS114 — Nhóm 10)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Banner cảnh báo & Hotline khẩn cấp phía trên khu vực kiểm tra (Tương phản cao WCAG AAA)
    st.markdown("""
    <div class="hotline-banner" style="
        background: #fff1f2;
        border: 1.5px solid #fecdd3;
        border-radius: 10px;
        padding: 8px 14px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
    ">
        <div style="font-size: clamp(13px, 3vw, 15px); font-weight: 700; color: #9f1239; display: flex; align-items: center; gap: 6px;">
            <span>🚨 <b>Bác đang bị thúc ép chuyển tiền hay đe dọa phạt nguội?</b> Hãy bình tĩnh dừng lại!</span>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <a href="tel:156" class="hotline-link-red" style="
                background: #dc2626 !important;
                color: #ffffff !important;
                text-decoration: none !important;
                padding: 5px 12px !important;
                border-radius: 8px !important;
                font-weight: 800 !important;
                font-size: 13px !important;
                box-shadow: 0 2px 5px rgba(220, 38, 38, 0.3) !important;
                display: inline-block !important;
            ">
                <span style="color: #ffffff !important; font-weight: 800 !important;">📞 Gọi 156</span>
            </a>
            <a href="tel:113" class="hotline-link-orange" style="
                background: #ea580c !important;
                color: #ffffff !important;
                text-decoration: none !important;
                padding: 5px 12px !important;
                border-radius: 8px !important;
                font-weight: 800 !important;
                font-size: 13px !important;
                box-shadow: 0 2px 5px rgba(234, 88, 12, 0.3) !important;
                display: inline-block !important;
            ">
                <span style="color: #ffffff !important; font-weight: 800 !important;">🚨 Gọi 113</span>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bố cục 2 cột chính (Split-View Workbench)
    col_left, col_right = st.columns([1.1, 1.2], gap="medium")

    with col_left:
        st.markdown(f"<h3 style='font-size: clamp(15px, 1.9vw, {int(19 * font_mult)}px); color: #1e3a8a; margin-bottom: 4px; line-height: 1.35; overflow-wrap: break-word; word-break: normal; text-wrap: balance;'>📩 NHẬP TIN NHẮN CẦN KIỂM TRA</h3>", unsafe_allow_html=True)

        if "sms_input" not in st.session_state:
            st.session_state["sms_input"] = ""

        # Đồng bộ tin nhắn từ URL Query Params nếu có (giữ kết quả đánh giá khi F5 / Reload trang)
        url_text = st.query_params.get("text", "").strip()
        if "sms_input" not in st.session_state:
            if url_text:
                st.session_state["sms_input"] = url_text
                st.session_state["evaluated_text"] = url_text
                st.session_state["auto_analyze"] = True
            else:
                st.session_state["sms_input"] = ""
                st.session_state["evaluated_text"] = ""
        elif url_text and not st.session_state.get("evaluated_text"):
            st.session_state["sms_input"] = url_text
            st.session_state["evaluated_text"] = url_text
            st.session_state["auto_analyze"] = True

        def select_preset(key: str):
            """Hỗ trợ nạp kịch bản mẫu và kích hoạt kiểm tra 1-chạm (One-Touch Execution)."""
            if key in PRESET_SAMPLES:
                preset_text = PRESET_SAMPLES[key]["text"]
                st.session_state["sms_input"] = preset_text
                st.session_state["evaluated_text"] = preset_text
                st.session_state["auto_analyze"] = True
                st.query_params["text"] = preset_text
            else:
                st.session_state["sms_input"] = ""
                st.session_state["evaluated_text"] = ""
                st.session_state["auto_analyze"] = False
                st.query_params.pop("text", None)

        # Kiểm tra trạng thái có dữ liệu nhập để hiển thị nút Nạp tin mẫu linh hoạt
        has_content = bool(st.session_state.get("sms_input", "").strip())

        col_lbl, col_act = st.columns([2.2, 1.8], gap="small")
        with col_lbl:
            st.markdown(f"<p style='font-size: clamp(13px, 1.6vw, {int(15 * font_mult)}px); color: #475569; margin-top: 6px; font-weight: 500; line-height: 1.3; overflow-wrap: break-word;'>Dán tin nhắn SMS, Zalo lạ vào ô dưới đây:</p>", unsafe_allow_html=True)
        with col_act:
            st.components.v1.html(
                f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                  body {{
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    background: transparent;
                  }}
                  .paste-btn {{
                    width: 100%;
                    height: 38px;
                    background-color: #ffffff;
                    color: #1e3a8a;
                    border: 1.5px solid #93c5fd;
                    border-radius: 8px;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    font-size: clamp(12px, 3.2vw, {int(14 * font_mult)}px);
                    font-weight: 700;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 6px;
                    cursor: pointer;
                    transition: all 0.15s ease;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
                  }}
                  .paste-btn:hover {{
                    background-color: #eff6ff;
                    border-color: #2563eb;
                    color: #1d4ed8;
                  }}
                  .paste-btn:active {{
                    background-color: #dbeafe;
                    transform: scale(0.98);
                  }}
                </style>
                </head>
                <body>
                <button class="paste-btn" id="btn-paste" title="Dán nội dung từ bộ nhớ tạm vào ô nhập tin nhắn">
                  📋 Dán tin nhắn
                </button>
                <script>
                  const btn = document.getElementById('btn-paste');
                  btn.addEventListener('click', async () => {{
                    try {{
                      let text = '';
                      if (window.parent && window.parent.navigator && window.parent.navigator.clipboard) {{
                        text = await window.parent.navigator.clipboard.readText();
                      }} else if (navigator.clipboard) {{
                        text = await navigator.clipboard.readText();
                      }}
                      if (!text || !text.trim()) {{
                        btn.innerText = '⚠️ Bộ nhớ tạm trống!';
                        setTimeout(() => {{ btn.innerText = '📋 Dán tin nhắn'; }}, 2200);
                        return;
                      }}
                      const ta = window.parent.document.querySelector('textarea');
                      if (ta) {{
                        ta.focus();
                        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                        setter.call(ta, text.trim());
                        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        ta.blur();
                        btn.innerText = '⚡ Đang kiểm tra...';

                        // Tự động kích hoạt kiểm tra ngay lập tức (1-chạm: Dán là phân tích luôn)
                        setTimeout(() => {{
                          const btnCheck = Array.from(window.parent.document.querySelectorAll('button')).find(b => b.innerText.includes('KIỂM TRA TIN NHẮN NGAY'));
                          if (btnCheck) {{
                            btnCheck.click();
                          }}
                          btn.innerText = '✅ Đã dán & kiểm tra!';
                          setTimeout(() => {{ btn.innerText = '📋 Dán tin nhắn'; }}, 2500);
                        }}, 150);
                      }}
                    }} catch (err) {{
                      btn.innerText = '⚠️ Cần cấp quyền';
                      setTimeout(() => {{ btn.innerText = '📋 Dán tin nhắn'; }}, 2500);
                      alert('Trình duyệt chưa cho phép đọc bộ nhớ tạm tự động. Ông/Bà hãy nhấn giữ vào ô bên dưới rồi chọn \"Dán\" (hoặc bấm phím Ctrl+V / Cmd+V) nhé!');
                    }}
                  }});
                </script>
                </body>
                </html>
                """,
                height=42,
            )

        # Ô nhập tin nhắn to, rộng rãi nhưng tinh gọn padding
        user_input = st.text_area(
            "Nội dung tin nhắn:",
            key="sms_input",
            height=180,
            placeholder="Ví dụ: CUC CSGT THONG BAO: Ban bi phat nguoi 5 trieu, nop phat gap neu khong se bi bat tam giam...",
            label_visibility="collapsed",
        )

        # Nút Kiểm tra chính & Nút Xóa nhanh bổ trợ khi có nội dung
        if has_content:
            btn_col1, btn_col2 = st.columns([3.2, 1.2], gap="small")
            with btn_col1:
                btn_check = st.button("🔍 KIỂM TRA TIN NHẮN NGAY", type="primary", use_container_width=True)
            with btn_col2:
                st.button("🗑️ Xóa tin", key="btn_clear_bottom", on_click=select_preset, args=("clear",), use_container_width=True)
        else:
            btn_check = st.button("🔍 KIỂM TRA TIN NHẮN NGAY", type="primary", use_container_width=True)

        # Cập nhật URL Query Params và trạng thái đánh giá khi người dùng bấm Kiểm tra
        if btn_check:
            clean_text = user_input.strip()
            if clean_text:
                st.session_state["evaluated_text"] = clean_text
                st.query_params["text"] = clean_text
            else:
                st.session_state["evaluated_text"] = ""
                st.query_params.pop("text", None)

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # Khối kịch bản mẫu 1-chạm thiết kế dạng danh sách dọc full-width (Mặc định thu gọn)
        with st.expander("💡 Hoặc bấm vào đây để thử nhanh các kịch bản lừa đảo thực tế", expanded=False):
            st.markdown(f"<p style='font-size: clamp(12px, 2.8vw, {int(15 * font_mult)}px); color: #64748b; margin-bottom: 8px;'>Bấm <b>1 chạm</b> vào kịch bản bên dưới để hệ thống tự động nạp và kiểm tra ngay:</p>", unsafe_allow_html=True)
            
            # Danh sách các nút kịch bản mẫu toàn chiều rộng
            st.button("⚖️ CSGT phạt nguội dọa bắt", key="btn_fear", on_click=select_preset, args=("fear",), use_container_width=True)
            st.button("🚨 Báo người thân tai nạn cấp cứu", key="btn_emergency", on_click=select_preset, args=("emergency",), use_container_width=True)
            st.button("🏛️ Giả VNeID dọa khóa định danh", key="btn_vneid", on_click=select_preset, args=("vneid",), use_container_width=True)
            st.button("🎁 Báo trúng thưởng xe & thuốc bổ", key="btn_gift", on_click=select_preset, args=("gift",), use_container_width=True)
            st.button("💳 Tin nhắn biến động số dư (An toàn)", key="btn_bank", on_click=select_preset, args=("bank",), use_container_width=True)

    with col_right:
        st.markdown(f"<h3 style='font-size: clamp(15px, 1.9vw, {int(19 * font_mult)}px); color: #1e3a8a; margin-bottom: 4px; line-height: 1.35; overflow-wrap: break-word; word-break: normal; text-wrap: balance;'>📊 KẾT QUẢ ĐÁNH GIÁ TỪ TRÍ TUỆ NHÂN TẠO</h3>", unsafe_allow_html=True)

        # Hỗ trợ cả 3 chế độ kích hoạt: Bấm nút Kiểm tra, Bấm 1-chạm kịch bản mẫu, hoặc URL Query Params
        auto_trigger = st.session_state.get("auto_analyze", False)
        if auto_trigger:
            st.session_state["auto_analyze"] = False

        evaluated_text = st.session_state.get("evaluated_text", "").strip()
        should_run_analysis = btn_check or auto_trigger or bool(evaluated_text)

        target_text = user_input.strip() if btn_check else (evaluated_text or user_input.strip())
        input_valid = bool(target_text and len(target_text) >= 10)

        if should_run_analysis and input_valid:
            # Chỉ kích hoạt cuộn mượt trên thiết bị di động sau khi kết quả đã kết xuất, tránh giật màn hình máy tính
            st.components.v1.html(
                """
                <script>
                    setTimeout(function() {
                        if (window.parent && window.parent.innerWidth <= 768) {
                            const target = window.parent.document.getElementById('verdict-anchor');
                            if (target) {
                                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                            }
                        }
                    }, 800);
                </script>
                """,
                height=0,
            )

            # Khối quét AI liên tục 60fps mượt mà, không giật cục (GPU-accelerated Fluid Scanning)
            scan_box = st.empty()
            scan_box.markdown(f"""
            <div class="ai-scan-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #2563eb; animation: aiPulseDot 1.2s ease-in-out infinite;"></span>
                        <span style="font-size: clamp(13px, 2.5vw, {int(15 * font_mult)}px); font-weight: 700; color: #1e40af;">
                            Đang phân tích 15 bẫy tâm lý & Đối soát mô hình {current_model_meta['name']}...
                        </span>
                    </div>
                    <span style="font-size: 11px; font-weight: 700; color: #1d4ed8; background: #dbeafe; padding: 3px 10px; border-radius: 12px;">Đang quét AI</span>
                </div>
                <div class="ai-scan-track">
                    <div class="ai-scan-bar"></div>
                </div>
                <div style="font-size: 12px; color: #64748b; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 4px;">
                    <span>⏳ Bóc tách đặc trưng đe dọa, viện phí, VNeID & liên kết</span>
                    <span>🔬 Không gian vector: {current_model_meta['dims']:,} chiều</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Tính toán suy luận học máy song song
            proba, is_scam, aux_dict, model_info = predict_text(target_text, selected_model_key, engines)
            category = diagnose_scam_category(target_text)

            # Độ trễ tự nhiên (0.65s) để mắt người dùng cảm nhận trọn vẹn chu trình quét AI chuyển động 60fps
            time.sleep(0.65)

            # Cập nhật huy hiệu hoàn tất tinh tế, giữ nguyên bố cục không gây giật
            scan_box.markdown(f"""
            <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 10px; padding: 9px 14px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 6px rgba(22, 101, 52, 0.05); animation: smoothFadeInUp 0.3s ease-out;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #15803d; font-size: 14px;">✅</span>
                    <span style="font-size: 13px; font-weight: 700; color: #166534;">
                        Hoàn tất đối soát qua {current_model_meta['name']} (15 đặc trưng • {current_model_meta['dims']:,} chiều)
                    </span>
                </div>
                <span style="font-size: 11px; font-weight: 700; color: #15803d; background: #dcfce7; padding: 2px 8px; border-radius: 10px;">Hoàn tất</span>
            </div>
            """, unsafe_allow_html=True)

            # 1. Thước đo rủi ro (Risk Meter)
            render_risk_meter(proba, font_multiplier=font_mult)

            # 2. Bôi đỏ từ khóa cảnh báo (Pre-compiled Keyword Highlighter)
            st.markdown(f"<div style='font-size: clamp(15px, 2.5vw, {int(18 * font_mult)}px); font-weight: 700; color: #1e293b; margin-top: 12px; margin-bottom: 6px;'>🔍 Phân tích các từ khóa nghi vấn trong tin nhắn:</div>", unsafe_allow_html=True)
            highlighted_html = highlight_text_html(target_text, font_multiplier=font_mult)
            st.markdown(highlighted_html, unsafe_allow_html=True)

            # 3. Lời khuyên an toàn chuyên biệt + Nút gọi khẩn cấp 1-chạm (Sát sao nội dung tin nhắn)
            render_safety_advisor(
                category=category,
                is_scam=is_scam,
                font_multiplier=font_mult,
                user_text=target_text,
                aux_dict=aux_dict,
            )

            # 4. Bảng Thanh tra Kỹ thuật dành cho Hội đồng Chấm thi CS114 (Academic Inspector Panel)
            with st.expander("🛠️ Xem chi tiết kỹ thuật mô hình", expanded=academic_mode):
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
                """)

                st.markdown("#### 2. Bảng Phân tích 15 Đặc trưng Tâm lý Real-time")
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

        elif should_run_analysis and not target_text:
            st.warning("⚠️ Ông/Bà vui lòng dán hoặc nhập nội dung tin nhắn vào ô bên trái trước khi bấm kiểm tra nhé!")
        elif should_run_analysis and len(target_text) < 10:
            st.warning("⚠️ Tin nhắn quá ngắn để phân tích chính xác các thủ đoạn thao túng tâm lý. Ông/Bà vui lòng nhập đầy đủ câu văn của tin nhắn nhé!")
        else:
            # Thay thế ảnh cũ bằng ảnh Cover chính thức của dự án CS114 (docs/cover.png)
            candidates = [
                PROJECT_ROOT.parent.parent / "docs" / "cover.png",
                PROJECT_ROOT.parent / "docs" / "cover.png",
                PROJECT_ROOT / "docs" / "cover.png",
            ]
            cover_img_file = next((p for p in candidates if p.exists()), None)

            if cover_img_file and cover_img_file.exists():
                st.image(
                    str(cover_img_file),
                    caption="Hệ thống Nghiên cứu và Xây dựng Mô hình Phát hiện Tin nhắn Lừa đảo Người cao tuổi (CS114)",
                    use_container_width=True,
                )

            st.markdown(f"""
            <div style="
                background: #f8fafc;
                border: 1.5px solid #e2e8f0;
                border-radius: 12px;
                padding: clamp(12px, 3vw, 16px);
                margin-top: 10px;
                margin-bottom: 24px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            ">
                <h4 style="font-size: clamp(15px, 2.0vw, {int(18 * font_mult)}px); font-weight: 800; color: #1e3a8a; margin-bottom: 8px; line-height: 1.35; overflow-wrap: break-word; text-wrap: balance;">
                    🛡️ HỆ THỐNG SẴN SÀNG BẢO VỆ ÔNG/BÀ
                </h4>
                <p style="font-size: clamp(13px, 3.2vw, {int(17 * font_mult)}px); line-height: 1.55; color: #334155; margin-bottom: 10px;">
                    Khi nhận được tin nhắn lạ yêu cầu chuyển tiền, đe dọa phạt nguội, hoặc báo người thân cấp cứu:
                </p>
                <div style="background: #ffffff; padding: 10px 14px; border-radius: 8px; border-left: 4px solid #0284c7; font-size: clamp(13px, 3vw, {int(16 * font_mult)}px); line-height: 1.6; color: #1e293b;">
                    ✅ <b>Cách 1:</b> Dán tin nhắn vào ô bên trái rồi bấm nút xanh <b>"KIỂM TRA TIN NHẮN NGAY"</b>.<br>
                    ✅ <b>Cách 2:</b> Bấm nhanh vào 1 trong các kịch bản mẫu màu xanh nhạt để xem thử ngay.<br>
                    ✅ <b>Cách 3:</b> Bấm gọi trực tiếp tổng đài <b>156</b> hoặc <b>113</b> nếu cảm thấy bất an.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- Chân Trang Đồ Án (4 Trụ Cột Tin Cậy - Trust Pillars & Thông Tin Dự Án) ---
    st.markdown(f"""
    <div class="project-portal-footer">
        <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 12px; font-weight: 700; font-size: clamp(12px, 1.4vw, {int(14 * font_mult)}px); color: #1e40af; margin-bottom: 3px;">
            <span>🛡️ 100% Zero Synthetic Text</span>
            <span>•</span>
            <span>🧠 4 Mô hình Học Máy</span>
            <span>•</span>
            <span>🔒 Bảo mật thông tin</span>
            <span>•</span>
            <span>👥 Vì Người Cao Tuổi</span>
        </div>
        <div style="font-size: clamp(11px, 1.3vw, {int(13 * font_mult)}px); color: #475569; font-weight: 500;">
            <b>CS114</b> — Trường ĐH Công nghệ Thông tin, ĐHQG-HCM <br/> Nhóm 10: <b>Đặng Chí Thanh</b> (25730067) • <b>Bùi Thị Mỷ Cẩm</b> (25730006) • <b>Hoàng Cao Sơn</b> (25730061) | GVHD: <b>ThS. Cáp Phạm Đình Thăng</b>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
