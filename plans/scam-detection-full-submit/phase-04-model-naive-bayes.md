# Phase 04 — Modeling — Naive Bayes Baseline

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 03 — EDA & Feature Engineering](./phase-03-eda-feature-engineering.md)  
**Next phase:** [Phase 05 — Modeling — Random Forest & XGBoost](./phase-05-model-rf-xgboost.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Cẩm** |
| Priority | P1 |
| Status | `done` ✅ |
| Review | ✅ Hoàn thành — xem Evidence Section |
| Estimated effort | 2–3h |
| Sprint | Sprint 2 Fast-Track (15/09 – 16/09/2026) |

## Context

Multinomial Naive Bayes là baseline model cho bài toán text classification. Đơn giản, nhanh, dễ giải thích — làm chuẩn so sánh cho các model phức tạp hơn.

## Implementation Steps

### Step 1 — Nạp Feature Matrices Từ Phase 03 (KHÔNG tự split lại)

> ⚠️ **BẮT BUỘC:** Dùng lại `X_train.pkl` / `X_test.pkl` từ Phase 03. TUYỆT ĐỐI KHÔNG gọi `train_test_split` hay `TfidfVectorizer.fit_transform` lại — sẽ tạo split khác và phá vỡ zero-leakage protocol.

```python
import joblib
import numpy as np
from pathlib import Path

DATA_DIR = Path("data/processed")

# Nạp feature matrices (sparse CSR) và labels
X_train = joblib.load(DATA_DIR / "X_train.pkl")   # shape (1754, 5015)
X_test  = joblib.load(DATA_DIR / "X_test.pkl")    # shape (439, 5015)
y_train = joblib.load(DATA_DIR / "y_train.pkl")   # 336 scam / 1418 normal
y_test  = joblib.load(DATA_DIR / "y_test.pkl")    # 84 scam / 355 normal

print(f"X_train: {X_train.shape}, X_test: {X_test.shape}")
# → X_train: (1754, 5015), X_test: (439, 5015)

# Nếu cần validation set (15% của train), tạo từ X_train:
from sklearn.model_selection import train_test_split
from src.utils import RANDOM_STATE

X_tr, X_val, y_tr, y_val = train_test_split(
    X_train, y_train, test_size=0.15,
    random_state=RANDOM_STATE, stratify=y_train
)
```


### Step 2 — Train Naive Bayes

```python
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

nb_model = MultinomialNB(alpha=1.0)
nb_model.fit(X_tr, y_tr)  # train trên 85% của X_train (không dùng X_test)

# Evaluate trên validation set
y_val_pred = nb_model.predict(X_val)
print(classification_report(y_val, y_val_pred, target_names=['Bình thường', 'Lừa đảo']))
```

### Step 3 — Hyperparameter Tuning (alpha)

```python
from sklearn.model_selection import GridSearchCV

param_grid = {'alpha': [0.01, 0.1, 0.5, 1.0, 2.0, 5.0]}
grid_search = GridSearchCV(
    MultinomialNB(), param_grid,
    cv=5, scoring='f1', n_jobs=-1
)
grid_search.fit(X_train, y_train)
print(f"Best alpha: {grid_search.best_params_}")
print(f"Best F1: {grid_search.best_score_:.4f}")
```

### Step 4 — Cross-Validation (Overfitting Check)

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    nb_model, X_train, y_train,
    cv=5, scoring='f1',
    train_sizes=np.linspace(0.1, 1.0, 10),
    random_state=RANDOM_STATE
)
# Plot learning curve → reports/figures/nb_learning_curve.png
```

### Step 5 — Save Model & Metrics

```python
import joblib

