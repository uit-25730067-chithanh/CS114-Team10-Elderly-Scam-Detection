# CS114 Final Project — Notebooks Registry & Execution Playbook

Thư mục này chứa toàn bộ sổ tay nghiên cứu và thực nghiệm Jupyter Notebooks (`.ipynb`) của Nhóm 10 cho bài toán phát hiện tin nhắn lừa đảo người cao tuổi.

---

## 🗺️ Bản Đồ Phân Công Notebooks (3 Thành Viên)

Nhằm đảm bảo quy trình song song (`--parallels`) không xảy ra xung đột merge nhị phân (merge conflicts), mỗi thành viên chịu trách nhiệm độc lập trên các notebook riêng:

| Notebook | Người phụ trách | Thuật toán / Tác vụ | Trạng thái |
|----------|----------------|---------------------|------------|
| `01_preprocessing.ipynb` | **Đặng Chí Thanh** | Tiền xử lý Unicode NFC, 160 teencode, Leet-speak, tách từ pyvi, 15 đặc trưng phụ | ✅ Done (Phase 02 PASSED) |
| `02_eda.ipynb` | **Đặng Chí Thanh** | Phân tích khám phá dữ liệu (EDA), sinh 7 biểu đồ 300 DPI, Zero-Leakage Pipeline | ✅ Done (Phase 03 PASSED) |
| `03_model_naive_bayes.ipynb` | **Bùi Thị Mỷ Cẩm** | Huấn luyện Multinomial Naive Bayes baseline, GridSearch alpha, Learning Curve | ✅ Done (Phase 04 — F1=0.8864) |
| `04_model_random_forest.ipynb` | **Hoàng Cao Sơn** | Huấn luyện Random Forest, tinh chỉnh n_estimators/max_depth, Feature Importance | ✅ Done (Phase 05 — F1=0.9425, Recall=0.9762) |
| `04_model_xgboost.ipynb` | **Bùi Thị Mỷ Cẩm** | Huấn luyện XGBoost Classifier, tinh chỉnh learning_rate/subsample | ✅ Done (Phase 05 — F1=0.9535) |
| `05_model_svm.ipynb` | **Bùi Thị Mỷ Cẩm** | Support Vector Machine (LinearSVC Calibrated / RBF Kernel) | ⏳ Next (Phase 06) |
| `06_evaluation_xai.ipynb` | **Đặng Chí Thanh** | So sánh tổng hợp 4 mô hình, ROC-AUC, Confusion Matrix, Top-20 SHAP XAI | ⏳ Sprint 3 (Phase 07) |

---

## 🔒 Quy tắc Nạp Dữ Liệu Zero-Leakage (BẮT BUỘC cho Notebooks 03–06)

> ⚠️ **LƯU Ý SỐNG CÒN:**  
> Kể từ Phase 03, toàn bộ dữ liệu đã được phân chia Stratified 80/20 và đóng gói tại `data/processed/`.  
> Các thành viên khi làm Notebook 03, 04, 05, 06 **TUYỆT ĐỐI KHÔNG** gọi lại `train_test_split` hay `TfidfVectorizer.fit_transform` từ file CSV thô. Phải nạp trực tiếp các ma trận đã xuất:

```python
import joblib
from pathlib import Path

DATA_DIR = Path("../data/processed")

X_train = joblib.load(DATA_DIR / "X_train.pkl")   # (1754, 5015) sparse CSR
X_test  = joblib.load(DATA_DIR / "X_test.pkl")    # (439, 5015)  sparse CSR
y_train = joblib.load(DATA_DIR / "y_train.pkl")   # 336 scam / 1418 normal
y_test  = joblib.load(DATA_DIR / "y_test.pkl")    # 84 scam / 355 normal
```

---

## 💡 Quy tắc Git Hygiene Cho Jupyter Notebooks

1. **Dọn sạch Output trước khi Commit (Stripped Outputs):**  
   Các notebook đã hoàn thành thực nghiệm kiểm chứng 100% được xóa sạch cell output trước khi commit lên Git. Điều này giúp:
   - Tránh phình to dung lượng repository (tuân thủ chính sách `< 50MB` của UIT).
   - Loại bỏ nguy cơ xung đột mã nhị phân khi nhiều thành viên cùng pull/push.
   - Kết quả trực quan chính thức được lưu trữ dưới dạng ảnh xuất bản 300 DPI tại `reports/figures/` và dữ liệu tại `data/processed/`.
2. **Reproducibility:** Mọi notebook bắt buộc phải set seed `RANDOM_STATE = 42` ở cell đầu tiên để bất kỳ ai chạy lại `Run All Cells` đều thu được kết quả đồng nhất 100%.
