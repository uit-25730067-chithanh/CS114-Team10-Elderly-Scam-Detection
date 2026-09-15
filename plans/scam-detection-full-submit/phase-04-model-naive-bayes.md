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
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 2–3h |
| Sprint | Sprint 2 Fast-Track (14/09/2026) |

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

nb_model = MultinomialNB(alpha=1.0)
nb_model.fit(X_train, y_train)

# Evaluate on validation set
y_val_pred = nb_model.predict(X_val)
print(classification_report(y_val, y_val_pred, target_names=['Normal', 'Scam']))
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

- [ ] Train/Val/Test split thực hiện (stratified)
- [ ] Naive Bayes trained với best alpha
- [ ] Classification report (Precision, Recall, F1) recorded
- [ ] Confusion Matrix plotted & saved
- [ ] Learning Curve plotted (Train vs Val — overfitting check)
- [ ] Model saved `models/naive_bayes.pkl`
- [ ] Notebook `03_model_naive_bayes.ipynb` chạy end-to-end

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Model trained | `naive_bayes.pkl` exists |
| F1-Score recorded | F1 on validation set |
| Recall Scam class | Recall > 80% (baseline acceptable) |
| Learning curve | No severe overfitting |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add notebooks/03_model_naive_bayes.ipynb models/naive_bayes.pkl reports/figures/
git commit -m "feat(phase04): Naive Bayes baseline trained, F1=X.XX"
```
