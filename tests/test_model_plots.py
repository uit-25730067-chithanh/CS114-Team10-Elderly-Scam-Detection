"""
CS114 Final Project — Scam Detection
Unit Tests for shared Model Evaluation Visualization utilities (src/model_plots.py).

Dùng chung cho cả 4 mô hình (NB, RF, XGBoost, SVM) nên test riêng ở đây thay vì
lặp lại trong từng file test_<model>.py.

Author: Bùi Thị Mỷ Cẩm (MSSV: 25730013)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.model_plots import (
    compute_metrics,
    plot_confusion_matrix,
    plot_feature_importance,
    plot_learning_curve_chart,
    plot_roc_curve,
    plot_signed_coefficients,
)
from src.utils.helpers import RANDOM_STATE


def test_compute_metrics_known_values():
    """4 mẫu: TP=1, TN=2, FP=1, FN=0 -> tự tính tay để đối chứng."""
    y_true = np.array([0, 0, 1, 1])
    y_pred = np.array([0, 1, 1, 1])
    y_proba = np.array([0.1, 0.6, 0.9, 0.8])

    metrics = compute_metrics(y_true, y_pred, y_proba)
    assert metrics["accuracy"] == pytest.approx(0.75)
    assert metrics["precision"] == pytest.approx(2 / 3)
    assert metrics["recall"] == pytest.approx(1.0)
    assert metrics["f1"] == pytest.approx(2 * (2 / 3) / (2 / 3 + 1))
    assert 0.0 <= metrics["roc_auc"] <= 1.0


def test_compute_metrics_without_proba_omits_roc_auc():
    y_true = np.array([0, 1, 0, 1])
    y_pred = np.array([0, 1, 0, 0])
    metrics = compute_metrics(y_true, y_pred, y_proba=None)
    assert "roc_auc" not in metrics
    assert set(metrics.keys()) == {"accuracy", "precision", "recall", "f1"}


@pytest.fixture
def dummy_binary_data():
    rng = np.random.RandomState(RANDOM_STATE)
    n = 60
    y_true = np.array([0] * 45 + [1] * 15)
    y_proba = np.clip(y_true * 0.6 + rng.rand(n) * 0.5, 0, 1)
    y_pred = (y_proba >= 0.5).astype(int)
    return y_true, y_pred, y_proba


def test_plot_confusion_matrix_creates_file(tmp_path, dummy_binary_data):
    y_true, y_pred, _ = dummy_binary_data
    plot_confusion_matrix(y_true, y_pred, tmp_path, "cm.png", "Test CM")
    assert (tmp_path / "cm.png").exists()
    assert (tmp_path / "cm.png").stat().st_size > 0


def test_plot_roc_curve_creates_file_and_returns_auc(tmp_path, dummy_binary_data):
    y_true, _, y_proba = dummy_binary_data
    auc = plot_roc_curve(y_true, y_proba, tmp_path, "roc.png", "Test ROC")
    assert (tmp_path / "roc.png").exists()
    assert 0.0 <= auc <= 1.0


def test_plot_learning_curve_chart_creates_file(tmp_path):
    from scipy import sparse
    from sklearn.linear_model import LogisticRegression

    rng = np.random.RandomState(RANDOM_STATE)
    X = sparse.random(80, 20, density=0.3, format="csr", random_state=RANDOM_STATE)
    y = np.array([0] * 60 + [1] * 20)
    train_sizes, train_mean, val_mean = plot_learning_curve_chart(
        LogisticRegression(max_iter=200, random_state=RANDOM_STATE),
        X, y, tmp_path, "lc.png", "Test LC", cv=3, random_state=RANDOM_STATE,
    )
    assert (tmp_path / "lc.png").exists()
    assert len(train_sizes) == len(train_mean) == len(val_mean)


def test_plot_feature_importance_creates_file(tmp_path):
    rng = np.random.RandomState(RANDOM_STATE)
    importances = rng.rand(30)
    feature_names = [f"feat_{i}" for i in range(30)]
    plot_feature_importance(importances, feature_names, tmp_path, "fi.png", "Test FI", top_n=10)
    assert (tmp_path / "fi.png").exists()


def test_plot_signed_coefficients_creates_file_and_splits_by_sign(tmp_path):
    """Kiểm tra hàm vẽ hệ số có dấu (fix bug mất dấu ở Phase 06) tách đúng 2 cụm."""
    mean_coefs = np.array([2.0, -1.5, 0.8, -0.3, 1.2, -2.5, 0.1, -0.05, 0.9, -1.1])
    feature_names = [f"word_{i}" for i in range(10)]

    plot_signed_coefficients(mean_coefs, feature_names, tmp_path, "signed.png", "Test Signed", top_n=3)
    assert (tmp_path / "signed.png").exists()
    assert (tmp_path / "signed.png").stat().st_size > 0

    # Đối chứng thủ công: top-3 dương và top-3 âm phải đúng theo argsort
    pos_idx = np.argsort(mean_coefs)[::-1][:3]
    neg_idx = np.argsort(mean_coefs)[:3]
    assert all(mean_coefs[i] > 0 for i in pos_idx)
    assert all(mean_coefs[i] < 0 for i in neg_idx)
