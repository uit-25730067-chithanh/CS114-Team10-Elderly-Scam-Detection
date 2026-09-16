"""
CS114 Final Project — Scam Detection
Model Evaluation Visualization: Confusion Matrix, Learning Curve, Feature Importance, ROC Curve.

Author: Bùi Thị Mỷ Cẩm (MSSV: 25730013)
Phase: 04 — Naive Bayes Baseline / Phase 05 — XGBoost
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import learning_curve

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)
SCAM_COLOR = "#e74c3c"
NORMAL_COLOR = "#2980b9"
DPI = 300


def compute_metrics(y_true, y_pred, y_proba=None) -> dict:
    """Compute Accuracy, Precision, Recall, F1 (positive=scam) và ROC-AUC nếu có xác suất."""
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred)),
        "recall": float(recall_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred)),
    }
    if y_proba is not None:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_proba))
    return metrics


def plot_confusion_matrix(y_true, y_pred, figures_dir: Path, filename: str, title: str) -> None:
    """Confusion matrix heatmap (2x2: Bình thường vs Lừa đảo)."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", cbar=False,
        xticklabels=["Bình thường", "Lừa đảo"],
        yticklabels=["Bình thường", "Lừa đảo"],
        annot_kws={"fontsize": 14, "fontweight": "bold"}, ax=ax,
    )
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Dự đoán", fontsize=12)
    ax.set_ylabel("Thực tế", fontsize=12)
    plt.tight_layout()
    fig.savefig(figures_dir / filename, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ {filename} saved")


def plot_learning_curve_chart(
    estimator, X, y, figures_dir: Path, filename: str, title: str,
    cv: int = 5, scoring: str = "f1", random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Train vs Validation learning curve (overfitting check)."""
    train_sizes, train_scores, val_scores = learning_curve(
        estimator, X, y, cv=cv, scoring=scoring,
        train_sizes=np.linspace(0.1, 1.0, 10),
        random_state=random_state, n_jobs=-1,
    )
    train_mean, train_std = train_scores.mean(axis=1), train_scores.std(axis=1)
    val_mean, val_std = val_scores.mean(axis=1), val_scores.std(axis=1)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(train_sizes, train_mean, "o-", color=NORMAL_COLOR, label="Train F1")
    ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std,
                     alpha=0.15, color=NORMAL_COLOR)
    ax.plot(train_sizes, val_mean, "o-", color=SCAM_COLOR, label="Validation F1 (5-fold CV)")
    ax.fill_between(train_sizes, val_mean - val_std, val_mean + val_std,
                     alpha=0.15, color=SCAM_COLOR)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Số lượng mẫu huấn luyện", fontsize=12)
    ax.set_ylabel(f"{scoring.upper()} Score", fontsize=12)
    ax.legend(loc="best")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(figures_dir / filename, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ {filename} saved")
    return train_sizes, train_mean, val_mean


def plot_feature_importance(
    importances: np.ndarray, feature_names: list[str], figures_dir: Path,
    filename: str, title: str, top_n: int = 20,
) -> None:
    """Horizontal bar chart of top-N most important features."""
    idx = np.argsort(importances)[::-1][:top_n]
    top_feats = [feature_names[i] for i in idx]
    top_vals = importances[idx]

    fig, ax = plt.subplots(figsize=(9, 8))
    ax.barh(range(top_n), top_vals[::-1], color=SCAM_COLOR, edgecolor="white")
    ax.set_yticks(range(top_n))
    ax.set_yticklabels(top_feats[::-1], fontsize=9)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Importance", fontsize=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(figures_dir / filename, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ {filename} saved")


def plot_roc_curve(y_true, y_proba, figures_dir: Path, filename: str, title: str) -> float:
    """ROC curve với AUC hiển thị trên biểu đồ."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    auc = roc_auc_score(y_true, y_proba)

    fig, ax = plt.subplots(figsize=(6.5, 6))
    ax.plot(fpr, tpr, color=SCAM_COLOR, linewidth=2.5, label=f"ROC (AUC = {auc:.4f})")
    ax.plot([0, 1], [0, 1], color="gray", linestyle="--", linewidth=1, label="Random baseline")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.legend(loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(figures_dir / filename, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ {filename} saved")
    return float(auc)
