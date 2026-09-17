"""
Random Forest Scam Detector for Vietnamese Elderly Scam Detection.
Phase 05 — CS114 Machine Learning Project.

Author: Hoàng Cao Sơn (MSSV: 25730061)
Group: Nhóm 10
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import RandomizedSearchCV

from src.model_plots import compute_metrics
from src.utils.helpers import RANDOM_STATE


class RandomForestScamDetector:
    """Random Forest Classifier wrapper for Vietnamese SMS scam detection.
    
    Tối ưu hóa cho dữ liệu thưa 5.015 chiều (TF-IDF + Auxiliary Features)
    với cơ chế bù mất cân bằng lớp `class_weight='balanced'`.
    """

    def __init__(
        self,
        n_estimators: int = 200,
        max_depth: Optional[int] = None,
        min_samples_split: int = 5,
        min_samples_leaf: int = 1,
        max_features: Union[str, float] = "sqrt",
        class_weight: str = "balanced",
        random_state: int = RANDOM_STATE,
        n_jobs: int = -1,
        **kwargs: Any,
    ) -> None:
        self.params: Dict[str, Any] = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "min_samples_split": min_samples_split,
            "min_samples_leaf": min_samples_leaf,
            "max_features": max_features,
            "class_weight": class_weight,
            "random_state": random_state,
            "n_jobs": n_jobs,
            **kwargs,
        }
        self.model: RandomForestClassifier = RandomForestClassifier(**self.params)
        self.is_fitted: bool = False
        self.best_params_: Optional[Dict[str, Any]] = None
        self.best_cv_score_: Optional[float] = None

    def fit(self, X: Any, y: Any) -> "RandomForestScamDetector":
        """Huấn luyện mô hình Random Forest trên tập dữ liệu X, y."""
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: Any) -> np.ndarray:
        """Dự đoán nhãn (0: Bình thường, 1: Lừa đảo)."""
        if not self.is_fitted:
            raise RuntimeError("Model chưa được fit. Hãy gọi .fit() trước khi predict.")
        return self.model.predict(X)

    def predict_proba(self, X: Any) -> np.ndarray:
        """Dự đoán xác suất các lớp [P(0), P(1)]."""
        if not self.is_fitted:
            raise RuntimeError("Model chưa được fit. Hãy gọi .fit() trước khi predict_proba.")
        return self.model.predict_proba(X)

    def evaluate(self, X: Any, y: Any) -> Dict[str, float]:
        """Đánh giá 5 chỉ số kỹ thuật: Accuracy, Precision, Recall, F1, ROC-AUC."""
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)[:, 1]
        return compute_metrics(y, y_pred, y_proba)

    def get_classification_report(self, X: Any, y: Any) -> str:
        """Trả về báo cáo chi tiết classification_report dạng văn bản."""
        y_pred = self.predict(X)
        return classification_report(
            y, y_pred, target_names=["Bình thường (0)", "Lừa đảo (1)"], digits=4
        )

    def get_feature_importances(
        self, feature_names: Optional[List[str]] = None, top_n: int = 20
    ) -> List[Tuple[str, float]]:
        """Trích xuất danh sách Top-N đặc trưng quan trọng nhất (Gini Importance)."""
        if not self.is_fitted:
            raise RuntimeError("Model chưa được fit.")
        importances = self.model.feature_importances_
        if feature_names is not None and len(feature_names) != len(importances):
            raise ValueError(
                f"Độ dài feature_names ({len(feature_names)}) không khớp với số đặc trưng ({len(importances)})."
            )
        idx = np.argsort(importances)[::-1][:top_n]
        if feature_names is None:
            return [(f"feature_{i}", float(importances[i])) for i in idx]
        return [(feature_names[i], float(importances[i])) for i in idx]

    def tune(
        self,
        X: Any,
        y: Any,
        param_distributions: Optional[Dict[str, List[Any]]] = None,
        n_iter: int = 25,
        cv: int = 5,
        scoring: str = "f1",
        random_state: int = RANDOM_STATE,
        n_jobs: int = -1,
    ) -> Dict[str, Any]:
        """Tinh chỉnh siêu tham số bằng RandomizedSearchCV trên tập train."""
        if param_distributions is None:
            param_distributions = {
                "n_estimators": [100, 200, 300],
                "max_depth": [15, 30, 50, None],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "max_features": ["sqrt", "log2", 0.2],
            }

        search = RandomizedSearchCV(
            estimator=RandomForestClassifier(
                class_weight="balanced", random_state=random_state, n_jobs=n_jobs
            ),
            param_distributions=param_distributions,
            n_iter=n_iter,
            cv=cv,
            scoring=scoring,
            random_state=random_state,
            n_jobs=n_jobs,
            verbose=0,
        )
        search.fit(X, y)
        self.best_params_ = search.best_params_
        self.best_cv_score_ = float(search.best_score_)
        self.model = search.best_estimator_
        self.is_fitted = True
        self.params.update(self.best_params_)
        return {
            "best_params": self.best_params_,
            "best_score": self.best_cv_score_,
        }

    def save(self, file_path: Union[str, Path]) -> None:
        """Lưu model weights (.pkl) bằng joblib."""
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, file_path)

    @classmethod
    def load(cls, file_path: Union[str, Path]) -> "RandomForestScamDetector":
        """Tải mô hình đã huấn luyện từ file (.pkl)."""
        detector = cls()
        detector.model = joblib.load(file_path)
        detector.is_fitted = True
        detector.params = detector.model.get_params()
        return detector
