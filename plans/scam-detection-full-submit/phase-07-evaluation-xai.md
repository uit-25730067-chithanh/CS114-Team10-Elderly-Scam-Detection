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
# Method 1: TF-IDF feature weights from best model
feature_names = tfidf.get_feature_names_out()

# For Naive Bayes: log probabilities
nb_scam_features = nb_model.feature_log_prob_[1] - nb_model.feature_log_prob_[0]

# For RF/XGB: feature_importances_
rf_importances = rf_model.feature_importances_[:len(feature_names)]

# For SVM: coef_
svm_weights = svm_model.estimator.coef_[0][:len(feature_names)]

# Top-20 keywords per model
top_20_indices = np.argsort(rf_importances)[-20:][::-1]
top_20_keywords = [(feature_names[i], rf_importances[i]) for i in top_20_indices]
```

### Step 7 — (Optional) SHAP Values

```python
import shap

# SHAP for XGBoost
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X_test[:100])
shap.summary_plot(shap_values, X_test[:100], feature_names=all_feature_names)
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
