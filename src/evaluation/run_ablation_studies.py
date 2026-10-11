"""CS114 Final Project — Scam Detection: Ablation Studies Runner (Phase 09).
Strictly adheres to UIT Zero-Data-Leakage protocol (fit solely on train, transform on test).
Author: Đặng Chí Thanh (MSSV: 25730067)
"""

from __future__ import annotations

import json
import logging
import sys
import warnings
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

warnings.filterwarnings("ignore")
import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier

from src.evaluation.metrics_calculator import evaluate_single_model, format_markdown_table
from src.feature_engineering_config import (
    TFIDF_MAX_DF,
    TFIDF_MAX_FEATURES,
    TFIDF_MIN_DF,
    TFIDF_NGRAM_RANGE,
    TFIDF_SUBLINEAR_TF,
)
from src.utils import RANDOM_STATE, TEST_SIZE

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def create_xgb_model() -> XGBClassifier:
    """Instantiate XGBoost classifier with verified Phase 05 tuned hyperparameters."""
    return XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.7,
        colsample_bytree=0.8,
        scale_pos_weight=4.220238095238095,
        random_state=RANDOM_STATE,
        eval_metric="logloss",
    )


def create_svm_model() -> CalibratedClassifierCV:
    """Instantiate Calibrated Linear SVM with verified Phase 06 tuned hyperparameters."""
    base_svc = LinearSVC(C=10.0, class_weight="balanced", max_iter=10000, random_state=RANDOM_STATE)
    return CalibratedClassifierCV(estimator=base_svc, cv=5)


def run_preprocessing_ablation(project_root: Path) -> dict[str, Any]:
    """Experiment 1: Preprocessing Ablation (Raw vs Preprocessed text)."""
    logger.info("Running Experiment 1: Preprocessing Ablation...")
    raw_csv = project_root / "data" / "raw" / "dataset.csv"
    processed_dir = project_root / "data" / "processed"

    df_raw = pd.read_csv(raw_csv)
    raw_train_text, raw_test_text, y_train_raw, y_test_raw = train_test_split(
        df_raw["text"],
        df_raw["label"],
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df_raw["label"],
    )

    # 1. Independent Raw TF-IDF Vectorizer (Zero-Leakage: fit ONLY on raw train)
    raw_vec = TfidfVectorizer(
        max_features=TFIDF_MAX_FEATURES,
        ngram_range=TFIDF_NGRAM_RANGE,
        min_df=TFIDF_MIN_DF,
        max_df=TFIDF_MAX_DF,
        sublinear_tf=TFIDF_SUBLINEAR_TF,
    )
    X_train_raw = raw_vec.fit_transform(raw_train_text)
    X_test_raw = raw_vec.transform(raw_test_text)

    # 2. Preprocessed TF-IDF (Loaded directly from Phase 03 feature matrices)
    X_train_all = joblib.load(processed_dir / "X_train.pkl")
    X_test_all = joblib.load(processed_dir / "X_test.pkl")
    y_train = joblib.load(processed_dir / "y_train.pkl")
    y_test = joblib.load(processed_dir / "y_test.pkl")

    X_train_prep = X_train_all[:, :TFIDF_MAX_FEATURES]
    X_test_prep = X_test_all[:, :TFIDF_MAX_FEATURES]

    models_to_test = [
        ("XGBoost", create_xgb_model()),
        ("Naive Bayes", MultinomialNB(alpha=0.01)),
    ]

    records = []
    for model_name, model_inst in models_to_test:
        model_raw = model_inst.__class__(**model_inst.get_params())
        model_raw.fit(X_train_raw, y_train_raw)
        records.append(evaluate_single_model(model_raw, X_test_raw, y_test_raw, f"{model_name} (Raw Text)"))

        model_prep = model_inst.__class__(**model_inst.get_params())
        model_prep.fit(X_train_prep, y_train)
        records.append(evaluate_single_model(model_prep, X_test_prep, y_test, f"{model_name} (Preprocessed)"))

    df_res = pd.DataFrame(records)
    logger.info("Experiment 1 complete.")
    return {"df": df_res, "records": records}


