"""
CS114 Final Project — Scam Detection
Orchestrator for Phase 07 Full Evaluation & XAI Generation.

Loads models, evaluates on test set, produces 4-model comparison figures,
computes SHAP analysis, and updates reports/model_comparison.csv.

Author: Đặng Chí Thanh (MSSV: 25730067)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import pandas as pd

from src.evaluation.metrics_calculator import evaluate_all_models, format_markdown_table
from src.evaluation.plot_comparator import (
    plot_confusion_matrices_grid,
    plot_learning_curves_summary,
    plot_precision_recall_comparison,
    plot_roc_comparison,
    plot_top20_keywords_comparison,
)
from src.evaluation.xai_explainer import (
    compute_and_save_shap_plot,
    extract_consensus_keywords,
    extract_keywords_from_model,
)


def run_evaluation(project_root: Path) -> dict:
    """Run full evaluation suite across 4 models."""
    data_dir = project_root / "data" / "processed"
    models_dir = project_root / "models"
    reports_dir = project_root / "reports"
    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    print("[*] Loading test data and feature metadata...")
    X_test = joblib.load(data_dir / "X_test.pkl")
    y_test = joblib.load(data_dir / "y_test.pkl")
    with open(data_dir / "feature_names.json", "r", encoding="utf-8") as f:
        feature_names = json.load(f)

    print(f"[*] Test matrix shape: {X_test.shape}, labels: {len(y_test)}")

    print("[*] Loading trained model artifacts...")
    models = {
        "XGBoost": joblib.load(models_dir / "xgboost.pkl"),
        "SVM Linear": joblib.load(models_dir / "svm_linear.pkl"),
        "Random Forest": joblib.load(models_dir / "random_forest.pkl"),
        "Naive Bayes": joblib.load(models_dir / "naive_bayes.pkl"),
    }

    # 1. Compute Metrics
    print("[*] Computing metrics across all 4 models...")
    metrics_df = evaluate_all_models(models, X_test, y_test)
    print("\n" + format_markdown_table(metrics_df) + "\n")

    # 2. Update model_comparison.csv
    csv_path = reports_dir / "model_comparison.csv"
    records = []
    meta = {
        "XGBoost": ("5015 (TF-IDF + 15 aux)", "n_estimators=300, max_depth=5, lr=0.05, subsample=0.7, scale_pos_weight=4.22", "Passed (Phase 05 — Cam)"),
        "SVM Linear": ("5015 (TF-IDF + 15 aux)", "C=10.0 (CalibratedClassifierCV 5-fold)", "Passed (Phase 06 — Cam)"),
        "Random Forest": ("5015 (TF-IDF + 15 aux)", "n_estimators=200, max_depth=50, split=2, leaf=2, max_feat=0.2", "Passed (Phase 05 — Son)"),
        "Naive Bayes": ("5000 (TF-IDF non-negative)", "alpha=0.01 (GridSearchCV 5-fold)", "Passed (Phase 04 — Cam)"),
    }
    for _, row in metrics_df.iterrows():
        m_name = row["model"]
        feat, hyper, st = meta.get(m_name, ("5015", "Tuned", "Passed"))
        records.append({
            "Model": m_name,
            "Features": feat,
            "Hyperparameters": hyper,
            "Accuracy": round(row["accuracy"], 4),
            "Precision": round(row["precision"], 4),
            "Recall": round(row["recall"], 4),
            "F1-Score": round(row["f1"], 4),
            "ROC-AUC": round(row["roc_auc"], 4),
            "Status": st,
        })
    pd.DataFrame(records).to_csv(csv_path, index=False)
    print(f"[✓] Saved updated comparison: {csv_path}")

    # 3. Generate Comparative Figures
    print("[*] Generating comparative charts (300 DPI)...")
    p_cm = plot_confusion_matrices_grid(models, X_test, y_test, figures_dir)
    print(f"[✓] Generated: {p_cm.name}")

    p_roc = plot_roc_comparison(models, X_test, y_test, figures_dir)
    print(f"[✓] Generated: {p_roc.name}")

    p_pr = plot_precision_recall_comparison(models, X_test, y_test, figures_dir)
    print(f"[✓] Generated: {p_pr.name}")

    p_lc = plot_learning_curves_summary(figures_dir)
    print(f"[✓] Generated: {p_lc.name}")

    # 4. Keyword Extraction & Consensus
    print("[*] Extracting top scam keywords & consensus ranking...")
    consensus_kws = extract_consensus_keywords(models, feature_names, top_n=20)
    p_kws = plot_top20_keywords_comparison(consensus_kws, figures_dir)
    print(f"[✓] Generated: {p_kws.name}")

    # 5. SHAP Analysis on XGBoost
    print("[*] Computing SHAP TreeExplainer for XGBoost...")
    sample_indices = list(range(min(150, X_test.shape[0])))
    X_sample = X_test[sample_indices]
    p_shap = compute_and_save_shap_plot(models["XGBoost"], X_sample, feature_names, figures_dir)
    print(f"[✓] Generated: {p_shap.name}")

    return {
        "metrics_df": metrics_df,
        "figures": [p_cm, p_roc, p_pr, p_kws, p_shap],
        "consensus_keywords": consensus_kws,
    }


if __name__ == "__main__":
    current_root = Path(__file__).resolve().parent.parent.parent
    run_evaluation(current_root)
