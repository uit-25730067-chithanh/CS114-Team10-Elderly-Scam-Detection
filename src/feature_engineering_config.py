"""
CS114 Final Project — Scam Detection
Feature Engineering Configuration Constants.

Centralized constants for the zero-leakage feature engineering pipeline.
Import from here to avoid magic numbers scattered across modules.

Author: Đặng Chí Thanh (MSSV: 25730067)
Phase: 03 — EDA & Feature Engineering
"""

from __future__ import annotations

# ─── Auxiliary Feature Column Names (15 columns from Phase 02) ───────────────
AUX_FEATURE_COLS: list[str] = [
    "num_urls",
    "num_phone_numbers",
    "num_money_mentions",
    "has_urgent_words",
    "num_authority_words",
    "has_emergency_words",
    "has_gift_words",
    "has_otp_request",
    "has_leet_speak",
    "is_unaccented",
    "text_length",
    "num_words",
    "num_exclamation",
    "num_question",
    "num_uppercase_words",
]

# ─── Column Names ─────────────────────────────────────────────────────────────
TEXT_COL: str = "text_cleaned"
LABEL_COL: str = "label"

# ─── TF-IDF Hyperparameters ──────────────────────────────────────────────────
TFIDF_MAX_FEATURES: int = 5000
TFIDF_NGRAM_RANGE: tuple[int, int] = (1, 2)
TFIDF_MIN_DF: int = 2
TFIDF_MAX_DF: float = 0.95
TFIDF_SUBLINEAR_TF: bool = True

# ─── Expected Output Dimension (for test assertions) ─────────────────────────
EXPECTED_N_FEATURES: int = TFIDF_MAX_FEATURES + len(AUX_FEATURE_COLS)  # 5015
