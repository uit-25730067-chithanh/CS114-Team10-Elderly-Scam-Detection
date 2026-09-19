"""
CS114 Final Project — Scam Detection
Unit Tests for Phase 07: Evaluation & XAI Modules.

Author: Đặng Chí Thanh (MSSV: 25730067)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics_calculator import (
    evaluate_all_models,
    evaluate_single_model,
    format_markdown_table,
)
from src.evaluation.plot_comparator import (
    plot_confusion_matrices_grid,
    plot_precision_recall_comparison,
    plot_roc_comparison,
    plot_top20_keywords_comparison,
)
from src.evaluation.xai_explainer import (
    compute_and_save_shap_plot,
    extract_consensus_keywords,
    extract_keywords_from_model,
)


@pytest.fixture
def dummy_eval_data():
    """Create dummy test data and models for evaluation testing."""
    np.random.seed(42)
    X = np.random.rand(50, 30)
    y = np.random.choice([0, 1], size=50, p=[0.7, 0.3])
    feature_names = [f"feat_{i}" for i in range(30)]

    m1 = LogisticRegression()
    m1.fit(X, y)

    m2 = DecisionTreeClassifier(max_depth=3)
    m2.fit(X, y)

    m3 = MultinomialNB()
    m3.fit(X, y)

    models = {
        "Logistic": m1,
        "Tree": m2,
        "Naive Bayes": m3,
    }
    return models, X, y, feature_names


def test_evaluate_single_model(dummy_eval_data):
    models, X, y, _ = dummy_eval_data
    res = evaluate_single_model(models["Logistic"], X, y, model_name="Logistic")

    assert res["model"] == "Logistic"
    assert 0.0 <= res["accuracy"] <= 1.0
    assert 0.0 <= res["precision"] <= 1.0
    assert 0.0 <= res["recall"] <= 1.0
    assert 0.0 <= res["f1"] <= 1.0
    assert 0.0 <= res["roc_auc"] <= 1.0
    assert res["true_negatives"] + res["false_positives"] + res["false_negatives"] + res["true_positives"] == len(y)


def test_evaluate_all_models(dummy_eval_data):
    models, X, y, _ = dummy_eval_data
    df = evaluate_all_models(models, X, y)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    # Check descending sort by F1
    f1s = df["f1"].tolist()
    assert f1s == sorted(f1s, reverse=True)

    md = format_markdown_table(df)
    assert "model" in md
    assert "accuracy" in md


def test_extract_keywords(dummy_eval_data):
    models, _, _, feature_names = dummy_eval_data
    kws = extract_keywords_from_model(models["Tree"], "Tree", feature_names, top_n=5)
    assert len(kws) == 5
    assert isinstance(kws[0][0], str)
    assert isinstance(kws[0][1], float)

    consensus = extract_consensus_keywords(models, feature_names, top_n=5)
    assert len(consensus) == 5
    assert 0.0 <= consensus[0][1] <= 1.0


def test_plot_comparator_renders_files(dummy_eval_data, tmp_path):
    models, X, y, feature_names = dummy_eval_data

    p_cm = plot_confusion_matrices_grid(models, X, y, tmp_path)
    assert p_cm.is_file()
    assert p_cm.stat().st_size > 0

    p_roc = plot_roc_comparison(models, X, y, tmp_path)
    assert p_roc.is_file()
    assert p_roc.stat().st_size > 0

    p_pr = plot_precision_recall_comparison(models, X, y, tmp_path)
    assert p_pr.is_file()
    assert p_pr.stat().st_size > 0

    kws = extract_consensus_keywords(models, feature_names, top_n=10)
    p_kw = plot_top20_keywords_comparison(kws, tmp_path)
    assert p_kw.is_file()
    assert p_kw.stat().st_size > 0


def test_compute_and_save_shap_plot(dummy_eval_data, tmp_path):
    models, X, _, feature_names = dummy_eval_data
    p_shap = compute_and_save_shap_plot(
        models["Tree"],
        X[:10],
        feature_names,
        tmp_path,
        max_display=5,
    )
    assert p_shap.is_file()
    assert p_shap.stat().st_size > 0

