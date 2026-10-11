# EDA Figures Catalog & Statistical Evidence (300 DPI)

Thư mục này chứa 7 biểu đồ phân tích khám phá dữ liệu (Exploratory Data Analysis) độ phân giải cao (300 DPI), được tạo tự động bởi `src/eda_visualizations.py` trong Phase 03 để đưa trực tiếp vào Báo cáo đồ án Word (`DOCS/DoAnMonHoc.docx`) và Slide thuyết trình (`SLIDES/Presentation_CS114.pptx`).

---

## 📊 Danh Mục 7 Biểu Đồ & Ý Nghĩa Học Thuật

### 1. `label_distribution.png` (300 DPI)
- **Nội dung:** Biểu đồ cột thể hiện phân bố 1.773 tin nhắn bình thường (80.8%) vs 420 tin nhắn lừa đảo (19.2%).
- **Ý nghĩa học thuật:** Chứng minh tỷ lệ mất cân bằng mẫu (Imbalance Ratio = **4.22 : 1**). Đây là căn cứ khoa học để nhóm áp dụng tham số `class_weight='balanced'` trong các mô hình và sử dụng **F1-Score / PR-AUC** làm thước đo chính thay cho Accuracy.

### 2. `scam_category_distribution.png` (300 DPI)
- **Nội dung:** Cơ cấu 4 nhóm bẫy tâm lý trong 420 mẫu lừa đảo:
  - Giả mạo dịch vụ công (`public_service`): 159 mẫu (37.9%)
  - Đe dọa quyền lực (`fear_authority`): 127 mẫu (30.2%)
  - Thúc ép khẩn cấp gia đình (`family_emergency`): 88 mẫu (21.0%)
  - Dụ dỗ quà tặng sức khỏe (`health_gift`): 46 mẫu (11.0%)
- **Ý nghĩa học thuật:** Phản ánh đúng xu hướng tội phạm lừa đảo công nghệ cao năm 2026 tại Việt Nam khi chiêu trò lừa đảo qua cập nhật VNeID mức 2 và mạo danh Công an/Tòa án chiếm hơn 68%.

### 3. `text_length_comparison.png` (300 DPI)
- **Nội dung:** Biểu đồ histogram và KDE so sánh độ dài ký tự và số từ giữa hai lớp.
- **Ý nghĩa học thuật:** Tin nhắn lừa đảo có độ dài trung bình (142 ký tự / 28 từ) vượt trội so với tin thường (68 ký tự / 13 từ), chứng minh các đối tượng lừa đảo cần văn bản dài hơn để thiết lập uy quyền giả mạo hoặc tạo dựng tình huống khẩn cấp.

### 4. `wordcloud_scam_vs_normal.png` (300 DPI)
- **Nội dung:** Đám mây từ vựng so sánh song song giữa lớp lừa đảo và lớp bình thường sau khi đã loại bỏ từ dừng.
- **Ý nghĩa học thuật:** Trực quan hóa sự khác biệt ngữ nghĩa: Nhóm lừa đảo tập trung dày đặc vào *công an, viện kiểm sát, hồ sơ, chuyển khoản, tạm giam, tai nạn*, trong khi nhóm bình thường xoay quanh *cảm ơn, mai, gói cước, data, chúc mừng*.

### 5. `top_ngrams_scam_vs_normal.png` (300 DPI)
- **Nội dung:** Top-20 N-grams (1-gram và 2-gram) có mức độ phân tách mạnh nhất giữa hai lớp.
- **Ý nghĩa học thuật:** Minh chứng cho việc sử dụng N-gram (1, 2) trong TF-IDF giúp nắm bắt trọn vẹn các cụm từ quan trọng như `bộ_công_an`, `viện_kiểm_sát`, `chuyển_khoản_ngay`, `nâng_cấp_sim`.

### 6. `auxiliary_correlation_heatmap.png` (300 DPI)
- **Nội dung:** Ma trận tương quan Pearson giữa 15 đặc trưng phụ và nhãn lừa đảo (label).
- **Ý nghĩa học thuật:** Chỉ ra các đặc trưng có tính phân tách cao nhất:
  - `has_masked_otp`: +0.38
  - `has_urgent_words`: +0.35
  - `num_exclamation`: +0.32
  - `uppercase_ratio`: +0.29
  - `has_masked_url`: +0.27

