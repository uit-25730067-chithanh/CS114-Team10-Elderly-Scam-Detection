#!/usr/bin/env python3
"""
Rebuild models/best_model_bundle.pkl using the highest-F1 model among the
5.015-dim candidates (XGBoost, Random Forest, SVM Linear) currently available
as .pkl files in models/. Naive Bayes is excluded: it runs on the 5.000-dim
TF-IDF-only ablation space (Phase 04), not the full 5.015-dim contract.

Per models/README.md: "best_model_bundle.pkl = Model tốt nhất (F1 cao nhất)".
Run from draft/scam-detection/ directory whenever model artifacts change
(e.g. after Phase 07 re-evaluation) to refresh the Phase 08 interface contract.

Author: Bùi Thị Mỷ Cẩm (MSSV: 25730013)
"""
from __future__ import annotations

import json
import os
import sys
import warnings
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import pandas as pd
import sklearn
from scipy.sparse import csr_matrix, hstack

from src.feature_engineering_config import AUX_FEATURE_COLS
from src.preprocessing.pipeline import preprocess_pipeline
from src.utils.helpers import RANDOM_STATE

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"

# 5.015-dim candidates only — (metrics_json, model_pkl, display_name, algorithm_label)
CANDIDATES = [
    ("xgboost_metrics.json", "xgboost.pkl", "XGBoost", "XGBoost Classifier"),
    ("random_forest_metrics.json", "random_forest.pkl", "Random Forest", "Random Forest Classifier"),
    ("svm_metrics.json", "svm_linear.pkl", "SVM Linear", "Support Vector Machine (LinearSVC)"),
]


def predict_raw_text(text: str, bundle: dict) -> dict:
    cleaned_text, aux_dict = preprocess_pipeline(text)
    aux_df = pd.DataFrame([aux_dict])[AUX_FEATURE_COLS]
    aux_scaled = bundle["aux_scaler"].transform(aux_df.values)
    tfidf_vec = bundle["vectorizer"].transform([cleaned_text])
    full_vec = hstack([tfidf_vec, csr_matrix(aux_scaled)])
    proba = float(bundle["model"].predict_proba(full_vec)[0][1])
    label = 1 if proba >= bundle.get("threshold", 0.5) else 0
    return {"label": label, "risk_score": proba}


def main() -> None:
    warnings.filterwarnings("ignore")

    print("=" * 70)
    print("  REBUILD models/best_model_bundle.pkl — chọn model F1 cao nhất")
    print("=" * 70)

    ranked = []
    for metrics_name, model_name, display_name, algo_label in CANDIDATES:
        metrics_path = MODELS_DIR / metrics_name
        model_path = MODELS_DIR / model_name
        if not metrics_path.exists() or not model_path.exists():
            print(f"  [skip] {display_name}: thiếu {metrics_name if not metrics_path.exists() else model_name}")
            continue
        with open(metrics_path, encoding="utf-8") as f:
            record = json.load(f)
        f1 = record["test_metrics"]["f1"]
        ranked.append((f1, display_name, algo_label, model_path, record["test_metrics"]))
        print(f"  [ok]   {display_name}: F1={f1:.4f}")

    if not ranked:
        raise RuntimeError("Không tìm thấy model 5.015-dim nào hợp lệ trong models/.")

    ranked.sort(key=lambda x: x[0], reverse=True)
    best_f1, best_name, best_algo, best_model_path, best_test_metrics = ranked[0]
    print(f"\n  -> Model tốt nhất: {best_name} (F1={best_f1:.4f})")

    model = joblib.load(best_model_path)
    tfidf_vectorizer = joblib.load(DATA_DIR / "tfidf_vectorizer.pkl")
    aux_scaler = joblib.load(DATA_DIR / "aux_scaler.pkl")
    with open(DATA_DIR / "feature_names.json", encoding="utf-8") as f:
        feature_names = json.load(f)

    bundle = {
        "model": model,
        "vectorizer": tfidf_vectorizer,
        "aux_scaler": aux_scaler,
        "feature_names": feature_names,
        "model_name": best_name,
        "threshold": 0.5,
        "metrics": {
            "f1": best_test_metrics["f1"],
            "recall_scam": best_test_metrics["recall"],
            "precision": best_test_metrics["precision"],
            "roc_auc": best_test_metrics["roc_auc"],
        },
        "metadata": {
            "algorithm": best_algo,
            "random_state": RANDOM_STATE,
            "sklearn_version": sklearn.__version__,
        },
    }
    bundle_file = MODELS_DIR / "best_model_bundle.pkl"
    joblib.dump(bundle, bundle_file)
    bundle_size_mb = os.path.getsize(bundle_file) / (1024 * 1024)
    print(f"  Bundle saved: {bundle_file} ({bundle_size_mb:.2f} MB)")

    sample_scam = (
        "Chào ông/bà, chúng tôi là công an điều tra, tài khoản của ông/bà liên quan đường dây "
        "rửa tiền, chuyển khoản ngay 50 triệu để xác minh kẻo bị bắt giam"
    )
    sample_normal = (
        "Ngân hàng thông báo số dư tài khoản của bạn vào ngày hôm nay là 3.250.000 đồng. "
        "Cảm ơn quý khách đã sử dụng dịch vụ."
    )
    print("\n  --- Self-test hợp đồng suy luận (raw text -> prediction) ---")
    for label_txt, txt in [("SCAM mẫu", sample_scam), ("NORMAL mẫu", sample_normal)]:
        result = predict_raw_text(txt, bundle)
        print(f"  [{label_txt}] label={result['label']}, risk_score={result['risk_score']:.4f}")

    print(f"\n✅ best_model_bundle.pkl hiện đóng gói {best_name} (F1={best_f1:.4f}).")


if __name__ == "__main__":
    main()
