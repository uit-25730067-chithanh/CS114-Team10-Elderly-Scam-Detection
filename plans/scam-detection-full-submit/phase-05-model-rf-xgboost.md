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
| Status | `in-progress` 🚀 (XGBoost done — Cẩm; Random Forest pending — Sơn) |
| Review | ⏳ XGBoost hoàn thành, chờ Random Forest |
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

- [ ] Random Forest trained với best hyperparameters *(Sơn — pending)*
- [x] XGBoost trained với best hyperparameters *(Cẩm — done)*
- [ ] Classification report cho RF *(pending)* / [x] cho XGB *(done)*
- [ ] Confusion Matrix cho RF *(pending)* / [x] cho XGB *(done)*
- [x] Learning Curve XGBoost plotted *(RF pending)*
- [x] Feature importance (top-20) extracted — XGBoost *(RF pending)*
- [ ] Model saved: `random_forest.pkl` *(pending)* / [x] `xgboost.pkl` *(done)*
- [x] Notebook `04_model_xgboost.ipynb` chạy end-to-end (Cẩm) — RF ở `04_model_random_forest.ipynb` *(Sơn, pending)*

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| RF F1-Score | F1 > NB baseline |
| XGB F1-Score | F1 > NB baseline |
| Recall Scam class | ≥ 90% (target ≥ 92%) |
| No severe overfitting | Learning curves converge |

## Evidence Section *(điền sau khi làm)*

```
=== XGBoost (Cẩm) — 2026-09-16 ===
Notebook: notebooks/04_model_xgboost.ipynb (executed end-to-end via nbconvert, outputs stripped post-run)
Dùng đủ 5.015 chiều (TF-IDF + 15 aux) — XGBoost không có ràng buộc non-negative như NB.

scale_pos_weight (train split 85%) = 4.2281 (≈ đúng công thức normal/scam ≈ 4.22 trong task)

Baseline (n_estimators=200, max_depth=6, lr=0.1) — validation set:
  Accuracy=0.9773, Precision=0.9412, Recall=0.9412, F1=0.9412, ROC-AUC=0.9971

RandomizedSearchCV (n_iter=25, 5-fold CV, scoring=f1, trên X_train 1754×5015, 51.1s):
  Best params: subsample=0.7, n_estimators=300, max_depth=5, learning_rate=0.05,
               colsample_bytree=0.8
  Best CV F1 = 0.9603

Final model (tuned, refit trên toàn bộ X_train) — TEST SET (439 mẫu):
  Accuracy  = 0.9818
  Precision = 0.9318
  Recall    = 0.9762   (vượt target dự án ≥92% ✅✅)
  F1        = 0.9535   (vượt xa target F1≥0.88 ✅✅, vượt NB baseline F1=0.8864 ✅)
  ROC-AUC   = 0.9984

Classification report (test):
                precision  recall  f1-score  support
  Bình thường     0.99      0.98     0.99      355
  Lừa đảo         0.93      0.98     0.95       84

Learning curve: Train F1 ~0.98-1.00 (gần như bão hòa), Validation F1 tăng dần
  0.83 → 0.96 theo số mẫu, khoảng cách train/val thu hẹp dần — không overfitting
  nghiêm trọng dù có gap nhẹ (kỳ vọng với boosted trees trên high-dim sparse data).

Top-5 feature importance: "liên_hệ 198" (0.139), "money" (0.079), "198" (0.065),
  "number" (0.037), "tran" (0.036) — các n-gram liên quan số điện thoại/tiền bạc/liên hệ
  khớp với các category lừa đảo family_emergency & fear_authority.

Artifacts:
  models/xgboost.pkl, models/xgboost_metrics.json
  reports/figures/xgb_confusion_matrix.png, xgb_roc_curve.png, xgb_learning_curve.png,
  xgb_feature_importance.png

=== Random Forest (Sơn) ===
(Chưa thực hiện — chờ Sơn làm notebooks/04_model_random_forest.ipynb)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> 🚧 **Một phần hoàn thành (2026-09-16).** XGBoost (Cẩm) đã tune xong qua
> RandomizedSearchCV, đạt F1=0.9535, Recall=97.62%, ROC-AUC=0.9984 trên test set —
> vượt xa cả target dự án (F1≥0.88, Recall≥92%) và baseline Naive Bayes (F1=0.8864,
> Phase 04). Random Forest (Sơn) chưa thực hiện — phase chỉ đóng khi cả 2 model xong.

## Commit

```bash
git add notebooks/04_model_rf_xgboost.ipynb models/ reports/figures/
git commit -m "feat(phase05): RF & XGBoost trained, F1=X.XX / X.XX"
```
