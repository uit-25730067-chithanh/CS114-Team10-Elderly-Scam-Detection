"""
CS114 Final Project — Scam Detection
Explainable AI (XAI) & Psychological Trap Keyword Extraction (Phase 07).

Extracts top risk-triggering keywords via:
- Model-specific feature weights (NB log-ratio, Tree Gini/Gain, Linear SVM coef)
- Multi-model consensus ranking
- SHAP TreeExplainer summary plots for XGBoost

Author: Đặng Chí Thanh (MSSV: 25730067)
"""

from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import shap

DPI = 300


def extract_keywords_from_model(model, model_name: str, feature_names: list[str], top_n: int = 20) -> list[tuple[str, float]]:
    """Extract top-N scam-indicative keywords from a specific model."""
    num_text_features = min(5000, len(feature_names))
    text_names = feature_names[:num_text_features]

    if "naive" in model_name.lower() or "nb" in model_name.lower():
        # Difference in log probability: P(word | Scam) - P(word | Normal)
        diff = model.feature_log_prob_[1] - model.feature_log_prob_[0]
        scores = diff[:num_text_features]
    elif hasattr(model, "feature_importances_"):
        scores = model.feature_importances_[:num_text_features]
    elif hasattr(model, "calibrated_classifiers_"):
        # Mean signed coefficients across calibrated estimators
        coefs = [est.estimator.coef_[0][:num_text_features] for est in model.calibrated_classifiers_]
        scores = np.mean(coefs, axis=0)
    elif hasattr(model, "coef_"):
        scores = model.coef_[0][:num_text_features]
    else:
        scores = np.zeros(num_text_features)

    top_idx = np.argsort(scores)[::-1][:top_n]
    return [(text_names[i], float(scores[i])) for i in top_idx]


def extract_consensus_keywords(models_dict: dict, feature_names: list[str], top_n: int = 20) -> list[tuple[str, float]]:
    """Combine rankings across all models to compute unified consensus risk scores."""
    num_text = min(5000, len(feature_names))
    cumulative_rank = {feature_names[i]: 0.0 for i in range(num_text)}

    for name, model in models_dict.items():
        kws = extract_keywords_from_model(model, name, feature_names, top_n=num_text)
        for rank, (word, _) in enumerate(kws):
            # Reciprocal rank score
            cumulative_rank[word] += 1.0 / (rank + 1.0)

    sorted_kws = sorted(cumulative_rank.items(), key=lambda x: x[1], reverse=True)[:top_n]
    # Normalize score between 0 and 1
    max_val = sorted_kws[0][1] if (sorted_kws and sorted_kws[0][1] > 0) else 1.0
    return [(word, round(score / max_val, 4)) for word, score in sorted_kws]


def compute_and_save_shap_plot(model, X_sample, feature_names: list[str], figures_dir: Path, max_display: int = 20) -> Path:
    """Compute SHAP values on XGBoost and save summary beeswarm plot."""
    X_dense = X_sample.toarray() if hasattr(X_sample, "toarray") else np.array(X_sample)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_dense)

    # In case shap_values is 2D or 3D
    if isinstance(shap_values, list):
        vals = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    elif getattr(shap_values, "ndim", 0) == 3:
        vals = shap_values[:, :, 1]
    else:
        vals = shap_values

    plt.figure(figsize=(10, 7.5))
    try:
        shap.summary_plot(
            vals,
            X_dense,
            feature_names=feature_names,
            max_display=max_display,
            show=False,
        )
        plt.title("XGBoost SHAP Summary Plot — Đóng Góp Giá Trị Đặc Trưng Vào Xác Suất Lừa Đảo",
                  fontsize=12, fontweight="bold", pad=12)
        out_path = figures_dir / "shap_summary.png"
        plt.savefig(out_path, dpi=DPI, bbox_inches="tight")
        return out_path
    finally:
        plt.close("all")
