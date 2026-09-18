#!/usr/bin/env python3
"""
Script to generate 03_model_naive_bayes.ipynb notebook for Phase 04.
Run from draft/scam-detection/ directory.
"""
import json
from pathlib import Path

NB_PATH = Path("notebooks/03_model_naive_bayes.ipynb")


def cell_md(source, cell_id):
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}


def cell_code(source, cell_id, outputs=None):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": outputs or [],
        "source": source,
    }


cells = [
    cell_md(
        "# Phase 04 — Naive Bayes Baseline\n\n"
        "**Phase 04 — CS114 Final Project: Vietnamese Elderly Scam Detection**  \n"
        "**Tác giả:** Bùi Thị Mỷ Cẩm (MSSV: 25730013)  \n"
        "**Ngày:** 2026-09-16  \n\n---\n\n"
        "## Mục tiêu\n\n"
        "Huấn luyện baseline model MultinomialNB & ComplementNB trên ma trận đặc trưng "
        "5.015 chiều (5.000 TF-IDF + 15 aux) đã xuất sẵn từ Phase 03, đo 5 metrics "
        "(Accuracy, Precision, Recall, F1, ROC-AUC), tinh chỉnh `alpha` bằng GridSearchCV, "
        "và kiểm tra overfitting bằng Learning Curve.\n\n"
        "> **CRITICAL INVARIANT:** KHÔNG gọi lại `train_test_split` trên toàn dataset hay "
        "`TfidfVectorizer.fit_transform` — phải nạp thẳng `X_train.pkl` / `X_test.pkl` để "
        "giữ nguyên zero-leakage protocol của Phase 03.",
        "md_00_title",
    ),
    cell_md("## 0. Setup & Imports", "md_01_setup"),
    cell_code(
        "import sys\nimport json\nimport time\nfrom pathlib import Path\n\n"
        "import numpy as np\nimport joblib\n\n"
        "PROJECT_ROOT = Path('.').resolve()\n"
        "if not (PROJECT_ROOT / 'src').exists():\n"
        "    PROJECT_ROOT = PROJECT_ROOT.parent  # kernel cwd = notebooks/ in some launchers\n"
        "if str(PROJECT_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(PROJECT_ROOT))\n\n"
        "from src.utils import RANDOM_STATE, get_models_dir, get_reports_dir\n"
        "from src.feature_engineering_config import TFIDF_MAX_FEATURES\n"
        "from src.model_plots import (\n"
        "    compute_metrics, plot_confusion_matrix, plot_learning_curve_chart, plot_roc_curve,\n"
        ")\n\n"
        "DATA_DIR = PROJECT_ROOT / 'data' / 'processed'\n"
        "FIGURES_DIR = get_reports_dir() / 'figures'\n"
        "MODELS_DIR = get_models_dir()\n"
        "print(f'RANDOM_STATE={RANDOM_STATE}')",
        "co_01_imports",
    ),
    cell_md(
        "## 1. Nạp Feature Matrices Từ Phase 03 (KHÔNG split lại)",
        "md_02_load",
    ),
    cell_code(
        "X_train = joblib.load(DATA_DIR / 'X_train.pkl')   # sparse CSR\n"
        "X_test  = joblib.load(DATA_DIR / 'X_test.pkl')\n"
        "y_train = joblib.load(DATA_DIR / 'y_train.pkl')\n"
        "y_test  = joblib.load(DATA_DIR / 'y_test.pkl')\n\n"
        "print(f'X_train: {X_train.shape}, X_test: {X_test.shape}')\n"
        "print(f'y_train: {len(y_train)} samples, {y_train.sum()} scam / {len(y_train)-y_train.sum()} normal')\n"
        "print(f'y_test:  {len(y_test)} samples, {y_test.sum()} scam / {len(y_test)-y_test.sum()} normal')",
        "co_02_load",
    ),
    cell_code(
        "from sklearn.model_selection import train_test_split\n\n"
        "# Validation set (15% của X_train) — chỉ dùng cho model selection, KHÔNG đụng X_test\n"
        "X_tr, X_val, y_tr, y_val = train_test_split(\n"
        "    X_train, y_train, test_size=0.15,\n"
        "    random_state=RANDOM_STATE, stratify=y_train,\n"
        ")\n"
        "print(f'X_tr: {X_tr.shape}, X_val: {X_val.shape}')",
        "co_03_val_split",
    ),
    cell_md(
        "## 2. Baseline: MultinomialNB vs ComplementNB\n\n"
        "> ⚠️ **Lưu ý kỹ thuật:** `MultinomialNB`/`ComplementNB` giả định input là tần suất "
        "không âm (multinomial event model). 15 đặc trưng phụ trong `X_train.pkl` đã được "
        "`StandardScaler` chuẩn hóa (mean=0) nên **chứa giá trị âm** — không tương thích với "
        "2 model này (sklearn raise `ValueError: Negative values`). Do đó với riêng NB, ta chỉ "
        "dùng khối TF-IDF không âm (5.000 cột đầu của đúng `X_train.pkl`/`X_test.pkl` đã export "
        "ở Phase 03 — KHÔNG tính toán lại gì cả, chỉ chọn subset cột tương thích thuật toán). "
        "XGBoost ở notebook kế tiếp không có ràng buộc này nên dùng đủ 5.015 chiều.",
        "md_03_baseline",
    ),
    cell_code(
        "from sklearn.naive_bayes import MultinomialNB, ComplementNB\n\n"
        "# Chỉ giữ khối TF-IDF (5000 cột đầu) — tương thích non-negative cho NB\n"
        "X_tr_nb, X_val_nb = X_tr[:, :TFIDF_MAX_FEATURES], X_val[:, :TFIDF_MAX_FEATURES]\n"
        "X_train_nb, X_test_nb = X_train[:, :TFIDF_MAX_FEATURES], X_test[:, :TFIDF_MAX_FEATURES]\n"
        "print(f'X_tr_nb: {X_tr_nb.shape}, min value: {X_tr_nb.min()}')\n\n"
        "baselines = {\n"
        "    'MultinomialNB': MultinomialNB(alpha=1.0),\n"
        "    'ComplementNB': ComplementNB(alpha=1.0),\n"
        "}\n\n"
        "baseline_results = {}\n"
        "for name, clf in baselines.items():\n"
        "    clf.fit(X_tr_nb, y_tr)\n"
        "    y_val_pred = clf.predict(X_val_nb)\n"
        "    y_val_proba = clf.predict_proba(X_val_nb)[:, 1]\n"
        "    metrics = compute_metrics(y_val, y_val_pred, y_val_proba)\n"
        "    baseline_results[name] = metrics\n"
        "    print(f'--- {name} (validation) ---')\n"
        "    for k, v in metrics.items():\n"
        "        print(f'  {k:10s}: {v:.4f}')",
        "co_04_baseline_fit",
    ),
    cell_code(
        "from sklearn.metrics import classification_report\n\n"
        "best_baseline_name = max(baseline_results, key=lambda n: baseline_results[n]['f1'])\n"
        "print(f'Best baseline theo F1: {best_baseline_name}')\n"
        "print()\n"
        "print(classification_report(\n"
        "    y_val, baselines[best_baseline_name].predict(X_val_nb),\n"
        "    target_names=['Bình thường', 'Lừa đảo'],\n"
        "))",
        "co_05_baseline_report",
    ),
    cell_md("## 3. Hyperparameter Tuning (alpha) — GridSearchCV trên X_train_nb (5-fold CV)", "md_04_tuning"),
    cell_code(
        "from sklearn.model_selection import GridSearchCV\n\n"
        "NBClass = MultinomialNB if best_baseline_name == 'MultinomialNB' else ComplementNB\n"
        "param_grid = {'alpha': [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]}\n\n"
        "grid_search = GridSearchCV(\n"
        "    NBClass(), param_grid, cv=5, scoring='f1', n_jobs=-1,\n"
        ")\n"
        "grid_search.fit(X_train_nb, y_train)\n"
        "print(f'Best estimator: {NBClass.__name__}')\n"
        "print(f'Best alpha: {grid_search.best_params_[\"alpha\"]}')\n"
        "print(f'Best CV F1: {grid_search.best_score_:.4f}')",
        "co_06_gridsearch",
    ),
    cell_md("## 4. Huấn luyện Model Cuối Cùng (best alpha, full X_train_nb) & Đánh giá trên X_test_nb", "md_05_final"),
    cell_code(
        "nb_model = grid_search.best_estimator_  # đã tự refit trên toàn bộ X_train_nb (refit=True mặc định)\n\n"
        "y_test_pred = nb_model.predict(X_test_nb)\n"
        "y_test_proba = nb_model.predict_proba(X_test_nb)[:, 1]\n"
        "test_metrics = compute_metrics(y_test, y_test_pred, y_test_proba)\n\n"
        "print(f'--- {type(nb_model).__name__} (alpha={nb_model.alpha}) — TEST SET ---')\n"
        "for k, v in test_metrics.items():\n"
        "    print(f'  {k:10s}: {v:.4f}')\n"
        "print()\n"
        "print(classification_report(y_test, y_test_pred, target_names=['Bình thường', 'Lừa đảo']))",
        "co_07_final_eval",
    ),
    cell_md("## 5. Confusion Matrix & ROC Curve", "md_06_cm"),
    cell_code(
        "plot_confusion_matrix(\n"
        "    y_test, y_test_pred, FIGURES_DIR, 'nb_confusion_matrix.png',\n"
        "    f'Confusion Matrix — {type(nb_model).__name__} (Test Set)',\n"
        ")\n"
        "plot_roc_curve(\n"
        "    y_test, y_test_proba, FIGURES_DIR, 'nb_roc_curve.png',\n"
        "    f'ROC Curve — {type(nb_model).__name__} (Test Set)',\n"
        ")",
        "co_08_cm_roc",
    ),
    cell_md("## 6. Learning Curve (Overfitting Check)", "md_07_lc"),
    cell_code(
        "plot_learning_curve_chart(\n"
        "    NBClass(alpha=nb_model.alpha), X_train_nb, y_train, FIGURES_DIR,\n"
        "    'nb_learning_curve.png', f'Learning Curve — {type(nb_model).__name__} (alpha={nb_model.alpha})',\n"
        "    cv=5, scoring='f1', random_state=RANDOM_STATE,\n"
        ")",
        "co_09_learning_curve",
    ),
    cell_md("## 7. Save Model & Metrics", "md_08_save"),
    cell_code(
        "joblib.dump(nb_model, MODELS_DIR / 'naive_bayes.pkl')\n\n"
        "metrics_record = {\n"
        "    'algorithm': type(nb_model).__name__,\n"
        "    'n_features_used': X_train_nb.shape[1],\n"
        "    'feature_note': 'TF-IDF only (0:TFIDF_MAX_FEATURES) — aux features excluded (negative values incompatible with NB)',\n"
        "    'best_alpha': nb_model.alpha,\n"
        "    'cv_f1_gridsearch': grid_search.best_score_,\n"
        "    'baseline_comparison': baseline_results,\n"
        "    'test_metrics': test_metrics,\n"
        "    'random_state': RANDOM_STATE,\n"
        "}\n"
        "with open(MODELS_DIR / 'naive_bayes_metrics.json', 'w', encoding='utf-8') as f:\n"
        "    json.dump(metrics_record, f, ensure_ascii=False, indent=2)\n\n"
        "print('Model saved: models/naive_bayes.pkl')\n"
        "print('Metrics saved: models/naive_bayes_metrics.json')\n"
        "print(json.dumps(metrics_record, ensure_ascii=False, indent=2))",
        "co_10_save",
    ),
    cell_md(
        "## 8. Summary\n\n"
        "**Phase 04 — COMPLETED** ✅\n\n"
        "Kết quả chi tiết xem output cell 'Save Model & Metrics' phía trên "
        "(`models/naive_bayes_metrics.json`).\n\n"
        "**Ready for:** Phase 05 (XGBoost — `04_model_xgboost.ipynb`).",
        "md_09_summary",
    ),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12.3"},
    },
    "cells": cells,
}

NB_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

import os

size_kb = os.path.getsize(NB_PATH) / 1024
print(f"Notebook created: {NB_PATH}")
print(f"Size: {size_kb:.1f} KB")
print(f"Cell count: {len(cells)}")
