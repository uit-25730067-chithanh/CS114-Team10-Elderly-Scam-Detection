"""CS114 Final Project — Scam Detection: Ablation Figures Generator (Phase 09).
Generates high-resolution 300 DPI comparison figures for Preprocessing and Feature Space ablations.
Author: Đặng Chí Thanh (MSSV: 25730067)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]


def plot_preprocessing_ablation(exp_data: dict, out_path: Path) -> Path:
    """Plot grouped bar chart comparing Raw vs Preprocessed across Naive Bayes and XGBoost."""
    records = exp_data["records"]
    # Model order: Naive Bayes (Raw vs Prep), XGBoost (Raw vs Prep)
    labels = ["NB (Raw)", "NB (Prep)", "XGB (Raw)", "XGB (Prep)"]
    precisions = [r["precision"] * 100 for r in records]
    recalls = [r["recall"] * 100 for r in records]
    f1s = [r["f1"] * 100 for r in records]
    fps = [r["false_positives"] for r in records]

    fig, ax1 = plt.subplots(figsize=(10, 5.5), dpi=300)
    x = np.arange(len(labels))
    width = 0.22

    rects1 = ax1.bar(x - width, precisions, width, label="Precision (%)", color="#3498db")
    rects2 = ax1.bar(x, recalls, width, label="Recall (%)", color="#2ecc71")
    rects3 = ax1.bar(x + width, f1s, width, label="F1-Score (%)", color="#e67e22")

    ax1.set_ylabel("Chỉ số hiệu năng (%)", fontsize=11, fontweight="bold")
    ax1.set_ylim(70, 105)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=10, fontweight="bold")
    ax1.set_title("Thực Nghiệm 1: Đối Chứng Vai Trò Của Tiền Xử Lý NLP (Raw vs Preprocessed)", fontsize=13, pad=15, fontweight="bold")
    ax1.legend(loc="upper left", frameon=True)

    # Annotate False Positives as secondary badges on top
    for idx, (rect, fp) in enumerate(zip(rects3, fps)):
        ax1.annotate(
            f"FP={fp}",
            xy=(rect.get_x() + rect.get_width() / 2, rect.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#c0392b",
        )

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_featurespace_ablation(exp_data: dict, out_path: Path) -> Path:
    """Plot grouped bar chart comparing TF-IDF vs Aux vs Combined across XGBoost and Linear SVM."""
    records = exp_data["records"]
    # 6 configurations: XGB (TF-IDF, Aux, Comb), SVM (TF-IDF, Aux, Comb)
    cfg_labels = [
        "XGB (TF-IDF)",
        "SVM (TF-IDF)",
        "XGB (15 Aux)",
        "SVM (15 Aux)",
        "XGB (5,015 Comb)",
        "SVM (5,015 Comb)",
    ]
    precisions = [r["precision"] * 100 for r in records]
    recalls = [r["recall"] * 100 for r in records]
    f1s = [r["f1"] * 100 for r in records]

    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    x = np.arange(len(cfg_labels))
    width = 0.25

    ax.bar(x - width, precisions, width, label="Precision (%)", color="#2980b9")
    ax.bar(x, recalls, width, label="Recall (%)", color="#27ae60")
    ax.bar(x + width, f1s, width, label="F1-Score (%)", color="#d35400")

    ax.set_ylabel("Chỉ số hiệu năng (%)", fontsize=11, fontweight="bold")
    ax.set_ylim(65, 105)
    ax.set_xticks(x)
    ax.set_xticklabels(cfg_labels, fontsize=9.5, fontweight="bold", rotation=15)
    ax.set_title("Thực Nghiệm 2: Đối Chứng Không Gian Đặc Trưng (TF-IDF vs Aux vs Kết Hợp 5.015)", fontsize=13, pad=15, fontweight="bold")
    ax.legend(loc="lower right", frameon=True)

    # Highlight peak combined F1 on XGBoost
    comb_xgb_f1 = records[4]["f1"] * 100
    ax.annotate(
        f"Peak F1: {comb_xgb_f1:.2f}% (FP=6)",
        xy=(4 + width, comb_xgb_f1),
        xytext=(-20, 15),
        textcoords="offset points",
        arrowprops=dict(facecolor="#c0392b", arrowstyle="->", lw=1.5),
        fontsize=9.5,
        fontweight="bold",
        color="#c0392b",
    )

    plt.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main() -> None:
    """Generate both ablation figures from ablation_studies.json."""
    reports_dir = PROJECT_ROOT / "reports"
    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    json_path = reports_dir / "ablation_studies.json"
    if not json_path.is_file():
        raise FileNotFoundError(f"Missing artifact: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fig1_path = figures_dir / "ablation_preprocessing_comparison.png"
    fig2_path = figures_dir / "ablation_featurespace_comparison.png"

    plot_preprocessing_ablation(data["experiment_1_preprocessing_ablation"], fig1_path)
    plot_featurespace_ablation(data["experiment_2_feature_space_ablation"], fig2_path)

    print(f"[*] Generated: {fig1_path} ({fig1_path.stat().st_size / 1024:.1f} KB)")
    print(f"[*] Generated: {fig2_path} ({fig2_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