def run_feature_space_ablation(project_root: Path) -> dict[str, Any]:
    """Experiment 2: Feature Space Ablation (TF-IDF vs Aux vs Combined)."""
    logger.info("Running Experiment 2: Feature Space Ablation...")
    processed_dir = project_root / "data" / "processed"
    models_dir = project_root / "models"

    X_train = joblib.load(processed_dir / "X_train.pkl")
    X_test = joblib.load(processed_dir / "X_test.pkl")
    y_train = joblib.load(processed_dir / "y_train.pkl")
    y_test = joblib.load(processed_dir / "y_test.pkl")

    slices = {
        "TF-IDF Only (5,000)": (X_train[:, :TFIDF_MAX_FEATURES], X_test[:, :TFIDF_MAX_FEATURES]),
        "Aux Only (15)": (X_train[:, TFIDF_MAX_FEATURES:], X_test[:, TFIDF_MAX_FEATURES:]),
        "Combined (5,015)": (X_train, X_test),
    }

    records = []
    for slice_name, (X_tr, X_te) in slices.items():
        # XGBoost
        if slice_name == "Combined (5,015)" and (models_dir / "xgboost.pkl").is_file():
            xgb_model = joblib.load(models_dir / "xgboost.pkl")
        else:
            xgb_model = create_xgb_model()
            xgb_model.fit(X_tr, y_train)
        records.append(evaluate_single_model(xgb_model, X_te, y_test, f"XGBoost — {slice_name}"))

        # Linear SVM
        if slice_name == "Combined (5,015)" and (models_dir / "svm_linear.pkl").is_file():
            svm_model = joblib.load(models_dir / "svm_linear.pkl")
        else:
            svm_model = create_svm_model()
            svm_model.fit(X_tr, y_train)
        records.append(evaluate_single_model(svm_model, X_te, y_test, f"SVM Linear — {slice_name}"))

    df_res = pd.DataFrame(records)
    logger.info("Experiment 2 complete.")
    return {"df": df_res, "records": records}


def main() -> None:
    """Orchestrate both ablation experiments and save artifacts."""
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    exp1_res = run_preprocessing_ablation(PROJECT_ROOT)
    exp2_res = run_feature_space_ablation(PROJECT_ROOT)

    md_table_exp1 = format_markdown_table(exp1_res["df"])
    md_table_exp2 = format_markdown_table(exp2_res["df"])

    output_payload = {
        "experiment_1_preprocessing_ablation": {
            "title": "Thực nghiệm đối chứng 1: Vai trò của Tiền xử lý NLP",
            "models": ["XGBoost", "Naive Bayes"],
            "records": exp1_res["records"],
            "markdown_table": md_table_exp1,
        },
        "experiment_2_feature_space_ablation": {
            "title": "Thực nghiệm đối chứng 2: Vai trò của 15 Đặc trưng tâm lý",
            "models": ["XGBoost", "SVM Linear"],
            "records": exp2_res["records"],
            "markdown_table": md_table_exp2,
        },
    }

    out_file = reports_dir / "ablation_studies.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)
    logger.info("Saved ablation results to %s", out_file)

    print("\n" + "=" * 80)
    print("📊 BẢNG ĐỐI CHỨNG 1: VAI TRÒ CỦA TIỀN XỬ LÝ NLP (RAW VS PREPROCESSED)")
    print("=" * 80 + "\n" + md_table_exp1)
    print("\n" + "=" * 80)
    print("📊 BẢNG ĐỐI CHỨNG 2: VAI TRÒ CỦA 15 ĐẶC TRƯNG TÂM LÝ (TF-IDF VS AUX VS KẾT HỢP)")
    print("=" * 80 + "\n" + md_table_exp2 + "\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
