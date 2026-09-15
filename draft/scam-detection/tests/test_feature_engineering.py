"""
CS114 Final Project — Scam Detection
Unit Tests for Zero-Leakage Feature Engineering Pipeline.

Test suite validates:
1. No NaN/Inf in output matrices
2. Correct output shapes (5015 features)
3. Zero data leakage (test does not influence train vocabulary/scaling)
4. Reproducibility (bit-identical across 2 runs with random_state=42)

Author: Đặng Chí Thanh (MSSV: 25730067)
Phase: 03 — EDA & Feature Engineering
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import scipy.sparse as sp

# Ensure project root is in sys.path for src imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.feature_engineering import (
    AuxiliaryFeatureScaler,
    DataSplitter,
    TextFeatureExtractor,
    assemble_feature_matrix,
    export_feature_matrices,
)
from src.feature_engineering_config import (
    AUX_FEATURE_COLS,
    EXPECTED_N_FEATURES,
    LABEL_COL,
    TEXT_COL,
)
from src.utils import RANDOM_STATE

# ─── Fixture: Minimal Synthetic DataFrame ────────────────────────────────────
# Uses a synthetic fixture (acceptable for unit tests — NOT in training data).
# Fixture contains 100 samples: 80 normal (label=0), 20 scam (label=1).


@pytest.fixture(scope="module")
def synthetic_df() -> pd.DataFrame:
    """Create a small synthetic dataframe matching Phase 02 output schema."""
    rng = np.random.RandomState(RANDOM_STATE)
    n_samples = 100
    n_normal = 80
    n_scam = 20

    normal_texts = [
        f"tin nhắn bình thường số {i} giao dịch ngân hàng thông thường" for i in range(n_normal)
    ]
    scam_texts = [
        f"cảnh báo khẩn cấp lừa đảo tài khoản số {i} chuyển tiền ngay giả mạo công an" for i in range(n_scam)
    ]

    texts = normal_texts + scam_texts
    labels = [0] * n_normal + [1] * n_scam

    rows = []
    for i, (text, label) in enumerate(zip(texts, labels)):
        row = {
            "id": i + 1,
            TEXT_COL: text,
            LABEL_COL: label,
        }
        for col in AUX_FEATURE_COLS:
            if col.startswith("has_") or col.startswith("is_"):
                row[col] = rng.randint(0, 2)
            elif col in ("text_length",):
                row[col] = len(text)
            elif col in ("num_words",):
                row[col] = len(text.split())
            else:
                row[col] = rng.randint(0, 4)
        rows.append(row)

    df = pd.DataFrame(rows)
    return df


@pytest.fixture(scope="module")
def real_df() -> pd.DataFrame:
    """Load the real preprocessed dataset for integration-level checks."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "dataset_preprocessed.csv"
    if not csv_path.exists():
        pytest.skip(f"dataset_preprocessed.csv not found at {csv_path}")
    return pd.read_csv(csv_path)


# ─── TestDataSplitter ────────────────────────────────────────────────────────
class TestDataSplitter:
    """Verify DataSplitter produces valid stratified splits."""

    def test_split_sizes_80_20(self, synthetic_df: pd.DataFrame) -> None:
        """Train/test sizes must match 80/20 split."""
        splitter = DataSplitter()
        X_train_text, X_test_text, _, _, y_train, y_test = splitter.split(synthetic_df)
        total = len(synthetic_df)
        assert abs(len(y_train) - int(0.80 * total)) <= 1, "Train size off"
        assert abs(len(y_test) - int(0.20 * total)) <= 1, "Test size off"

    def test_stratified_label_ratio_preserved(self, synthetic_df: pd.DataFrame) -> None:
        """Label ratio in train/test must be close to overall ratio (±5%)."""
        overall_scam_ratio = synthetic_df[LABEL_COL].mean()
        splitter = DataSplitter()
        _, _, _, _, y_train, y_test = splitter.split(synthetic_df)
        assert abs(y_train.mean() - overall_scam_ratio) < 0.05, "Train ratio drift"
        assert abs(y_test.mean() - overall_scam_ratio) < 0.05, "Test ratio drift"

    def test_no_overlap_between_train_and_test(self, real_df: pd.DataFrame) -> None:
        """Train and test indices must not overlap."""
        splitter = DataSplitter()
        X_train_text, X_test_text, _, _, y_train, y_test = splitter.split(real_df)
        train_idx = set(X_train_text.index)
        test_idx = set(X_test_text.index)
        assert len(train_idx & test_idx) == 0, "Train/Test index overlap detected!"


