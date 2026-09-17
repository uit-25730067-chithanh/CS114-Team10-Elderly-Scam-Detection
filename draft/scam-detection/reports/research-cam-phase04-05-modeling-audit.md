# Research Report: Machine Learning Modeling Benchmarking, Zero-Leakage Audit & Ablation Study (Phase 04 & Phase 05)

- **Course:** CS114 — Machine Learning (Máy học), UIT ĐHQG-HCM
- **Project:** Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam
- **Author:** Bùi Thị Mỷ Cẩm (MSSV: 25730013 — Machine Learning Engineer) & Đặng Chí Thanh (MSSV: 25730067 — Trưởng nhóm / PM / Data Lead)
- **Date:** 16/09/2026
- **Scope:** Báo cáo kiểm toán kỹ thuật và nghiệm thu thực nghiệm Phase 04 (Naive Bayes Baseline) và Phase 05 (XGBoost Classifier); thẩm định giao thức Zero-Leakage; phân tích đối chứng Ablation Study; trực quan hóa 7 biểu đồ đánh giá chuẩn xuất bản 300 DPI.

---

## Executive Summary

Trong khuôn khổ Sprint 2 của đồ án cuối kỳ môn CS114, thành viên Bùi Thị Mỷ Cẩm đã triển khai thành công hai mô hình học máy cốt lõi:
1. **Mô hình Naive Bayes Baseline (Phase 04):** `MultinomialNB` được tinh chỉnh qua `GridSearchCV` 5-fold, đạt **F1-Score = 0.8864**, **Recall = 92.86%**, **ROC-AUC = 0.9911** trên tập kiểm thử độc lập 439 mẫu.
2. **Mô hình XGBoost Classifier (Phase 05):** Gradient Boosting xử lý mất cân bằng lớp (`scale_pos_weight = 4.22`), tinh chỉnh bằng `RandomizedSearchCV` (25 iterations, 5-fold CV), đạt **F1-Score = 0.9535**, **Recall = 97.62%**, **ROC-AUC = 0.9984** trên tập kiểm thử.

Toàn bộ quá trình thực nghiệm tuân thủ 100% giao thức **Zero-Leakage**, nạp trực tiếp các ma trận đặc trưng sẵn có từ Phase 03 mà không chia lại dữ liệu hay fit lại TF-IDF. Đồng thời, nghiên cứu triệt tiêu (Ablation Study) đã chứng minh quyết định sử dụng không gian 5.000 chiều TF-IDF không âm cho Naive Bayes là tối ưu về mặt toán học và thực nghiệm.

---

## 1. Giao Thức Nạp Dữ Liệu Zero-Leakage & Kiểm Toán Kỹ Thuật

Nhằm bảo toàn tính toàn vẹn học thuật và tính nhất quán với Phase 03 và Phase 07, các sổ tay thực nghiệm `03_model_naive_bayes.ipynb` và `04_model_xgboost.ipynb` tuân thủ nghiêm ngặt nguyên tắc **Step 0**:
- Nạp trực tiếp `data/processed/X_train.pkl` (1.754 × 5.015), `X_test.pkl` (439 × 5.015), `y_train.pkl`, `y_test.pkl`.
- Tuyệt đối không gọi `train_test_split` trên file CSV thô.
- Tuyệt đối không gọi lại `fit_transform` trên `TfidfVectorizer` hoặc `StandardScaler`.
- Giữ nguyên tỷ lệ phân tầng 80/20 với seed cố định `RANDOM_STATE = 42`.

---

## 2. Phase 04 — Multinomial Naive Bayes & Ablation Study

### 2.1. Rào cản kỹ thuật & Quyết định kiến trúc
`MultinomialNB` và `ComplementNB` dựa trên mô hình phân phối đa thức (Multinomial Event Model), đòi hỏi dữ liệu đầu vào không âm. Trong khi đó, 15 đặc trưng phụ trong `X_train.pkl` đã qua chuẩn hóa z-score (`StandardScaler`, mean=0) nên chứa giá trị âm, dẫn đến lỗi runtime `ValueError: Negative values in data passed to MultinomialNB`.

Giải pháp ban đầu: Tách lấy khối 5.000 chiều TF-IDF đầu tiên (`X[:, :5000]`), vốn là các trọng số TF-IDF nằm trong đoạn [0, 1].

