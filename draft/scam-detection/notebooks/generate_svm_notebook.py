#!/usr/bin/env python3
"""
Script to generate 05_model_svm.ipynb notebook for Phase 06 (SVM, owned by Cam).
Also executes the training pipeline to generate model weights, metrics, academic
figures, and the best_model_bundle.pkl interface contract consumed by Phase 08.

Author: Bùi Thị Mỷ Cẩm (MSSV: 25730013)
Run from draft/scam-detection/ directory.
"""
from __future__ import annotations

import json
import os
import sys
import time
import warnings
from pathlib import Path

# Ensure draft/scam-detection root is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
import sklearn
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVC, LinearSVC

from src.feature_engineering_config import AUX_FEATURE_COLS
from src.model_plots import (
    compute_metrics,
    plot_confusion_matrix,
    plot_feature_importance,
    plot_learning_curve_chart,
    plot_roc_curve,
)
from src.preprocessing.pipeline import preprocess_pipeline
from src.utils.helpers import RANDOM_STATE

NB_PATH = PROJECT_ROOT / "notebooks" / "05_model_svm.ipynb"
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
            "# Phase 06 — Modeling: Support Vector Machine (SVM)\n\n"
            "**Học phần:** CS114 — Machine Learning (ThS. Cáp Phạm Đình Thăng)\n\n"
            "**Thành viên phụ trách:** **Bùi Thị Mỷ Cẩm** (MSSV: `25730013`)\n\n"
            "**Mục tiêu:**\n"
            "- Nạp ma trận đặc trưng Zero-Leakage từ Phase 03 (`X_train.pkl`, `X_test.pkl`: 5.015 chiều).\n"
            "- Huấn luyện `LinearSVC` bọc trong `CalibratedClassifierCV` (để có `predict_proba`), bù mất cân bằng lớp `class_weight='balanced'`.\n"
            "- So sánh đối chứng nhanh với SVM nhân RBF (`kernel='rbf'`).\n"
            "- Tinh chỉnh siêu tham số `C` bằng `GridSearchCV` (5-fold CV).\n"
            "- Đánh giá toàn diện trên tập kiểm thử độc lập `X_test` (439 mẫu), đo 5 chỉ số (Accuracy, Precision, Recall, F1, ROC-AUC).\n"
            "- Vẽ biểu đồ học thuật 300 DPI: Confusion Matrix, ROC Curve, Learning Curve, Top-20 |Coefficient| Weight.\n"
            "- Đóng gói **`models/best_model_bundle.pkl`** — hợp đồng suy luận cứng cho Phase 08 (Demo UI — Sơn).\n\n"
            "> **CRITICAL INVARIANT:** KHÔNG fit lại TF-IDF hay split lại dataset — dùng thẳng "
            "`X_train.pkl` / `X_test.pkl` từ Phase 03 để đảm bảo tính nhất quán với Phase 04, 05 và Phase 07.",
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
            "import sklearn\n"
            "from sklearn.calibration import CalibratedClassifierCV\n"
            "from sklearn.metrics import classification_report\n"
            "from sklearn.model_selection import GridSearchCV, train_test_split\n"
            "from sklearn.svm import SVC, LinearSVC\n\n"
            "PROJECT_ROOT = Path('.').resolve()\n"
            "if not (PROJECT_ROOT / 'src').exists():\n"
            "    PROJECT_ROOT = PROJECT_ROOT.parent\n"
            "if str(PROJECT_ROOT) not in sys.path:\n"
            "    sys.path.insert(0, str(PROJECT_ROOT))\n\n"
            "from src.feature_engineering_config import AUX_FEATURE_COLS\n"
            "from src.model_plots import (\n"
            "    compute_metrics,\n"
            "    plot_confusion_matrix,\n"
            "    plot_feature_importance,\n"
            "    plot_learning_curve_chart,\n"
            "    plot_roc_curve,\n"
            ")\n"
            "from src.preprocessing.pipeline import preprocess_pipeline\n"
            "from src.utils.helpers import RANDOM_STATE\n\n"
            "DATA_DIR = PROJECT_ROOT / 'data' / 'processed'\n"
            "MODELS_DIR = PROJECT_ROOT / 'models'\n"
            "FIGURES_DIR = PROJECT_ROOT / 'reports' / 'figures'\n\n"
            "MODELS_DIR.mkdir(parents=True, exist_ok=True)\n"
            "FIGURES_DIR.mkdir(parents=True, exist_ok=True)\n\n"
            "print('Setup completed successfully!')\n"
            "print(f'RANDOM_STATE = {RANDOM_STATE}, sklearn version = {sklearn.__version__}')",
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
            "# Vectorizer & aux scaler fit sẵn ở Phase 03 — tái sử dụng nguyên trạng cho bundle suy luận\n"
            "tfidf_vectorizer = joblib.load(DATA_DIR / 'tfidf_vectorizer.pkl')\n"
            "aux_scaler = joblib.load(DATA_DIR / 'aux_scaler.pkl')\n\n"
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
        cell_md(
            "## 2. Baseline SVM Linear (LinearSVC + CalibratedClassifierCV để có predict_proba)",
            "md_04_baseline",
        ),
        cell_code(
            "svm_base = LinearSVC(\n"
            "    C=1.0,\n"
            "    class_weight='balanced',\n"
            "    random_state=RANDOM_STATE,\n"
            "    max_iter=5000,\n"
            ")\n"
            "svm_baseline = CalibratedClassifierCV(svm_base, cv=5)\n\n"
            "t0 = time.time()\n"
            "svm_baseline.fit(X_tr, y_tr)\n"
            "print(f'SVM Linear Baseline trained in {time.time()-t0:.2f}s')\n\n"
            "y_val_pred = svm_baseline.predict(X_val)\n"
            "y_val_proba = svm_baseline.predict_proba(X_val)[:, 1]\n"
            "baseline_val_metrics = compute_metrics(y_val, y_val_pred, y_val_proba)\n\n"
            "print('--- SVM Linear Baseline (Validation Set) ---')\n"
            "for k, v in baseline_val_metrics.items():\n"
            "    print(f'  {k:12s}: {v:.4f}')",
            "co_04_baseline_eval",
        ),
        cell_md(
            "## 3. SVM Nhân RBF (Đối chứng — Alternative Kernel)",
            "md_05_rbf",
        ),
        cell_code(
            "# ⚠️ RBF chậm hơn Linear trên ma trận thưa lớn — chỉ chạy đối chứng nhanh trên X_tr/X_val,\n"
            "# KHÔNG dùng để chọn model cuối cùng (Linear vẫn là lựa chọn mặc định theo Phase 06 plan).\n"
            "svm_rbf = SVC(\n"
            "    kernel='rbf',\n"
            "    C=1.0,\n"
            "    gamma='scale',\n"
            "    class_weight='balanced',\n"
            "    random_state=RANDOM_STATE,\n"
            "    probability=True,\n"
            ")\n\n"
            "t0 = time.time()\n"
            "svm_rbf.fit(X_tr, y_tr)\n"
            "rbf_fit_time = time.time() - t0\n"
            "print(f'SVM RBF trained in {rbf_fit_time:.2f}s')\n\n"
            "y_val_pred_rbf = svm_rbf.predict(X_val)\n"
            "y_val_proba_rbf = svm_rbf.predict_proba(X_val)[:, 1]\n"
            "rbf_val_metrics = compute_metrics(y_val, y_val_pred_rbf, y_val_proba_rbf)\n\n"
            "print('--- SVM RBF (Validation Set) ---')\n"
            "for k, v in rbf_val_metrics.items():\n"
            "    print(f'  {k:12s}: {v:.4f}')\n"
            "print(f'\\nLinear F1={baseline_val_metrics[\"f1\"]:.4f} vs RBF F1={rbf_val_metrics[\"f1\"]:.4f} '\n"
            "      f'-> giữ Linear (nhanh hơn, phù hợp dữ liệu thưa TF-IDF, dễ diễn giải hệ số).')",
            "co_05_rbf_eval",
        ),
        cell_md(
            "## 4. Tinh chỉnh Siêu tham số — GridSearchCV trên C (5-Fold CV trên X_train)",
            "md_06_tuning",
        ),
        cell_code(
            "param_grid = {\n"
            "    'estimator__C': [0.01, 0.1, 1.0, 10.0],\n"
            "}\n\n"
            "grid_svm = GridSearchCV(\n"
            "    CalibratedClassifierCV(\n"
            "        LinearSVC(class_weight='balanced', random_state=RANDOM_STATE, max_iter=5000),\n"
            "    ),\n"
            "    param_grid, cv=5, scoring='f1', n_jobs=-1,\n"
            ")\n\n"
            "t0 = time.time()\n"
            "print('Đang thực thi GridSearchCV (4 giá trị C, 5-Fold CV = 20 fits)...')\n"
            "grid_svm.fit(X_train, y_train)\n"
            "print(f'GridSearchCV hoàn tất trong {time.time()-t0:.1f}s')\n"
            "print(f'Best Parameters: {grid_svm.best_params_}')\n"
            "print(f'Best 5-Fold CV F1 Score: {grid_svm.best_score_:.4f}')",
            "co_06_tuning_exec",
        ),
        cell_md("## 5. Huấn luyện Model Tối ưu & Đánh giá trên Test Set Độc lập (439 mẫu)", "md_07_final"),
        cell_code(
            "# Trích xuất model tốt nhất (đã được refit tự động trên toàn bộ X_train bởi GridSearchCV)\n"
            "svm_model = grid_svm.best_estimator_\n\n"
            "y_test_pred = svm_model.predict(X_test)\n"
            "y_test_proba = svm_model.predict_proba(X_test)[:, 1]\n"
            "test_metrics = compute_metrics(y_test, y_test_pred, y_test_proba)\n\n"
            "print('======================================================')\n"
            "print('         KẾT QUẢ ĐÁNH GIÁ SVM LINEAR TRÊN TEST SET   ')\n"
            "print('======================================================')\n"
            "for k, v in test_metrics.items():\n"
            "    print(f'  {k:12s}: {v:.4f}')\n"
            "print('------------------------------------------------------')\n"
            "print(classification_report(y_test, y_test_pred, target_names=['Bình thường (0)', 'Lừa đảo (1)'], digits=4))",
            "co_07_eval_test",
        ),
        cell_md("## 6. Trực quan hóa Ma trận Nhầm lẫn & Đường cong ROC", "md_08_cm_roc"),
        cell_code(
            "plot_confusion_matrix(\n"
            "    y_test, y_test_pred, FIGURES_DIR, 'svm_confusion_matrix.png',\n"
            "    'Confusion Matrix — SVM Linear (Test Set)',\n"
            ")\n\n"
            "auc_score = plot_roc_curve(\n"
            "    y_test, y_test_proba, FIGURES_DIR, 'svm_roc_curve.png',\n"
            "    'ROC Curve — SVM Linear (Test Set)',\n"
            ")\n"
            "print(f'Biểu đồ đã lưu: svm_confusion_matrix.png & svm_roc_curve.png (AUC = {auc_score:.4f})')",
            "co_08_save_cm_roc",
        ),
        cell_md("## 7. Đánh giá Overfitting qua Đường cong Học tập (Learning Curve)", "md_09_lc"),
        cell_code(
            "best_C = grid_svm.best_params_['estimator__C']\n"
            "plot_learning_curve_chart(\n"
            "    CalibratedClassifierCV(\n"
            "        LinearSVC(C=best_C, class_weight='balanced', random_state=RANDOM_STATE, max_iter=5000),\n"
            "    ),\n"
            "    X_train, y_train, FIGURES_DIR, 'svm_learning_curve.png',\n"
            "    'Learning Curve — SVM Linear (tuned)', cv=5, scoring='f1', random_state=RANDOM_STATE,\n"
            ")\n"
            "print('Biểu đồ đã lưu: svm_learning_curve.png')",
            "co_09_save_lc",
        ),
        cell_md(
            "## 8. Trích xuất & Phân tích Top-20 Đặc trưng Có Trọng số Lớn Nhất (|Coefficient|)",
            "md_10_fi",
        ),
        cell_code(
            "# LinearSVC là mô hình tuyến tính — |hệ số| lớn nghĩa là đặc trưng đóng góp mạnh vào quyết định.\n"
            "# Lấy trung bình |coef_| trên 5 folds calibration để ổn định hơn 1 fold đơn lẻ.\n"
            "fold_coefs = np.array([\n"
            "    cc.estimator.coef_.ravel() for cc in svm_model.calibrated_classifiers_\n"
            "])\n"
            "mean_abs_coefs = np.abs(fold_coefs).mean(axis=0)\n\n"
            "plot_feature_importance(\n"
            "    mean_abs_coefs, feature_names, FIGURES_DIR, 'svm_feature_importance.png',\n"
            "    'Top-20 Đặc trưng |Trọng số| Lớn Nhất — SVM Linear',\n"
            "    top_n=20,\n"
            ")\n\n"
            "top_idx = np.argsort(mean_abs_coefs)[::-1][:20]\n"
            "print('Top-20 đặc trưng có |hệ số| lớn nhất của SVM Linear:')\n"
            "for rank, idx in enumerate(top_idx, 1):\n"
            "    print(f'  {rank:2d}. {feature_names[idx]:32s} |coef|: {mean_abs_coefs[idx]:.4f}')",
            "co_10_save_fi",
        ),
        cell_md("## 9. Đóng gói & Lưu trữ Model (.pkl) và Hồ sơ Chỉ số (.json)", "md_11_save"),
        cell_code(
            "# 1. Lưu trọng số mô hình (đúng đường dẫn quy định trong Phase 06 plan)\n"
            "model_file = MODELS_DIR / 'svm_linear.pkl'\n"
            "joblib.dump(svm_model, model_file)\n\n"
            "# 2. Lưu hồ sơ chỉ số kỹ thuật\n"
            "metrics_record = {\n"
            "    'algorithm': 'SVM Linear (LinearSVC + CalibratedClassifierCV)',\n"
            "    'author': 'Bùi Thị Mỷ Cẩm (MSSV: 25730013)',\n"
            "    'phase': '06 — Modeling (SVM)',\n"
            "    'best_params': grid_svm.best_params_,\n"
            "    'cv_f1_gridsearch': float(grid_svm.best_score_),\n"
            "    'baseline_val_metrics': baseline_val_metrics,\n"
            "    'rbf_kernel_val_metrics_comparison': rbf_val_metrics,\n"
            "    'test_metrics': test_metrics,\n"
            "    'sklearn_version': sklearn.__version__,\n"
            "    'random_state': RANDOM_STATE,\n"
            "    'n_features': len(feature_names),\n"
            "}\n\n"
            "metrics_file = MODELS_DIR / 'svm_metrics.json'\n"
            "with open(metrics_file, 'w', encoding='utf-8') as f:\n"
            "    json.dump(metrics_record, f, ensure_ascii=False, indent=2)\n\n"
            "import os\n"
            "model_size_mb = os.path.getsize(model_file) / (1024 * 1024)\n"
            "print(f'✅ Model saved:   {model_file} ({model_size_mb:.2f} MB)')\n"
            "print(f'✅ Metrics saved: {metrics_file}')\n"
            "print(json.dumps(metrics_record, ensure_ascii=False, indent=2))",
            "co_11_save_artifacts",
        ),
        cell_md(
            "## 10. Đóng gói Hợp đồng Suy luận — `models/best_model_bundle.pkl` (Phase 06 → Phase 08)\n\n"
            "> [!IMPORTANT]\n"
            "> Phase 08 (Demo UI — Sơn) phụ thuộc trực tiếp vào định dạng chính xác của file này. "
            "Bundle gộp `model` + `vectorizer` + `aux_scaler` + `feature_names` để suy luận độc lập "
            "trên văn bản thô, không cần refit gì thêm.",
            "md_12_bundle",
        ),
        cell_code(
            "best_model_bundle = {\n"
            "    'model': svm_model,\n"
            "    'vectorizer': tfidf_vectorizer,\n"
            "    'aux_scaler': aux_scaler,\n"
            "    'feature_names': feature_names,\n"
            "    'model_name': 'SVM Linear',\n"
            "    'threshold': 0.5,\n"
            "    'metrics': {\n"
            "        'f1': test_metrics['f1'],\n"
            "        'recall_scam': test_metrics['recall'],\n"
            "        'precision': test_metrics['precision'],\n"
            "        'roc_auc': test_metrics['roc_auc'],\n"
            "    },\n"
            "    'metadata': {\n"
            "        'algorithm': 'Support Vector Machine (LinearSVC)',\n"
            "        'random_state': RANDOM_STATE,\n"
            "        'sklearn_version': sklearn.__version__,\n"
            "    },\n"
            "}\n\n"
            "bundle_file = MODELS_DIR / 'best_model_bundle.pkl'\n"
            "joblib.dump(best_model_bundle, bundle_file)\n"
            "bundle_size_mb = os.path.getsize(bundle_file) / (1024 * 1024)\n"
            "print(f'✅ Bundle saved: {bundle_file} ({bundle_size_mb:.2f} MB)')",
            "co_12_save_bundle",
        ),
        cell_md(
            "## 11. Kiểm thử Hợp đồng Suy luận End-to-End (Raw Text → Prediction)\n\n"
            "Mô phỏng chính xác luồng suy luận mà Phase 08 (Streamlit) sẽ dùng: tiền xử lý văn bản thô, "
            "trích 15 đặc trưng phụ, chuẩn hóa, ghép TF-IDF, và dự đoán — để phát hiện sớm mọi lỗi lệch "
            "chiều không gian đặc trưng trước khi bàn giao.",
            "md_13_selftest",
        ),
        cell_code(
            "from scipy.sparse import csr_matrix, hstack\n"
            "import pandas as pd\n\n"
            "def predict_raw_text(text: str, bundle: dict) -> dict:\n"
            "    cleaned_text, aux_dict = preprocess_pipeline(text)\n"
            "    aux_df = pd.DataFrame([aux_dict])[AUX_FEATURE_COLS]\n"
            "    aux_scaled = bundle['aux_scaler'].transform(aux_df)\n"
            "    tfidf_vec = bundle['vectorizer'].transform([cleaned_text])\n"
            "    full_vec = hstack([tfidf_vec, csr_matrix(aux_scaled)])\n"
            "    proba = float(bundle['model'].predict_proba(full_vec)[0][1])\n"
            "    label = 1 if proba >= bundle.get('threshold', 0.5) else 0\n"
            "    return {'label': label, 'risk_score': proba}\n\n"
            "sample_scam = 'Chào ông/bà, chúng tôi là công an điều tra, tài khoản của ông/bà liên quan đường dây rửa tiền, chuyển khoản ngay 50 triệu để xác minh kẻo bị bắt giam'\n"
            "sample_normal = 'Ngân hàng thông báo số dư tài khoản của bạn vào ngày hôm nay là 3.250.000 đồng. Cảm ơn quý khách đã sử dụng dịch vụ.'\n\n"
            "loaded_bundle = joblib.load(MODELS_DIR / 'best_model_bundle.pkl')\n"
            "for label_txt, txt in [('SCAM mẫu', sample_scam), ('NORMAL mẫu', sample_normal)]:\n"
            "    result = predict_raw_text(txt, loaded_bundle)\n"
            "    print(f\"[{label_txt}] label={result['label']} ({'Lừa đảo' if result['label'] == 1 else 'Bình thường'}), risk_score={result['risk_score']:.4f}\")",
            "co_13_selftest",
        ),
        cell_md(
            "## 12. Tổng kết Thực nghiệm Phase 06 (SVM)\n\n"
            "- **Hoàn thành:** Huấn luyện SVM Linear (Calibrated) với siêu tham số C tối ưu trên không gian 5.015 chiều Zero-Leakage, đối chứng với SVM RBF.\n"
            "- **Chỉ số đạt được:** Xem `models/svm_metrics.json` — so sánh trực tiếp với Naive Bayes (Phase 04), XGBoost & Random Forest (Phase 05).\n"
            "- **Hợp đồng bàn giao:** `models/best_model_bundle.pkl` đã đóng gói đầy đủ model + vectorizer + aux_scaler + feature_names, kiểm thử end-to-end thành công trên văn bản thô.\n"
            "- **Sẵn sàng:** Phase 07 (So sánh chéo 4 mô hình & XAI — Thanh) và Phase 08 (Demo UI Streamlit — Sơn).\n"
            "- **PhoBERT (Optional):** Không thực hiện trong sprint này do giới hạn thời gian/GPU trước hạn bảo vệ 23/09 — có thể bổ sung sau nếu còn dư thời gian.",
            "md_14_conclusion",
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
    warnings.filterwarnings("ignore")

    print("=" * 70)
    print("  CS114 NHÓM 10 — HUẤN LUYỆN SVM MODEL (BÙI THỊ MỶ CẨM)")
    print("=" * 70)

    # 1. Nạp dữ liệu
    print("[1/7] Nạp ma trận đặc trưng Zero-Leakage từ data/processed/...")
    X_train = joblib.load(DATA_DIR / "X_train.pkl")
    X_test = joblib.load(DATA_DIR / "X_test.pkl")
    y_train = joblib.load(DATA_DIR / "y_train.pkl")
    y_test = joblib.load(DATA_DIR / "y_test.pkl")
    with open(DATA_DIR / "feature_names.json", encoding="utf-8") as f:
        feature_names = json.load(f)
    tfidf_vectorizer = joblib.load(DATA_DIR / "tfidf_vectorizer.pkl")
    aux_scaler = joblib.load(DATA_DIR / "aux_scaler.pkl")

    print(f"  X_train: {X_train.shape} | y_train: {y_train.shape}")
    print(f"  X_test:  {X_test.shape}  | y_test:  {y_test.shape}")
    print(f"  Feature dimensions: {len(feature_names)}")

    # 2. Validation Split
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train, y_train, test_size=0.15, random_state=RANDOM_STATE, stratify=y_train
    )

    # 3. Baseline SVM Linear
    print("\n[2/7] Huấn luyện Baseline SVM Linear (LinearSVC + CalibratedClassifierCV)...")
    svm_base = LinearSVC(C=1.0, class_weight="balanced", random_state=RANDOM_STATE, max_iter=5000)
    svm_baseline = CalibratedClassifierCV(svm_base, cv=5)
    t0 = time.time()
    svm_baseline.fit(X_tr, y_tr)
    print(f"  Baseline fit xong trong {time.time()-t0:.2f}s")
    y_val_pred = svm_baseline.predict(X_val)
    y_val_proba = svm_baseline.predict_proba(X_val)[:, 1]
    baseline_val_metrics = compute_metrics(y_val, y_val_pred, y_val_proba)
    print("  Baseline Validation Metrics:", baseline_val_metrics)

    # 4. SVM RBF comparison
    print("\n[3/7] Huấn luyện SVM RBF đối chứng (X_tr/X_val)...")
    svm_rbf = SVC(
        kernel="rbf", C=1.0, gamma="scale", class_weight="balanced",
        random_state=RANDOM_STATE, probability=True,
    )
    t0 = time.time()
    svm_rbf.fit(X_tr, y_tr)
    print(f"  RBF fit xong trong {time.time()-t0:.2f}s")
    y_val_pred_rbf = svm_rbf.predict(X_val)
    y_val_proba_rbf = svm_rbf.predict_proba(X_val)[:, 1]
    rbf_val_metrics = compute_metrics(y_val, y_val_pred_rbf, y_val_proba_rbf)
    print("  RBF Validation Metrics:", rbf_val_metrics)
    print(
        f"  Linear F1={baseline_val_metrics['f1']:.4f} vs RBF F1={rbf_val_metrics['f1']:.4f} "
        "-> giữ Linear làm lựa chọn chính thức."
    )

    # 5. Hyperparameter Tuning
    print("\n[4/7] Tinh chỉnh siêu tham số C với GridSearchCV (4 giá trị, 5-fold CV)...")
    param_grid = {"estimator__C": [0.01, 0.1, 1.0, 10.0]}
    grid_svm = GridSearchCV(
        CalibratedClassifierCV(
            LinearSVC(class_weight="balanced", random_state=RANDOM_STATE, max_iter=5000)
        ),
        param_grid, cv=5, scoring="f1", n_jobs=-1,
    )
    t0 = time.time()
    grid_svm.fit(X_train, y_train)
    print(f"  Tuning hoàn tất trong {time.time()-t0:.1f}s")
    print("  Best Parameters:", grid_svm.best_params_)
    print(f"  Best 5-Fold CV F1: {grid_svm.best_score_:.4f}")

    # 6. Đánh giá trên Test Set
    print("\n[5/7] Đánh giá trên tập kiểm thử độc lập X_test (439 mẫu)...")
    svm_model = grid_svm.best_estimator_
    y_test_pred = svm_model.predict(X_test)
    y_test_proba = svm_model.predict_proba(X_test)[:, 1]
    test_metrics = compute_metrics(y_test, y_test_pred, y_test_proba)

    print("=" * 60)
    print("           KẾT QUẢ TEST SET — SVM LINEAR TUNED")
    print("=" * 60)
    for k, v in test_metrics.items():
        print(f"  {k:15s}: {v:.4f}")
    print("-" * 60)
    print(classification_report(y_test, y_test_pred, target_names=["Bình thường (0)", "Lừa đảo (1)"], digits=4))
    print("=" * 60)

    # 7. Vẽ biểu đồ
    print("\n[6/7] Xuất 4 biểu đồ học thuật 300 DPI...")
    plot_confusion_matrix(
        y_test, y_test_pred, FIGURES_DIR, "svm_confusion_matrix.png",
        "Confusion Matrix — SVM Linear (Test Set)",
    )
    auc_score = plot_roc_curve(
        y_test, y_test_proba, FIGURES_DIR, "svm_roc_curve.png",
        "ROC Curve — SVM Linear (Test Set)",
    )
    print(f"  ROC-AUC: {auc_score:.4f}")

    print("  Đang sinh Learning Curve (5-Fold CV)...")
    best_C = grid_svm.best_params_["estimator__C"]
    plot_learning_curve_chart(
        CalibratedClassifierCV(
            LinearSVC(C=best_C, class_weight="balanced", random_state=RANDOM_STATE, max_iter=5000)
        ),
        X_train, y_train, FIGURES_DIR, "svm_learning_curve.png",
        "Learning Curve — SVM Linear (tuned)", cv=5, scoring="f1", random_state=RANDOM_STATE,
    )

    fold_coefs = np.array([cc.estimator.coef_.ravel() for cc in svm_model.calibrated_classifiers_])
    mean_abs_coefs = np.abs(fold_coefs).mean(axis=0)
    plot_feature_importance(
        mean_abs_coefs, feature_names, FIGURES_DIR, "svm_feature_importance.png",
        "Top-20 Đặc trưng |Trọng số| Lớn Nhất — SVM Linear", top_n=20,
    )

    # 8. Lưu artifacts
    print("\n[7/7] Lưu trữ model, metrics, bundle và notebook...")
    model_file = MODELS_DIR / "svm_linear.pkl"
    joblib.dump(svm_model, model_file)

    metrics_record = {
        "algorithm": "SVM Linear (LinearSVC + CalibratedClassifierCV)",
        "author": "Bùi Thị Mỷ Cẩm (MSSV: 25730013)",
        "phase": "06 — Modeling (SVM)",
        "best_params": grid_svm.best_params_,
        "cv_f1_gridsearch": float(grid_svm.best_score_),
        "baseline_val_metrics": baseline_val_metrics,
        "rbf_kernel_val_metrics_comparison": rbf_val_metrics,
        "test_metrics": test_metrics,
        "sklearn_version": sklearn.__version__,
        "random_state": RANDOM_STATE,
        "n_features": len(feature_names),
    }
    metrics_file = MODELS_DIR / "svm_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics_record, f, ensure_ascii=False, indent=2)

    # Interface contract bundle for Phase 08
    best_model_bundle = {
        "model": svm_model,
        "vectorizer": tfidf_vectorizer,
        "aux_scaler": aux_scaler,
        "feature_names": feature_names,
        "model_name": "SVM Linear",
        "threshold": 0.5,
        "metrics": {
            "f1": test_metrics["f1"],
            "recall_scam": test_metrics["recall"],
            "precision": test_metrics["precision"],
            "roc_auc": test_metrics["roc_auc"],
        },
        "metadata": {
            "algorithm": "Support Vector Machine (LinearSVC)",
            "random_state": RANDOM_STATE,
            "sklearn_version": sklearn.__version__,
        },
    }
    bundle_file = MODELS_DIR / "best_model_bundle.pkl"
    joblib.dump(best_model_bundle, bundle_file)

    # End-to-end self-test of the inference contract (raw text -> prediction)
    from scipy.sparse import csr_matrix, hstack
    import pandas as pd

    def predict_raw_text(text: str, bundle: dict) -> dict:
        cleaned_text, aux_dict = preprocess_pipeline(text)
        aux_df = pd.DataFrame([aux_dict])[AUX_FEATURE_COLS]
        aux_scaled = bundle["aux_scaler"].transform(aux_df)
        tfidf_vec = bundle["vectorizer"].transform([cleaned_text])
        full_vec = hstack([tfidf_vec, csr_matrix(aux_scaled)])
        proba = float(bundle["model"].predict_proba(full_vec)[0][1])
        label = 1 if proba >= bundle.get("threshold", 0.5) else 0
        return {"label": label, "risk_score": proba}

    loaded_bundle = joblib.load(bundle_file)
    sample_scam = (
        "Chào ông/bà, chúng tôi là công an điều tra, tài khoản của ông/bà liên quan đường dây "
        "rửa tiền, chuyển khoản ngay 50 triệu để xác minh kẻo bị bắt giam"
    )
    sample_normal = (
        "Ngân hàng thông báo số dư tài khoản của bạn vào ngày hôm nay là 3.250.000 đồng. "
        "Cảm ơn quý khách đã sử dụng dịch vụ."
    )
    print("\n  --- Self-test hợp đồng suy luận (raw text -> prediction) ---")
    for label_txt, txt in [("SCAM mẫu", sample_scam), ("NORMAL mẫu", sample_normal)]:
        result = predict_raw_text(txt, loaded_bundle)
        print(f"  [{label_txt}] label={result['label']}, risk_score={result['risk_score']:.4f}")

    # Sinh notebook chuẩn
    nb_dict = build_notebook_structure()
    with open(NB_PATH, "w", encoding="utf-8") as f:
        json.dump(nb_dict, f, ensure_ascii=False, indent=1)

    model_size_mb = os.path.getsize(model_file) / (1024 * 1024)
    bundle_size_mb = os.path.getsize(bundle_file) / (1024 * 1024)
    nb_size_kb = os.path.getsize(NB_PATH) / 1024

    print(f"\n  Model saved:   {model_file} ({model_size_mb:.2f} MB)")
    print(f"  Metrics saved: {metrics_file}")
    print(f"  Bundle saved:  {bundle_file} ({bundle_size_mb:.2f} MB)")
    print(f"  Notebook:      {NB_PATH} ({nb_size_kb:.1f} KB)")
    print("\n✅ HOÀN TẤT HUẤN LUYỆN VÀ XUẤT BẢN ARTIFACTS SVM 100% XUẤT SẮC!")


if __name__ == "__main__":
    run_pipeline()
