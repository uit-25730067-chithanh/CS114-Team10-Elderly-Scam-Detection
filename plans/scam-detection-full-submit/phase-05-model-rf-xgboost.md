# Phase 05 — Modeling — Random Forest & XGBoost

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 04 — Modeling — Naive Bayes Baseline](./phase-04-model-naive-bayes.md)  
**Next phase:** [Phase 06 — Modeling — SVM (Optional: PhoBERT)](./phase-06-model-svm-phobert.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Sơn** (Random Forest) + **Cẩm** (XGBoost) |
| Priority | P1 |
| Status | `in-progress` 🚀 |
| Review | ⏳ Đang tiến hành thực nghiệm |
| Estimated effort | 4–5h |
| Sprint | Sprint 2 Fast-Track (15/09 – 16/09/2026) |

## Context

Ensemble models (Random Forest, XGBoost) thường vượt trội NB trên tabular/text features. Đánh giá tương tác giữa TF-IDF features và auxiliary features.

## Implementation Steps

### Step 0 — Nạp Feature Matrices Từ Phase 03 (KHÔNG tự split lại)

> ⚠️ **BẮT BUỘC:** Load `X_train.pkl` / `X_test.pkl` đã có từ Phase 03. TUYỆT ĐỐI KHÔNG fit lại TF-IDF hay split lại dataset — sẽ tạo split khác, phá vỡ consistency với Phase 04 và Phase 07.

```python
import joblib
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.utils import RANDOM_STATE

DATA_DIR = Path("data/processed")

X_train = joblib.load(DATA_DIR / "X_train.pkl")   # (1754, 5015) sparse CSR
X_test  = joblib.load(DATA_DIR / "X_test.pkl")    # (439, 5015)  sparse CSR
y_train = joblib.load(DATA_DIR / "y_train.pkl")   # 336 scam / 1418 normal
y_test  = joblib.load(DATA_DIR / "y_test.pkl")    # 84 scam / 355 normal

# Tạo validation set từ X_train (15%)
X_tr, X_val, y_tr, y_val = train_test_split(
    X_train, y_train, test_size=0.15,
    random_state=RANDOM_STATE, stratify=y_train
)
```

### Step 1 — Random Forest

```python
from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    min_samples_split=5,
    class_weight='balanced',
    random_state=RANDOM_STATE,
    n_jobs=-1,
)
rf_model.fit(X_tr, y_tr)
```

### Step 2 — XGBoost

```python
import xgboost as xgb

# scale_pos_weight = normal/scam = 1418/336 ≈ 4.22 (bù class imbalance)
scale_pw = len(y_tr[y_tr == 0]) / len(y_tr[y_tr == 1])

xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=scale_pw,
    random_state=RANDOM_STATE,
    eval_metric='logloss',
    # use_label_encoder đã bị bỏ trong XGBoost 2.x — KHÔNG thêm vào
)
xgb_model.fit(
    X_tr, y_tr,
    eval_set=[(X_val, y_val)],
    verbose=False,
)
```

### Step 3 — Hyperparameter Tuning (RandomizedSearch)

```python
from sklearn.model_selection import RandomizedSearchCV

# RF tuning
rf_param_dist = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

# XGB tuning
xgb_param_dist = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'subsample': [0.7, 0.8, 0.9],
    'colsample_bytree': [0.7, 0.8, 0.9],
}
```

### Step 4 — Evaluation & Learning Curves

- Classification report (Precision, Recall, F1) cho cả RF và XGB
- Confusion Matrix cho cả 2 models
- Learning Curves (Train vs Val) kiểm tra overfitting
- Feature importance (top-20 features)

### Step 5 — Save Models

```python
import joblib

joblib.dump(rf_model, "models/random_forest.pkl")
joblib.dump(xgb_model, "models/xgboost.pkl")
```

## Checklist

- [ ] Random Forest trained với best hyperparameters
- [ ] XGBoost trained với best hyperparameters
- [ ] Classification report cho cả RF và XGB
- [ ] Confusion Matrix cho cả 2 models
- [ ] Learning Curves plotted
- [ ] Feature importance (top-20) extracted
- [ ] Models saved: `random_forest.pkl`, `xgboost.pkl`
- [ ] Notebook `04_model_rf_xgboost.ipynb` chạy end-to-end

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| RF F1-Score | F1 > NB baseline |
| XGB F1-Score | F1 > NB baseline |
| Recall Scam class | ≥ 90% (target ≥ 92%) |
| No severe overfitting | Learning curves converge |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add notebooks/04_model_rf_xgboost.ipynb models/ reports/figures/
git commit -m "feat(phase05): RF & XGBoost trained, F1=X.XX / X.XX"
```
