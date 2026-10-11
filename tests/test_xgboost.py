"""
CS114 Final Project — Scam Detection
Unit Tests for XGBoost Classifier Modeling Pipeline (Phase 05).

Không có wrapper class riêng — XGBoost dùng trực tiếp xgb.XGBClassifier trong
notebook, nên test ở đây nhắm vào hành vi thực tế: fit/predict trên dữ liệu
thưa 5.015-dim-like (được phép có giá trị âm, khác Naive Bayes), scale_pos_weight
bù mất cân bằng lớp, và quy trình RandomizedSearchCV giống notebook thật.

Author: Bùi Thị Mỷ Cẩm (MSSV: 25730013)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
import scipy.sparse as sp
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.model_plots import compute_metrics
from src.utils.helpers import RANDOM_STATE


@pytest.fixture
def dummy_mixed_sign_dataset():
    """Mô phỏng không gian 5.015-dim (TF-IDF + 15 aux features chuẩn hóa) — CÓ giá trị
    âm, khác Naive Bayes. XGBoost (tree-based) không bị ảnh hưởng bởi giá trị âm."""
    rng = np.random.RandomState(RANDOM_STATE)
    n_samples, n_features = 60, 40
    X = sp.random(n_samples, n_features, density=0.2, format="csr", random_state=RANDOM_STATE)
    X.data = X.data * 2 - 1  # cho phép âm/dương, giống aux features đã StandardScaler
    y = np.array([0] * 48 + [1] * 12)  # mất cân bằng 4:1, giống thật (~4.22:1)
    return X, y


def test_scale_pos_weight_computation(dummy_mixed_sign_dataset):
    """Đúng công thức thật dùng trong 04_model_xgboost.ipynb."""
    _, y = dummy_mixed_sign_dataset
    scale_pw = float((y == 0).sum() / (y == 1).sum())
    assert scale_pw == pytest.approx(4.0)


def test_xgboost_fit_predict_with_imbalance(dummy_mixed_sign_dataset):
    X, y = dummy_mixed_sign_dataset
    scale_pw = float((y == 0).sum() / (y == 1).sum())

    clf = xgb.XGBClassifier(
        n_estimators=20, max_depth=3, learning_rate=0.1,
        scale_pos_weight=scale_pw, random_state=RANDOM_STATE,
        eval_metric="logloss", n_jobs=1,
    )
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


def test_feature_importances_available(dummy_mixed_sign_dataset):
    X, y = dummy_mixed_sign_dataset
    clf = xgb.XGBClassifier(
        n_estimators=15, max_depth=3, random_state=RANDOM_STATE,
        eval_metric="logloss", n_jobs=1,
    )
    clf.fit(X, y)
    importances = clf.feature_importances_
    assert importances.shape == (X.shape[1],)
    assert np.all(importances >= 0)


def test_randomizedsearch_tuning(dummy_mixed_sign_dataset):
    """Mô phỏng đúng bước RandomizedSearchCV thật trong 04_model_xgboost.ipynb."""
    X, y = dummy_mixed_sign_dataset
    scale_pw = float((y == 0).sum() / (y == 1).sum())

    param_dist = {
        "n_estimators": [10, 20],
        "max_depth": [3, 5],
        "learning_rate": [0.05, 0.1],
    }
    search = RandomizedSearchCV(
        xgb.XGBClassifier(scale_pos_weight=scale_pw, random_state=RANDOM_STATE,
                           eval_metric="logloss", n_jobs=1),
        param_distributions=param_dist, n_iter=3, cv=3, scoring="f1",
        random_state=RANDOM_STATE, n_jobs=1,
    )
    search.fit(X, y)

    assert 0.0 <= search.best_score_ <= 1.0
    # best_estimator_ đã tự refit trên toàn bộ X, y (refit=True mặc định) — không cần fit lại
    best_model = search.best_estimator_
    preds = best_model.predict(X)
    assert preds.shape == (X.shape[0],)