### 7. `source_distribution.png` (300 DPI)
- **Nội dung:** Biểu đồ phân bố các nguồn thu thập dữ liệu đời thực.
- **Ý nghĩa học thuật:** Chứng thực tính minh bạch và độ tin cậy của tập dữ liệu từ IEEE Access 2026, báo chí chính thống (Dân Trí, VnExpress, Tuổi Trẻ) và CS114 Evidence Vault.

---

## 📈 Danh Mục Biểu Đồ Đánh Giá Mô Hình (Phases 04 & 05)

### 8. `nb_confusion_matrix.png` (300 DPI)
- **Nội dung:** Ma trận nhầm lẫn của MultinomialNB trên Test Set (439 mẫu: 355 Normal / 84 Scam).
- **Ý nghĩa học thuật:** Phản ánh tỷ lệ phân loại của mô hình baseline: dự đoán đúng 78/84 mẫu lừa đảo (Recall = 92.86%), 6 mẫu FN (bỏ sót) và 14 mẫu FP (báo động giả).

### 9. `nb_roc_curve.png` (300 DPI)
- **Nội dung:** Đường cong ROC và chỉ số diện tích dưới đường cong ROC-AUC của MultinomialNB.
- **Ý nghĩa học thuật:** Đạt ROC-AUC = **0.9911**, chứng minh khả năng xếp hạng phân tách xác suất giữa tin nhắn lừa đảo và tin thường vượt trội so với đường chuẩn ngẫu nhiên (Random Baseline AUC = 0.5).

### 10. `nb_learning_curve.png` (300 DPI)
- **Nội dung:** Đường cong học tập (Learning Curve) đối chiếu Train F1 vs Validation F1 (5-fold CV) theo số lượng mẫu huấn luyện.
- **Ý nghĩa học thuật:** Điểm Train F1 giảm từ 1.00 về 0.96 và Val F1 tăng từ 0.73 lên 0.91, hai đường tiệm cận nhau khi tăng kích thước dữ liệu, chứng thực mô hình Naive Bayes không bị overfitting nghiêm trọng.

### 11. `xgb_confusion_matrix.png` (300 DPI)
- **Nội dung:** Ma trận nhầm lẫn của XGBoost tuned trên Test Set (439 mẫu).
- **Ý nghĩa học thuật:** Đạt độ chính xác cao: dự đoán đúng 82/84 mẫu lừa đảo (Recall = **97.62%**), chỉ bỏ sót 2 mẫu lừa đảo (FN = 2) và báo động giả 6 mẫu (FP = 6), vượt trội toàn diện so với Naive Bayes baseline.

### 12. `xgb_roc_curve.png` (300 DPI)
- **Nội dung:** Đường cong ROC và AUC của XGBoost classifier.
- **Ý nghĩa học thuật:** Đạt ROC-AUC = **0.9984**, biểu thị đường cong tiệm cận góc trên bên trái, thể hiện năng lực phân định gần như tuyệt đối của gradient boosting trên không gian 5.015 chiều.

### 13. `xgb_learning_curve.png` (300 DPI)
- **Nội dung:** Đường cong học tập Train F1 vs Validation F1 (5-fold CV) của mô hình XGBoost tinh chỉnh.
- **Ý nghĩa học thuật:** Train F1 duy trì ~0.98–1.00, Validation F1 tăng tiến đều đặn từ 0.83 lên 0.96, khoảng cách giữa 2 tập thu hẹp dần, khẳng định việc áp dụng `subsample=0.7` và `colsample_bytree=0.8` đã kiểm soát tốt hiện tượng quá khớp (overfitting) trên dữ liệu thưa chiều cao.

### 14. `xgb_feature_importance.png` (300 DPI)
- **Nội dung:** Biểu đồ ngang xếp hạng Top-20 đặc trưng có trọng số quan trọng nhất trích xuất từ cây quyết định của XGBoost.
- **Ý nghĩa học thuật:** Nổi bật các đặc trưng quyết định: `liên_hệ 198` (0.139), `money` (0.079), `198` (0.065), `number` (0.037), `tran` (0.036), xác nhận mối tương quan chặt chẽ với các thủ đoạn giả mạo đầu số nhà mạng và thao túng tâm lý chuyển khoản khẩn cấp.