### 2.2. Kết quả tối ưu hóa siêu tham số
- Đối chứng baseline (validation set, 15% train): `MultinomialNB` (F1 = 0.8468) vượt trội `ComplementNB` (F1 = 0.8065).
- `GridSearchCV` 5-fold trên lưới tham số `alpha ∈ [0.01, 0.1, 0.5, 1.0, 2.0, 5.0]`:
  - Siêu tham số tối ưu: `alpha = 0.01` (làm mịn Laplace cực tiểu).
  - Điểm CV F1 = **0.9058**.
- Kết quả trên Test Set (439 mẫu — 355 Normal / 84 Scam):
  - Accuracy: 95.44%
  - Precision: 84.78%
  - **Recall (Lừa đảo):** **92.86%** (78/84 mẫu lừa đảo được nhận diện đúng)
  - **F1-Score:** **0.8864** (Vượt ngưỡng cơ sở F1 ≥ 0.88 của đề tài)
  - **ROC-AUC:** **0.9911**
  - Ma trận nhầm lẫn: TN = 341, FP = 14, FN = 6, TP = 78.

### 2.3. Ablation Study thực nghiệm (3 Phương án)
Để chứng minh việc loại bỏ 15 đặc trưng phụ khỏi Naive Bayes là quyết định khoa học chứ không phải né tránh vấn đề, nhóm đã tiến hành đối chứng thực nghiệm:

| Phương án | Không gian đặc trưng | Xử lý đặc trưng âm | CV-F1 | Test F1 | Test Recall | Test ROC-AUC | FN / FP | Nhận xét |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **A** | **5.000 TF-IDF** | **Cắt bỏ cột âm (chỉ TF-IDF)** | **0.9058** | **0.8864** | **92.86%** | **0.9911** | **6 / 14** | **Tối ưu nhất** (F1 cao nhất, cân bằng giữa Precision và Recall) |
| B | 5.015 kết hợp | Khôi phục đếm gốc qua `aux_scaler.inverse_transform` | 0.8739 ↓ | 0.8649 ↓ | 95.24% ↑ | 0.9758 ↓ | 4 / 21 ↑ | Độ dài ký tự (vài trăm) lấn át TF-IDF (0–1), tăng báo động giả (FP 14→21) |
| C | 5.015 kết hợp | Co đặc trưng phụ về đoạn MinMax [0, 1] | 0.9014 ↓ | 0.8864 = | 92.86% = | 0.9919 ≈ | 6 / 14 | Khi co nhỏ, đặc trưng phụ không đóng góp thêm; CV-F1 giảm nhẹ do nhiễu chiều |

**Kết luận học thuật:** Phương án A là giải pháp tối ưu toán học và thực nghiệm, bảo toàn tính chất thống kê của Naive Bayes.

---

## 3. Phase 05 — XGBoost Classifier & Tối Ưu Hóa Siêu Tham Số

### 3.1. Thiết lập mô hình trên không gian 5.015 chiều
Không giống như Naive Bayes, các thuật toán cây quyết định tăng cường độ dốc (Gradient Boosted Trees) như XGBoost hoàn toàn không bị ảnh hưởng bởi giá trị âm của `StandardScaler`. Do đó, XGBoost khai thác trọn vẹn sức mạnh kết hợp của 5.000 đặc trưng TF-IDF N-grams và 15 đặc trưng bẫy tâm lý.

Nhằm xử lý tỷ lệ mất cân bằng mẫu 4.22 : 1 giữa tin bình thường và tin lừa đảo, nhóm áp dụng:
```python
scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)  # ≈ 4.22
```

### 3.2. Tối ưu hóa siêu tham số (RandomizedSearchCV)
Chạy `RandomizedSearchCV` 25 lượt lặp, 5-fold Stratified CV trên ma trận huấn luyện 1.754 × 5.015:
- Bộ tham số tối ưu:
  - `n_estimators`: 300
  - `max_depth`: 5
  - `learning_rate`: 0.05
  - `subsample`: 0.7
  - `colsample_bytree`: 0.8
  - `scale_pos_weight`: 4.22
