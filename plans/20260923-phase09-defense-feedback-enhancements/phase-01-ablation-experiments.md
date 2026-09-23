# Phase 01 — Ablation Experiments (Thực Nghiệm Đối Chứng)

> **Kế hoạch cha:** [plan.md](./plan.md)  
> **Người phụ trách:** Đặng Chí Thanh (25730067)  
> **Trạng thái:** `ready`  
> **Mục tiêu:** Đo đạc thực tế 2 bảng số liệu đối chứng trên cùng tập Test cố định (439 mẫu) để trả lời trọn vẹn 2 câu hỏi lớn của ThS. Cáp Phạm Đình Thăng.

---

## 🎯 Chi Tiết 2 Bài Thực Nghiệm Đối Chứng

### 1. Thực nghiệm 1: Vai trò của Tiền Xử Lý NLP (Preprocessing Ablation)
* **Câu hỏi của Thầy Thăng**: *"Ở đây mình có tiền xử lý. Nhưng mình chưa có thực nghiệm là ví dụ nếu mình chưa tiền xử lý và nếu mình tiền xử lý thì kết quả như thế nào? Nó phải tăng thì mình mới làm tiền xử lý đúng không?"*
* **Phương pháp thực nghiệm**:
  1. **Cấu hình 1.1 (Raw Text Baseline)**:
     - Dữ liệu: Cột `text` gốc trong `data/raw/dataset.csv` (chưa qua chuẩn hóa Unicode NFC, chưa sửa teencode, không tách từ ghép).
     - Chia tập: Cùng chỉ số index Train (1.754) và Test (439 mẫu) như tập dữ liệu chuẩn.
     - Vector hóa: `TfidfVectorizer(max_features=5000, ngram_range=(1,2))` fit trên Train, transform Test.
     - Huấn luyện: XGBoost (`scale_pos_weight=4.22, n_estimators=300, max_depth=5`) và Naive Bayes.
  2. **Cấu hình 1.2 (Preprocessed Text — Pipeline Nhóm 10)**:
     - Dữ liệu: Văn bản đã qua pipeline 5 bước (`Unicode NFC + 160 teencode rules + PyVi word segmentation + Regex cleaner`).
     - Vector hóa: TF-IDF 5.000 chiều chuẩn.
     - Huấn luyện: Cùng mô hình và siêu tham số như Cấu hình 1.1.
* **Kỳ vọng**: Chứng minh con số cụ thể rằng F1-Score và Recall tăng rõ rệt nhờ tiền xử lý chuẩn hóa từ vựng và giữ đúng từ ghép tiếng Việt.

---

### 2. Thực nghiệm 2: Vai trò của 15 Đặc Trưng Tâm Lý (Feature Space Ablation)
* **Câu hỏi của Thầy Thăng**: *"Chỉ dùng đặc trưng TF-IDF thôi, bỏ 15 cái phụ đi thì kết quả như thế nào? Sau đó kết hợp cả hai thì kết quả như thế nào? Để giải thích lý do tại sao mình lại chọn thêm 15 đặc trưng phụ này."*
* **Phương pháp thực nghiệm** (đo trên mô hình tốt nhất XGBoost và Linear SVM):
  1. **Cấu hình 2.1 (Chỉ dùng 5.000 TF-IDF)**:
     - Ma trận đầu vào: 5.000 cột đầu tiên của `X_train.pkl` và `X_test.pkl`.
     - Đại diện cho phương pháp dựa hoàn toàn vào từ vựng xuất hiện.
  2. **Cấu hình 2.2 (Chỉ dùng 15 Đặc trưng tâm lý)**:
     - Ma trận đầu vào: 15 cột cuối của `X_train.pkl` và `X_test.pkl` (đã qua `StandardScaler`).
     - Đại diện cho các tín hiệu hành vi/ngữ cảnh (từ khóa đe dọa, khẩn cấp, tài chính, đường dẫn liên kết).
  3. **Cấu hình 2.3 (Kết hợp cả hai — 5.015 chiều)**:
     - Ma trận đầu vào: Trọn vẹn 5.015 chiều (mô hình chính thức của nhóm).
* **Kỳ vọng**:
  - Cấu hình 2.2 với chỉ 15 đặc trưng đạt hiệu năng tương đối khá (chứng minh tính chắt lọc của đặc trưng miền).
  - Cấu hình 2.3 đạt hiệu năng cao nhất (Recall 97.62%, F1 0.9535), chứng minh 15 đặc trưng bù đắp các trường hợp kẻ gian thay đổi từ vựng nhưng giữ nguyên hành vi thao túng.

---

## 🛠️ Công Việc Cụ Thể

- [ ] Tạo file script `assignments/Final/draft/scam-detection/src/evaluation/run_ablation_studies.py`.
- [ ] Tải dữ liệu gốc `data/raw/dataset.csv` và dữ liệu chia train/test đã lưu `data/processed/`.
- [ ] Chạy pipeline tính toán và xuất kết quả ra file `assignments/Final/draft/scam-detection/reports/ablation_studies.json`.
- [ ] Định dạng kết quả thành Markdown Tables sẵn sàng chèn vào Báo cáo Chương 4.