# ─── TestTextFeatureExtractor ────────────────────────────────────────────────
class TestTextFeatureExtractor:
    """Verify TF-IDF extractor follows zero-leakage protocol."""

    def test_vocabulary_built_from_train_only(self, synthetic_df: pd.DataFrame) -> None:
        """Vocabulary must be built exclusively from training text."""
        splitter = DataSplitter()
        X_train_text, X_test_text, _, _, _, _ = splitter.split(synthetic_df)
        extractor = TextFeatureExtractor()
        extractor.fit_transform_train(X_train_text)

        # Inject a word that ONLY exists in test to verify it's OOV (ignored)
        modified_test = X_test_text.copy()
        if len(modified_test) > 0:
            modified_test.iloc[0] = modified_test.iloc[0] + " xyzzzuniquetestword123"

        vocab_before = set(extractor.vectorizer.vocabulary_.keys())
        extractor.transform_test(modified_test)  # must NOT update vocab
        vocab_after = set(extractor.vectorizer.vocabulary_.keys())
        assert vocab_before == vocab_after, "Vocabulary changed after test transform — data leakage!"

    def test_transform_test_raises_if_not_fitted(self) -> None:
        """transform_test must raise RuntimeError if not fitted yet."""
        extractor = TextFeatureExtractor()
        with pytest.raises(RuntimeError):
            extractor.transform_test(pd.Series(["test text"]))

    def test_no_nan_inf_in_tfidf_matrix(self, synthetic_df: pd.DataFrame) -> None:
        """TF-IDF output matrices must not contain NaN or Inf."""
        splitter = DataSplitter()
        X_train_text, X_test_text, _, _, _, _ = splitter.split(synthetic_df)
        extractor = TextFeatureExtractor()
        X_train_tfidf = extractor.fit_transform_train(X_train_text)
        X_test_tfidf = extractor.transform_test(X_test_text)
        for name, mat in [("X_train_tfidf", X_train_tfidf), ("X_test_tfidf", X_test_tfidf)]:
            data = mat.data  # non-zero elements
            assert not np.isnan(data).any(), f"NaN in {name}"
            assert not np.isinf(data).any(), f"Inf in {name}"


# ─── TestAuxiliaryFeatureScaler ──────────────────────────────────────────────
class TestAuxiliaryFeatureScaler:
    """Verify StandardScaler follows zero-leakage protocol for aux features."""

    def test_scaler_uses_train_statistics_only(self, synthetic_df: pd.DataFrame) -> None:
        """Test set must not influence scaler's mean_ or scale_."""
        splitter = DataSplitter()
        _, _, X_train_aux, X_test_aux, _, _ = splitter.split(synthetic_df)
        scaler_obj = AuxiliaryFeatureScaler()
        scaler_obj.fit_transform_train(X_train_aux)

        mean_after_train = scaler_obj.scaler.mean_.copy()
        scale_after_train = scaler_obj.scaler.scale_.copy()

        scaler_obj.transform_test(X_test_aux)  # must NOT change fitted stats
        np.testing.assert_array_equal(
            mean_after_train, scaler_obj.scaler.mean_,
            err_msg="Scaler mean changed after transform_test — data leakage!",
        )
        np.testing.assert_array_equal(
            scale_after_train, scaler_obj.scaler.scale_,
            err_msg="Scaler scale changed after transform_test — data leakage!",
        )

    def test_transform_test_raises_if_not_fitted(self) -> None:
        """transform_test must raise RuntimeError if not fitted."""
        scaler_obj = AuxiliaryFeatureScaler()
        dummy = pd.DataFrame(np.zeros((5, len(AUX_FEATURE_COLS))), columns=AUX_FEATURE_COLS)
        with pytest.raises(RuntimeError):
            scaler_obj.transform_test(dummy)

    def test_no_nan_inf_in_scaled_output(self, synthetic_df: pd.DataFrame) -> None:
        """Scaled auxiliary features must not contain NaN or Inf."""
        splitter = DataSplitter()
        _, _, X_train_aux, X_test_aux, _, _ = splitter.split(synthetic_df)
        scaler_obj = AuxiliaryFeatureScaler()
        X_train_scaled = scaler_obj.fit_transform_train(X_train_aux)
        X_test_scaled = scaler_obj.transform_test(X_test_aux)
        for name, arr in [("X_train_scaled", X_train_scaled), ("X_test_scaled", X_test_scaled)]:
            assert not np.isnan(arr).any(), f"NaN in {name}"
            assert not np.isinf(arr).any(), f"Inf in {name}"


