"""
CS114 Final Project — Scam Detection
Unit Tests for Random Forest Classifier & Modeling Pipeline.

Author: Hoàng Cao Sơn (MSSV: 25730061)
Phase: 05 — Modeling (Random Forest & XGBoost)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
import scipy.sparse as sp

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.random_forest_model import RandomForestScamDetector
from src.utils.helpers import RANDOM_STATE


@pytest.fixture
def dummy_sparse_dataset():
    """Tạo tập dữ liệu thưa nhân tạo nhỏ để test pipeline."""
    np.random.seed(RANDOM_STATE)
    n_samples = 40
    n_features = 50
    # Ma trận thưa nhị phân 0-1
    data = sp.random(n_samples, n_features, density=0.1, format="csr", random_state=RANDOM_STATE)
    # 30 mẫu bình thường (0), 10 mẫu lừa đảo (1)
    labels = np.array([0] * 30 + [1] * 10)
    return data, labels


def test_random_forest_instantiation():
    detector = RandomForestScamDetector(n_estimators=50, random_state=42)
    assert detector.params["n_estimators"] == 50
    assert detector.params["class_weight"] == "balanced"
    assert not detector.is_fitted


def test_random_forest_fit_predict(dummy_sparse_dataset):
    X, y = dummy_sparse_dataset
    detector = RandomForestScamDetector(n_estimators=20, random_state=42)
    detector.fit(X, y)

    assert detector.is_fitted
    preds = detector.predict(X)
    assert preds.shape == (X.shape[0],)
    assert set(np.unique(preds)).issubset({0, 1})

    probas = detector.predict_proba(X)
    assert probas.shape == (X.shape[0], 2)
    np.testing.assert_allclose(probas.sum(axis=1), 1.0, atol=1e-5)


def test_random_forest_evaluate(dummy_sparse_dataset):
    X, y = dummy_sparse_dataset
    detector = RandomForestScamDetector(n_estimators=20, random_state=42)
    detector.fit(X, y)

    metrics = detector.evaluate(X, y)
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics
    assert "roc_auc" in metrics

    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["f1"] <= 1.0
    assert 0.0 <= metrics["roc_auc"] <= 1.0


def test_random_forest_feature_importances(dummy_sparse_dataset):
    X, y = dummy_sparse_dataset
    detector = RandomForestScamDetector(n_estimators=20, random_state=42)
    detector.fit(X, y)

    feat_names = [f"word_{i}" for i in range(X.shape[1])]
    top_feats = detector.get_feature_importances(feature_names=feat_names, top_n=10)

    assert len(top_feats) == 10
    assert isinstance(top_feats[0][0], str)
    assert isinstance(top_feats[0][1], float)
    # Độ quan trọng phải giảm dần
    scores = [score for _, score in top_feats]
    assert scores == sorted(scores, reverse=True)


def test_random_forest_save_and_load(dummy_sparse_dataset, tmp_path):
    X, y = dummy_sparse_dataset
    detector = RandomForestScamDetector(n_estimators=20, random_state=42)
    detector.fit(X, y)

    model_path = tmp_path / "test_rf.pkl"
    detector.save(model_path)
    assert model_path.exists()

    loaded_detector = RandomForestScamDetector.load(model_path)
    assert loaded_detector.is_fitted

    orig_preds = detector.predict(X)
    loaded_preds = loaded_detector.predict(X)
    np.testing.assert_array_equal(orig_preds, loaded_preds)


def test_random_forest_unfitted_raises(dummy_sparse_dataset):
    """Kiểm tra gọi hàm suy luận khi chưa fit phải ném RuntimeError."""
    X, _ = dummy_sparse_dataset
    detector = RandomForestScamDetector(n_estimators=10, random_state=42)

    with pytest.raises(RuntimeError, match="chưa được fit"):
        detector.predict(X)

    with pytest.raises(RuntimeError, match="chưa được fit"):
        detector.predict_proba(X)

    with pytest.raises(RuntimeError, match="chưa được fit"):
        detector.get_feature_importances()


def test_random_forest_feature_importances_validation(dummy_sparse_dataset):
    """Kiểm tra validate độ dài feature_names không khớp."""
    X, y = dummy_sparse_dataset
    detector = RandomForestScamDetector(n_estimators=10, random_state=42)
    detector.fit(X, y)

    with pytest.raises(ValueError, match="không khớp với số đặc trưng"):
        detector.get_feature_importances(feature_names=["only_one_feature"])


def test_random_forest_classification_report(dummy_sparse_dataset):
    """Kiểm tra xuất báo cáo phân loại văn bản."""
    X, y = dummy_sparse_dataset
    detector = RandomForestScamDetector(n_estimators=10, random_state=42)
    detector.fit(X, y)

    report = detector.get_classification_report(X, y)
    assert isinstance(report, str)
    assert "Bình thường (0)" in report
    assert "Lừa đảo (1)" in report


def test_random_forest_tune_fast(dummy_sparse_dataset):
    """Kiểm tra quy trình RandomizedSearchCV tune siêu tham số."""
    X, y = dummy_sparse_dataset
    detector = RandomForestScamDetector(random_state=42)

    param_dist = {
        "n_estimators": [5, 10],
        "max_depth": [5, 10],
    }
    result = detector.tune(X, y, param_distributions=param_dist, n_iter=2, cv=2, random_state=42)

    assert "best_params" in result
    assert "best_score" in result
    assert detector.is_fitted
    assert detector.best_params_ is not None
    assert 0.0 <= result["best_score"] <= 1.0

