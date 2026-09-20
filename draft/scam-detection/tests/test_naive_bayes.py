"""
CS114 Final Project — Scam Detection
Unit Tests for Naive Bayes Baseline Modeling Pipeline (Phase 04).

Không có wrapper class riêng (khác Random Forest) — NB dùng trực tiếp
MultinomialNB/ComplementNB của sklearn trong notebook, nên test ở đây nhắm vào
hành vi thực tế: fit/predict trên dữ liệu thưa KHÔNG ÂM (bắt buộc với
MultinomialNB), và quy trình GridSearchCV alpha giống notebook thật.

Author: Bùi Thị Mỷ Cẩm (MSSV: 25730013)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
import scipy.sparse as sp
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import ComplementNB, MultinomialNB

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.model_plots import compute_metrics
from src.utils.helpers import RANDOM_STATE


@pytest.fixture
def dummy_nonnegative_dataset():
    """Mô phỏng đúng không gian 5.000-dim TF-IDF không âm mà NB thật sự dùng
    (loại 15 aux features vì StandardScaler sinh giá trị âm — xem Phase 04 Ablation)."""
    rng = np.random.RandomState(RANDOM_STATE)
    n_samples, n_features = 60, 40
    X = sp.random(n_samples, n_features, density=0.15, format="csr", random_state=RANDOM_STATE)
    X.data = np.abs(X.data)  # đảm bảo không âm, giống TF-IDF thật
    y = np.array([0] * 45 + [1] * 15)
    return X, y


def test_multinomial_nb_rejects_negative_values(dummy_nonnegative_dataset):
    """Xác nhận đúng lý do NB loại 15 aux features (StandardScaler sinh giá trị âm)."""
    X, y = dummy_nonnegative_dataset
    X_signed = X.copy()
    X_signed[0, 0] = -1.0  # giả lập 1 giá trị âm như aux feature đã chuẩn hóa
    clf = MultinomialNB()
    with pytest.raises(ValueError):
        clf.fit(X_signed, y)


def test_multinomial_nb_fit_predict(dummy_nonnegative_dataset):
    X, y = dummy_nonnegative_dataset
    clf = MultinomialNB(alpha=0.01)
    clf.fit(X, y)

    preds = clf.predict(X)
    assert preds.shape == (X.shape[0],)
    assert set(np.unique(preds)).issubset({0, 1})

    probas = clf.predict_proba(X)
    assert probas.shape == (X.shape[0], 2)
    np.testing.assert_allclose(probas.sum(axis=1), 1.0, atol=1e-5)

    metrics = compute_metrics(y, preds, probas[:, 1])
    for key in ("accuracy", "precision", "recall", "f1", "roc_auc"):
        assert 0.0 <= metrics[key] <= 1.0


def test_complementnb_also_works(dummy_nonnegative_dataset):
    """ComplementNB là đối chứng baseline thật đã so sánh trong notebook (MultinomialNB thắng)."""
    X, y = dummy_nonnegative_dataset
    clf = ComplementNB()
    clf.fit(X, y)
    preds = clf.predict(X)
    assert preds.shape == (X.shape[0],)


def test_gridsearch_alpha_tuning(dummy_nonnegative_dataset):
    """Mô phỏng đúng bước tuning alpha thật trong 03_model_naive_bayes.ipynb."""
    X, y = dummy_nonnegative_dataset
    param_grid = {"alpha": [0.01, 0.1, 1.0]}
    grid_search = GridSearchCV(MultinomialNB(), param_grid, cv=3, scoring="f1", n_jobs=1)
    grid_search.fit(X, y)

    assert grid_search.best_params_["alpha"] in param_grid["alpha"]
    assert 0.0 <= grid_search.best_score_ <= 1.0

    # best_estimator_ đã tự refit trên toàn bộ X, y (refit=True mặc định) — không cần fit lại
    best_model = grid_search.best_estimator_
    preds = best_model.predict(X)
    assert preds.shape == (X.shape[0],)
