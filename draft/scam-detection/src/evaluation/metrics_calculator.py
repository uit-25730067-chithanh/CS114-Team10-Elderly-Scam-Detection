"""
CS114 Final Project — Scam Detection
Comprehensive Model Metrics Calculator (Phase 07: Evaluation & XAI).

Computes Accuracy, Precision, Recall, F1, ROC-AUC, Brier score, and Confusion Matrix
across multiple models on holdout test set.

Author: Đặng Chí Thanh (MSSV: 25730067)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.special import expit
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

MODEL_METADATA = {
    "XGBoost": {
        "features": "5,015 (TF-IDF + 15 aux)",
        "hyperparameters": "n_est=300, depth=5, lr=0.05, subsample=0.7, colsample=0.8, scale_pos_weight=4.22",
        "notes": "Best Overall Model, FN=2, FP=6 (Phase 05 — Cẩm)",
    },
    "SVM Linear": {
        "features": "5,015 (TF-IDF + 15 aux)",
        "hyperparameters": "C=10.0 (CalibratedClassifierCV 5-fold)",
        "notes": "Best Linear Model, FN=3, FP=6 (Phase 06 — Cẩm)",
    },
    "Random Forest": {
        "features": "5,015 (TF-IDF + 15 aux)",
        "hyperparameters": "n_est=200, depth=50, split=2, leaf=2, max_feat=0.2",
        "notes": "Best Tree Ensemble, FN=2, FP=8 (Phase 05 — Sơn)",
    },
    "Naive Bayes": {
        "features": "5,000 (TF-IDF)",
        "hyperparameters": "alpha=0.5 (MultinomialNB)",
        "notes": "Baseline Model, FN=6, FP=14 (Phase 04 — Thanh)",
    },
}


def resolve_eval_features(model, model_name: str, X_test):
    """Dynamically resolve feature slice if model expects fewer features than X_test."""
    n_expected = getattr(model, "n_features_in_", None)
    if n_expected is None and hasattr(model, "feature_log_prob_"):
        n_expected = model.feature_log_prob_.shape[1]

    if n_expected is not None and hasattr(X_test, "shape") and X_test.shape[1] > n_expected:
        return X_test[:, :n_expected]
    if ("naive" in model_name.lower() or "nb" in model_name.lower()) and hasattr(X_test, "shape") and X_test.shape[1] > 5000:
        return X_test[:, :5000]
    return X_test


def get_predicted_probabilities(model, X) -> np.ndarray | None:
    """Safely extract positive class probability estimates from any classifier."""
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    if hasattr(model, "decision_function"):
        df = model.decision_function(X)
        return expit(df)
    return None


def evaluate_single_model(model, X_test, y_test, model_name: str = "") -> dict:
    """Evaluate one model on test set. Dynamically adapts feature dimension."""
    X_eval = resolve_eval_features(model, model_name, X_test)
    y_pred = model.predict(X_eval)
    y_proba = get_predicted_probabilities(model, X_eval)

    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()

    metrics = {
        "model": model_name,
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)) if y_proba is not None else np.nan,
        "brier_score": float(brier_score_loss(y_test, y_proba)) if y_proba is not None else np.nan,
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }
    return metrics


def evaluate_all_models(models_dict: dict, X_test, y_test) -> pd.DataFrame:
    """Evaluate dictionary of models and return sorted summary DataFrame."""
    records = []
    for name, model in models_dict.items():
        res = evaluate_single_model(model, X_test, y_test, model_name=name)
        records.append(res)

    df = pd.DataFrame(records)
    # Sort descending by F1 score
    df = df.sort_values(by="f1", ascending=False).reset_index(drop=True)
    return df


def format_markdown_table(df: pd.DataFrame) -> str:
    """Format DataFrame as clean Markdown table with tabulate-independent fallback."""
    formatted = df.copy()
    for col in ["accuracy", "precision", "recall"]:
        if col in formatted:
            formatted[col] = formatted[col].map("{:.2%}".format)
    for col in ["f1", "roc_auc"]:
        if col in formatted:
            formatted[col] = formatted[col].map("{:.4f}".format)

    cols = ["model", "accuracy", "precision", "recall", "f1", "roc_auc", "false_negatives", "false_positives"]
    available_cols = [c for c in cols if c in formatted.columns]

    try:
        return formatted[available_cols].to_markdown(index=False)
    except (ImportError, ModuleNotFoundError, AttributeError):
        return formatted[available_cols].to_string(index=False)
