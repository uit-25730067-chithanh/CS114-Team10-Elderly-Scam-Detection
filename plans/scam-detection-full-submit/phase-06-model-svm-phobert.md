# Phase 06 — Modeling — SVM (Optional: PhoBERT)

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 05 — Modeling — Random Forest & XGBoost](./phase-05-model-rf-xgboost.md)  
**Next phase:** [Phase 07 — Evaluation & XAI](./phase-07-evaluation-xai.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Cẩm** |
| Priority | P1 |
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 3–5h |
| Sprint | Sprint 3 Fast-Track (19/09 – 20/09/2026) *(dời từ Sprint 2 để tránh overcapacity cho Cẩm)* |

## Context

SVM (Support Vector Machine) là mô hình thứ 3 bắt buộc theo yêu cầu thầy Thăng. Linear SVM rất hiệu quả cho text classification với TF-IDF features. Optional: Fine-tune PhoBERT nếu nhóm có thời gian.

## Implementation Steps

### Step 1 — SVM Linear

```python
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from src.utils import RANDOM_STATE

# LinearSVC + CalibratedClassifierCV để có predict_proba
svm_base = LinearSVC(
    C=1.0,
    class_weight='balanced',
    random_state=RANDOM_STATE,
    max_iter=5000,
)
svm_model = CalibratedClassifierCV(svm_base, cv=5)
svm_model.fit(X_train, y_train)
```

### Step 2 — SVM RBF Kernel (Alternative)

```python
from sklearn.svm import SVC

svm_rbf = SVC(
    kernel='rbf',
    C=1.0,
    gamma='scale',
    class_weight='balanced',
    random_state=RANDOM_STATE,
    probability=True,
)
# ⚠️ RBF SVM chậm trên sparse matrix lớn — cân nhắc subsample hoặc PCA
```

### Step 3 — Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'estimator__C': [0.01, 0.1, 1.0, 10.0],
}
grid_svm = GridSearchCV(
    CalibratedClassifierCV(LinearSVC(class_weight='balanced', random_state=RANDOM_STATE)),
    param_grid, cv=5, scoring='f1', n_jobs=-1,
)
grid_svm.fit(X_train, y_train)
```

### Step 4 — (Optional) PhoBERT Fine-tuning

> ⚠️ Chỉ thực hiện nếu có đủ thời gian và GPU resources.

```python
# PhoBERT approach (sketch):
# 1. pip install transformers torch
# 2. Load vinai/phobert-base
# 3. Tokenize với PhoBERTTokenizer
# 4. Fine-tune classification head
# 5. Train 3-5 epochs
```

### Step 5 — Save Model

```python
import joblib
joblib.dump(svm_model, "models/svm_linear.pkl")
```


## 🔌 Interface Contract — Model Output (Phase 06 → Phase 08)

> [!IMPORTANT]
> Phase 08 (Demo UI) **phụ thuộc** vào output format chính xác từ Phase 06. Đây là hợp đồng cứng giữa Cẩm (train model) và Sơn (build app). Phải thống nhất trước khi bắt đầu code Phase 08.

| Field | Spec bắt buộc |
|---|---|
| **Format lưu model** | `joblib` — `joblib.dump(bundle, 'models/best_model_bundle.pkl')` |
| **Bundle structure** | `{'model': calibrated_svc, 'vectorizer': tfidf_vectorizer, 'threshold': 0.5, 'label_names': ['Bình thường', 'Lừa đảo']}` |
| **Path chuẩn** | `models/best_model_bundle.pkl` (relative to repo root) |
| **sklearn version** | Phải khớp với `requirements.txt` — kiểm tra bằng `sklearn.__version__` trước khi lưu |
| **Tên vectorizer** | TF-IDF vectorizer được `fit` trên X_train — **tích hợp trong bundle**, không lưu tách rời |
| **Input format** | Raw text string → vectorizer.transform → model.predict_proba |
| **Output format** | `{'label': int, 'proba': [p_normal, p_scam], 'scam_keywords': list}` |

```python
# Mẫu sử dụng chuẩn trong Streamlit (Phase 08)
import joblib
bundle = joblib.load('models/best_model_bundle.pkl')
model = bundle['model']
vectorizer = bundle['vectorizer']
X = vectorizer.transform([user_input])
proba = model.predict_proba(X)[0]
label = 1 if proba[1] >= bundle['threshold'] else 0
```

## Checklist

- [ ] SVM Linear trained với best C
- [ ] Classification report recorded
- [ ] Confusion Matrix plotted
- [ ] Learning Curve plotted
- [ ] Model saved `models/svm_linear.pkl`
- [ ] (Optional) PhoBERT fine-tuned
- [ ] Notebook `05_model_svm.ipynb` chạy end-to-end

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| SVM F1-Score | F1 competitive with RF/XGB |
| 3+ models compared | NB, RF, XGB, SVM all trained |
| Recall Scam | ≥ 90% |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add notebooks/05_model_svm.ipynb models/svm_linear.pkl reports/figures/
git commit -m "feat(phase06): SVM trained, all 3+ models ready for comparison"
```
