# Phase 08 — Demo UI (Streamlit)

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 07 — Evaluation & XAI](./phase-07-evaluation-xai.md)  
**Next phase:** [Phase 09 — Report & PPT](./phase-09-report-ppt.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Sơn** |
| Priority | P2 |
| Status | `passed` ✅ |
| Review | ✅ Passed |
| Estimated effort | 4–6h |


| Sprint | Sprint 2–3 Fast-Track (15/09 shell → 20/09 integrated) |

## Context

Web app demo bằng Streamlit giả lập khung chat kiểm tra tin nhắn lừa đảo. Hiển thị mức độ nguy cơ, bôi đỏ từ khóa nhạy cảm, phân loại bẫy tâm lý, và đưa ra lời khuyên an toàn.

## Requirements

- Chạy trên localhost (`streamlit run app.py`)
- Giao diện 2 cột: input bên trái, kết quả bên phải
- Tích hợp model đã train (best model)
- Hiển thị: thanh nguy cơ, từ khóa bôi đỏ, loại bẫy tâm lý, lời khuyên

> [!IMPORTANT]
> **Phụ thuộc Phase 06:** Phase 08 yêu cầu Cẩm xuất đúng format bundle theo [Interface Contract trong phase-06](./phase-06-model-svm-phobert.md).  
> Load model bằng: `bundle = joblib.load('models/best_model_bundle.pkl')` — **không dùng pickle, không load vectorizer tách rời**.  
> Sơn cần xác nhận với Cẩm về path `models/best_model_bundle.pkl` trước khi bắt đầu Step 6 (Integration).

## Implementation Steps

### Step 1 — App Structure

```
draft/scam-detection/demo/
├── app.py                    ← Main Streamlit app
├── components/
│   ├── risk_meter.py         ← Thanh đo nguy cơ
│   ├── keyword_highlighter.py ← Bôi đỏ từ khóa
│   └── safety_advisor.py     ← Lời khuyên an toàn
└── assets/
    └── logo.png              ← (optional)
```

### Step 2 — Main App Layout

```python
import streamlit as st

st.set_page_config(page_title="🛡️ Kiểm tra Tin nhắn Lừa đảo", layout="wide")

st.title("🛡️ Hệ thống Phát hiện Tin nhắn Lừa đảo")
st.markdown("*Bảo vệ Người cao tuổi khỏi các chiêu trò thao túng tâm lý*")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📩 Nhập tin nhắn")
    user_text = st.text_area("Dán tin nhắn SMS / Zalo / Telegram:", height=200)
    check_btn = st.button("🔍 Kiểm tra ngay", type="primary")

with col2:
    st.header("📊 Kết quả phân tích")
    if check_btn and user_text:
        # 1. Preprocess
        # 2. Predict
        # 3. Display results
        pass
```

### Step 3 — Risk Meter Component

```python
def display_risk_meter(probability: float):
    """Hiển thị thanh đo mức độ nguy cơ."""
    if probability < 0.3:
        color, label = "green", "🟢 An toàn"
    elif probability < 0.7:
        color, label = "orange", "🟡 Nghi vấn"
    else:
        color, label = "red", "🔴 CẢNH BÁO LỪA ĐẢO"
    
    st.markdown(f"### {label}")
    st.progress(probability)
    st.metric("Xác suất lừa đảo", f"{probability:.1%}")
```

### Step 4 — Keyword Highlighter

```python
def highlight_keywords(text: str, keywords: list) -> str:
    """Bôi đỏ các từ khóa cảnh báo trong text."""
    for kw in keywords:
        text = text.replace(kw, f'<span style="color:red;font-weight:bold">{kw}</span>')
    return text
```

### Step 5 — Scam Category Explanation

```python
SCAM_EXPLANATIONS = {
    "fear_authority": {
        "name": "🚔 Đe dọa / Giả danh Quyền lực",
        "description": "Kẻ lừa đảo giả danh Công an, Viện kiểm sát, Tòa án để đe dọa.",
        "advice": "⚠️ Cơ quan chức năng KHÔNG BAO GIỜ yêu cầu chuyển tiền qua điện thoại.",
    },
    "family_emergency": {
        "name": "🏥 Thúc ép Khẩn cấp Gia đình",
        "description": "Giả báo người thân bị tai nạn, cần chuyển viện phí gấp.",
        "advice": "⚠️ Hãy GỌI LẠI trực tiếp cho con/cháu để xác minh trước khi làm gì.",
    },
    "health_gift": {
        "name": "🎁 Dụ dỗ Sức khỏe / Tri ân",
        "description": "Mời nhận thuốc miễn phí, quà tri ân, trúng thưởng.",
        "advice": "⚠️ Không có chương trình tri ân nào yêu cầu cung cấp thông tin ngân hàng.",
    },
    "public_service": {
        "name": "🏛️ Giả mạo Dịch vụ Công",
        "description": "Hướng dẫn cập nhật VNeID, nâng cấp SIM, nhận trợ cấp.",
        "advice": "⚠️ Chỉ thực hiện thủ tục qua cổng dịch vụ công CHÍNH THỨC hoặc đến trực tiếp.",
    },
}
```

### Step 6 — Integration

Load best model + TF-IDF vectorizer → preprocess user input → predict → display results.

## Checklist

- [x] `streamlit run demo/app.py` chạy không lỗi
- [x] Giao diện 2 cột hoạt động (Cột trái: Nhập tin nhắn & Presets; Cột phải: Kết quả AI & Phân tích)
- [x] Model loaded và predict đúng (Đa mô hình: XGBoost Mặc định F1=0.9535 + Linear SVM + Random Forest + Naive Bayes)
- [x] Thanh đo nguy cơ (xanh/vàng/đỏ) hiển thị với tỷ lệ phần trăm trực quan
- [x] Từ khóa cảnh báo bôi đỏ/vàng theo nhóm bẫy tâm lý (cả có dấu và không dấu)
- [x] Phân loại bẫy tâm lý hiển thị (4 nhóm: fear_authority, family_emergency, public_service, health_gift)
- [x] Lời khuyên an toàn chuyên sâu hiển thị + Hộp quy tắc "3 KHÔNG & 1 GỌI" và Hotline 156
- [x] Tùy biến cỡ chữ người cao tuổi (100%, 125%, 150%) giúp mắt yếu dễ đọc
- [x] Dán tin nhắn tự động phân tích qua Web Clipboard API và lưu trạng thái qua URL query params (`?text=...`)
- [x] Screenshots nghiệm thu (4 ảnh chuẩn 300 DPI lưu tại `reports/figures/demo_*.png`)
- [x] Bộ kiểm thử tự động Playwright E2E (`run_full_web_test_suite.py`) đạt 16/16 ca PASS 100%

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| App runs | `python -m streamlit run demo/app.py` passes compilation & execution test |
| Prediction works | Input scam text → correct detection (>60% to 100% probability); Normal message -> Safe |
| UI complete | Split-view + Risk meter + keywords + category + advice + Elderly font scaling |
| Model Catalog | 4 mô hình (XGBoost default F1=0.9535, Linear SVM F1=0.9474, RF F1=0.9425, NB F1=0.8864) |
| Screenshots | 4 ảnh chụp 300 DPI (`demo_01` → `demo_04`) lưu tại `reports/figures/` |
| Automated E2E Tests | 16/16 test cases Playwright PASS trên Google Chrome + 70/70 pytest PASS |

## Evidence Section *(điền sau khi làm)*

```
[STREAMLIT DEMO & MULTI-MODEL INTEGRATION VALIDATION — 2026-09-20]
- App path: draft/scam-detection/demo/app.py
- Components:
  + demo/components/risk_meter.py: 3-level card (🟢 An toàn <30%, 🟡 Nghi vấn 30-50%, 🔴 Cảnh báo lừa đảo >=50%)
  + demo/components/keyword_highlighter.py: Multi-category precompiled regex highlighter with HTML escaping
  + demo/components/safety_advisor.py: 4 psychological traps diagnosis + "3 KHÔNG & 1 GỌI" box + Hotline 1-touch 156 & 113
- Model Catalog (4 models supported):
  + XGBoost (Default): F1 = 0.9535, Recall = 97.62%, ROC-AUC = 0.9984
  + Linear SVM (Calibrated): F1 = 0.9474, Recall = 96.43%, ROC-AUC = 0.9986
  + Random Forest: F1 = 0.9425, Recall = 97.62%, ROC-AUC = 0.9976
  + Naive Bayes: F1 = 0.8864, Recall = 92.86%, ROC-AUC = 0.9911
- Real-time Feature Inspector: Trích xuất 15 đặc trưng phụ (URL, SĐT, tiền tệ, từ hối thúc, mạo danh...)
- Preset Test Results (XGBoost Default):
  + Preset 0 (Đe dọa quyền lực - Công an bắt giam): proba = 98.42% -> 🔴 CẢNH BÁO LỪA ĐẢO (fear_authority)
  + Preset 1 (Cấp cứu gia đình - Chuyển viện phí): proba = 97.80% -> 🔴 CẢNH BÁO LỪA ĐẢO (family_emergency)
  + Preset 2 (Dịch vụ công - VNeID khóa mã): proba = 99.15% -> 🔴 CẢNH BÁO LỪA ĐẢO (public_service)
  + Preset 3 (Tri ân trúng thưởng - Xe SH): proba = 98.67% -> 🔴 CẢNH BÁO LỪA ĐẢO (health_gift)
  + Preset 4 (Biến động số dư VCB an toàn): proba = 1.25% -> 🟢 AN TOÀN (none)
- Test Suite Verification:
  + Pytest: 70/70 unit tests PASS (11.37s)
  + Playwright E2E: 16/16 test cases PASS (Desktop layout, font scale 150%, input validations, 4 models switch, mobile responsive)
- Artifact Figures: 4 screenshots (300 DPI) committed to draft/scam-detection/reports/figures/
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **Hoàn thành xuất sắc toàn diện Web App Streamlit phát hiện tin nhắn lừa đảo nhắm vào người cao tuổi:**
> - Thiết kế giao diện theo phong cách Split-View Workbench tối ưu trợ năng cho người cao tuổi: cỡ chữ tùy biến 100% – 125% – 150%, tương phản cao, hotline gọi khẩn cấp 1-chạm (156 và 113), tự động cuộn trang sau phân tích.
> - Tích hợp bộ điều phối 4 mô hình học máy với XGBoost (F1=0.9535, Recall=97.62%) làm mô hình mặc định khuyến nghị, hỗ trợ chuyển đổi linh hoạt sang Linear SVM, Random Forest và Naive Bayes.
> - Bổ sung tính năng Dán tin nhắn tự động từ Clipboard qua Web Clipboard API và lưu trữ trạng thái kiểm tra qua URL query params (`?text=...`).
> - Trích xuất 15 đặc trưng tâm lý và ngôn ngữ thời gian thực trong mục chi tiết kỹ thuật cho Giảng viên.
> - Kiểm thử tự động toàn diện qua Playwright (16 ca E2E pass 100%) và xuất 4 ảnh nghiệm thu chất lượng cao chuẩn 300 DPI.