# ─── TestFeatureMatrixShape ───────────────────────────────────────────────────
class TestFeatureMatrixShape:
    """Verify final combined matrices have expected shapes (n_samples × 5015)."""

    def test_combined_matrix_shape_real_data(self, real_df: pd.DataFrame) -> None:
        """X_train and X_test columns must equal EXPECTED_N_FEATURES (5015)."""
        splitter = DataSplitter()
        X_train_text, X_test_text, X_train_aux, X_test_aux, y_train, y_test = splitter.split(real_df)

        extractor = TextFeatureExtractor()
        X_train_tfidf = extractor.fit_transform_train(X_train_text)
        X_test_tfidf = extractor.transform_test(X_test_text)

        scaler_obj = AuxiliaryFeatureScaler()
        X_train_aux_scaled = scaler_obj.fit_transform_train(X_train_aux)
        X_test_aux_scaled = scaler_obj.transform_test(X_test_aux)

        X_train = assemble_feature_matrix(X_train_tfidf, X_train_aux_scaled)
        X_test = assemble_feature_matrix(X_test_tfidf, X_test_aux_scaled)

        assert X_train.shape[0] == len(y_train), "Train row count mismatch"
        assert X_test.shape[0] == len(y_test), "Test row count mismatch"
        assert X_train.shape[1] == EXPECTED_N_FEATURES, (
            f"Expected {EXPECTED_N_FEATURES} features, got {X_train.shape[1]}"
        )
        assert X_test.shape[1] == EXPECTED_N_FEATURES, (
            f"Test expected {EXPECTED_N_FEATURES} features, got {X_test.shape[1]}"
        )

    def test_train_test_same_number_of_columns(self, real_df: pd.DataFrame) -> None:
        """X_train and X_test must have identical column counts."""
        splitter = DataSplitter()
        X_train_text, X_test_text, X_train_aux, X_test_aux, _, _ = splitter.split(real_df)
        extractor = TextFeatureExtractor()
        X_train_tfidf = extractor.fit_transform_train(X_train_text)
        X_test_tfidf = extractor.transform_test(X_test_text)
        scaler_obj = AuxiliaryFeatureScaler()
        X_train_scaled = scaler_obj.fit_transform_train(X_train_aux)
        X_test_scaled = scaler_obj.transform_test(X_test_aux)
        X_train = assemble_feature_matrix(X_train_tfidf, X_train_scaled)
        X_test = assemble_feature_matrix(X_test_tfidf, X_test_scaled)
        assert X_train.shape[1] == X_test.shape[1], "Column count mismatch between train and test"


# ─── TestReproducibility ─────────────────────────────────────────────────────
class TestReproducibility:
    """Verify bit-identical results across 2 runs with random_state=42."""

    def test_two_runs_produce_identical_y_train(self, real_df: pd.DataFrame) -> None:
        """Two independent splits with same seed must yield identical y_train."""
        splitter1 = DataSplitter()
        splitter2 = DataSplitter()
        _, _, _, _, y_train1, y_test1 = splitter1.split(real_df)
        _, _, _, _, y_train2, y_test2 = splitter2.split(real_df)
        np.testing.assert_array_equal(y_train1.values, y_train2.values, err_msg="y_train not reproducible")
        np.testing.assert_array_equal(y_test1.values, y_test2.values, err_msg="y_test not reproducible")

    def test_tfidf_vocab_identical_across_runs(self, real_df: pd.DataFrame) -> None:
        """TF-IDF vocabulary must be identical for both runs."""
        splitter = DataSplitter()
        X_train_text1, _, _, _, _, _ = splitter.split(real_df)
        X_train_text2, _, _, _, _, _ = splitter.split(real_df)

        ext1 = TextFeatureExtractor()
        ext2 = TextFeatureExtractor()
        ext1.fit_transform_train(X_train_text1)
        ext2.fit_transform_train(X_train_text2)

        assert ext1.vectorizer.vocabulary_ == ext2.vectorizer.vocabulary_, "TF-IDF vocab not reproducible"