joblib.dump(nb_model, "models/naive_bayes.pkl")
# Save metrics dict for comparison later
```

## Checklist

- [x] Train/Val/Test split thực hiện (stratified)
- [x] Naive Bayes trained với best alpha
- [x] Classification report (Precision, Recall, F1) recorded
- [x] Confusion Matrix plotted & saved
- [x] Learning Curve plotted (Train vs Val — overfitting check)
- [x] Model saved `models/naive_bayes.pkl`
- [x] Notebook `03_model_naive_bayes.ipynb` chạy end-to-end

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Model trained | `naive_bayes.pkl` exists |
| F1-Score recorded | F1 on validation set |
| Recall Scam class | Recall > 80% (baseline acceptable) |
| Learning curve | No severe overfitting |

## Evidence Section *(điền sau khi làm)*

```
Ngày chạy: 2026-09-16
Notebook: notebooks/03_model_naive_bayes.ipynb (executed end-to-end via nbconvert, outputs stripped post-run)

Vấn đề kỹ thuật phát hiện & xử lý:
  MultinomialNB/ComplementNB yêu cầu input non-negative (multinomial event model).
  15 đặc trưng phụ trong X_train.pkl/X_test.pkl đã được StandardScaler chuẩn hóa
  (mean=0) nên chứa giá trị âm → ValueError khi fit trên đủ 5.015 chiều.
  Giải pháp: chỉ dùng khối TF-IDF không âm (5.000 cột đầu, đúng dữ liệu Phase 03,
  không tính toán lại) cho model NB. XGBoost (Phase 05) không bị ràng buộc này.

Baseline comparison (validation set, alpha=1.0 mặc định):
  MultinomialNB: Acc=0.9356, Precision=0.7833, Recall=0.9216, F1=0.8468, ROC-AUC=0.9873
  ComplementNB:  Acc=0.9091, Precision=0.6849, Recall=0.9804, F1=0.8065, ROC-AUC=0.9873
  → MultinomialNB thắng theo F1, được chọn cho GridSearchCV.

GridSearchCV (5-fold CV, scoring=f1, trên X_train_nb 1754×5000):
  Best alpha = 0.01, Best CV F1 = 0.9058

Final model (MultinomialNB, alpha=0.01, refit trên toàn bộ X_train_nb) — TEST SET (439 mẫu):
  Accuracy  = 0.9544
  Precision = 0.8478
  Recall    = 0.9286   (> 80% baseline target ✅, đạt luôn target dự án ≥92% xấp xỉ)
  F1        = 0.8864   (gần mục tiêu dự án F1≥0.88 — ĐẠT)
  ROC-AUC   = 0.9911

Classification report (test):
                precision  recall  f1-score  support
  Bình thường     0.98      0.96     0.97      355
  Lừa đảo         0.85      0.93     0.89       84

Learning curve: Train F1 giảm dần từ 1.00 → 0.96, Validation F1 tăng dần từ 0.73 → 0.91,
  hội tụ dần khi tăng số mẫu, không có dấu hiệu overfitting nghiêm trọng.

Artifacts:
  models/naive_bayes.pkl, models/naive_bayes_metrics.json
  reports/figures/nb_confusion_matrix.png, nb_roc_curve.png, nb_learning_curve.png
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **Hoàn thành 2026-09-16.** MultinomialNB (alpha=0.01, tuned qua GridSearchCV 5-fold)
> đạt F1=0.8864, Recall=92.86%, ROC-AUC=0.9911 trên test set (439 mẫu) — vượt baseline
> ComplementNB và đạt mục tiêu dự án. Phát hiện & xử lý đúng ràng buộc kỹ thuật:
> NB chỉ tương thích với khối TF-IDF không âm, không dùng được 15 đặc trưng phụ đã
> chuẩn hóa (chứa giá trị âm) — quyết định này không vi phạm zero-leakage protocol vì
> vẫn dùng đúng `X_train.pkl`/`X_test.pkl` gốc, chỉ chọn subset cột tương thích thuật toán.
> Sẵn sàng cho Phase 05 (XGBoost).

## Commit

```bash
git add notebooks/03_model_naive_bayes.ipynb models/naive_bayes.pkl reports/figures/
git commit -m "feat(phase04): Naive Bayes baseline trained, F1=X.XX"
```
