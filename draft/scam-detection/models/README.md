# CS114 Final Project — Model Artifacts Registry

Thư mục này dùng để lưu trữ các trọng số mô hình đã huấn luyện (`.pkl`), bộ tham số tối ưu (`.json`), và các gói suy luận tích hợp (`best_model_bundle.pkl`).

---

## 📂 Quy ước Đặt tên File Mô hình

| Tên File | Thuật toán | Thành viên phụ trách | Mô tả |
|----------|-----------|---------------------|-------|
| `naive_bayes.pkl` | Multinomial Naive Bayes | **Bùi Thị Mỷ Cẩm** | Baseline model (Phase 04) |
| `random_forest.pkl` | Random Forest Classifier | **Hoàng Cao Sơn** | Ensemble bagging model (Phase 05) — F1: 0.9425, Recall: 0.9762 |
| `xgboost.pkl` | XGBoost Classifier | **Bùi Thị Mỷ Cẩm** | Gradient boosting model (Phase 05) |
| `svm_linear.pkl` | LinearSVC + CalibratedCV | **Bùi Thị Mỷ Cẩm** | Support Vector Machine (Phase 06) — F1: 0.9474, Recall: 0.9643 |
| `best_model_bundle.pkl` | Model tốt nhất (F1 cao nhất) | **Cả nhóm** | Gói tích hợp nạp vào Streamlit Demo (`demo/app.py`). Hiện đóng gói **SVM Linear** theo Interface Contract gốc của Phase 06 (`plans/.../phase-06-model-svm-phobert.md`) — F1 cao nhất thực tế là XGBoost (0.9535), dùng `notebooks/build_best_model_bundle.py` để re-bundle nếu Phase 07 quyết định đổi. |

---

## 📊 Bảng Đăng Ký Mô Hình & Kết Quả Thực Nghiệm (Test Set: 439 mẫu)

| Tên File Model & Metrics | Thuật toán | Không gian đặc trưng | Hyperparameters tối ưu | Accuracy | Precision | Recall (Lừa đảo) | F1-Score | ROC-AUC | Trạng thái |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `naive_bayes.pkl`<br>`naive_bayes_metrics.json` | MultinomialNB | 5.000 dims (TF-IDF non-negative) | `alpha=0.01` (GridSearchCV 5-fold) | 95.44% | 84.78% | 92.86% | **0.8864** | 0.9911 | ✅ Passed (Phase 04 — Cẩm) |
| `xgboost.pkl`<br>`xgboost_metrics.json` | XGBoost Classifier | 5.015 dims (TF-IDF + 15 aux features) | `n_estimators=300, max_depth=5, lr=0.05, subsample=0.7, colsample_bytree=0.8, scale_pos_weight=4.22` | **98.18%** | **93.18%** | **97.62%** | **0.9535** | **0.9984** | ✅ Hoàn thành (Phase 05 — Cẩm) |
| `random_forest.pkl`<br>`random_forest_metrics.json` | Random Forest Classifier | 5.015 dims (TF-IDF + 15 aux features) | `n_estimators=200, max_depth=50, min_samples_split=2, min_samples_leaf=2, max_features=0.2` | **97.72%** | **91.11%** | **97.62%** | **0.9425** | **0.9977** | ✅ Hoàn thành (Phase 05 — Sơn) |
| `svm_linear.pkl`<br>`svm_metrics.json` | LinearSVC Calibrated | 5.015 dims (TF-IDF + 15 aux features) | `C=10.0` (GridSearchCV 5-fold) | 97.95% | 93.10% | 96.43% | **0.9474** | 0.9986 | ✅ Hoàn thành (Phase 06 — Cẩm) |

---

## 🔒 Quy chuẩn Đóng gói Suy luận (Model Bundle Contract)

Nhằm đảm bảo Web App Demo (`demo/app.py`) suy luận tin nhắn mới một cách độc lập và không gặp lỗi lệch chiều không gian đặc trưng (feature space mismatch), **tuyệt đối không lưu mô hình và bộ trích xuất vectorizer tách rời**.

Mỗi mô hình được chọn làm ứng viên triển khai bắt buộc phải đóng gói theo cấu trúc Dictionary chuẩn:

```python
import joblib

model_bundle = {
    "model": fitted_model,                     # Đối tượng estimator (vd: CalibratedClassifierCV)
    "vectorizer": tfidf_vectorizer,            # TfidfVectorizer (fit trên X_train_text)
    "aux_scaler": auxiliary_scaler,            # StandardScaler (fit trên X_train_aux)
    "feature_names": feature_names,            # Danh sách 5.015 tên đặc trưng
    "metrics": {
        "f1": f1_score_value,
        "recall_scam": recall_scam_value,
        "precision": precision_value,
        "roc_auc": roc_auc_value
    },
    "metadata": {
        "algorithm": "Support Vector Machine (LinearSVC)",
        "train_date": "2026-09-16",
        "random_state": 42
    }
}

joblib.dump(model_bundle, "models/best_model_bundle.pkl")
```

---

## ⚠️ Quy tắc Git Hygiene & Dung lượng
- Mọi tệp trọng số lưu tại đây bắt buộc phải có dung lượng `< 50MB` để tuân thủ chính sách Git của UIT.
- Nếu mô hình vượt quá 50MB, phải cấu hình nén `compress=3` trong `joblib.dump()` hoặc thêm vào `.gitignore`.
