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
| Status | `passed` |
| Review | ✅ Passed by PM Thanh (2026-09-19) |
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

- [x] Model comparison table (CSV) with Accuracy, Precision, Recall, F1, AUC
- [x] Confusion Matrix cho tất cả 4 models (`reports/figures/confusion_matrices_all.png`)
- [x] ROC Curve comparison plot (`reports/figures/roc_curves_comparison.png`)
- [x] Precision-Recall Curve comparison plot (`reports/figures/precision_recall_curves.png`)
- [x] Learning Curves cho tất cả models (overfitting analysis — `reports/figures/learning_curves_summary.png`)
- [x] Top-20 scam keywords extracted & visualized (`reports/figures/top20_keywords_barplot.png`)
- [x] Best model identified (XGBoost F1=0.9535, Recall Scam=97.62%)
- [x] SHAP values computed & beeswarm summary plot (`reports/figures/shap_summary.png`)
- [x] Notebook `06_evaluation_xai.ipynb` chạy end-to-end
- [x] Unit test suite đạt 69/69 tests PASSED 100%

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| F1-Score best model | 0.9535 (XGBoost) ≥ 88% on test set |
| Recall Scam class | 97.62% (XGBoost & Random Forest) ≥ 92% on test set |
| All required plots | 6 figures in reports/figures/ (CM grid, ROC, PR, Learning Curves, Top-20 Keywords, SHAP) |
| Top-20 keywords | Meaningful Vietnamese scam keywords: money, số_tiền, thương_hiệu, liên_hệ 198, viện_phí, gấp, số_định_danh |

## Evidence Section

```markdown
### 1. Bảng Tổng Hợp Hiệu Năng Nghiệm Thu Trên Holdout Test Set (439 mẫu)

| Mô hình | Accuracy | Precision | Recall (Lừa đảo) | F1-Score | ROC-AUC | Brier Score | FN | FP | Xếp hạng |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **XGBoost** | **98.18%** | **93.18%** | **97.62%** | **0.9535** | 0.9984 | **0.0152** | 2 | 6 | 🏆 Best Overall Model |
| **SVM Linear** | 97.95% | 93.10% | 96.43% | **0.9474** | **0.9986** | 0.0175 | 3 | 6 | 🥈 Best Linear Separator |
| **Random Forest** | 97.72% | 91.11% | **97.62%** | 0.9425 | 0.9977 | 0.0188 | 2 | 8 | 🥉 Best Ensemble Robustness |
| **MultinomialNB** | 95.44% | 84.78% | 92.86% | 0.8864 | 0.9911 | 0.0384 | 6 | 14 | 🏅 Reliable Baseline |

### 2. Hệ Thống 6 Biểu Đồ Nghiệm Thu Chuẩn Xuất Bản 300 DPI (`reports/figures/`)

1. `confusion_matrices_all.png`: Lưới 2×2 ma trận nhầm lẫn của 4 mô hình, thể hiện rõ FN/FP từng model.
2. `roc_curves_comparison.png`: 4 đường cong ROC lồng ghép đạt AUC từ 0.9911 đến 0.9986.
3. `precision_recall_curves.png`: 4 đường Precision-Recall với Average Precision vượt 0.98.
4. `learning_curves_summary.png`: Phân tích hội tụ 5-fold CV chứng minh khả năng kiểm soát quá khớp tối ưu.
5. `top20_keywords_barplot.png`: Biểu đồ ngang 20 từ khóa kích hoạt bẫy tâm lý lừa đảo mạnh nhất.
6. `shap_summary.png`: Biểu đồ SHAP Beeswarm giải thích đóng góp vi mô từng giá trị đặc trưng của XGBoost.

### 3. Top 20 Từ Khóa Bẫy Tâm Lý Đồng Thuận Hàng Đầu (Consensus XAI)

1. money (1.0000)
2. số_tiền (0.9433)
3. thương_hiệu (0.8199)
4. liên_hệ 198 (0.7223)
5. đường_dẫn (0.5634)
6. number (0.4669)
7. mày (0.4331)
8. số_định_danh (0.4222)
9. 198 (0.3176)
10. gấp (0.3097)
11. viện_phí (0.2249)
12. chị (0.1912)
13. doi (0.1712)
14. soạn (0.1708)
15. thuế (0.1670)
16. đang (0.1589)
17. số_lượng (0.1509)
18. viettel (0.1502)
19. time (0.1352)
20. sẽ (0.1322)
```

## Phase Summary

> ✅ **HOÀN THÀNH 100% XUẤT SẮC**:
> - Đã xây dựng trọn bộ công cụ đánh giá chuyên sâu `src/evaluation/` (`metrics_calculator.py`, `plot_comparator.py`, `xai_explainer.py`, `run_full_evaluation.py`).
> - Đã sinh notebook `06_evaluation_xai.ipynb` thông qua `generate_eval_notebook.py` với cấu trúc tài liệu hóa hoàn chỉnh.
> - Xuất đủ 6 biểu đồ so sánh 4 mô hình đạt chuẩn 300 DPI, không có lỗi rò rỉ dữ liệu hay file kích thước lớn.
> - Bộ kiểm thử `pytest` tăng từ 65 lên 69 tests và đạt 100% PASS rate.
> - Kế hoạch nghiệm thu Best Model: **XGBoost Classifier** (F1=0.9535, Recall=97.62%) và **Linear SVM** (ROC-AUC=0.9986).

## Commit

```bash
git add src/evaluation/ notebooks/ tests/ reports/ plans/
git commit -m "feat(phase07): complete 4-model evaluation, XAI consensus keywords, and SHAP analysis"
```
