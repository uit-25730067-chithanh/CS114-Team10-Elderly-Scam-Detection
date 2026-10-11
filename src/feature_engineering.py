"""
CS114 Final Project — Scam Detection
Zero-Leakage Feature Engineering Pipeline for Vietnamese Elderly Scam Detection.

This module implements the stratified train/test split, TF-IDF feature extraction,
and auxiliary feature scaling following strict UIT academic anti-leakage protocol.

CRITICAL INVARIANT: TfidfVectorizer and StandardScaler are ONLY fitted on the
training set. The test set is NEVER used to influence vocabulary or scaling weights.

Author: Đặng Chí Thanh (MSSV: 25730067)
Phase: 03 — EDA & Feature Engineering
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.feature_engineering_config import (
    AUX_FEATURE_COLS,
    LABEL_COL,
    TEXT_COL,
    TFIDF_MAX_DF,
    TFIDF_MAX_FEATURES,
    TFIDF_MIN_DF,
    TFIDF_NGRAM_RANGE,
    TFIDF_SUBLINEAR_TF,
)
from src.utils import RANDOM_STATE, TEST_SIZE, get_data_dir

logger = logging.getLogger(__name__)


# ─── Class: DataSplitter ─────────────────────────────────────────────────────
class DataSplitter:
    """Perform a stratified 80/20 train/test split.

    Must be called BEFORE any feature extraction to prevent data leakage.
    """

    def __init__(self, test_size: float = TEST_SIZE, random_state: int = RANDOM_STATE) -> None:
        self.test_size = test_size
        self.random_state = random_state

    def split(
        self, df: pd.DataFrame
    ) -> Tuple[pd.Series, pd.Series, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Split dataframe into stratified train/test sets.

        Returns: X_train_text, X_test_text, X_train_aux, X_test_aux, y_train, y_test
        """
        missing = [c for c in [TEXT_COL, LABEL_COL] + AUX_FEATURE_COLS if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        X_train_text, X_test_text, X_train_aux, X_test_aux, y_train, y_test = train_test_split(
            df[TEXT_COL], df[AUX_FEATURE_COLS], df[LABEL_COL],
            test_size=self.test_size, random_state=self.random_state, stratify=df[LABEL_COL],
        )
        logger.info("Split: train=%d, test=%d (stratified)", len(y_train), len(y_test))
        return X_train_text, X_test_text, X_train_aux, X_test_aux, y_train, y_test


# ─── Class: TextFeatureExtractor ─────────────────────────────────────────────
class TextFeatureExtractor:
    """Extract TF-IDF features with strict zero-leakage protocol."""

    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(
            max_features=TFIDF_MAX_FEATURES, ngram_range=TFIDF_NGRAM_RANGE,
            min_df=TFIDF_MIN_DF, max_df=TFIDF_MAX_DF, sublinear_tf=TFIDF_SUBLINEAR_TF,
        )

    def fit_transform_train(self, X_train_text: pd.Series) -> sp.csr_matrix:
        """Fit vocabulary ONLY on training text, then transform."""
        if X_train_text.isnull().any():
            raise ValueError("X_train_text contains null values.")
        result = self.vectorizer.fit_transform(X_train_text)
        logger.info("TF-IDF fit: vocab=%d, shape=%s", len(self.vectorizer.vocabulary_), result.shape)
        return result

    def transform_test(self, X_test_text: pd.Series) -> sp.csr_matrix:
        """Transform test text using train-fitted vocabulary only."""
        if not hasattr(self.vectorizer, "vocabulary_"):
            raise RuntimeError("Vectorizer must be fitted via fit_transform_train first.")
        return self.vectorizer.transform(X_test_text)

    def get_feature_names(self) -> list[str]:
        """Return n-gram feature names from fitted vocabulary."""
        if not hasattr(self.vectorizer, "vocabulary_"):
            raise RuntimeError("Vectorizer must be fitted before get_feature_names.")
        return list(self.vectorizer.get_feature_names_out())


# ─── Class: AuxiliaryFeatureScaler ───────────────────────────────────────────
class AuxiliaryFeatureScaler:
    """Scale 15 auxiliary numeric features with strict zero-leakage protocol."""

    def __init__(self) -> None:
        self.scaler = StandardScaler()

    def fit_transform_train(self, X_train_aux: pd.DataFrame) -> np.ndarray:
        """Fit scaler on train auxiliary features and return scaled array."""
        result = self.scaler.fit_transform(X_train_aux.values.astype(float))
        logger.info("Scaler fit: %d features, %d samples", X_train_aux.shape[1], X_train_aux.shape[0])
        return result

    def transform_test(self, X_test_aux: pd.DataFrame) -> np.ndarray:
        """Transform test aux features using train-fitted scaler parameters."""
        if not hasattr(self.scaler, "mean_"):
            raise RuntimeError("Scaler must be fitted via fit_transform_train first.")
        return self.scaler.transform(X_test_aux.values.astype(float))


# ─── Helpers ─────────────────────────────────────────────────────────────────
def assemble_feature_matrix(tfidf_matrix: sp.csr_matrix, aux_scaled: np.ndarray) -> sp.csr_matrix:
    """Horizontally stack sparse TF-IDF matrix with dense auxiliary features."""
    return sp.hstack([tfidf_matrix, sp.csr_matrix(aux_scaled)], format="csr")


def export_feature_matrices(df: pd.DataFrame, output_dir: Path | None = None) -> dict:
    """Run zero-leakage feature pipeline and export all training artifacts.

    Pipeline order (MUST NOT be reordered):
        1. Stratified split (80/20) — FIRST
        2. TF-IDF fit on X_train_text → transform X_test_text
        3. StandardScaler fit on X_train_aux → transform X_test_aux
        4. hstack(tfidf, aux) for train and test
        5. Export pkl + feature_names.json

    Returns: dict with X_train, X_test, y_train, y_test, vectorizer, scaler,
             feature_names, split_info.
    """
    if output_dir is None:
        output_dir = get_data_dir() / "processed"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    splitter = DataSplitter()
    X_train_text, X_test_text, X_train_aux, X_test_aux, y_train, y_test = splitter.split(df)

    text_extractor = TextFeatureExtractor()
    X_train_tfidf = text_extractor.fit_transform_train(X_train_text)
    X_test_tfidf = text_extractor.transform_test(X_test_text)

    aux_scaler = AuxiliaryFeatureScaler()
    X_train_aux_scaled = aux_scaler.fit_transform_train(X_train_aux)
    X_test_aux_scaled = aux_scaler.transform_test(X_test_aux)

    X_train = assemble_feature_matrix(X_train_tfidf, X_train_aux_scaled)
    X_test = assemble_feature_matrix(X_test_tfidf, X_test_aux_scaled)

    all_feature_names = text_extractor.get_feature_names() + AUX_FEATURE_COLS
    assert len(all_feature_names) == X_train.shape[1], (
        f"Feature count mismatch: {len(all_feature_names)} != {X_train.shape[1]}"
    )

    joblib.dump(X_train, output_dir / "X_train.pkl")
    joblib.dump(X_test, output_dir / "X_test.pkl")
    joblib.dump(y_train, output_dir / "y_train.pkl")
    joblib.dump(y_test, output_dir / "y_test.pkl")
    joblib.dump(text_extractor.vectorizer, output_dir / "tfidf_vectorizer.pkl")
    joblib.dump(aux_scaler.scaler, output_dir / "aux_scaler.pkl")

    with open(output_dir / "feature_names.json", "w", encoding="utf-8") as f:
        json.dump(all_feature_names, f, ensure_ascii=False, indent=2)

    split_info = {
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "n_features": int(X_train.shape[1]),
        "n_tfidf_features": int(X_train_tfidf.shape[1]),
        "n_aux_features": len(AUX_FEATURE_COLS),
        "train_scam_ratio": float(y_train.mean()),
        "test_scam_ratio": float(y_test.mean()),
    }
    logger.info("Export done: X_train=%s, X_test=%s", X_train.shape, X_test.shape)
    return {
        "X_train": X_train, "X_test": X_test,
        "y_train": y_train, "y_test": y_test,
        "vectorizer": text_extractor.vectorizer, "scaler": aux_scaler.scaler,
        "feature_names": all_feature_names, "split_info": split_info,
    }
