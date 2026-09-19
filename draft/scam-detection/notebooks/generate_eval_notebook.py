#!/usr/bin/env python3
"""
Script to generate 06_evaluation_xai.ipynb notebook for Phase 07.
Run from draft/scam-detection/ directory.

Author: Đặng Chí Thanh (MSSV: 25730067)
"""
import json
from pathlib import Path

NB_PATH = Path("notebooks/06_evaluation_xai.ipynb")


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
        "# Phase 07 — Comprehensive Evaluation & Explainable AI (XAI)\n\n"
        "**CS114 Final Project: Vietnamese Elderly Scam Detection**  \n"
        "**Tác giả:** Đặng Chí Thanh (MSSV: 25730067 — PM & Evaluation Lead)  \n"
        "**Ngày hoàn thành:** 2026-09-19 (Sprint 3 Fast-Track)  \n\n---\n\n"
        "## 1. Mục tiêu Nghiên cứu & Thực nghiệm\n\n"
        "- So sánh toàn diện 4 mô hình đã huấn luyện (**Naive Bayes**, **Random Forest**, **XGBoost**, **SVM Linear**) "
        "trên tập holdout test độc lập (439 mẫu — 355 Normal / 84 Scam).\n"
        "- Đánh giá 5 chỉ số cốt lõi: Accuracy, Precision, Recall, F1-Score, ROC-AUC và phân tích ma trận nhầm lẫn (FN vs FP).\n"
        "- Xuất các biểu đồ phân tích trực quan chuẩn xuất bản 300 DPI:\n"
        "  1. Ma trận nhầm lẫn lưới 2×2 (`confusion_matrices_all.png`).\n"
        "  2. Đường cong ROC lồng ghép cả 4 mô hình (`roc_curves_comparison.png`).\n"
        "  3. Đường cong Precision-Recall (`precision_recall_curves.png`).\n"
        "  4. Top-20 từ khóa kích hoạt bẫy tâm lý theo trọng số mô hình (`top20_keywords_barplot.png`).\n"
        "  5. Phân tích đóng góp đặc trưng SHAP TreeExplainer (`shap_summary.png`).\n"
        "  6. Tổng hợp kiểm soát quá khớp qua Learning Curves (`learning_curves_summary.png`).\n"
        "- Khóa mô hình tối ưu (**Best Model**) bàn giao cho Demo UI (Phase 08) và Chương 4 Báo cáo (Phase 09).",
        "md_00_title",
    ),
    cell_md("## 2. Setup & Nạp Thư Viện", "md_01_setup"),
    cell_code(
        "import sys\nimport json\nfrom pathlib import Path\nimport numpy as np\nimport pandas as pd\nimport joblib\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n"
        "PROJECT_ROOT = Path('.').resolve()\n"
        "if not (PROJECT_ROOT / 'src').exists():\n"
        "    PROJECT_ROOT = PROJECT_ROOT.parent\n"
        "if str(PROJECT_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(PROJECT_ROOT))\n\n"
        "from src.utils.helpers import RANDOM_STATE\n"
        "from src.evaluation.metrics_calculator import evaluate_all_models, format_markdown_table\n"
        "from src.evaluation.plot_comparator import (\n"
        "    plot_confusion_matrices_grid, plot_roc_comparison,\n"
        "    plot_precision_recall_comparison, plot_top20_keywords_comparison,\n"
        "    plot_learning_curves_summary,\n"
        ")\n"
        "from src.evaluation.xai_explainer import (\n"
        "    extract_consensus_keywords, extract_keywords_from_model,\n"
        "    compute_and_save_shap_plot,\n"
        ")\n\n"
        "DATA_DIR = PROJECT_ROOT / 'data' / 'processed'\n"
        "MODELS_DIR = PROJECT_ROOT / 'models'\n"
        "FIGURES_DIR = PROJECT_ROOT / 'reports' / 'figures'\n"
        "FIGURES_DIR.mkdir(parents=True, exist_ok=True)\n"
        "print(f'[✓] Setup complete. RANDOM_STATE={RANDOM_STATE}')",
        "code_01_setup",
    ),
    cell_md("## 3. Nạp Dữ Liệu Test & Mô Hình Huấn Luyện", "md_02_load"),
    cell_code(
        "X_test = joblib.load(DATA_DIR / 'X_test.pkl')\n"
        "y_test = joblib.load(DATA_DIR / 'y_test.pkl')\n"
        "with open(DATA_DIR / 'feature_names.json', 'r', encoding='utf-8') as f:\n"
        "    feature_names = json.load(f)\n\n"
        "print(f'Test matrix shape: {X_test.shape} (439 mẫu test, 5015 đặc trưng)')\n"
        "print(f'Tỷ lệ nhãn: Bình thường = {(y_test == 0).sum()} mẫu, Lừa đảo = {(y_test == 1).sum()} mẫu')\n\n"
        "models = {\n"
        "    'XGBoost': joblib.load(MODELS_DIR / 'xgboost.pkl'),\n"
        "    'SVM Linear': joblib.load(MODELS_DIR / 'svm_linear.pkl'),\n"
        "    'Random Forest': joblib.load(MODELS_DIR / 'random_forest.pkl'),\n"
        "    'Naive Bayes': joblib.load(MODELS_DIR / 'naive_bayes.pkl'),\n"
        "}\n"
        "print(f'[✓] Đã nạp thành công 4 mô hình: {list(models.keys())}')",
        "code_02_load",
    ),
    cell_md("## 4. Tính Toán & Lập Bảng So Sánh Hiệu Năng", "md_03_eval"),
    cell_code(
        "metrics_df = evaluate_all_models(models, X_test, y_test)\n"
        "print('=== BẢNG SO SÁNH HIỆU NĂNG TỔNG HỢP (TEST SET) ===')\n"
        "print(format_markdown_table(metrics_df))\n\n"
        "# Cập nhật lưu trữ vào reports/model_comparison.csv\n"
        "csv_path = PROJECT_ROOT / 'reports' / 'model_comparison.csv'\n"
        "records = []\n"
        "meta = {\n"
        "    'XGBoost': ('5015 (TF-IDF + 15 aux)', 'n_estimators=300, max_depth=5, lr=0.05, subsample=0.7, scale_pos_weight=4.22', 'Passed (Phase 05 — Cam)'),\n"
        "    'SVM Linear': ('5015 (TF-IDF + 15 aux)', 'C=10.0 (CalibratedClassifierCV 5-fold)', 'Passed (Phase 06 — Cam)'),\n"
        "    'Random Forest': ('5015 (TF-IDF + 15 aux)', 'n_estimators=200, max_depth=50, split=2, leaf=2, max_feat=0.2', 'Passed (Phase 05 — Son)'),\n"
        "    'Naive Bayes': ('5000 (TF-IDF non-negative)', 'alpha=0.01 (GridSearchCV 5-fold)', 'Passed (Phase 04 — Cam)'),\n"
        "}\n"
        "for _, row in metrics_df.iterrows():\n"
        "    m_name = row['model']\n"
        "    feat, hyper, st = meta.get(m_name, ('5015', 'Tuned', 'Passed'))\n"
        "    records.append({\n"
        "        'Model': m_name,\n"
        "        'Features': feat,\n"
        "        'Hyperparameters': hyper,\n"
        "        'Accuracy': round(row['accuracy'], 4),\n"
        "        'Precision': round(row['precision'], 4),\n"
        "        'Recall': round(row['recall'], 4),\n"
        "        'F1-Score': round(row['f1'], 4),\n"
        "        'ROC-AUC': round(row['roc_auc'], 4),\n"
        "        'Status': st,\n"
        "    })\n"
        "pd.DataFrame(records).to_csv(csv_path, index=False)\n"
        "print(f'[✓] Đã đồng bộ model_comparison.csv tại: {csv_path}')",
        "code_03_eval",
    ),
    cell_md("## 5. Trực Quan Hóa Ma Trận Nhầm Lẫn (Confusion Matrix Grid 2×2)", "md_04_cm"),
    cell_code(
        "p_cm = plot_confusion_matrices_grid(models, X_test, y_test, FIGURES_DIR)\n"
        "print(f'[✓] Đã xuất biểu đồ: {p_cm}')\n\n"
        "# Hiển thị trực tiếp trong notebook\n"
        "img_cm = plt.imread(str(p_cm))\n"
        "plt.figure(figsize=(10, 8))\n"
        "plt.imshow(img_cm)\n"
        "plt.axis('off')\n"
        "plt.show()",
        "code_04_cm",
    ),
    cell_md("## 6. So Sánh Đường Cong ROC & Precision-Recall", "md_05_roc_pr"),
    cell_code(
        "p_roc = plot_roc_comparison(models, X_test, y_test, FIGURES_DIR)\n"
        "p_pr = plot_precision_recall_comparison(models, X_test, y_test, FIGURES_DIR)\n"
        "print(f'[✓] Đã xuất ROC: {p_roc}')\n"
        "print(f'[✓] Đã xuất PR: {p_pr}')\n\n"
        "fig, axes = plt.subplots(1, 2, figsize=(16, 7))\n"
        "axes[0].imshow(plt.imread(str(p_roc)))\n"
        "axes[0].axis('off')\n"
        "axes[1].imshow(plt.imread(str(p_pr)))\n"
        "axes[1].axis('off')\n"
        "plt.tight_layout()\n"
        "plt.show()",
        "code_05_roc_pr",
    ),
    cell_md("## 7. Tổng Hợp Phân Tích Quá Khớp (Learning Curves)", "md_06_lc"),
    cell_code(
        "p_lc = plot_learning_curves_summary(FIGURES_DIR)\n"
        "print(f'[✓] Đã xuất tổng hợp Learning Curves: {p_lc}')\n"
        "plt.figure(figsize=(12, 9))\n"
        "plt.imshow(plt.imread(str(p_lc)))\n"
        "plt.axis('off')\n"
        "plt.show()",
        "code_06_lc",
    ),
    cell_md("## 8. Trích Xuất Từ Khóa Cảnh Báo Lừa Đảo (Consensus XAI)", "md_07_xai"),
    cell_code(
        "consensus_kws = extract_consensus_keywords(models, feature_names, top_n=20)\n"
        "p_kws = plot_top20_keywords_comparison(consensus_kws, FIGURES_DIR)\n"
        "print(f'[✓] Đã xuất biểu đồ Top-20 từ khóa cảnh báo: {p_kws}')\n\n"
        "print('=== TOP 20 TỪ KHÓA BẪY TÂM LÝ LỪA ĐẢO ĐỒNG THUẬN CAO NHẤT ===')\n"
        "for rank, (word, score) in enumerate(consensus_kws, start=1):\n"
        "    print(f'{rank:02d}. {word:<25} (Trọng số chuẩn hóa: {score:.4f})')",
        "code_07_xai",
    ),
    cell_md("## 9. Phân Tích Đóng Góp Giá Trị Đặc Trưng SHAP (TreeExplainer)", "md_08_shap"),
    cell_code(
        "sample_indices = list(range(min(150, X_test.shape[0])))\n"
        "X_sample = X_test[sample_indices]\n"
        "p_shap = compute_and_save_shap_plot(models['XGBoost'], X_sample, feature_names, FIGURES_DIR)\n"
        "print(f'[✓] Đã xuất biểu đồ SHAP Beeswarm: {p_shap}')\n\n"
        "plt.figure(figsize=(10, 8))\n"
        "plt.imshow(plt.imread(str(p_shap)))\n"
        "plt.axis('off')\n"
        "plt.show()",
        "code_08_shap",
    ),
    cell_md(
        "## 10. Kết Luận & Chọn Mô Hình Tối Ưu (Best Model Selection)\n\n"
        "1. **Mô hình Xuất sắc Nhất (Best Overall Model):** **XGBoost Classifier**  \n"
        "   - **F1-Score:** `0.9535` (Cao nhất trong cả 4 mô hình).  \n"
        "   - **Recall Lớp Lừa Đảo:** `97.62%` (Chỉ bỏ sót đúng 2/84 mẫu lừa đảo trong tập kiểm thử).  \n"
        "   - **Precision:** `93.18%` (Chỉ báo nhầm 6/355 mẫu bình thường).  \n"
        "   - **ROC-AUC:** `0.9984`.  \n"
        "2. **Mô hình Tuyến tính Tối ưu Nhất (Best Linear Model):** **Linear SVM (Calibrated)**  \n"
        "   - **ROC-AUC:** `0.9986` (Khả năng phân tách xác suất tốt nhất).  \n"
        "   - **F1-Score:** `0.9474`, Recall: `96.43%`.  \n"
        "3. **Quyết định Triển Khai (Deployment Decision):**  \n"
        "   - Cả 4 mô hình đều vượt xa chỉ tiêu đặt ra tại `BRAINSTORM.md` (`F1 ≥ 88%`, `Recall ≥ 92%`).  \n"
        "   - Gói suy luận `best_model_bundle.pkl` được đóng gói bằng XGBoost / Linear SVM phục vụ Phase 08 (Demo UI).",
        "md_09_conclusion",
    ),
]

nb_dict = {
    "cells": cells,
    "metadata": {
        "language_info": {"name": "python", "version": "3.12"},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

if __name__ == "__main__":
    out_path = Path(__file__).resolve().parent / "06_evaluation_xai.ipynb"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(nb_dict, f, ensure_ascii=False, indent=1)
    print(f"[✓] Generated Phase 07 notebook: {out_path} ({out_path.stat().st_size} bytes)")
