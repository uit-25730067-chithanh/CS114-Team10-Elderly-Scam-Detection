"""Model adapter for elderly scam detection web app.

Combines Machine Learning model inference (XGBoost / Random Forest trained on 5,015 features)
with domain knowledge psychological risk safeguards for robust prediction.
"""

from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional, Tuple

import joblib
import pandas as pd
from scipy.sparse import csr_matrix, hstack

# Add parent directory to sys.path to access src modules
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_DIR = os.path.dirname(CURRENT_DIR)
PROJECT_DIR = os.path.dirname(DEMO_DIR)

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from src.feature_engineering_config import AUX_FEATURE_COLS
from src.preprocessing.pipeline import extract_auxiliary_features
from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.tokenizer import segment_vietnamese


class ScamDetectionModel:
    """Manages model artifacts and performs hybrid ML + heuristic inference."""

    def __init__(self):
        self.vectorizer = None
        self.scaler = None
        self.model = None
        self.model_name = "Rule-based Fallback"
        self.is_ready = False
        self._load_artifacts()

    def _load_artifacts(self):
        """Attempts to load trained TF-IDF vectorizer, scaler, and XGBoost/RF models."""
        vec_path = os.path.join(PROJECT_DIR, "data", "processed", "tfidf_vectorizer.pkl")
        scaler_path = os.path.join(PROJECT_DIR, "data", "processed", "aux_scaler.pkl")
        xgb_path = os.path.join(PROJECT_DIR, "models", "xgboost.pkl")
        rf_path = os.path.join(PROJECT_DIR, "models", "random_forest.pkl")

        try:
            if os.path.exists(vec_path) and os.path.exists(scaler_path):
                self.vectorizer = joblib.load(vec_path)
                self.scaler = joblib.load(scaler_path)

                if os.path.exists(xgb_path):
                    self.model = joblib.load(xgb_path)
                    self.model_name = "XGBoost (5.015 đặc trưng, F1=0.9535)"
                    self.is_ready = True
                elif os.path.exists(rf_path):
                    self.model = joblib.load(rf_path)
                    self.model_name = "Random Forest (5.015 đặc trưng, Recall=97.6%)"
                    self.is_ready = True
        except Exception as e:
            print(f"[!] Warning: Could not load ML artifacts: {e}")
            self.is_ready = False

    def predict(self, raw_text: str) -> Dict[str, Any]:
        """Performs robust inference on user-submitted message."""
        if not raw_text or not raw_text.strip():
            return {
                "risk_score": 0.0,
                "is_scam": False,
                "model_used": self.model_name,
                "aux_features": {},
                "cleaned_text": "",
                "tokenized_text": "",
            }

        # 1. Trích xuất 15 đặc trưng phụ (tâm lý, đe dọa, tiền bạc, liên kết)
        aux_dict = extract_auxiliary_features(raw_text)

        # 2. Tiền xử lý văn bản tiếng Việt
        cleaned = clean_text(raw_text)
        tokenized = segment_vietnamese(cleaned)

        # 3. Tính điểm bẫy tâm lý theo domain rule
        heuristic_score = 0.0
        # Authority fear bẫy: dọa bắt giam, công an, viện kiểm sát
        if aux_dict.get("num_authority_words", 0) > 0 and (aux_dict.get("num_money_mentions", 0) > 0 or aux_dict.get("has_urgent_words", 0) > 0):
            heuristic_score += 0.85
        elif aux_dict.get("num_authority_words", 0) > 0:
            heuristic_score += 0.50

        # Family emergency bẫy: cấp cứu, tai nạn, mổ gấp + chuyển tiền
        if aux_dict.get("has_emergency_words", 0) > 0 and aux_dict.get("num_money_mentions", 0) > 0:
            heuristic_score += 0.90
        elif aux_dict.get("has_emergency_words", 0) > 0:
            heuristic_score += 0.45

        # Fake Gift bẫy: trúng thưởng, tri ân + link hoặc tiền
        if aux_dict.get("has_gift_words", 0) > 0 and (aux_dict.get("num_urls", 0) > 0 or aux_dict.get("num_money_mentions", 0) > 0):
            heuristic_score += 0.85
        elif aux_dict.get("has_gift_words", 0) > 0:
            heuristic_score += 0.40

        # Đòi mã OTP hoặc mật khẩu
        if aux_dict.get("has_otp_request", 0) > 0 and aux_dict.get("has_urgent_words", 0) > 0:
            heuristic_score += 0.90

        # Nếu hoàn toàn không có bất kỳ tín hiệu nghi vấn nào
        has_any_signal = (
            aux_dict.get("num_authority_words", 0) > 0
            or aux_dict.get("has_emergency_words", 0) > 0
            or aux_dict.get("has_gift_words", 0) > 0
            or aux_dict.get("has_urgent_words", 0) > 0
            or aux_dict.get("has_otp_request", 0) > 0
            or aux_dict.get("num_urls", 0) > 0
            or aux_dict.get("num_money_mentions", 0) > 0
        )

        # 4. ML Model Prediction
        ml_score = 0.0
        if self.is_ready and self.vectorizer is not None and self.scaler is not None:
            try:
                aux_df = pd.DataFrame([aux_dict])[AUX_FEATURE_COLS]
                aux_scaled = self.scaler.transform(aux_df.values)
                tfidf_vec = self.vectorizer.transform([tokenized])
                X_full = hstack([tfidf_vec, csr_matrix(aux_scaled)])
                ml_score = float(self.model.predict_proba(X_full)[0][1])
            except Exception as ex:
                print(f"[!] Inference warning: {ex}")
                ml_score = heuristic_score

        # 5. Hybrid Ensemble Score
        if not has_any_signal:
            # Tin nhắn gia đình / sinh hoạt bình thường không chứa từ nhạy cảm
            final_risk = min(ml_score * 0.1, 0.15)
        elif heuristic_score >= 0.70:
            # Bẫy lừa đảo rõ ràng với bằng chứng đe dọa / cấp cứu / tiền bạc
            final_risk = max(ml_score, heuristic_score)
        else:
            # Kết hợp giữa ML và Heuristic
            final_risk = 0.6 * ml_score + 0.4 * heuristic_score

        final_risk = float(min(max(final_risk, 0.0), 1.0))
        is_scam = final_risk >= 0.50

        return {
            "risk_score": final_risk,
            "is_scam": is_scam,
            "model_used": self.model_name,
            "aux_features": aux_dict,
            "cleaned_text": cleaned,
            "tokenized_text": tokenized,
        }


# Global singleton instance
_model_instance: Optional[ScamDetectionModel] = None

def get_detector() -> ScamDetectionModel:
    global _model_instance
    if _model_instance is None:
        _model_instance = ScamDetectionModel()
    return _model_instance
