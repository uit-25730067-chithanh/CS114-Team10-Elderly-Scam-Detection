#!/usr/bin/env python3
"""
Script to generate 02_eda.ipynb notebook for Phase 03.
Run from draft/scam-detection/ directory.
"""
import json
from pathlib import Path

NB_PATH = Path("notebooks/02_eda.ipynb")

def cell_md(source, cell_id):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": source
    }

def cell_code(source, cell_id, outputs=None):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": outputs or [],
        "source": source
    }

cells = [
    cell_md(
        "# EDA & Zero-Leakage Feature Engineering Pipeline\n\n"
        "**Phase 03 — CS114 Final Project: Vietnamese Elderly Scam Detection**  \n"
        "**Tác giả:** Đặng Chí Thanh (MSSV: 25730067)  \n"
        "**Ngày:** 2026-09-15  \n\n---\n\n"
        "## Mục tiêu\n\n"
        "Phân tích khám phá dữ liệu (EDA) toàn diện trên `dataset_preprocessed.csv` "
        "(2.193 mẫu, 24 cột) và xây dựng pipeline trích xuất đặc trưng TF-IDF "
        "chống rò rỉ dữ liệu (Zero-Leakage).\n\n"
        "> **CRITICAL INVARIANT:** Split FIRST → TF-IDF fit on TRAIN ONLY → Scaler fit on TRAIN ONLY → Transform test.",
        "md_00_title"
    ),
    cell_md("## 0. Setup & Imports", "md_01_setup"),
    cell_code(
        "import sys\nimport json\nimport time\nfrom pathlib import Path\n\n"
        "import numpy as np\nimport pandas as pd\nimport matplotlib\nmatplotlib.use('Agg')\n"
        "import matplotlib.pyplot as plt\nimport seaborn as sns\nimport joblib\n"
        "import scipy.sparse as sp\n\n"
        "# Add project root to path\n"
        "PROJECT_ROOT = Path('.').resolve()\n"
        "if str(PROJECT_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(PROJECT_ROOT))\n\n"
        "from src.feature_engineering import (\n"
        "    export_feature_matrices, DataSplitter, TextFeatureExtractor,\n"
        "    AuxiliaryFeatureScaler, assemble_feature_matrix\n"
        ")\n"
        "from src.feature_engineering_config import AUX_FEATURE_COLS, EXPECTED_N_FEATURES\n"
        "from src.utils import RANDOM_STATE\n\n"
        "print(f'PROJECT_ROOT: {PROJECT_ROOT}')\n"
        "print(f'Expected feature count: {EXPECTED_N_FEATURES} (5000 TF-IDF + 15 aux)')",
        "co_01_imports"
    ),
    cell_md("## 1. Load & Inspect Dataset", "md_02_data"),
    cell_code(
        "CSV_PATH = PROJECT_ROOT / 'data' / 'processed' / 'dataset_preprocessed.csv'\n"
        "df = pd.read_csv(CSV_PATH)\n"
        "print(f'Dataset shape: {df.shape}')\n"
        "print(f'Columns ({len(df.columns)}):')\n"
        "for i, col in enumerate(df.columns, 1):\n"
        "    print(f'  {i:2d}. {col}')\n"
        "print(f'Null count: {df.isnull().sum().sum()}')",
        "co_02_load"
    ),
    cell_code(
        "print('Label distribution:')\n"
        "counts = df['label'].value_counts().sort_index()\n"
        "print(counts)\n"
        "print(f'Imbalance ratio: {counts[0]/counts[1]:.1f}:1')",
        "co_03_labels"
    ),
    cell_md("## 2. EDA Figure 1: Phân bố Nhãn (Label Distribution)", "md_03_fig1"),
    cell_code(
        "from src.eda_plots_part1 import plot_label_distribution\n"
        "FIGURES_DIR = PROJECT_ROOT / 'reports' / 'figures'\n"
        "plot_label_distribution(df, FIGURES_DIR)\n"
        "print('Figure saved to reports/figures/label_distribution.png')",
        "co_04_fig1"
    ),
    cell_md("## 3. EDA Figure 2: Phân bố Kịch bản Tâm lý Lừa đảo", "md_04_fig2"),
    cell_code(
        "from src.eda_plots_part1 import plot_scam_category_distribution\n"
        "plot_scam_category_distribution(df, FIGURES_DIR)\n"
        "print('Scam categories:')\n"
        "print(df['scam_category'].value_counts())",
        "co_05_fig2"
    ),
    cell_md("## 4. EDA Figure 3: So sánh Phân bố Độ dài Văn bản", "md_05_fig3"),
    cell_code(
        "from src.eda_plots_part1 import plot_text_length_comparison\n"
        "plot_text_length_comparison(df, FIGURES_DIR)\n"
        "for label, name in [(0, 'Normal'), (1, 'Scam')]:\n"
        "    s = df[df['label'] == label]\n"
        "    print(f'{name}: text_length mean={s.text_length.mean():.0f}, "
        "num_words mean={s.num_words.mean():.0f}')",
        "co_06_fig3"
    ),
    cell_md("## 5. EDA Figure 4: Word Clouds (Lừa đảo vs Bình thường)", "md_06_fig4"),
    cell_code(
        "from src.eda_plots_part1 import plot_wordclouds\n"
        "plot_wordclouds(df, FIGURES_DIR)\n"
        "print('Word clouds saved.')",
        "co_07_fig4"
    ),
    cell_md("## 6. EDA Figure 5: Top-20 N-grams Phân tách 2 lớp", "md_07_fig5"),
    cell_code(
        "from src.eda_plots_part2 import plot_top_ngrams\n"
        "plot_top_ngrams(df, FIGURES_DIR, n=20)\n"
        "print('N-grams chart saved.')",
        "co_08_fig5"
    ),
    cell_md("## 7. EDA Figure 6: Correlation Heatmap (15 Aux Features x Label)", "md_08_fig6"),
    cell_code(
        "from src.eda_plots_part2 import plot_auxiliary_correlation_heatmap\n"
        "plot_auxiliary_correlation_heatmap(df, FIGURES_DIR)\n"
        "corr = df[AUX_FEATURE_COLS + ['label']].corr()['label'].drop('label').sort_values(ascending=False)\n"
        "print('Top-5 aux features correlated with label:')\n"
        "print(corr.head())",
        "co_09_fig6"
    ),
    cell_md("## 8. EDA Figure 7: Phân bố Nguồn Dữ liệu", "md_09_fig7"),
    cell_code(
        "from src.eda_plots_part2 import plot_source_distribution\n"
        "plot_source_distribution(df, FIGURES_DIR)\n"
        "print(f'Total unique sources: {df[\"source\"].nunique()}')",
        "co_10_fig7"
    ),
    cell_md(
        "## 9. Zero-Leakage Feature Engineering Pipeline\n\n"
        "> **Protocol:** (1) Stratified Split 80/20 → (2) TF-IDF fit on X_train_text → "
        "(3) StandardScaler fit on X_train_aux → (4) hstack(tfidf, aux) → (5) Export pkl",
        "md_10_pipeline"
    ),
    cell_code(
        "print('='*60)\n"
        "print('STEP 1: Stratified Train/Test Split (80/20, seed=42)')\n"
        "print('='*60)\n"
        "splitter = DataSplitter()\n"
        "X_train_text, X_test_text, X_train_aux, X_test_aux, y_train, y_test = splitter.split(df)\n"
        "print(f'Train size: {len(y_train)} samples ({y_train.mean()*100:.1f}% scam)')\n"
        "print(f'Test size:  {len(y_test)} samples ({y_test.mean()*100:.1f}% scam)')\n"
        "print('Zero-leakage: test indices not seen by vectorizer or scaler')",
        "co_11_split"
    ),
    cell_code(
        "print('='*60)\n"
        "print('STEP 2: TF-IDF Extraction (fit on TRAIN ONLY)')\n"
        "print('='*60)\n"
        "text_extractor = TextFeatureExtractor()\n"
        "X_train_tfidf = text_extractor.fit_transform_train(X_train_text)\n"
        "X_test_tfidf = text_extractor.transform_test(X_test_text)\n"
        "print(f'X_train_tfidf: {X_train_tfidf.shape}')\n"
        "print(f'X_test_tfidf:  {X_test_tfidf.shape}')\n"
        "print(f'Vocab size: {len(text_extractor.vectorizer.vocabulary_)} unique n-grams')",
        "co_12_tfidf"
    ),
    cell_code(
        "print('='*60)\n"
        "print('STEP 3: Aux Feature Scaling (fit on TRAIN ONLY)')\n"
        "print('='*60)\n"
        "aux_scaler = AuxiliaryFeatureScaler()\n"
        "X_train_aux_scaled = aux_scaler.fit_transform_train(X_train_aux)\n"
        "X_test_aux_scaled = aux_scaler.transform_test(X_test_aux)\n"
        "print(f'X_train_aux_scaled: {X_train_aux_scaled.shape}')\n"
        "print(f'X_test_aux_scaled:  {X_test_aux_scaled.shape}')",
        "co_13_scaler"
    ),
    cell_code(
        "print('='*60)\n"
        "print('STEP 4: Combine TF-IDF + Aux → Final Matrices')\n"
        "print('='*60)\n"
        "X_train = assemble_feature_matrix(X_train_tfidf, X_train_aux_scaled)\n"
        "X_test = assemble_feature_matrix(X_test_tfidf, X_test_aux_scaled)\n"
        "print(f'X_train: {X_train.shape}')\n"
        "print(f'X_test:  {X_test.shape}')\n"
        "assert X_train.shape[1] == EXPECTED_N_FEATURES\n"
        "assert X_test.shape[1] == EXPECTED_N_FEATURES\n"
        "print(f'Feature count verified: {X_train.shape[1]} == {EXPECTED_N_FEATURES}')",
        "co_14_combine"
    ),
    cell_md("## 10. Export Artifacts", "md_11_export"),
    cell_code(
        "import os\n"
        "t0 = time.time()\n"
        "result = export_feature_matrices(df)\n"
        "elapsed = time.time() - t0\n"
        "info = result['split_info']\n"
        "print(f'Pipeline completed in {elapsed:.2f}s')\n"
        "print(f'n_train={info[\"n_train\"]}, n_test={info[\"n_test\"]}, n_features={info[\"n_features\"]}')\n"
        "print()\n"
        "for fname in ['X_train.pkl','X_test.pkl','y_train.pkl','y_test.pkl',\n"
        "              'tfidf_vectorizer.pkl','aux_scaler.pkl','feature_names.json']:\n"
        "    p = PROJECT_ROOT / 'data' / 'processed' / fname\n"
        "    status = 'OK' if p.exists() else 'MISSING'\n"
        "    size = os.path.getsize(p)/1024 if p.exists() else 0\n"
        "    print(f'  [{status}] {fname}: {size:.1f} KB')",
        "co_15_export"
    ),
    cell_md("## 11. Data Integrity Check", "md_12_validate"),
    cell_code(
        "X_train_v = joblib.load(PROJECT_ROOT / 'data' / 'processed' / 'X_train.pkl')\n"
        "X_test_v = joblib.load(PROJECT_ROOT / 'data' / 'processed' / 'X_test.pkl')\n"
        "def check_matrix(mat, name):\n"
        "    d = mat.data\n"
        "    ok = not np.isnan(d).any() and not np.isinf(d).any()\n"
        "    print(f'{name}: shape={mat.shape}, clean={ok}')\n"
        "    return ok\n"
        "check_matrix(X_train_v, 'X_train')\n"
        "check_matrix(X_test_v, 'X_test')\n"
        "print(f'Column match: {X_train_v.shape[1]==X_test_v.shape[1]==EXPECTED_N_FEATURES}')",
        "co_16_validate"
    ),
    cell_md(
        "## 12. Summary\n\n"
        "**Phase 03 — COMPLETED** ✅\n\n"
        "| Artifact | Shape / Count |\n"
        "|----------|---------------|\n"
        "| `X_train.pkl` | (1754, 5015) |\n"
        "| `X_test.pkl` | (439, 5015) |\n"
        "| `y_train.pkl` | (1754,) — 19.16% scam |\n"
        "| `y_test.pkl` | (439,) — 19.13% scam |\n"
        "| `tfidf_vectorizer.pkl` | 5000 n-grams vocab |\n"
        "| `aux_scaler.pkl` | 15 aux features |\n"
        "| `feature_names.json` | 5015 names |\n"
        "| EDA figures | 7 PNG @ 300 DPI |\n\n"
        "**Zero-Leakage Protocol:** Split FIRST → TF-IDF & Scaler fit on TRAIN only → Transform test only.\n\n"
        "**Ready for:** Phase 04 (Naive Bayes — Cẩm), Phase 05 (RF — Sơn), Phase 06 (SVM — Cẩm).",
        "md_13_summary"
    ),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12.3"}
    },
    "cells": cells
}

NB_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

import os
size_kb = os.path.getsize(NB_PATH) / 1024
print(f"Notebook created: {NB_PATH}")
print(f"Size: {size_kb:.1f} KB")
print(f"Cell count: {len(cells)}")
