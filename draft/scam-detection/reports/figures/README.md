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
