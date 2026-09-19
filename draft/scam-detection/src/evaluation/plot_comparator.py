"""
CS114 Final Project — Scam Detection
Comprehensive Model Comparison Visualization (Phase 07: Evaluation & XAI).

Renders 4-model comparison figures at 300 DPI:
- 2x2 Confusion Matrices Grid
- Multi-Model ROC Curves Comparison
- Multi-Model Precision-Recall Curves
- Top-20 Scam Keywords Horizontal Bar Chart

Author: Đặng Chí Thanh (MSSV: 25730067)
"""

from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)

from src.evaluation.metrics_calculator import (
    get_predicted_probabilities,
    resolve_eval_features,
)

DPI = 300
PALETTE = {
    "XGBoost": "#e74c3c",       # Red
    "SVM Linear": "#2980b9",     # Blue
    "Random Forest": "#27ae60",  # Green
    "Naive Bayes": "#8e44ad",    # Purple
}


def plot_confusion_matrices_grid(models_dict: dict, X_test, y_test, figures_dir: Path) -> Path:
    """Render 2x2 grid of confusion matrices for all 4 models."""
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    try:
        axes_flat = axes.flatten()
        for idx, (name, model) in enumerate(models_dict.items()):
            ax = axes_flat[idx]
            X_eval = resolve_eval_features(model, name, X_test)
            y_pred = model.predict(X_eval)
            cm = confusion_matrix(y_test, y_pred)
            sns.heatmap(
                cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Bình thường", "Lừa đảo"], yticklabels=["Bình thường", "Lừa đảo"],
                annot_kws={"fontsize": 13, "fontweight": "bold"}, ax=ax,
            )
            ax.set_title(f"{name} (FN={cm[1, 0]}, FP={cm[0, 1]})", fontsize=12, fontweight="bold", pad=8)
            ax.set_xlabel("Dự đoán", fontsize=10)
            ax.set_ylabel("Thực tế", fontsize=10)

        plt.suptitle("Ma Trận Nhầm Lẫn So Sánh 4 Mô Hình (Holdout Test Set = 439 mẫu)",
                     fontsize=14, fontweight="bold", y=0.98)
        plt.tight_layout()
        out_path = figures_dir / "confusion_matrices_all.png"
        fig.savefig(out_path, dpi=DPI, bbox_inches="tight")
        return out_path
    finally:
        plt.close(fig)


