# CS114 Final Project — Model Artifacts Registry

Thư mục này dùng để lưu trữ các trọng số mô hình đã huấn luyện (`.pkl`), bộ tham số tối ưu (`.json`), và các gói suy luận tích hợp (`best_model_bundle.pkl`).

---

## 📂 Quy ước Đặt tên File Mô hình

| Tên File | Thuật toán | Thành viên phụ trách | Mô tả |
|----------|-----------|---------------------|-------|
| `naive_bayes.pkl` | Multinomial Naive Bayes | **Bùi Thị Mỷ Cẩm** | Baseline model (Phase 04) |
| `random_forest.pkl` | Random Forest Classifier | **Hoàng Cao Sơn** | Ensemble bagging model (Phase 05) |
| `xgboost.pkl` | XGBoost Classifier | **Bùi Thị Mỷ Cẩm** | Gradient boosting model (Phase 05) |
| `svm_linear.pkl` | LinearSVC + CalibratedCV | **Bùi Thị Mỷ Cẩm** | Support Vector Machine (Phase 06) |
| `best_model_bundle.pkl` | Model tốt nhất (F1 cao nhất) | **Cả nhóm** | Gói tích hợp nạp vào Streamlit Demo (`demo/app.py`) |

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
