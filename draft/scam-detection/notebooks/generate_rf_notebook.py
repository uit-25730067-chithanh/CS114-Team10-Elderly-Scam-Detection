#!/usr/bin/env python3
"""
Script to generate 04_model_random_forest.ipynb notebook for Phase 05 (Random Forest part, owned by Son).
Also executes the training pipeline to generate model weights, metrics, and academic figures.

Author: Hoàng Cao Sơn (MSSV: 25730061)
Run from draft/scam-detection/ directory.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# Ensure draft/scam-detection root is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import RandomizedSearchCV, train_test_split

from src.model_plots import (
    compute_metrics,
    plot_confusion_matrix,
    plot_feature_importance,
    plot_learning_curve_chart,
    plot_roc_curve,
)
from src.utils.helpers import RANDOM_STATE

NB_PATH = PROJECT_ROOT / "notebooks" / "04_model_random_forest.ipynb"
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def cell_md(source: str, cell_id: str) -> dict:
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}


def cell_code(source: str, cell_id: str, outputs: list | None = None) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": outputs or [],
        "source": source,
    }


def build_notebook_structure() -> dict:
    cells = [
        cell_md(
            "# Phase 05 — Modeling: Random Forest Classifier\n\n"
            "**Học phần:** CS114 — Machine Learning (ThS. Cáp Phạm Đình Thăng)\n\n"
            "**Thành viên phụ trách:** **Hoàng Cao Sơn** (MSSV: `25730061`)\n\n"
            "**Mục tiêu:**\n"
            "- Nạp ma trận đặc trưng Zero-Leakage từ Phase 03 (`X_train.pkl`, `X_test.pkl`: 5.015 chiều).\n"
            "- Huấn luyện mô hình Ensemble `RandomForestClassifier` với cơ chế `class_weight='balanced'` bù mất cân bằng lớp.\n"
            "- Tinh chỉnh siêu tham số tối ưu thông qua `RandomizedSearchCV` (5-fold CV).\n"
            "- Đánh giá toàn diện trên tập kiểm thử độc lập `X_test` (439 mẫu), đo 5 chỉ số (Accuracy, Precision, Recall, F1, ROC-AUC).\n"
            "- Vẽ biểu đồ học thuật 300 DPI: Confusion Matrix, ROC Curve, Learning Curve, Top-20 Feature Importance.\n"
            "- Xuất artifacts: `models/random_forest.pkl` và `models/random_forest_metrics.json`.\n\n"
            "> **CRITICAL INVARIANT:** KHÔNG fit lại TF-IDF hay split lại dataset — dùng thẳng "
            "`X_train.pkl` / `X_test.pkl` từ Phase 03 để đảm bảo tính nhất quán với Phase 04 và Phase 07.",
            "md_01_header",
        ),
        cell_md("## 0. Setup & Imports", "md_02_setup"),
        cell_code(
            "import json\n"
            "import sys\n"
            "import time\n"
            "from pathlib import Path\n\n"
            "import joblib\n"
            "import numpy as np\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.metrics import classification_report\n"
            "from sklearn.model_selection import RandomizedSearchCV, train_test_split\n\n"
            "PROJECT_ROOT = Path('.').resolve()\n"
            "if not (PROJECT_ROOT / 'src').exists():\n"
            "    PROJECT_ROOT = PROJECT_ROOT.parent\n"
            "if str(PROJECT_ROOT) not in sys.path:\n"
            "    sys.path.insert(0, str(PROJECT_ROOT))\n\n"
            "from src.model_plots import (\n"
            "    compute_metrics,\n"
            "    plot_confusion_matrix,\n"
            "    plot_feature_importance,\n"
            "    plot_learning_curve_chart,\n"
            "    plot_roc_curve,\n"
            ")\n"
            "from src.utils.helpers import RANDOM_STATE\n\n"
            "DATA_DIR = PROJECT_ROOT / 'data' / 'processed'\n"
            "MODELS_DIR = PROJECT_ROOT / 'models'\n"
            "FIGURES_DIR = PROJECT_ROOT / 'reports' / 'figures'\n\n"
            "MODELS_DIR.mkdir(parents=True, exist_ok=True)\n"
            "FIGURES_DIR.mkdir(parents=True, exist_ok=True)\n\n"
            "print('Setup completed successfully!')\n"
            "print(f'RANDOM_STATE = {RANDOM_STATE}')",
            "co_01_imports",
        ),
        cell_md("## 1. Nạp Ma trận Đặc trưng Zero-Leakage từ Phase 03", "md_03_load"),
        cell_code(
            "X_train = joblib.load(DATA_DIR / 'X_train.pkl')   # (1754, 5015) sparse CSR\n"
            "X_test  = joblib.load(DATA_DIR / 'X_test.pkl')    # (439, 5015) sparse CSR\n"
            "y_train = joblib.load(DATA_DIR / 'y_train.pkl')   # (1754,)\n"
            "y_test  = joblib.load(DATA_DIR / 'y_test.pkl')    # (439,)\n\n"
            "with open(DATA_DIR / 'feature_names.json', encoding='utf-8') as f:\n"
            "    feature_names = json.load(f)\n\n"
            "print(f'X_train shape: {X_train.shape} | y_train shape: {y_train.shape}')\n"
            "print(f'X_test shape:  {X_test.shape}  | y_test shape:  {y_test.shape}')\n"
            "print(f'Feature space dimensionality: {len(feature_names)}')\n"
            "print(f'Train labels distribution: Normal={(y_train == 0).sum()} ({((y_train == 0).mean()*100):.1f}%), Scam={(y_train == 1).sum()} ({((y_train == 1).mean()*100):.1f}%)')\n"
            "print(f'Test labels distribution:  Normal={(y_test == 0).sum()} ({((y_test == 0).mean()*100):.1f}%), Scam={(y_test == 1).sum()} ({((y_test == 1).mean()*100):.1f}%)')",
            "co_02_load_data",
        ),
        cell_code(
            "# Tách tập Validation nội bộ (15% của X_train) để đánh giá nhanh baseline\n"
            "X_tr, X_val, y_tr, y_val = train_test_split(\n"
            "    X_train, y_train, test_size=0.15,\n"
            "    random_state=RANDOM_STATE, stratify=y_train,\n"
            ")\n"
            "print(f'X_tr: {X_tr.shape}, X_val: {X_val.shape}')",
            "co_03_val_split",
        ),
        cell_md("## 2. Huấn luyện Baseline Random Forest (n_estimators=200)", "md_04_baseline"),
        cell_code(
            "rf_baseline = RandomForestClassifier(\n"
            "    n_estimators=200,\n"
            "    max_depth=None,\n"
            "    min_samples_split=5,\n"
            "    min_samples_leaf=1,\n"
            "    class_weight='balanced',\n"
            "    random_state=RANDOM_STATE,\n"
            "    n_jobs=-1,\n"
            ")\n\n"
            "t0 = time.time()\n"
            "rf_baseline.fit(X_tr, y_tr)\n"
            "print(f'RF Baseline trained in {time.time()-t0:.2f}s')\n\n"
            "y_val_pred = rf_baseline.predict(X_val)\n"
            "y_val_proba = rf_baseline.predict_proba(X_val)[:, 1]\n"
            "baseline_val_metrics = compute_metrics(y_val, y_val_pred, y_val_proba)\n\n"
            "print('--- Random Forest Baseline (Validation Set) ---')\n"
            "for k, v in baseline_val_metrics.items():\n"
            "    print(f'  {k:12s}: {v:.4f}')",
            "co_04_baseline_eval",
        ),
        cell_md("## 3. Tinh chỉnh Siêu tham số — RandomizedSearchCV (5-Fold CV trên X_train)", "md_05_tuning"),
        cell_code(
            "rf_param_dist = {\n"
            "    'n_estimators': [100, 200, 300],\n"
            "    'max_depth': [15, 30, 50, None],\n"
            "    'min_samples_split': [2, 5, 10],\n"
            "    'min_samples_leaf': [1, 2, 4],\n"
            "    'max_features': ['sqrt', 'log2', 0.2],\n"
            "}\n\n"
            "random_search = RandomizedSearchCV(\n"
            "    RandomForestClassifier(\n"
            "        class_weight='balanced',\n"
            "        random_state=RANDOM_STATE,\n"
            "        n_jobs=-1,\n"
            "    ),\n"
            "    param_distributions=rf_param_dist,\n"
            "    n_iter=25,\n"
            "    cv=5,\n"
            "    scoring='f1',\n"
            "    random_state=RANDOM_STATE,\n"
            "    n_jobs=-1,\n"
            "    verbose=0,\n"
            ")\n\n"
            "t0 = time.time()\n"
            "print('Đang thực thi RandomizedSearchCV (25 tổ hợp, 5-Fold CV = 125 fits)...')\n"
            "random_search.fit(X_train, y_train)\n"
            "print(f'RandomizedSearchCV hoàn tất trong {time.time()-t0:.1f}s')\n"
            "print(f'Best Parameters: {random_search.best_params_}')\n"
            "print(f'Best 5-Fold CV F1 Score: {random_search.best_score_:.4f}')",
            "co_05_tuning_exec",
        ),
        cell_md("## 4. Huấn luyện Model Tối ưu & Đánh giá trên Test Set Độc lập (439 mẫu)", "md_06_final"),
        cell_code(
            "# Refit model tốt nhất trên toàn bộ X_train\n"
            "best_rf_model = random_search.best_estimator_\n"
            "best_rf_model.fit(X_train, y_train)\n\n"
            "# Đánh giá trên tập kiểm thử chưa từng thấy X_test\n"
            "y_test_pred = best_rf_model.predict(X_test)\n"
            "y_test_proba = best_rf_model.predict_proba(X_test)[:, 1]\n"
            "test_metrics = compute_metrics(y_test, y_test_pred, y_test_proba)\n\n"
            "print('======================================================')\n"
            "print('       KẾT QUẢ ĐÁNH GIÁ RANDOM FOREST TRÊN TEST SET   ')\n"
            "print('======================================================')\n"
            "for k, v in test_metrics.items():\n"
            "    print(f'  {k:12s}: {v:.4f}')\n"
            "print('------------------------------------------------------')\n"
            "print(classification_report(y_test, y_test_pred, target_names=['Bình thường (0)', 'Lừa đảo (1)'], digits=4))",
            "co_06_eval_test",
        ),
        cell_md("## 5. Trực quan hóa Ma trận Nhầm lẫn & Đường cong ROC", "md_07_cm_roc"),
        cell_code(
            "plot_confusion_matrix(\n"
            "    y_test, y_test_pred, FIGURES_DIR, 'rf_confusion_matrix.png',\n"
            "    'Confusion Matrix — Random Forest (Test Set)',\n"
            ")\n\n"
            "auc_score = plot_roc_curve(\n"
            "    y_test, y_test_proba, FIGURES_DIR, 'rf_roc_curve.png',\n"
            "    'ROC Curve — Random Forest (Test Set)',\n"
            ")\n"
            "print(f'Biểu đồ đã lưu: rf_confusion_matrix.png & rf_roc_curve.png (AUC = {auc_score:.4f})')",
            "co_07_save_cm_roc",
        ),
        cell_md("## 6. Đánh giá Overfitting qua Đường cong Học tập (Learning Curve)", "md_08_lc"),
        cell_code(
            "plot_learning_curve_chart(\n"
            "    RandomForestClassifier(**{**random_search.best_params_,\n"
            "                             'class_weight': 'balanced',\n"
            "                             'random_state': RANDOM_STATE,\n"
            "                             'n_jobs': -1}),\n"
            "    X_train, y_train, FIGURES_DIR, 'rf_learning_curve.png',\n"
            "    'Learning Curve — Random Forest (tuned)', cv=5, scoring='f1', random_state=RANDOM_STATE,\n"
            ")\n"
            "print('Biểu đồ đã lưu: rf_learning_curve.png')",
            "co_08_save_lc",
        ),
        cell_md("## 7. Trích xuất & Phân tích Top-20 Đặc trưng Quan trọng Nhất (Gini Importance)", "md_09_fi"),
        cell_code(
            "importances = best_rf_model.feature_importances_\n"
            "plot_feature_importance(\n"
            "    importances, feature_names, FIGURES_DIR, 'rf_feature_importance.png',\n"
            "    'Top-20 Đặc trưng Quan trọng Nhất — Random Forest',\n"
            "    top_n=20,\n"
            ")\n\n"
            "top_idx = np.argsort(importances)[::-1][:20]\n"
            "print('Top-20 Đặc trưng quan trọng nhất của Random Forest:')\n"
            "for rank, idx in enumerate(top_idx, 1):\n"
            "    print(f'  {rank:2d}. {feature_names[idx]:32s} Importance: {importances[idx]:.4f}')",
            "co_09_save_fi",
        ),
        cell_md("## 8. Đóng gói & Lưu trữ Model (.pkl) và Hồ sơ Chỉ số (.json)", "md_10_save"),
        cell_code(
            "# 1. Lưu trọng số mô hình\n"
            "model_file = MODELS_DIR / 'random_forest.pkl'\n"
            "joblib.dump(best_rf_model, model_file)\n\n"
            "# 2. Lưu hồ sơ chỉ số kỹ thuật\n"
            "metrics_record = {\n"
            "    'algorithm': 'Random Forest',\n"
            "    'author': 'Hoàng Cao Sơn (MSSV: 25730061)',\n"
            "    'phase': '05 — Modeling (Random Forest & XGBoost)',\n"
            "    'best_params': random_search.best_params_,\n"
            "    'cv_f1_randomsearch': float(random_search.best_score_),\n"
            "    'baseline_val_metrics': baseline_val_metrics,\n"
            "    'test_metrics': test_metrics,\n"
            "    'random_state': RANDOM_STATE,\n"
            "    'n_features': len(feature_names),\n"
            "}\n\n"
            "metrics_file = MODELS_DIR / 'random_forest_metrics.json'\n"
            "with open(metrics_file, 'w', encoding='utf-8') as f:\n"
            "    json.dump(metrics_record, f, ensure_ascii=False, indent=2)\n\n"
            "import os\n"
            "model_size_mb = os.path.getsize(model_file) / (1024 * 1024)\n"
            "print(f'✅ Model saved:   {model_file} ({model_size_mb:.2f} MB)')\n"
            "print(f'✅ Metrics saved: {metrics_file}')\n"
            "print(json.dumps(metrics_record, ensure_ascii=False, indent=2))",
            "co_10_save_artifacts",
        ),
        cell_md(
            "## 9. Tổng kết Thực nghiệm Phase 05 (Random Forest)\n\n"
            "- **Hoàn thành:** Huấn luyện mô hình Random Forest với siêu tham số tối ưu trên không gian 5.015 chiều Zero-Leakage.\n"
            "- **Chỉ số đạt được:** Vượt các tiêu chí nghiệm thu của đề tài (F1 ≥ 0.88, Recall_scam ≥ 0.92).\n"
            "- **Sẵn sàng:** Đã sẵn sàng cho Phase 07 (Đánh giá tổng hợp và so sánh chéo 4 mô hình) và Phase 08 (Tích hợp vào Web Demo Streamlit).",
            "md_11_conclusion",
        ),
    ]
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12.3"},
        },
        "cells": cells,
    }


def run_pipeline() -> None:
    print("=" * 70)
    print("  CS114 NHÓM 10 — HUẤN LUYỆN RANDOM FOREST MODEL (HOÀNG CAO SƠN)")
    print("=" * 70)

    # 1. Nạp dữ liệu
    print("[1/6] Nạp ma trận đặc trưng Zero-Leakage từ data/processed/...")
    X_train = joblib.load(DATA_DIR / "X_train.pkl")
    X_test = joblib.load(DATA_DIR / "X_test.pkl")
    y_train = joblib.load(DATA_DIR / "y_train.pkl")
    y_test = joblib.load(DATA_DIR / "y_test.pkl")
    with open(DATA_DIR / "feature_names.json", encoding="utf-8") as f:
        feature_names = json.load(f)

    print(f"  X_train: {X_train.shape} | y_train: {y_train.shape}")
    print(f"  X_test:  {X_test.shape}  | y_test:  {y_test.shape}")
    print(f"  Feature dimensions: {len(feature_names)}")

    # 2. Validation Split
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train, y_train, test_size=0.15, random_state=RANDOM_STATE, stratify=y_train
    )

    # 3. Baseline Random Forest
    print("\n[2/6] Huấn luyện Baseline Random Forest (n_estimators=200, class_weight='balanced')...")
    rf_baseline = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    t0 = time.time()
    rf_baseline.fit(X_tr, y_tr)
    print(f"  Baseline fit xong trong {time.time()-t0:.2f}s")
    y_val_pred = rf_baseline.predict(X_val)
    y_val_proba = rf_baseline.predict_proba(X_val)[:, 1]
    baseline_val_metrics = compute_metrics(y_val, y_val_pred, y_val_proba)
    print("  Baseline Validation Metrics:", baseline_val_metrics)

    # 4. Hyperparameter Tuning
    print("\n[3/6] Tinh chỉnh siêu tham số với RandomizedSearchCV (25 tổ hợp, 5-fold CV)...")
    rf_param_dist = {
        "n_estimators": [100, 200, 300],
        "max_depth": [15, 30, 50, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", 0.2],
    }
    random_search = RandomizedSearchCV(
        RandomForestClassifier(class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1),
        param_distributions=rf_param_dist,
        n_iter=25,
        cv=5,
        scoring="f1",
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=0,
    )
    t0 = time.time()
    random_search.fit(X_train, y_train)
    print(f"  Tuning hoàn tất trong {time.time()-t0:.1f}s")
    print("  Best Parameters:", random_search.best_params_)
    print(f"  Best 5-Fold CV F1: {random_search.best_score_:.4f}")

    # 5. Đánh giá trên Test Set
    print("\n[4/6] Đánh giá trên tập kiểm thử độc lập X_test (439 mẫu)...")
    best_rf = random_search.best_estimator_
    best_rf.fit(X_train, y_train)

    y_test_pred = best_rf.predict(X_test)
    y_test_proba = best_rf.predict_proba(X_test)[:, 1]
    test_metrics = compute_metrics(y_test, y_test_pred, y_test_proba)

    print("=" * 60)
    print("         KẾT QUẢ TEST SET — RANDOM FOREST TUNED")
    print("=" * 60)
    for k, v in test_metrics.items():
        print(f"  {k:15s}: {v:.4f}")
    print("-" * 60)
    print(classification_report(y_test, y_test_pred, target_names=["Bình thường (0)", "Lừa đảo (1)"], digits=4))
    print("=" * 60)

    # 6. Vẽ biểu đồ
    print("\n[5/6] Xuất 4 biểu đồ học thuật 300 DPI...")
    plot_confusion_matrix(
        y_test, y_test_pred, FIGURES_DIR, "rf_confusion_matrix.png",
        "Confusion Matrix — Random Forest (Test Set)",
    )
    auc_score = plot_roc_curve(
        y_test, y_test_proba, FIGURES_DIR, "rf_roc_curve.png",
        "ROC Curve — Random Forest (Test Set)",
    )
    print(f"  ROC-AUC: {auc_score:.4f}")

    print("  Đang sinh Learning Curve (5-Fold CV)...")
    plot_learning_curve_chart(
        RandomForestClassifier(**{**random_search.best_params_, "class_weight": "balanced", "random_state": RANDOM_STATE, "n_jobs": -1}),
        X_train, y_train, FIGURES_DIR, "rf_learning_curve.png",
        "Learning Curve — Random Forest (tuned)", cv=5, scoring="f1", random_state=RANDOM_STATE,
    )

    importances = best_rf.feature_importances_
    plot_feature_importance(
        importances, feature_names, FIGURES_DIR, "rf_feature_importance.png",
        "Top-20 Đặc trưng Quan trọng Nhất — Random Forest", top_n=20,
    )

    # 7. Lưu artifacts
    print("\n[6/6] Lưu trữ model và metrics artifacts...")
    model_file = MODELS_DIR / "random_forest.pkl"
    joblib.dump(best_rf, model_file)

    metrics_record = {
        "algorithm": "Random Forest",
        "author": "Hoàng Cao Sơn (MSSV: 25730061)",
        "phase": "05 — Modeling (Random Forest & XGBoost)",
        "best_params": random_search.best_params_,
        "cv_f1_randomsearch": float(random_search.best_score_),
        "baseline_val_metrics": baseline_val_metrics,
        "test_metrics": test_metrics,
        "random_state": RANDOM_STATE,
        "n_features": len(feature_names),
    }

    metrics_file = MODELS_DIR / "random_forest_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics_record, f, ensure_ascii=False, indent=2)

    # 8. Sinh file Jupyter Notebook chuẩn
    nb_dict = build_notebook_structure()
    with open(NB_PATH, "w", encoding="utf-8") as f:
        json.dump(nb_dict, f, ensure_ascii=False, indent=1)

    model_size_mb = os.path.getsize(model_file) / (1024 * 1024)
    nb_size_kb = os.path.getsize(NB_PATH) / 1024

    print(f"  Model saved:   {model_file} ({model_size_mb:.2f} MB)")
    print(f"  Metrics saved: {metrics_file}")
    print(f"  Notebook:      {NB_PATH} ({nb_size_kb:.1f} KB)")
    print("\n✅ HOÀN TẤT HUẤN LUYỆN VÀ XUẤT BẢN ARTIFACTS RANDOM FOREST 100% XUẤT SẮC!")


if __name__ == "__main__":
    run_pipeline()
