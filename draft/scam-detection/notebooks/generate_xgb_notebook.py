#!/usr/bin/env python3
"""
Script to generate 04_model_xgboost.ipynb notebook for Phase 05 (XGBoost part, owned by Cam).
Run from draft/scam-detection/ directory.
"""
import json
from pathlib import Path

NB_PATH = Path("notebooks/04_model_xgboost.ipynb")


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
        "# Phase 05 — XGBoost Classifier\n\n"
        "**Phase 05 — CS114 Final Project: Vietnamese Elderly Scam Detection**  \n"
        "**Tác giả:** Bùi Thị Mỷ Cẩm (MSSV: 25730013)  \n"
        "**Ngày:** 2026-09-16  \n\n---\n\n"
        "## Mục tiêu\n\n"
        "Huấn luyện XGBoost Classifier trên ma trận đặc trưng 5.015 chiều đã xuất sẵn từ "
        "Phase 03, xử lý mất cân bằng lớp bằng `scale_pos_weight ≈ 4.22`, tinh chỉnh "
        "hyperparameters bằng RandomizedSearchCV, đo 5 metrics, vẽ Confusion Matrix / "
        "ROC Curve / Learning Curve / Top-20 Feature Importance.\n\n"
        "> **CRITICAL INVARIANT:** KHÔNG fit lại TF-IDF hay split lại dataset — dùng thẳng "
        "`X_train.pkl` / `X_test.pkl` từ Phase 03 để giữ consistency với Phase 04 và Phase 07.",
        "md_00_title",
    ),
    cell_md("## 0. Setup & Imports", "md_01_setup"),
    cell_code(
        "import sys\nimport json\nimport time\nfrom pathlib import Path\n\n"
        "import numpy as np\nimport joblib\nimport xgboost as xgb\n\n"
        "PROJECT_ROOT = Path('.').resolve()\n"
        "if not (PROJECT_ROOT / 'src').exists():\n"
        "    PROJECT_ROOT = PROJECT_ROOT.parent  # kernel cwd = notebooks/ in some launchers\n"
        "if str(PROJECT_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(PROJECT_ROOT))\n\n"
        "from src.utils import RANDOM_STATE, get_models_dir, get_reports_dir\n"
        "from src.model_plots import (\n"
        "    compute_metrics, plot_confusion_matrix, plot_learning_curve_chart,\n"
        "    plot_roc_curve, plot_feature_importance,\n"
        ")\n\n"
        "DATA_DIR = PROJECT_ROOT / 'data' / 'processed'\n"
        "FIGURES_DIR = get_reports_dir() / 'figures'\n"
        "MODELS_DIR = get_models_dir()\n"
        "print(f'RANDOM_STATE={RANDOM_STATE}, xgboost version={xgb.__version__}')",
        "co_01_imports",
    ),
    cell_md("## 1. Nạp Feature Matrices Từ Phase 03 (KHÔNG split lại)", "md_02_load"),
    cell_code(
        "X_train = joblib.load(DATA_DIR / 'X_train.pkl')   # (1754, 5015) sparse CSR\n"
        "X_test  = joblib.load(DATA_DIR / 'X_test.pkl')    # (439, 5015)\n"
        "y_train = joblib.load(DATA_DIR / 'y_train.pkl')\n"
        "y_test  = joblib.load(DATA_DIR / 'y_test.pkl')\n\n"
        "with open(DATA_DIR / 'feature_names.json', encoding='utf-8') as f:\n"
        "    feature_names = json.load(f)\n\n"
        "print(f'X_train: {X_train.shape}, X_test: {X_test.shape}')\n"
        "print(f'feature_names: {len(feature_names)} entries')",
        "co_02_load",
    ),
    cell_code(
        "from sklearn.model_selection import train_test_split\n\n"
        "# Validation set (15% của X_train) — dùng cho early-stop / model selection, KHÔNG đụng X_test\n"
        "X_tr, X_val, y_tr, y_val = train_test_split(\n"
        "    X_train, y_train, test_size=0.15,\n"
        "    random_state=RANDOM_STATE, stratify=y_train,\n"
        ")\n"
        "print(f'X_tr: {X_tr.shape}, X_val: {X_val.shape}')",
        "co_03_val_split",
    ),
    cell_md(
        "## 2. Baseline XGBoost (scale_pos_weight bù mất cân bằng lớp)",
        "md_03_baseline",
    ),
    cell_code(
        "# scale_pos_weight = normal/scam trên tập train hiện tại\n"
        "scale_pw = float((y_tr == 0).sum() / (y_tr == 1).sum())\n"
        "print(f'scale_pos_weight = {scale_pw:.4f}')\n\n"
        "xgb_baseline = xgb.XGBClassifier(\n"
        "    n_estimators=200, max_depth=6, learning_rate=0.1,\n"
        "    scale_pos_weight=scale_pw, random_state=RANDOM_STATE,\n"
        "    eval_metric='logloss', n_jobs=-1,\n"
        ")\n"
        "xgb_baseline.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)\n\n"
        "y_val_pred = xgb_baseline.predict(X_val)\n"
        "y_val_proba = xgb_baseline.predict_proba(X_val)[:, 1]\n"
        "baseline_metrics = compute_metrics(y_val, y_val_pred, y_val_proba)\n"
        "print('--- XGBoost baseline (validation) ---')\n"
        "for k, v in baseline_metrics.items():\n"
        "    print(f'  {k:10s}: {v:.4f}')",
        "co_04_baseline_fit",
    ),
    cell_md(
        "## 3. Hyperparameter Tuning — RandomizedSearchCV (5-fold CV trên X_train)",
        "md_04_tuning",
    ),
    cell_code(
        "from sklearn.model_selection import RandomizedSearchCV\n\n"
        "scale_pw_full = float((y_train == 0).sum() / (y_train == 1).sum())\n\n"
        "xgb_param_dist = {\n"
        "    'n_estimators': [100, 200, 300],\n"
        "    'max_depth': [3, 5, 7, 10],\n"
        "    'learning_rate': [0.01, 0.05, 0.1, 0.2],\n"
        "    'subsample': [0.7, 0.8, 0.9],\n"
        "    'colsample_bytree': [0.7, 0.8, 0.9],\n"
        "}\n\n"
        "random_search = RandomizedSearchCV(\n"
        "    xgb.XGBClassifier(\n"
        "        scale_pos_weight=scale_pw_full, random_state=RANDOM_STATE,\n"
        "        eval_metric='logloss', n_jobs=-1,\n"
        "    ),\n"
        "    param_distributions=xgb_param_dist,\n"
        "    n_iter=25, cv=5, scoring='f1', n_jobs=-1,\n"
        "    random_state=RANDOM_STATE, verbose=0,\n"
        ")\n"
        "t0 = time.time()\n"
        "random_search.fit(X_train, y_train)\n"
        "print(f'RandomizedSearchCV done in {time.time()-t0:.1f}s')\n"
        "print(f'Best params: {random_search.best_params_}')\n"
        "print(f'Best CV F1: {random_search.best_score_:.4f}')",
        "co_05_random_search",
    ),
    cell_md(
        "## 4. Huấn luyện Model Cuối Cùng (best params, full X_train) & Đánh giá trên X_test",
        "md_05_final",
    ),
    cell_code(
        "xgb_model = random_search.best_estimator_\n"
        "xgb_model.fit(X_train, y_train)  # refit trên toàn bộ X_train với best params\n\n"
        "y_test_pred = xgb_model.predict(X_test)\n"
        "y_test_proba = xgb_model.predict_proba(X_test)[:, 1]\n"
        "test_metrics = compute_metrics(y_test, y_test_pred, y_test_proba)\n\n"
        "from sklearn.metrics import classification_report\n"
        "print('--- XGBoost (tuned) — TEST SET ---')\n"
        "for k, v in test_metrics.items():\n"
        "    print(f'  {k:10s}: {v:.4f}')\n"
        "print()\n"
        "print(classification_report(y_test, y_test_pred, target_names=['Bình thường', 'Lừa đảo']))",
        "co_06_final_eval",
    ),
    cell_md("## 5. Confusion Matrix & ROC Curve", "md_06_cm"),
    cell_code(
        "plot_confusion_matrix(\n"
        "    y_test, y_test_pred, FIGURES_DIR, 'xgb_confusion_matrix.png',\n"
        "    'Confusion Matrix — XGBoost (Test Set)',\n"
        ")\n"
        "plot_roc_curve(\n"
        "    y_test, y_test_proba, FIGURES_DIR, 'xgb_roc_curve.png',\n"
        "    'ROC Curve — XGBoost (Test Set)',\n"
        ")",
        "co_07_cm_roc",
    ),
    cell_md("## 6. Learning Curve (Overfitting Check)", "md_07_lc"),
    cell_code(
        "plot_learning_curve_chart(\n"
        "    xgb.XGBClassifier(**{**random_search.best_params_,\n"
        "                         'scale_pos_weight': scale_pw_full,\n"
        "                         'random_state': RANDOM_STATE,\n"
        "                         'eval_metric': 'logloss', 'n_jobs': -1}),\n"
        "    X_train, y_train, FIGURES_DIR, 'xgb_learning_curve.png',\n"
        "    'Learning Curve — XGBoost (tuned)', cv=5, scoring='f1', random_state=RANDOM_STATE,\n"
        ")",
        "co_08_learning_curve",
    ),
    cell_md("## 7. Feature Importance (Top-20)", "md_08_fi"),
    cell_code(
        "importances = xgb_model.feature_importances_\n"
        "plot_feature_importance(\n"
        "    importances, feature_names, FIGURES_DIR, 'xgb_feature_importance.png',\n"
        "    'Top-20 Đặc trưng Quan trọng Nhất — XGBoost', top_n=20,\n"
        ")\n\n"
        "top_idx = np.argsort(importances)[::-1][:20]\n"
        "for rank, i in enumerate(top_idx, 1):\n"
        "    print(f'{rank:2d}. {feature_names[i]:30s} {importances[i]:.4f}')",
        "co_09_feature_importance",
    ),
    cell_md("## 8. Save Model & Metrics", "md_09_save"),
    cell_code(
        "joblib.dump(xgb_model, MODELS_DIR / 'xgboost.pkl')\n\n"
        "metrics_record = {\n"
        "    'algorithm': 'XGBoost',\n"
        "    'best_params': random_search.best_params_,\n"
        "    'scale_pos_weight': scale_pw_full,\n"
        "    'cv_f1_randomsearch': random_search.best_score_,\n"
        "    'baseline_metrics_validation': baseline_metrics,\n"
        "    'test_metrics': test_metrics,\n"
        "    'random_state': RANDOM_STATE,\n"
        "}\n"
        "with open(MODELS_DIR / 'xgboost_metrics.json', 'w', encoding='utf-8') as f:\n"
        "    json.dump(metrics_record, f, ensure_ascii=False, indent=2)\n\n"
        "print('Model saved: models/xgboost.pkl')\n"
        "print('Metrics saved: models/xgboost_metrics.json')\n"
        "print(json.dumps(metrics_record, ensure_ascii=False, indent=2))",
        "co_10_save",
    ),
    cell_md(
        "## 9. Summary\n\n"
        "**Phase 05 (XGBoost) — COMPLETED** ✅\n\n"
        "Kết quả chi tiết xem output cell 'Save Model & Metrics' phía trên "
        "(`models/xgboost_metrics.json`). So sánh với baseline Naive Bayes "
        "(`models/naive_bayes_metrics.json`) ở Phase 04.\n\n"
        "**Ready for:** Phase 06 (SVM — `05_model_svm.ipynb`), Phase 07 (So sánh tổng hợp — Thanh).",
        "md_10_summary",
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
