# Demo UI — Streamlit Application & Integration Contract

> Hướng dẫn tích hợp mô hình phát hiện lừa đảo vào giao diện Web Demo Streamlit (`draft/scam-detection/demo/`).

---

## 1. Kiến trúc luồng Demo (Data Flow)

```
Người dùng nhập tin nhắn (raw text)
  │
  ▼
[Tiền xử lý văn bản] (text_cleaner.py + tokenizer.py)
  │
  ▼
[Transform vector] (vectorizer đã fit trong bundle)
  │
  ▼
[Inference] (clf.predict_proba)
  │
  ├─► Xác suất lừa đảo (% Risk) ──► Risk Meter Component
  ├─► Nhãn dự đoán (0: Bình thường / 1: Lừa đảo) ──► Cảnh báo
  └─► Trích xuất từ khóa bẫy tâm lý ──► Keyword Highlighter + Lời khuyên an toàn
```

---

## 2. Integration Contract (Hợp đồng giao tiếp giữa Model & UI)

### 2.1 File Bundle quy ước
- **Đường dẫn mặc định:** `models/best_model_bundle.pkl` (hoặc dropdown chọn model từ `models/*_bundle.pkl`).
- **Cấu trúc Bundle Dictionary:**
```python
{
    "model": classifier,            # sklearn / xgboost model instance (đã train trên 5.015 features)
    "vectorizer": tfidf_vectorizer, # TfidfVectorizer instance đã fit (5.000 n-grams)
    "aux_scaler": auxiliary_scaler, # StandardScaler instance đã fit (15 đặc trưng phụ)
    "feature_names": feature_names, # List 5.015 tên đặc trưng
    "model_name": "XGBoost",        # str: Tên hiển thị trên giao diện
    "threshold": 0.5                # float: Ngưỡng cảnh báo (mặc định 0.5)
}
```

### 2.2 Hàm Inference chuẩn cho UI
Trong `demo/app.py` hoặc module hỗ trợ:

```python
import os
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix

from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.tokenizer import segment_vietnamese
from src.preprocessing.pipeline import extract_auxiliary_features
from src.feature_engineering_config import AUXILIARY_FEATURE_NAMES

def load_bundle(model_path="models/best_model_bundle.pkl"):
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

def predict_message(raw_text: str, bundle: dict) -> dict:
    """
    Hàm chuẩn đầu ra cho giao diện Streamlit (hỗ trợ không gian 5.015 đặc trưng)
    """
    if bundle is None:
        # Fallback Mock Mode nếu chưa có file model thực tế
        return {
            "is_scam": False,
            "risk_score": 0.0,
            "label": 0,
            "tokenized_text": "",
            "highlight_keywords": [],
            "message": "Model chưa sẵn sàng (Chế độ mô phỏng giao diện)"
        }

    # 1. Trích xuất đặc trưng phụ (15 đặc trưng) & chuẩn hóa qua aux_scaler
    aux_dict = extract_auxiliary_features(raw_text)
    aux_df = pd.DataFrame([aux_dict])[AUXILIARY_FEATURE_NAMES]
    if "aux_scaler" in bundle:
        aux_scaled = bundle["aux_scaler"].transform(aux_df)
    else:
        aux_scaled = aux_df.values

    # 2. Tiền xử lý & tách từ tiếng Việt
    cleaned = clean_text(raw_text)
    tokenized = segment_vietnamese(cleaned)

    # 3. Vector hóa TF-IDF (5.000 chiều)
    tfidf_vec = bundle["vectorizer"].transform([tokenized])

    # 4. Hợp nhất thành vector 5.015 chiều
    full_vec = hstack([tfidf_vec, csr_matrix(aux_scaled)])

    # 5. Dự đoán xác suất
    clf = bundle["model"]
    if hasattr(clf, "predict_proba"):
        proba = float(clf.predict_proba(full_vec)[0][1])
    else:
        decision = clf.decision_function(full_vec)[0]
        proba = float(1.0 / (1.0 + np.exp(-decision)))

    threshold = bundle.get("threshold", 0.5)
    is_scam = bool(proba >= threshold)

    # Trích xuất từ khóa bẫy tâm lý cơ bản (phục vụ hiển thị UI)
    risk_keywords = [
        "chuyển khoản", "mã otp", "công an", "viện kiểm sát", 
        "trúng thưởng", "bắt giam", "phạt nguội", "khóa tài khoản",
        "vneid", "bảo hiểm", "cấp cứu", "bệnh viện"
    ]
    highlight_keywords = [kw for kw in risk_keywords if kw in raw_text.lower()]

    return {
        "is_scam": is_scam,
        "risk_score": proba,
        "label": 1 if is_scam else 0,
        "tokenized_text": tokenized,
        "highlight_keywords": highlight_keywords,
        "message": "Cảnh báo: Phát hiện dấu hiệu lừa đảo!" if is_scam else "Tin nhắn có mức độ an toàn cao."
    }
```

