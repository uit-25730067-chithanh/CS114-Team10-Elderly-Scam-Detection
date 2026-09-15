# Phase 07 — Evaluation & XAI (Explainable AI)

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 06 — Modeling — SVM](./phase-06-model-svm-phobert.md)  
**Next phase:** [Phase 08 — Demo UI](./phase-08-demo-ui.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P1 |
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 4–5h |
| Sprint | Sprint 3 Fast-Track (18/09 – 19/09/2026) |

## Context

So sánh tổng hợp tất cả models (NB, RF, XGB, SVM) trên **test set**, trực quan hóa kết quả theo yêu cầu thầy Thăng: Confusion Matrix, Train vs Val curves, Precision-Recall. Thêm giải thích mô hình (XAI) qua SHAP / Feature Weights.

## Implementation Steps

### Step 1 — Model Comparison Table

```python
models = {
    "Naive Bayes": nb_model,
    "Random Forest": rf_model,
    "XGBoost": xgb_model,
    "SVM Linear": svm_model,
}

results = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred),
        "AUC-ROC": roc_auc_score(y_test, y_proba),
    })

comparison_df = pd.DataFrame(results)
comparison_df.to_csv("reports/model_comparison.csv", index=False)
```

### Step 2 — Confusion Matrix (tất cả models)

```python
from sklearn.metrics import ConfusionMatrixDisplay

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
for ax, (name, model) in zip(axes.flat, models.items()):
    ConfusionMatrixDisplay.from_estimator(
        model, X_test, y_test,
        display_labels=['Normal', 'Scam'],
        cmap='Blues', ax=ax
    )
    ax.set_title(name)
plt.tight_layout()
plt.savefig("reports/figures/confusion_matrices_all.png", dpi=150)
```

### Step 3 — ROC Curve Comparison

```python
from sklearn.metrics import RocCurveDisplay

fig, ax = plt.subplots(figsize=(10, 8))
for name, model in models.items():
    RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax, name=name)
ax.set_title("ROC Curve Comparison — All Models")
plt.savefig("reports/figures/roc_curves_comparison.png", dpi=150)
```

### Step 4 — Learning Curves (Train vs Val — Overfitting Analysis)

Plot learning curves cho tất cả models theo yêu cầu thầy Thăng:

```python
from sklearn.model_selection import learning_curve

for name, model in models.items():
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_train, y_train,
        cv=5, scoring='f1',
        train_sizes=np.linspace(0.1, 1.0, 10),
        random_state=RANDOM_STATE,
    )
    # Plot & save each
```

### Step 5 — Precision-Recall Curve

```python
from sklearn.metrics import PrecisionRecallDisplay

fig, ax = plt.subplots(figsize=(10, 8))
for name, model in models.items():
    PrecisionRecallDisplay.from_estimator(model, X_test, y_test, ax=ax, name=name)
ax.set_title("Precision-Recall Curve — All Models")
plt.savefig("reports/figures/precision_recall_curves.png", dpi=150)
```

### Step 6 — XAI: Top-20 Scam Keywords

```python
import json
import numpy as np

# Load feature names từ Phase 03 artifact (5000 TF-IDF + 15 aux)
with open("data/processed/feature_names.json") as f:
    feature_names = json.load(f)   # list của 5015 tên
tfidf_names = feature_names[:5000]  # chỉ lấy phần TF-IDF cho XAI text

# For Naive Bayes: log probabilities
nb_scam_features = nb_model.feature_log_prob_[1] - nb_model.feature_log_prob_[0]
top_20_nb = np.argsort(nb_scam_features[:5000])[-20:][::-1]

# For RF/XGB: feature_importances_
rf_importances = rf_model.feature_importances_[:5000]  # chỉ lấy TF-IDF part
xgb_importances = xgb_model.feature_importances_[:5000]

# For SVM (CalibratedClassifierCV): độ quan trọng qua calibrated estimators
# LinearSVC được bao trong CalibratedClassifierCV — không dùng .estimator.coef_ trực tiếp
svm_weights_list = [
    est.estimator.coef_[0][:5000]
    for est in svm_model.calibrated_classifiers_
]
svm_weights = np.mean(svm_weights_list, axis=0)

# Top-20 keywords per model
for name, importances in [("NB", nb_scam_features[:5000]), ("RF", rf_importances),
                          ("XGB", xgb_importances), ("SVM", svm_weights)]:
    top20_idx = np.argsort(importances)[-20:][::-1]
    top20 = [(tfidf_names[i], float(importances[i])) for i in top20_idx]
    print(f"\nTop-20 Scam Keywords [{name}]:")
    for kw, score in top20:
        print(f"  {kw}: {score:.4f}")
```

### Step 7 — (Optional) SHAP Values

> ⚠️ Cài đặt SHAP nếu chưa có: `pip install shap>=0.45.0`  
> **Hiện tại `shap` chưa trong môi trường — chạy `pip install shap` trước khi thực hiện step này.**

```python
import shap

# SHAP for XGBoost (nếp nhanh hơn các model khác)
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test[:100])  # chỉ lấy 100 mẫu đầu tiên cho tốc độ
shap.summary_plot(
    shap_values, X_test[:100].toarray(),  # sparse → dense cho SHAP
    feature_names=tfidf_names,
    max_display=20,
    show=False,
)
import matplotlib.pyplot as plt
plt.tight_layout()
plt.savefig("reports/figures/shap_summary.png", dpi=150, bbox_inches='tight')
```

## Related Files

```
draft/scam-detection/
├── notebooks/
│   └── 06_evaluation_xai.ipynb
├── reports/
│   ├── model_comparison.csv
│   └── figures/
│       ├── confusion_matrices_all.png
│       ├── roc_curves_comparison.png
│       ├── precision_recall_curves.png
│       ├── learning_curve_nb.png
│       ├── learning_curve_rf.png
│       ├── learning_curve_xgb.png
│       ├── learning_curve_svm.png
│       ├── top20_keywords_barplot.png
│       └── shap_summary.png (optional)
```

## Checklist

- [ ] Model comparison table (CSV) with Accuracy, Precision, Recall, F1, AUC
- [ ] Confusion Matrix cho tất cả 4 models
- [ ] ROC Curve comparison plot
- [ ] Precision-Recall Curve comparison plot
- [ ] Learning Curves cho tất cả models (overfitting analysis)
- [ ] Top-20 scam keywords extracted & visualized
- [ ] Best model identified (F1 ≥ 88%, Recall Scam ≥ 92%)
- [ ] (Optional) SHAP values computed
- [ ] Notebook `06_evaluation_xai.ipynb` chạy end-to-end

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| F1-Score best model | ≥ 88% on test set |
| Recall Scam class | ≥ 92% on test set |
| All required plots | ≥ 8 figures in reports/figures/ |
| Top-20 keywords | Meaningful Vietnamese scam keywords |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add notebooks/06_evaluation_xai.ipynb reports/ src/evaluation/
git commit -m "feat(phase07): full evaluation, XAI top-20 keywords, best model F1=X.XX"
```
