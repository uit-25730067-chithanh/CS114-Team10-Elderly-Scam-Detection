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
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_single_model(model, X_test, y_test, model_name: str = "") -> dict:
    """Evaluate one model on test set. Handles 5000 TF-IDF slice for Naive Bayes."""
    # MultinomialNB only accepts 5000 non-negative TF-IDF features
    if "naive" in model_name.lower() or "nb" in model_name.lower():
        if hasattr(X_test, "shape") and X_test.shape[1] > 5000:
            X_eval = X_test[:, :5000]
        else:
            X_eval = X_test
    else:
        X_eval = X_test

    y_pred = model.predict(X_eval)

    # Predict proba
    y_proba = None
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_eval)[:, 1]
    elif hasattr(model, "decision_function"):
        df = model.decision_function(X_eval)
        y_proba = (df - df.min()) / (df.max() - df.min() + 1e-9)

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
    """Format DataFrame as a clean Markdown table with percentage formatting."""
    formatted = df.copy()
    formatted["accuracy"] = formatted["accuracy"].map("{:.2%}".format)
    formatted["precision"] = formatted["precision"].map("{:.2%}".format)
    formatted["recall"] = formatted["recall"].map("{:.2%}".format)
    formatted["f1"] = formatted["f1"].map("{:.4f}".format)
    formatted["roc_auc"] = formatted["roc_auc"].map("{:.4f}".format)

    cols = ["model", "accuracy", "precision", "recall", "f1", "roc_auc", "false_negatives", "false_positives"]
    return formatted[cols].to_markdown(index=False)
