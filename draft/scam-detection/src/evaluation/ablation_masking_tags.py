"""
CS114 Final Project — Scam Detection
Ablation: how much do the dataset's anonymisation tags ([MONEY], [NUMBER], [ĐƯỜNG_DẪN]...) matter?

The raw dataset comes from sources that were masked with different tag schemes (normal messages carry
[MONEY]/[NUMBER]/[TIME]; several scam messages carry [ĐƯỜNG_DẪN]/[THƯƠNG_HIỆU]/[SỐ_TIỀN]). This script
(1) measures how class-specific the Top-20 consensus keywords are and (2) retrains XGBoost and Naive Bayes
with every tag-derived feature removed, using the exact training recipe of notebooks 03/04.

Output: reports/ablation_masking_tags.json (read by reports/slides/generate_slides.js).

Author: Bùi Thị Mỷ Cẩm (MSSV: 25730013)
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from scipy import sparse
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB

from src.utils import RANDOM_STATE

TAG_MIN_DOCS = 10          # a bracket tag counts as an anonymisation tag if it appears in >= 10 messages
TFIDF_DIMS = 5000          # Naive Bayes uses the TF-IDF block only (aux features are negative)
# Top-20 consensus keywords of the 4 models (Phase 07, plans/.../phase-07-evaluation-xai.md)
TOP20_CONSENSUS = [
    "money", "số_tiền", "thương_hiệu", "liên_hệ 198", "đường_dẫn", "number", "mày", "số_định_danh",
    "198", "gấp", "viện_phí", "chị", "doi", "soạn", "thuế", "đang", "số_lượng", "viettel", "time", "sẽ",
]


def _metrics(y_true, y_pred) -> dict[str, float]:
    return {
        "f1": round(float(f1_score(y_true, y_pred)), 4),
        "recall": round(float(recall_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred)), 4),
    }


def _fit_eval(X_tr, X_te, y_tr, y_te, xgb_params: dict, scale_pw: float) -> dict[str, dict[str, float]]:
    """Same recipe as the notebooks: NB(alpha=0.01) on TF-IDF only, XGBoost(best_params) on all features."""
    nb = MultinomialNB(alpha=0.01).fit(X_tr[:, :TFIDF_DIMS], y_tr)
    model = xgb.XGBClassifier(
        **xgb_params, scale_pos_weight=scale_pw, random_state=RANDOM_STATE, eval_metric="logloss", n_jobs=-1
    ).fit(X_tr, y_tr)
    return {"naive_bayes": _metrics(y_te, nb.predict(X_te[:, :TFIDF_DIMS])), "xgboost": _metrics(y_te, model.predict(X_te))}


def main() -> None:
    processed = PROJECT_ROOT / "data" / "processed"
    raw = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "dataset.csv", encoding="utf-8-sig")
    pre = pd.read_csv(processed / "dataset_preprocessed.csv", encoding="utf-8-sig")
    names = json.loads((processed / "feature_names.json").read_text(encoding="utf-8-sig"))
    names = names if isinstance(names, list) else names["feature_names"]
    X_tr = joblib.load(processed / "X_train.pkl").tocsr()
    X_te = joblib.load(processed / "X_test.pkl").tocsr()
    y_tr = np.asarray(joblib.load(processed / "y_train.pkl"))
    y_te = np.asarray(joblib.load(processed / "y_test.pkl"))
    xgb_meta = json.loads((PROJECT_ROOT / "models" / "xgboost_metrics.json").read_text(encoding="utf-8-sig"))
    scale_pw = float((y_tr == 0).sum() / (y_tr == 1).sum())

    # 1. anonymisation tags present in the raw text, and their class split
    tag_docs = collections.Counter()
    tag_by_class: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0])
    for text, label in zip(raw.text, raw.label):
        for tag in set(re.findall(r"\[([^\]\s]{1,25})\]", text)):
            tag_docs[tag.lower()] += 1
            tag_by_class[tag.lower()][int(label)] += 1
    tags = {t for t, n in tag_docs.items() if n >= TAG_MIN_DOCS}

    # 2. class-specificity of the Top-20 keywords (share of scam among messages that contain the keyword)
    padded = [f" {t} " for t in pre.text_cleaned.fillna("")]
    labels = pre.label.to_numpy()
    keyword_share = {}
    for kw in TOP20_CONSENSUS:
        hit = np.array([f" {kw} " in t for t in padded])
        n = int(hit.sum())
        keyword_share[kw] = {"docs": n, "scam_share": round(float(labels[hit].mean()), 4) if n else None}

    # 3. ablation: zero every feature (unigram/bigram) that contains an anonymisation-tag token
    drop = [i for i, name in enumerate(names[:TFIDF_DIMS]) if any(tok in tags for tok in name.split())]
    keep = np.ones(X_tr.shape[1])
    keep[drop] = 0
    D = sparse.diags(keep)
    baseline = _fit_eval(X_tr, X_te, y_tr, y_te, xgb_meta["best_params"], scale_pw)
    ablated = _fit_eval(X_tr @ D, X_te @ D, y_tr, y_te, xgb_meta["best_params"], scale_pw)

    reported = xgb_meta["test_metrics"]["f1"]
    result = {
        "tags_min_docs": TAG_MIN_DOCS,
        "tags": sorted(tags),
        "tag_class_split": {t: {"normal": v[0], "scam": v[1]} for t, v in tag_by_class.items() if t in tags},
        "features_removed": len(drop),
        "features_total_tfidf": TFIDF_DIMS,
        "baseline": baseline,
        "without_tags": ablated,
        "baseline_matches_reported_xgb_f1": abs(baseline["xgboost"]["f1"] - reported) < 5e-4,
        "keyword_scam_share": keyword_share,
        "overall_scam_share": round(float(labels.mean()), 4),
        "random_state": RANDOM_STATE,
    }
    out = PROJECT_ROOT / "reports" / "ablation_masking_tags.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"tags ({len(tags)}): {sorted(tags)}")
    print(f"features removed: {len(drop)}/{TFIDF_DIMS}")
    print(f"baseline    : {baseline}   (reported XGBoost F1 = {reported:.4f}, reproduced = {result['baseline_matches_reported_xgb_f1']})")
    print(f"without tags: {ablated}")
    print(f"saved -> {out}")


if __name__ == "__main__":
    main()