def plot_roc_comparison(models_dict: dict, X_test, y_test, figures_dir: Path) -> Path:
    """Render multi-model ROC Curves on a single canvas."""
    fig, ax = plt.subplots(figsize=(8, 6.5))
    try:
        for name, model in models_dict.items():
            X_eval = resolve_eval_features(model, name, X_test)
            y_proba = get_predicted_probabilities(model, X_eval)
            if y_proba is None:
                continue
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            auc = roc_auc_score(y_test, y_proba)
            color = PALETTE.get(name, "#34495e")
            ax.plot(fpr, tpr, color=color, linewidth=2.2, label=f"{name} (ROC-AUC = {auc:.4f})")

        ax.plot([0, 1], [0, 1], "k--", linewidth=1.2, alpha=0.6, label="Ngẫu nhiên (AUC = 0.5000)")
        ax.set_title("So Sánh Đường Cong ROC Giữa 4 Mô Hình (Test Set = 439 mẫu)",
                     fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("False Positive Rate (Tỷ lệ báo nhầm)", fontsize=11)
        ax.set_ylabel("True Positive Rate (Tỷ lệ phát hiện lừa đảo)", fontsize=11)
        ax.legend(loc="lower right", fontsize=10, frameon=True)
        ax.set_xlim([-0.01, 1.01])
        ax.set_ylim([-0.01, 1.01])
        ax.grid(True, linestyle=":", alpha=0.6)
        plt.tight_layout()
        out_path = figures_dir / "roc_curves_comparison.png"
        fig.savefig(out_path, dpi=DPI, bbox_inches="tight")
        return out_path
    finally:
        plt.close(fig)


def plot_precision_recall_comparison(models_dict: dict, X_test, y_test, figures_dir: Path) -> Path:
    """Render multi-model Precision-Recall Curves."""
    fig, ax = plt.subplots(figsize=(8, 6.5))
    try:
        for name, model in models_dict.items():
            X_eval = resolve_eval_features(model, name, X_test)
            y_proba = get_predicted_probabilities(model, X_eval)
            if y_proba is None:
                continue
            prec, rec, _ = precision_recall_curve(y_test, y_proba)
            ap = average_precision_score(y_test, y_proba)
            color = PALETTE.get(name, "#34495e")
            ax.plot(rec, prec, color=color, linewidth=2.2, label=f"{name} (Avg Prec = {ap:.4f})")

        ax.axhline(y=float(np.mean(y_test)), color="k", linestyle="--", linewidth=1.2, alpha=0.5,
                   label=f"Tỷ lệ lừa đảo gốc ({np.mean(y_test):.1%})")
        ax.set_title("Đường Cong Precision-Recall So Sánh 4 Mô Hình",
                     fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Recall (Độ nhạy thu hồi lừa đảo)", fontsize=11)
        ax.set_ylabel("Precision (Độ chính xác cảnh báo)", fontsize=11)
        ax.legend(loc="lower left", fontsize=10, frameon=True)
        ax.set_xlim([-0.01, 1.01])
        ax.set_ylim([-0.01, 1.01])
        ax.grid(True, linestyle=":", alpha=0.6)
        plt.tight_layout()
        out_path = figures_dir / "precision_recall_curves.png"
        fig.savefig(out_path, dpi=DPI, bbox_inches="tight")
        return out_path
    finally:
        plt.close(fig)


def plot_top20_keywords_comparison(keywords_data: list[tuple[str, float]], figures_dir: Path) -> Path:
    """Render horizontal bar chart for top-20 scam alert keywords."""
    fig, ax = plt.subplots(figsize=(9.5, 7.5))
    try:
        top_n = min(20, len(keywords_data))
        sorted_data = keywords_data[:top_n][::-1]
        kws = [item[0] for item in sorted_data]
        scores = [item[1] for item in sorted_data]

        ax.barh(range(top_n), scores, color="#e74c3c", edgecolor="#c0392b", height=0.65)
        ax.set_yticks(range(top_n))
        ax.set_yticklabels(kws, fontsize=10, fontweight="bold")
        ax.set_title("Top 20 Từ Khóa Kích Hoạt Bẫy Tâm Lý Lừa Đảo Hàng Đầu (XAI Feature Weights)",
                     fontsize=12, fontweight="bold", pad=12)
        ax.set_xlabel("Trọng số ảnh hưởng trung bình chuẩn hóa", fontsize=10)
        ax.grid(True, axis="x", linestyle=":", alpha=0.6)
        plt.tight_layout()
        out_path = figures_dir / "top20_keywords_barplot.png"
        fig.savefig(out_path, dpi=DPI, bbox_inches="tight")
        return out_path
    finally:
        plt.close(fig)


def plot_learning_curves_summary(figures_dir: Path) -> Path:
    """Compose 2x2 summary grid from individual 300 DPI learning curves."""
    curves = [
        ("XGBoost", figures_dir / "xgb_learning_curve.png"),
        ("SVM Linear", figures_dir / "svm_learning_curve.png"),
        ("Random Forest", figures_dir / "rf_learning_curve.png"),
        ("Naive Bayes", figures_dir / "nb_learning_curve.png"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    try:
        axes_flat = axes.flatten()
        for idx, (name, img_path) in enumerate(curves):
            ax = axes_flat[idx]
            if img_path.exists():
                img = plt.imread(str(img_path))
                ax.imshow(img)
                ax.axis("off")
            else:
                ax.text(0.5, 0.5, f"{name}\n(Chưa có biểu đồ)", ha="center", va="center")
                ax.axis("off")

        plt.suptitle("Tổng Hợp Đánh Giá Quá Khớp (Learning Curves Overfitting Analysis — 5-Fold CV)",
                     fontsize=14, fontweight="bold", y=0.99)
        plt.tight_layout()
        out_path = figures_dir / "learning_curves_summary.png"
        fig.savefig(out_path, dpi=DPI, bbox_inches="tight")
        return out_path
    finally:
        plt.close(fig)