---

## 🌲 Danh Mục Biểu Đồ Đánh Giá Random Forest (Hoàng Cao Sơn — Phase 05)

### 15. `rf_confusion_matrix.png` (300 DPI)
- **Nội dung:** Ma trận nhầm lẫn 2×2 của Random Forest trên tập kiểm thử độc lập (439 mẫu).
- **Kết quả:** TN=347, FP=8, FN=2, TP=82.
- **Ý nghĩa học thuật:** Tỷ lệ bỏ sót tin lừa đảo cực thấp (chỉ 2/84 mẫu lừa đảo bị bỏ sót, Recall đạt 97.62%), bảo vệ an toàn tối đa cho đối tượng người cao tuổi.

### 16. `rf_roc_curve.png` (300 DPI)
- **Nội dung:** Đường cong ROC và chỉ số AUC của mô hình Random Forest trên tập Test.
- **Kết quả:** ROC-AUC đạt **0.9976**, phản ánh khả năng phân tách nhãn gần như hoàn hảo giữa tin thường và tin lừa đảo.

### 17. `rf_learning_curve.png` (300 DPI)
- **Nội dung:** Đường cong học tập (Train F1 vs Validation F1 qua 5-Fold Cross-Validation) theo quy mô kích thước tập huấn luyện.
- **Ý nghĩa học thuật:** Điểm Train F1 duy trì ổn định, Validation F1 tăng đều từ 0.85 lên ~0.95 khi tăng kích thước mẫu, khoảng cách thu hẹp chứng minh mô hình hội tụ tốt và không bị Overfitting nghiêm trọng.

### 18. `rf_feature_importance.png` (300 DPI)
- **Nội dung:** Biểu đồ ngang xếp hạng Top-20 đặc trưng có độ giảm độ tinh khiết Gini cao nhất (Gini Importance).
- **Ý nghĩa học thuật:** Làm nổi bật các từ khóa và đặc trưng phụ chỉ báo lừa đảo mạnh nhất trong các kịch bản đe dọa quyền lực và cấp cứu gia đình: `liên_hệ 198`, `number`, `money`, `tran`, `hotline` và các đặc trưng đếm URL/từ khẩn cấp.

---

## ⚔️ Danh Mục Biểu Đồ Đánh Giá Support Vector Machine (Bùi Thị Mỷ Cẩm — Phase 06)

### 19. `svm_confusion_matrix.png` (300 DPI)
- **Nội dung:** Ma trận nhầm lẫn của LinearSVC Calibrated trên Test Set (439 mẫu). TN=349, FP=6, FN=3, TP=81.
- **Ý nghĩa học thuật:** F1-Score đạt 0.9474, Recall 96.43%, Precision 93.10%.

### 20. `svm_roc_curve.png` (300 DPI)
- **Nội dung:** Đường cong ROC và AUC của Linear SVM đạt **0.9986** (cao nhất trong các mô hình đơn).

### 21. `svm_learning_curve.png` (300 DPI)
- **Nội dung:** Đường cong học tập 5-fold CV của Linear SVM.

### 22. `svm_feature_importance.png` (300 DPI)
- **Nội dung:** Biểu đồ hệ số hồi quy trung bình có dấu (signed coefficients) của Linear SVM.

---

## 🎯 Danh Mục Biểu Đồ Đánh Giá Tổng Hợp & XAI (Đặng Chí Thanh — Phase 07)

### 23. `confusion_matrices_all.png` (300 DPI)
- **Nội dung:** Lưới 2×2 ma trận nhầm lẫn của cả 4 mô hình (XGBoost, SVM Linear, Random Forest, Naive Bayes).
- **Ý nghĩa học thuật:** Cho phép đối chiếu trực tiếp số ca báo nhầm (FP) và bỏ sót (FN) giữa các kiến trúc học máy.

### 24. `roc_curves_comparison.png` (300 DPI)
- **Nội dung:** Biểu đồ lồng ghép 4 đường cong ROC trên cùng hệ trục tọa độ với Random Baseline.
- **Ý nghĩa học thuật:** So sánh trực quan năng lực phân tách xác suất: SVM Linear (0.9986) ≈ XGBoost (0.9984) > Random Forest (0.9977) > Naive Bayes (0.9911).

