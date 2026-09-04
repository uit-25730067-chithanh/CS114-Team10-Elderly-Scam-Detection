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
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 4–5h |
| Sprint | Sprint 3 |

## Context

Ensemble models (Random Forest, XGBoost) thường vượt trội NB trên tabular/text features. Đánh giá tương tác giữa TF-IDF features và auxiliary features.

## Implementation Steps

### Step 1 — Random Forest

```python
from sklearn.ensemble import RandomForestClassifier
from src.utils import RANDOM_STATE

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    min_samples_split=5,
    class_weight='balanced',
    random_state=RANDOM_STATE,
    n_jobs=-1,
)
rf_model.fit(X_train, y_train)
```

### Step 2 — XGBoost

```python
import xgboost as xgb

xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=len(y_train[y_train==0]) / len(y_train[y_train==1]),
    random_state=RANDOM_STATE,
    eval_metric='logloss',
    use_label_encoder=False,
)
xgb_model.fit(
    X_train, y_train,
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
