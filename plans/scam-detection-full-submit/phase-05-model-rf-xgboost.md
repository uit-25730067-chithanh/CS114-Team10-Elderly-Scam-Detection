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
| Status | `passed` ✅ (Cả Random Forest — Sơn và XGBoost — Cẩm đều hoàn thành) |
| Review | ✅ Đã kiểm định chuyên sâu (--hard) PASSED |
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

- [x] Random Forest trained với best hyperparameters *(Sơn — done: n_estimators=200, max_depth=50, max_features=0.2, split=2, leaf=2)*
- [x] XGBoost trained với best hyperparameters *(Cẩm — done: n_estimators=300, max_depth=5, lr=0.05, subsample=0.7, colsample_bytree=0.8, scale_pos_weight=4.22)*
- [x] Classification report cho RF *(Sơn — done: F1=0.9425, Recall=0.9762, Precision=0.9111, Acc=0.9772)* / [x] cho XGB *(Cẩm — done: F1=0.9535, Recall=0.9762, Precision=0.9318, Acc=0.9818)*
- [x] Confusion Matrix cho RF *(rf_confusion_matrix.png)* / [x] cho XGB *(xgb_confusion_matrix.png)*
- [x] Learning Curves plotted cho RF *(rf_learning_curve.png)* / [x] cho XGB *(xgb_learning_curve.png)*
- [x] Feature importance (top-20) extracted cho RF *(rf_feature_importance.png)* / [x] cho XGB *(xgb_feature_importance.png)*
- [x] Model saved: `random_forest.pkl` & `random_forest_metrics.json` *(Sơn)* / [x] `xgboost.pkl` & `xgboost_metrics.json` *(Cẩm)*
- [x] Notebook `04_model_random_forest.ipynb` chạy end-to-end *(Sơn — done, 11.8 KB)* / [x] `04_model_xgboost.ipynb` chạy end-to-end *(Cẩm — done)*

## Success Criteria

| Criterion | Target | Evidence (Random Forest — Sơn) | Evidence (XGBoost — Cẩm) | Status |
|-----------|:---:|:---:|:---:|:---:|
| F1-Score | F1 > NB baseline (0.8864) | **0.9425 (94.25%)** | **0.9535 (95.35%)** | ✅ PASSED (Cả 2 vượt xa NB) |
| Recall Scam class | ≥ 92.0% | **0.9762 (97.62%)** | **0.9762 (97.62%)** | ✅ PASSED (Bắt 82/84 mẫu lừa đảo) |
| ROC-AUC | ≥ 0.9500 | **0.9976 (99.76%)** | **0.9984 (99.84%)** | ✅ PASSED (Phân tách gần tuyệt đối) |
| No severe overfitting | Train/Val converge | Learning curve hội tụ đều từ 0.85 → 0.95 | Val F1 tăng từ 0.83 → 0.96 | ✅ PASSED |

## Evidence Section *(điền sau khi làm)*

```text
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

=== Random Forest (Sơn) — 2026-09-17 ===
Notebook: notebooks/04_model_random_forest.ipynb (executed end-to-end, outputs stripped post-run)
Ma trận đầu vào Zero-Leakage: X_train (1754, 5015), X_test (439, 5015) — nạp thẳng từ Phase 03.
class_weight='balanced' bù mất cân bằng lớp (tỷ lệ 80.84% normal / 19.16% scam).

Baseline (n_estimators=200, max_depth=None, min_samples_split=5) — validation set:
  Accuracy=0.9848, Precision=0.9608, Recall=0.9608, F1=0.9608, ROC-AUC=0.9980

RandomizedSearchCV (25 tổ hợp, 5-Fold CV = 125 fits):
  Best params: n_estimators=200, max_depth=50, max_features=0.2, min_samples_split=2, min_samples_leaf=2
  Best 5-Fold CV F1 Score: 0.9479

Final model (tuned, refit trên toàn bộ X_train) — TEST SET (439 mẫu unseen):
  Accuracy  = 0.9772 (97.72%)
  Precision = 0.9111 (91.11%)
  Recall    = 0.9762 (97.62%)  <-- VƯỢT XA TARGET >= 92% (82/84 mẫu lừa đảo)
  F1        = 0.9425 (94.25%)  <-- VƯỢT XA TARGET >= 88% (+6.25%)
  ROC-AUC   = 0.9976 (99.76%)

Classification report (test):
                precision    recall  f1-score   support
  Bình thường     0.9943    0.9775    0.9858       355
  Lừa đảo         0.9111    0.9762    0.9425        84

  accuracy                         0.9772       439
  macro avg       0.9527    0.9768    0.9642       439
  weighted avg    0.9784    0.9772    0.9775       439

Confusion Matrix: TN=347, FP=8, FN=2, TP=82 (Chỉ bỏ sót đúng 2/84 mẫu lừa đảo).

Top-5 feature importance (Gini): "liên_hệ 198", "number", "money", "tran", "hotline".

Artifacts:
  models/random_forest.pkl (1.32 MB), models/random_forest_metrics.json (802 bytes)
  reports/figures/rf_confusion_matrix.png, rf_roc_curve.png, rf_learning_curve.png,
  rf_feature_importance.png
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **HOÀN THÀNH 100% (2026-09-17).** Cả 2 mô hình Ensemble trong Phase 05 đều đã được huấn luyện, tinh chỉnh siêu tham số và đánh giá độc lập thành công xuất sắc:
> - **XGBoost Classifier (Cẩm):** F1 = **0.9535**, Recall = **97.62%**, ROC-AUC = **0.9984** trên tập Test 439 mẫu.
> - **Random Forest Classifier (Sơn):** F1 = **0.9425**, Recall = **97.62%**, ROC-AUC = **0.9976** trên tập Test 439 mẫu.
> Cả 2 mô hình đều vượt xa chỉ tiêu tối thiểu của đề tài (F1 ≥ 88%, Recall ≥ 92%), chỉ bỏ sót đúng 2/84 mẫu lừa đảo, vượt trội so với baseline Naive Bayes (F1 = 88.64%). Toàn bộ 8 biểu đồ học thuật 300 DPI, sổ tay thực nghiệm sạch output cells, và hồ sơ metrics JSON đã được tích hợp đầy đủ. Sẵn sàng cho Phase 06 (SVM) và Phase 07 (So sánh tổng hợp & XAI).

