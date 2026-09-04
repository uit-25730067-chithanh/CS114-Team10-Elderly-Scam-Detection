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

## Evaluation Checklist

Trước khi báo cáo, đảm bảo mỗi model có đủ:
- [ ] Classification report: Precision, Recall, F1 (class 0 và class 1)
- [ ] Confusion Matrix (normalized + raw)
- [ ] ROC-AUC Score + ROC Curve
- [ ] Learning Curve (Train vs Val — 10 points)
- [ ] Thời gian training ghi lại
