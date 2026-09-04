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
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 4–6h |
| Sprint | Sprint 3–4 |

## Context

Web app demo bằng Streamlit giả lập khung chat kiểm tra tin nhắn lừa đảo. Hiển thị mức độ nguy cơ, bôi đỏ từ khóa nhạy cảm, phân loại bẫy tâm lý, và đưa ra lời khuyên an toàn.

## Requirements

- Chạy trên localhost (`streamlit run app.py`)
- Giao diện 2 cột: input bên trái, kết quả bên phải
- Tích hợp model đã train (best model)
- Hiển thị: thanh nguy cơ, từ khóa bôi đỏ, loại bẫy tâm lý, lời khuyên

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

- [ ] `streamlit run demo/app.py` chạy không lỗi
- [ ] Giao diện 2 cột hoạt động
- [ ] Model loaded và predict đúng
- [ ] Thanh đo nguy cơ (xanh/vàng/đỏ) hiển thị
- [ ] Từ khóa cảnh báo bôi đỏ
- [ ] Phân loại bẫy tâm lý hiển thị
- [ ] Lời khuyên an toàn hiển thị
- [ ] Screenshots chụp cho báo cáo

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| App runs | `streamlit run demo/app.py` opens in browser |
| Prediction works | Input scam text → correct detection |
| UI complete | Risk meter + keywords + category + advice |
| Screenshots | ≥3 screenshots in reports/figures/ |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add demo/ reports/figures/demo_*.png
git commit -m "feat(phase08): Streamlit demo app with risk meter, keyword highlight, scam category"
```
