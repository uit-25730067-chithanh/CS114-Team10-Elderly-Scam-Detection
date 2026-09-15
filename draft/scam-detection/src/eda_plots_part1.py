"""
CS114 Final Project — Scam Detection
EDA Visualization Plots: Part 1 (Label, Category, Text Length, WordClouds).

Author: Đặng Chí Thanh (MSSV: 25730067)
Phase: 03 — EDA & Feature Engineering
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path
from wordcloud import WordCloud

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)
SCAM_COLOR = "#e74c3c"
NORMAL_COLOR = "#2980b9"
DPI = 300


def plot_label_distribution(df: pd.DataFrame, figures_dir: Path) -> None:
    """Figure 1: Bar chart of label distribution with imbalance ratio."""
    counts = df["label"].value_counts().sort_index()
    total = counts.sum()
    imbalanced_ratio = counts[0] / counts[1]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        ["Bình thường (label=0)", "Lừa đảo (label=1)"],
        counts.values,
        color=[NORMAL_COLOR, SCAM_COLOR],
        edgecolor="white", linewidth=1.5, width=0.5,
    )
    for bar, val in zip(bars, counts.values):
        pct = val / total * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
                f"{val}\n({pct:.1f}%)", ha="center", va="bottom", fontweight="bold", fontsize=12)
    ax.set_title(f"Phân bố Nhãn (Label Distribution)\nImbalance ratio: {imbalanced_ratio:.1f}:1",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Số lượng mẫu", fontsize=12)
    ax.set_ylim(0, counts.max() * 1.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(figures_dir / "label_distribution.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("✅ label_distribution.png saved")


def plot_scam_category_distribution(df: pd.DataFrame, figures_dir: Path) -> None:
    """Figure 2: Bar chart of 4 scam psychological bait categories."""
    cat_order = ["fear_authority", "family_emergency", "health_gift", "public_service", "none"]
    cat_labels = {
        "fear_authority": "Giả danh\nCông an",
        "family_emergency": "Cấp cứu\nNgười thân",
        "health_gift": "Tặng thuốc\n/ Quà tặng",
        "public_service": "Giả mạo\nDịch vụ công",
        "none": "Bình thường",
    }
    counts = df["scam_category"].value_counts().reindex(cat_order, fill_value=0)
    colors = [SCAM_COLOR, SCAM_COLOR, SCAM_COLOR, SCAM_COLOR, NORMAL_COLOR]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar([cat_labels[c] for c in cat_order], counts.values, color=colors,
                  edgecolor="white", linewidth=1.5, width=0.6)
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                str(val), ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Phân bố Kịch bản Tâm lý Lừa đảo\n(Scam Category Distribution)",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Số lượng mẫu", fontsize=12)
    ax.set_ylim(0, counts.max() * 1.2)
    legend_patches = [
        mpatches.Patch(color=SCAM_COLOR, label="Kịch bản Lừa đảo"),
        mpatches.Patch(color=NORMAL_COLOR, label="Bình thường"),
    ]
    ax.legend(handles=legend_patches, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(figures_dir / "scam_category_distribution.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("✅ scam_category_distribution.png saved")


def plot_text_length_comparison(df: pd.DataFrame, figures_dir: Path) -> None:
    """Figure 3: Histogram comparing character length and word count distributions."""
    scam = df[df["label"] == 1]
    normal = df[df["label"] == 0]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, metric, title, xlabel in zip(
        axes,
        ["text_length", "num_words"],
        ["Phân bố Độ dài Ký tự", "Phân bố Số từ"],
        ["Số ký tự", "Số từ"],
    ):
        ax.hist(normal[metric], bins=40, color=NORMAL_COLOR, alpha=0.6,
                label=f"Bình thường (n={len(normal)})", density=True)
        ax.hist(scam[metric], bins=40, color=SCAM_COLOR, alpha=0.6,
                label=f"Lừa đảo (n={len(scam)})", density=True)
        ax.axvline(normal[metric].median(), color=NORMAL_COLOR, linestyle="--", linewidth=2,
                   label=f"Median bình thường={normal[metric].median():.0f}")
        ax.axvline(scam[metric].median(), color=SCAM_COLOR, linestyle="--", linewidth=2,
                   label=f"Median lừa đảo={scam[metric].median():.0f}")
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel("Mật độ", fontsize=11)
        ax.legend(fontsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("So sánh Phân bố Độ dài Văn bản: Lừa đảo vs Bình thường",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    fig.savefig(figures_dir / "text_length_comparison.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("✅ text_length_comparison.png saved")


def plot_wordclouds(df: pd.DataFrame, figures_dir: Path) -> None:
    """Figure 4: Word clouds for scam vs normal messages."""
    scam_text = " ".join(df[df["label"] == 1]["text_cleaned"].dropna())
    normal_text = " ".join(df[df["label"] == 0]["text_cleaned"].dropna())

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for ax, text, title, bg, colormap in zip(
        axes,
        [scam_text, normal_text],
        ["[SCAM] Word Cloud: Tin nhắn LUA DAO", "[OK] Word Cloud: Tin nhan BINH THUONG"],
        ["#1a0000", "#001a00"],
        ["Reds", "Blues"],
    ):
        wc = WordCloud(
            width=800, height=400, background_color=bg,
            colormap=colormap, max_words=150, min_font_size=8,
            max_font_size=80, collocations=False,
        ).generate(text)
        ax.imshow(wc, interpolation="bilinear")
        ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
        ax.axis("off")
        ax.set_facecolor(bg)
    fig.patch.set_facecolor("#0d0d0d")
    plt.tight_layout(pad=1.0)
    fig.savefig(figures_dir / "wordcloud_scam_vs_normal.png", dpi=DPI, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print("✅ wordcloud_scam_vs_normal.png saved")
