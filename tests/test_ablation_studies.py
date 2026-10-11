"""
CS114 Final Project — Scam Detection
Unit Tests for Ablation Studies Runner (Phase 09).

Verifies execution, structure, and integrity of run_ablation_studies.py.
Author: Đặng Chí Thanh (MSSV: 25730067)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.run_ablation_studies import (
    create_svm_model,
    create_xgb_model,
    run_feature_space_ablation,
    run_preprocessing_ablation,
)


def test_model_initialization():
    """Verify factory functions create valid model instances with correct params."""
    xgb = create_xgb_model()
    assert xgb.n_estimators == 300
    assert xgb.max_depth == 5
    assert xgb.random_state == 42

    svm = create_svm_model()
    assert svm.estimator.C == 10.0
    assert svm.cv == 5


def test_ablation_artifacts_exist():
    """Verify that reports/ablation_studies.json exists and adheres to schema."""
    json_path = PROJECT_ROOT / "reports" / "ablation_studies.json"
    assert json_path.is_file(), "ablation_studies.json must exist"

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "experiment_1_preprocessing_ablation" in data
    assert "experiment_2_feature_space_ablation" in data

    exp1 = data["experiment_1_preprocessing_ablation"]
    assert len(exp1["records"]) == 4
    for r in exp1["records"]:
        assert "model" in r
        assert 0.0 <= r["f1"] <= 1.0
        assert 0.0 <= r["precision"] <= 1.0
        assert 0.0 <= r["recall"] <= 1.0

    exp2 = data["experiment_2_feature_space_ablation"]
    assert len(exp2["records"]) == 6
    for r in exp2["records"]:
        assert "model" in r
        assert 0.0 <= r["f1"] <= 1.0
