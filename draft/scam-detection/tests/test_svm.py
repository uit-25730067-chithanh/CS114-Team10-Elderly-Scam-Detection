"""
CS114 Final Project — Scam Detection
Unit Tests for SVM Linear Modeling Pipeline & Inference Bundle Contract (Phase 06).

Không có wrapper class riêng — SVM dùng trực tiếp LinearSVC + CalibratedClassifierCV
trong notebook. Test ở đây bao gồm: fit/predict/predict_proba, GridSearchCV C,
trích xuất hệ số CÓ DẤU (bug đã fix — xem plan Phase 06 Evidence Section), và
luồng suy luận `best_model_bundle.pkl` (raw text -> prediction) mà Phase 08 phụ thuộc.

Author: Bùi Thị Mỷ Cẩm (MSSV: 25730013)
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import scipy.sparse as sp
from scipy.sparse import csr_matrix, hstack
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.model_plots import compute_metrics
from src.utils.helpers import RANDOM_STATE


@pytest.fixture
def dummy_mixed_sign_dataset():
    """Mô phỏng không gian 5.015-dim (TF-IDF + 15 aux features chuẩn hóa) — CÓ giá trị âm."""
    X = sp.random(60, 40, density=0.2, format="csr", random_state=RANDOM_STATE)
    X.data = X.data * 2 - 1
    y = np.array([0] * 45 + [1] * 15)
    return X, y


def test_linear_svc_calibrated_fit_predict(dummy_mixed_sign_dataset):
    X, y = dummy_mixed_sign_dataset
    base = LinearSVC(C=1.0, class_weight="balanced", random_state=RANDOM_STATE, max_iter=10000)
    clf = CalibratedClassifierCV(base, cv=5)
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


def test_linear_svc_max_iter_10000_converges_without_warning(dummy_mixed_sign_dataset):
    """Regression test: max_iter=5000 phát ConvergenceWarning ở C lớn (đã xác nhận thật
    trong code review Phase 06) — max_iter=10000 phải hết cảnh báo."""
    X, y = dummy_mixed_sign_dataset
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        base = LinearSVC(C=10.0, class_weight="balanced", random_state=RANDOM_STATE, max_iter=10000)
        clf = CalibratedClassifierCV(base, cv=5)
        clf.fit(X, y)
    conv_warnings = [w for w in caught if "onverge" in str(w.message)]
    assert not conv_warnings, f"Unexpected ConvergenceWarning: {conv_warnings}"


def test_rbf_calibrated_no_future_warning(dummy_mixed_sign_dataset):
    """Regression test: SVC(probability=True) phát FutureWarning (deprecate ở sklearn 1.9,
    xóa ở 1.11) — CalibratedClassifierCV(SVC(), ensemble=False) phải không còn cảnh báo."""
    X, y = dummy_mixed_sign_dataset
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        clf = CalibratedClassifierCV(
            SVC(kernel="rbf", C=1.0, gamma="scale", class_weight="balanced", random_state=RANDOM_STATE),
            ensemble=False, cv=5,
        )
        clf.fit(X, y)
        proba = clf.predict_proba(X)
    future_warnings = [w for w in caught if issubclass(w.category, FutureWarning)]
    assert not future_warnings, f"Unexpected FutureWarning: {future_warnings}"
    assert proba.shape == (X.shape[0], 2)


def test_gridsearch_c_tuning(dummy_mixed_sign_dataset):
    """Mô phỏng đúng bước GridSearchCV C thật trong 05_model_svm.ipynb."""
    X, y = dummy_mixed_sign_dataset
    param_grid = {"estimator__C": [0.1, 1.0, 10.0]}
    grid = GridSearchCV(
        CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=RANDOM_STATE, max_iter=10000)),
        param_grid, cv=3, scoring="f1", n_jobs=1,
    )
    grid.fit(X, y)

    assert grid.best_params_["estimator__C"] in param_grid["estimator__C"]
    best_model = grid.best_estimator_
    preds = best_model.predict(X)
    assert preds.shape == (X.shape[0],)


def test_signed_coefficient_extraction_preserves_sign(dummy_mixed_sign_dataset):
    """Regression test cho bug mất dấu hệ số (Phase 06 review): trung bình PHẢI lấy
    CÓ DẤU (fold_coefs.mean), không phải abs() trước khi trung bình."""
    X, y = dummy_mixed_sign_dataset
    base = LinearSVC(C=1.0, class_weight="balanced", random_state=RANDOM_STATE, max_iter=10000)
    clf = CalibratedClassifierCV(base, cv=5)
    clf.fit(X, y)

    fold_coefs = np.array([cc.estimator.coef_.ravel() for cc in clf.calibrated_classifiers_])
    mean_coefs_signed = fold_coefs.mean(axis=0)
    mean_coefs_wrong = np.abs(fold_coefs).mean(axis=0)

    # Với ít nhất 1 feature có hệ số âm thật, 2 cách tính phải cho kết quả khác nhau
    assert np.any(mean_coefs_signed < 0), "Fixture nên có ít nhất 1 hệ số âm để test có ý nghĩa"
    assert not np.allclose(mean_coefs_signed, mean_coefs_wrong)
    # Dấu của mean_coefs_signed phải nhất quán với ít nhất đa số các fold riêng lẻ
    for i in range(len(mean_coefs_signed)):
        fold_signs = np.sign(fold_coefs[:, i])
        if np.all(fold_signs == fold_signs[0]):  # tất cả fold đồng dấu cho feature này
            assert np.sign(mean_coefs_signed[i]) == fold_signs[0]


class _FakeAuxScaler(StandardScaler):
    """StandardScaler fit trên numpy array (không có feature names) — giống thật
    (Phase 03 fit aux_scaler.pkl bằng .fit(X_aux.values), không phải DataFrame)."""


def _build_fake_bundle(n_tfidf: int = 20, n_aux: int = 5):
    """Dựng 1 bundle giả (đủ nhỏ, đủ nhanh) để test luồng suy luận contract mà không
    cần load model/data thật của repo — cách ly test khỏi trạng thái data/processed/."""
    rng = np.random.RandomState(RANDOM_STATE)
    X_tfidf = np.abs(rng.rand(30, n_tfidf))
    X_aux = rng.randn(30, n_aux)
    y = np.array([0] * 22 + [1] * 8)

    aux_scaler = _FakeAuxScaler().fit(X_aux)  # fit bằng ndarray, không có feature names
    X_aux_scaled = aux_scaler.transform(X_aux)
    X_full = hstack([csr_matrix(X_tfidf), csr_matrix(X_aux_scaled)]).tocsr()

    model = CalibratedClassifierCV(
        LinearSVC(class_weight="balanced", random_state=RANDOM_STATE, max_iter=10000), cv=3,
    )
    model.fit(X_full, y)

    class _FakeVectorizer:
        def transform(self, texts):
            vecs = rng.rand(len(texts), n_tfidf)
            return csr_matrix(vecs)

    feature_names = [f"tfidf_{i}" for i in range(n_tfidf)] + [f"aux_{i}" for i in range(n_aux)]
    return {
        "model": model,
        "vectorizer": _FakeVectorizer(),
        "aux_scaler": aux_scaler,
        "feature_names": feature_names,
        "model_name": "SVM Linear",
        "threshold": 0.5,
    }, n_aux


def _predict_raw_text(text: str, bundle: dict, aux_dict: dict, aux_cols: list[str]) -> dict:
    """Bản rút gọn của predict_raw_text() thật trong generate_svm_notebook.py, dùng
    trong test để không phải import notebook script (chỉ sinh side-effect khi chạy)."""
    aux_df = pd.DataFrame([aux_dict])[aux_cols]
    aux_scaled = bundle["aux_scaler"].transform(aux_df.values)  # .values -- fix UserWarning
    tfidf_vec = bundle["vectorizer"].transform([text])
    full_vec = hstack([tfidf_vec, csr_matrix(aux_scaled)])
    proba = float(bundle["model"].predict_proba(full_vec)[0][1])
    label = 1 if proba >= bundle.get("threshold", 0.5) else 0
    return {"label": label, "risk_score": proba}


def test_bundle_inference_contract_no_feature_name_warning():
    """Regression test: aux_scaler.transform(aux_df) (DataFrame) phát UserWarning
    'fitted without feature names' (đã xác nhận thật) — .transform(aux_df.values) phải hết."""
    bundle, n_aux = _build_fake_bundle()
    aux_cols = [f"aux_{i}" for i in range(n_aux)]
    aux_dict = {col: 0.0 for col in aux_cols}

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = _predict_raw_text("mã otp khẩn cấp", bundle, aux_dict, aux_cols)

    user_warnings = [w for w in caught if issubclass(w.category, UserWarning)]
    assert not user_warnings, f"Unexpected UserWarning: {user_warnings}"
    assert result["label"] in (0, 1)
    assert 0.0 <= result["risk_score"] <= 1.0


def test_bundle_threshold_logic():
    """Kiểm tra logic ngưỡng label = 1 if proba >= threshold else 0."""
    bundle, n_aux = _build_fake_bundle()
    bundle["threshold"] = 0.9  # ngưỡng cao giả định
    aux_cols = [f"aux_{i}" for i in range(n_aux)]
    aux_dict = {col: 0.0 for col in aux_cols}

    result = _predict_raw_text("bất kỳ văn bản", bundle, aux_dict, aux_cols)
    if result["risk_score"] < 0.9:
        assert result["label"] == 0
    else:
        assert result["label"] == 1
