"""
CS114 Final Project — Scam Detection
EDA Orchestrator: Runs all 7 visualizations for Phase 03 EDA.

This is the main entry point to generate all EDA figures.
Delegates to modular plot functions in eda_plots_part1 and eda_plots_part2.

Usage:
    cd draft/scam-detection
    python3 src/eda_visualizations.py

Author: Đặng Chí Thanh (MSSV: 25730067)
Phase: 03 — EDA & Feature Engineering
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import pandas as pd

# ─── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
CSV_PATH = DATA_DIR / "dataset_preprocessed.csv"


def ensure_project_in_path() -> None:
    """Add project root to sys.path so src.* imports work correctly."""
    root_str = str(PROJECT_ROOT)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def load_data() -> pd.DataFrame:
    """Load preprocessed dataset from CSV."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def run_all_figures(df: pd.DataFrame, figures_dir: Path) -> list[str]:
    """Generate all 7 EDA figures and return list of saved filenames."""
    figures_dir.mkdir(parents=True, exist_ok=True)

    from src.eda_plots_part1 import (
        plot_label_distribution,
        plot_scam_category_distribution,
        plot_text_length_comparison,
        plot_wordclouds,
    )
    from src.eda_plots_part2 import (
        plot_auxiliary_correlation_heatmap,
        plot_source_distribution,
        plot_top_ngrams,
    )

    print(f"\nGenerating 7 EDA figures → {figures_dir}\n")
    t0 = time.time()

    plot_label_distribution(df, figures_dir)           # Figure 1
    plot_scam_category_distribution(df, figures_dir)   # Figure 2
    plot_text_length_comparison(df, figures_dir)       # Figure 3
    plot_wordclouds(df, figures_dir)                   # Figure 4
    plot_top_ngrams(df, figures_dir, n=20)             # Figure 5
    plot_auxiliary_correlation_heatmap(df, figures_dir)  # Figure 6
    plot_source_distribution(df, figures_dir)          # Figure 7

    elapsed = time.time() - t0
    saved = sorted(figures_dir.glob("*.png"))
    print(f"\n✅ {len(saved)} PNG figures saved in {elapsed:.1f}s")
    for f in saved:
        size_kb = os.path.getsize(f) / 1024
        print(f"   {f.name}: {size_kb:.1f} KB")
    return [f.name for f in saved]


if __name__ == "__main__":
    ensure_project_in_path()
    os.chdir(PROJECT_ROOT)

    df = load_data()
    saved_files = run_all_figures(df, FIGURES_DIR)

    required = [
        "label_distribution.png",
        "scam_category_distribution.png",
        "text_length_comparison.png",
        "wordcloud_scam_vs_normal.png",
        "auxiliary_correlation_heatmap.png",
    ]
    missing = [r for r in required if r not in saved_files]
    if missing:
        print(f"\n⚠ WARNING: Required figures missing: {missing}")
        sys.exit(1)
    else:
        print(f"\n✅ All {len(required)} required figures confirmed present.")
