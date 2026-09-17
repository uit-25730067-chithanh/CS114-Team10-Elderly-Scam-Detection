# Code Standards — CS114 Scam Detection Project

## Quy ước đặt tên

- **Files Python**: `snake_case` (`text_cleaner.py`, `random_forest_model.py`)
- **Directories**: `kebab-case` (`scam-detection/`, `data-processed/`)
- **Functions/Variables**: `snake_case` (`clean_text()`, `X_train`, `y_test`)
- **Classes**: `PascalCase` (`ScamDetector`, `TextPreprocessor`)
- **Constants**: `UPPER_SNAKE_CASE` (`RANDOM_STATE = 42`, `TEST_SIZE = 0.2`)

## Reproducibility

Luôn set random seed ở đầu mỗi script/notebook:

```python
from src.utils.helpers import set_seeds, RANDOM_STATE
set_seeds(RANDOM_STATE)  # sets numpy + random
```

## Cấu trúc Notebook

Mỗi notebook tuân theo cấu trúc:

```
# [Tiêu đề Notebook]
## 0. Imports & Config
## 1. Load Data
## 2. [Nội dung chính]
## 3. Save Artifacts
## 4. Kết luận / Observations
```

## Phân công Notebook (tránh conflict)

| Notebook | Người phụ trách | Mô tả |
|----------|----------------|-------|
| `01_preprocessing.ipynb` | **Thanh** | Text cleaning + tokenization |
| `02_eda.ipynb` | **Thanh** | EDA + Feature Engineering |
| `03_model_naive_bayes.ipynb` | **Cẩm** | Naive Bayes baseline |
| `04_model_random_forest.ipynb` | **Sơn** | Random Forest |
| `04_model_xgboost.ipynb` | **Cẩm** | XGBoost |
| `05_model_svm.ipynb` | **Cẩm** | SVM Linear |
| `06_evaluation_xai.ipynb` | **Thanh** | Evaluation tổng hợp + XAI |

> Mỗi người làm trên notebook của mình — không sửa file người khác khi chưa discuss.

## Git Conventions

- Commit message: `feat(phase02): vietnamese preprocessing pipeline`
- Format: `type(scope): message` — types: `feat`, `fix`, `data`, `model`, `report`
- **Không commit** `data/raw/dataset.csv` nếu file > 10MB
- **Không commit** `.venv/` — dùng `requirements.txt`
- **Không commit** model `.pkl` nếu > 50MB — dùng `.gitignore`

## Vietnamese NLP Conventions

- **Tokenizer**: dùng `pyvi.ViTokenizer` (primary), `underthesea` (fallback)
- **Word boundary**: compound words dùng underscore: `công_an`, `tài_khoản`
- **Encoding**: luôn đọc/ghi CSV với `encoding='utf-8-sig'`
- **Unicode**: luôn normalize NFC trước khi xử lý

## Model Bundle Save/Load Convention (BẮT BUỘC)

Để tránh lỗi không khớp feature space (5.015 chiều) hoặc thiếu vectorizer/scaler khi tích hợp Demo UI (`demo/app.py`), **tuyệt đối không lưu model, vectorizer và scaler riêng lẻ**. Luôn đóng gói (bundle) vào một dictionary chuẩn:

```python
import joblib
import sklearn
from datetime import datetime

# 1. Lưu Bundle (Áp dụng khi train xong mô hình chính thức)
bundle = {
    'model': model,                 # scikit-learn / xgboost classifier
    'vectorizer': tfidf_vectorizer, # TfidfVectorizer đã fit trên train data (5.000 n-grams)
    'aux_scaler': aux_scaler,       # StandardScaler đã fit trên 15 đặc trưng phụ
    'feature_names': feature_names, # Danh sách 5.015 tên đặc trưng
    'model_name': 'XGBoost',        # Tên hiển thị trên UI
    'threshold': 0.5,                # Ngưỡng phân loại (mặc định 0.5)
    'sklearn_version': sklearn.__version__,
    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
}
joblib.dump(bundle, 'models/best_model_bundle.pkl')

# 2. Load Bundle (Áp dụng trong Demo UI / Evaluation)
bundle = joblib.load('models/best_model_bundle.pkl')
clf = bundle['model']
tfidf = bundle['vectorizer']
scaler = bundle.get('aux_scaler')

# Inference chuẩn 5.015 chiều (xem chi tiết tại draft/scam-detection/demo/README.md)
```

## Evaluation Checklist

Trước khi báo cáo, đảm bảo mỗi model có đủ:
- [ ] Classification report: Precision, Recall, F1 (class 0 và class 1)
- [ ] Confusion Matrix (normalized + raw)
- [ ] ROC-AUC Score + ROC Curve
- [ ] Learning Curve (Train vs Val — 10 points)
- [ ] Thời gian training ghi lại
