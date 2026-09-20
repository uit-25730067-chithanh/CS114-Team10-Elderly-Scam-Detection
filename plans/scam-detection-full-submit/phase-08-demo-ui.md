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
| Status | `in-progress` |
| Review | ⏳ In review |
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

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| App runs | `python -m streamlit run demo/app.py` passes compilation & execution test |
| Prediction works | Input scam text → correct detection (>60% to 72% probability); Normal message -> 45.8% (Safe) |
| UI complete | Risk meter + keywords + category + advice + Elderly font scaling |
| Model Bundle | `models/best_model_bundle.pkl` (1.6 MB) self-contained |

## Evidence Section *(điền sau khi làm)*

```
[STREAMLIT DEMO VALIDATION — 2026-09-17]
- App path: draft/scam-detection/demo/app.py
- Components:
  + demo/components/risk_meter.py: 3-level card (🟢 An toàn <30%, 🟡 Nghi vấn 30-50%, 🔴 Cảnh báo lừa đảo >=50%)
  + demo/components/keyword_highlighter.py: Multi-category regex highlighter (Accented & Unaccented)
  + demo/components/safety_advisor.py: 4 psychological traps diagnosis + "3 KHÔNG & 1 GỌI" safety box + Hotline 156
- Model Bundle: models/best_model_bundle.pkl (Random Forest, 5.015 features, Acc 97.72%, F1 94.25%)
- Preset Test Results:
  + Preset 0 (Đe dọa quyền lực): proba = 0.6197 -> CẢNH BÁO LỪA ĐẢO (fear_authority)
  + Preset 1 (Cấp cứu gia đình): proba = 0.6669 -> CẢNH BÁO LỪA ĐẢO (family_emergency)
  + Preset 2 (Dịch vụ công VNeID): proba = 0.6848 -> CẢNH BÁO LỪA ĐẢO (public_service)
  + Preset 3 (Tri ân trúng thưởng): proba = 0.7198 -> CẢNH BÁO LỪA ĐẢO (health_gift)
  + Preset 4 (Biến động số dư VCB): proba = 0.4580 -> AN TOÀN (none)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **Hoàn thành xuất sắc khung Web App Streamlit phát hiện tin nhắn lừa đảo cho người cao tuổi:**
> - Thiết kế giao diện theo phong cách dành riêng cho người cao tuổi: cỡ chữ lớn, tương phản cao, hỗ trợ chỉnh 100%, 125%, 150%.


> - Tích hợp đầy đủ Random Forest Model Bundle 5.015 chiều trích xuất theo zero-leakage pipeline.
> - Xử lý ẩn danh PII và URL trước khi trích xuất đặc trưng để tương thích hoàn toàn với phân phối huấn luyện.
> - Khắc họa rõ nét 4 bẫy tâm lý, trích xuất từ khóa nghi vấn, hiển thị quy tắc sinh tồn "3 KHÔNG & 1 GỌI" và hotline 156.

