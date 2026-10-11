"""
CS114 Final Project — Scam Detection
EDA Visualization Plots: Part 2 (N-grams, Correlation Heatmap, Source Distribution).

Author: Đặng Chí Thanh (MSSV: 25730067)
Phase: 03 — EDA & Feature Engineering
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

from src.feature_engineering_config import AUX_FEATURE_COLS

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.2)
SCAM_COLOR = "#e74c3c"
NORMAL_COLOR = "#2980b9"
DPI = 300


def _get_top_ngrams(texts: pd.Series, top_n: int = 20) -> tuple[list[str], list[float]]:
    """Extract top n-grams by raw term frequency from a text corpus."""
    vec = TfidfVectorizer(ngram_range=(1, 2), max_features=10000, min_df=1,
                          use_idf=False, norm=None)
    X = vec.fit_transform(texts)
    sums = X.sum(axis=0).A1
    terms = vec.get_feature_names_out()
    pairs = sorted(zip(terms, sums), key=lambda x: -x[1])[:top_n]
    terms_out, freqs_out = zip(*pairs) if pairs else ([], [])
    return list(terms_out), list(freqs_out)


def plot_top_ngrams(df: pd.DataFrame, figures_dir: Path, n: int = 20) -> None:
    """Figure 5: Top-20 N-grams (1-2) separating scam vs normal classes."""
    scam_texts = df[df["label"] == 1]["text_cleaned"].dropna()
    normal_texts = df[df["label"] == 0]["text_cleaned"].dropna()

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    for ax, texts, title, color in zip(
        axes,
        [scam_texts, normal_texts],
        [f"Top {n} N-grams: Lừa đảo", f"Top {n} N-grams: Bình thường"],
        [SCAM_COLOR, NORMAL_COLOR],
    ):
        try:
            terms, freqs = _get_top_ngrams(texts, top_n=n)
            terms_rev = terms[::-1]
            freqs_rev = freqs[::-1]
            ax.barh(range(len(terms_rev)), freqs_rev, color=color, alpha=0.85)
            ax.set_yticks(range(len(terms_rev)))
            ax.set_yticklabels(terms_rev, fontsize=9)
            ax.set_title(title, fontsize=13, fontweight="bold")
            ax.set_xlabel("Tần suất xuất hiện", fontsize=11)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
        except Exception as e:
            ax.text(0.5, 0.5, f"Error: {e}", transform=ax.transAxes, ha="center")

    fig.suptitle("Top-20 N-grams đặc trưng phân tách Lừa đảo vs Bình thường",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(figures_dir / "top_ngrams_scam_vs_normal.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("✅ top_ngrams_scam_vs_normal.png saved")


def plot_auxiliary_correlation_heatmap(df: pd.DataFrame, figures_dir: Path) -> None:
    """Figure 6: Correlation heatmap between 15 auxiliary features and label."""
    cols_for_corr = AUX_FEATURE_COLS + ["label"]
    corr = df[cols_for_corr].corr()

    fig, ax = plt.subplots(figsize=(13, 11))
    sns.heatmap(
        corr, ax=ax, annot=True, fmt=".2f", cmap="RdYlGn",
        center=0, vmin=-1, vmax=1, square=True, linewidths=0.5,
        cbar_kws={"shrink": 0.8}, annot_kws={"fontsize": 8},
    )
    ax.set_title(
        "Ma trận Tương quan: 15 Đặc trưng Phụ & Nhãn (label)\n"
        "(Auxiliary Features × Label Correlation Heatmap)",
        fontsize=13, fontweight="bold", pad=15,
    )
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    fig.savefig(figures_dir / "auxiliary_correlation_heatmap.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("✅ auxiliary_correlation_heatmap.png saved")


def plot_source_distribution(df: pd.DataFrame, figures_dir: Path) -> None:
    """Figure 7: Source diversity distribution to verify real-world data breadth."""
    source_counts = df["source"].value_counts()
    labels = [str(s)[:40] + "..." if len(str(s)) > 40 else str(s) for s in source_counts.index]

    fig, ax = plt.subplots(figsize=(12, max(5, len(source_counts) * 0.5)))
    colors = plt.cm.tab20.colors[:len(source_counts)]
    bars = ax.barh(range(len(source_counts)), source_counts.values, color=colors, edgecolor="white")

    for bar, val in zip(bars, source_counts.values):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                str(val), ha="left", va="center", fontweight="bold", fontsize=9)

    ax.set_yticks(range(len(source_counts)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_title("Phân bố Nguồn Dữ liệu\n(Source Diversity Distribution)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Số lượng mẫu", fontsize=11)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(figures_dir / "source_distribution.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("✅ source_distribution.png saved")