- Điểm CV F1 trung bình đạt **0.9603**.

### 3.3. Hiệu năng vượt trội trên Test Set (439 mẫu)
- **Accuracy:** **98.18%** (431/439 mẫu chính xác)
- **Precision:** **93.18%**
- **Recall (Lừa đảo):** **97.62%** (Dự đoán đúng 82/84 mẫu lừa đảo, chỉ bỏ sót đúng 2 mẫu!)
- **F1-Score:** **0.9535** (Vượt xa mục tiêu đề tài F1 ≥ 0.88)
- **ROC-AUC:** **0.9984**
- Ma trận nhầm lẫn: TN = 349, FP = 6, FN = 2, TP = 82.
- **Top-5 đặc trưng quan trọng nhất (Feature Importance):**
  1. `liên_hệ 198` (0.139): Bắt cặp kịch bản giả mạo tổng đài viễn thông Viettel/VinaPhone để lừa nâng cấp SIM.
  2. `money` (0.079): Cờ nhận diện các mệnh giá tiền tệ và yêu cầu chuyển khoản.
  3. `198` (0.065): Đầu số tổng đài chăm sóc khách hàng bị lợi dụng trong tin nhắn lừa.
  4. `number` (0.037): Cụm chữ số phục vụ định danh giả mạo.
  5. `tran` (0.036): Tiền tố trong giao dịch ngân hàng / mã giao dịch.

---

## 4. Hệ Thống 7 Biểu Đồ Đánh Giá Mô Hình (300 DPI)

7 biểu đồ đánh giá chuyên sâu đã được kết xuất tự động tại `draft/scam-detection/reports/figures/`:
1. `nb_confusion_matrix.png`: Trực quan hóa ma trận phân loại của MultinomialNB.
2. `nb_roc_curve.png`: Đường cong ROC-AUC = 0.9911 của Naive Bayes.
3. `nb_learning_curve.png`: Phân tích Train F1 vs Val F1 chứng minh Naive Bayes hội tụ tốt, không quá khớp.
4. `xgb_confusion_matrix.png`: Trực quan hóa ma trận nhầm lẫn của XGBoost với FN = 2 cực thấp.
5. `xgb_roc_curve.png`: Đường cong ROC-AUC = 0.9984 tiệm cận góc trên bên trái.
6. `xgb_learning_curve.png`: Phân tích hội tụ của XGBoost, Train F1 bão hòa ~0.99, Val F1 đạt 0.96.
7. `xgb_feature_importance.png`: Xếp hạng Top-20 đặc trưng quan trọng nhất từ mô hình cây.

---

## 5. Git Hygiene & Quản Lý Trọng Số

- **Stripped Outputs:** Hai sổ tay `03_model_naive_bayes.ipynb` và `04_model_xgboost.ipynb` được tự động tạo qua các script Python (`generate_nb_notebook.py`, `generate_xgb_notebook.py`) và dọn sạch ô kết quả (stripped outputs), giữ dung lượng mỗi notebook dưới 40 KB, đảm bảo an toàn tuyệt đối cho Git repository.
- **Model Checkpoints:** Trọng số `.pkl` được quản lý chặt chẽ qua `.gitignore` để tránh phình to kích thước repository. Metrics JSON (`naive_bayes_metrics.json`, `xgboost_metrics.json`) được commit minh bạch để phục vụ kiểm toán tự động.

---

## 6. Phân Công & Bước Tiếp Theo

1. **Phase 05 (Random Forest):** Thành viên Hoàng Cao Sơn tiếp tục triển khai sổ tay `04_model_random_forest.ipynb`, tinh chỉnh siêu tham số và xuất kết quả đối chứng với XGBoost để hoàn tất trọn vẹn Phase 05.
2. **Phase 06 (Support Vector Machine):** Thành viên Bùi Thị Mỷ Cẩm chuẩn bị triển khai `05_model_svm.ipynb` (LinearSVC Calibrated & RBF Kernel) trên không gian 5.015 chiều.
3. **Phase 07 (Evaluation & XAI):** Trưởng nhóm Đặng Chí Thanh sẽ tổng hợp cả 4 mô hình, chạy phân tích XAI SHAP giải thích từ khóa cảnh báo cho người cao tuổi.