---

## 3. Mock Model (Dành riêng cho Sơn khi dựng khung UI sớm)

Trong Sprint 2 (15/09 – 17/09), khi Thanh và Cẩm chưa export xong `best_model_bundle.pkl`, Sơn có thể dựng giao diện và test tương tác bằng **Mock Bundle**:

```python
# Tạo mock bundle tạm để test UI
class MockModel:
    def predict_proba(self, X):
        return [[0.15, 0.85]]

class MockVectorizer:
    def transform(self, texts):
        return None

mock_bundle = {
    "model": MockModel(),
    "vectorizer": MockVectorizer(),
    "model_name": "Mock Detector (Test UI)",
    "threshold": 0.5
}
```

---

## 4. Hướng dẫn chạy Demo & Khởi chạy Nhanh

### 4.1. Khởi chạy trên Web Browser
```bash
# Từ thư mục gốc repo hoặc draft/scam-detection/
streamlit run draft/scam-detection/demo/app.py
```
Hoặc trên Windows: Click đúp tệp `Chay_Demo.bat` tại thư mục gốc để mở ứng dụng ngay trên trình duyệt mặc định.

### 4.2. Các tính năng nổi bật trong bản chính thức (PR #21)
- **Model Catalog đa mô hình:** Cho phép chọn giữa 4 mô hình học máy:
  1. `XGBoost (Mặc định)`: F1 = 0.9535, Recall = 97.62%, ROC-AUC = 0.9984
  2. `Linear SVM (Calibrated)`: F1 = 0.9474, Recall = 96.43%, ROC-AUC = 0.9986
  3. `Random Forest`: F1 = 0.9425, Recall = 97.62%, ROC-AUC = 0.9976
  4. `Naive Bayes`: F1 = 0.8864, Recall = 92.86%, ROC-AUC = 0.9911
- **Bộ phóng đại cỡ chữ (Elderly Accessibility):** Chuyển đổi 100% (Mặc định) → 125% (Rõ ràng) → 150% (Rất lớn) với cỡ chữ clamp co dãn tối ưu.
- **Dán tin nhắn một-chạm:** Tự động đọc và dán nội dung từ clipboard qua Web Clipboard API và kích hoạt phân tích ngay lập tức.
- **Bảo lưu trạng thái URL:** Tin nhắn và kết quả kiểm tra được tự động lưu vào query parameters (`?text=...`) tránh mất dữ liệu khi refresh.
- **Hotline khẩn cấp 1-chạm:** Nút gọi khẩn cấp `tel:156` (Cục ATTT) và `tel:113` (Công an) tích hợp trực tiếp cho smartphone.

### 4.3. Bộ kiểm thử tự động Playwright E2E
```bash
# Chạy bộ test tự động trên Google Chrome (16 ca kiểm thử giao diện & chức năng)
python3 draft/scam-detection/tests/run_full_web_test_suite.py

# Chạy demo tự động duyệt kịch bản thực tế
python3 draft/scam-detection/tests/run_live_browser_demo.py
```