### 25. `precision_recall_curves.png` (300 DPI)
- **Nội dung:** Biểu đồ lồng ghép 4 đường Precision-Recall kèm điểm cân bằng tỷ lệ mẫu lừa đảo gốc (19.1%).
- **Ý nghĩa học thuật:** Thước đo khoa học quan trọng nhất cho bài toán mất cân bằng nhãn (Imbalance 4.22:1). Cả 4 mô hình đều duy trì Precision > 90% ở mức Recall > 95%.

### 26. `learning_curves_summary.png` (300 DPI)
- **Nội dung:** Tổng hợp 4 biểu đồ học tập Train vs Validation (5-fold CV) dạng lưới 2×2.
- **Ý nghĩa học thuật:** Bằng chứng thực nghiệm phản biện trước Giảng viên về việc kiểm soát hiện tượng quá khớp (Overfitting).

### 27. `top20_keywords_barplot.png` (300 DPI)
- **Nội dung:** Biểu đồ xếp hạng 20 từ khóa cảnh báo kích hoạt bẫy tâm lý lừa đảo có trọng số đồng thuận cao nhất qua 4 mô hình.
- **Ý nghĩa học thuật:** Phản ánh chính xác các đặc trưng ngôn ngữ đe dọa quyền lực (`mày`, `số_định_danh`), thúc ép khẩn cấp (`viện_phí`, `gấp`), và giả mạo tổ chức (`money`, `liên_hệ 198`, `thuế`).

### 28. `shap_summary.png` (300 DPI)
- **Nội dung:** Biểu đồ SHAP Beeswarm trích xuất từ `shap.TreeExplainer` cho mô hình XGBoost.
- **Ý nghĩa học thuật:** Giải thích chi tiết sự phân bố giá trị đóng góp (SHAP values) của từng đặc trưng vi mô vào xác suất phân loại lừa đảo.

---

## 🖥️ Danh Mục Ảnh Nghiệm Thu Giao Diện Web Demo Streamlit (Hoàng Cao Sơn — Phase 08)

### 29. `demo_01_initial_layout.png` (300 DPI)
- **Nội dung:** Bố cục tổng thể giao diện Split-View Workbench trên màn hình Desktop: khu vực nhập liệu bên trái và bảng kết quả phân tích AI bên phải.
- **Ý nghĩa học thuật:** Minh chứng kiến trúc giao diện tương tác hai luồng trực quan, tối ưu cho quá trình thao tác kiểm tra tin nhắn nhanh chóng và thân thiện.

### 30. `demo_02_font_scaling_elderly.png` (300 DPI)
- **Nội dung:** Giao diện khi kích hoạt bộ phóng đại cỡ chữ 150% dành riêng cho người cao tuổi hoặc người có thị lực kém.
- **Ý nghĩa học thuật:** Chứng thực việc hiện thực hóa các tiêu chuẩn trợ năng (Accessibility Standards), giúp đối tượng yếu thế dễ dàng tiếp cận và đọc rõ nội dung cảnh báo.

### 31. `demo_03_scam_detection_verdict.png` (300 DPI)
- **Nội dung:** Kết quả nhận diện bẫy lừa đảo đe dọa quyền lực: thanh đo nguy cơ màu đỏ (Risk Meter), từ khóa nhạy cảm bôi đỏ, chẩn đoán bẫy tâm lý, và hộp quy tắc an toàn "3 KHÔNG & 1 GỌI" kèm Hotline 156/113.
- **Ý nghĩa học thuật:** Trực quan hóa năng lực suy luận thời gian thực kết hợp giữa mô hình học máy (XGBoost/SVM) và hệ luật diễn giải bẫy tâm lý học.

### 32. `demo_04_mobile_responsive.png` (300 DPI)
- **Nội dung:** Giao diện ứng dụng tự động co dãn trên màn hình điện thoại di động (Mobile Responsive View).
- **Ý nghĩa học thuật:** Chứng minh tính tương thích đa nền tảng, cho phép người cao tuổi có thể gọi trực tiếp Hotline khẩn cấp bằng 1 chạm (`tel:156`, `tel:113`) trên smartphone.

