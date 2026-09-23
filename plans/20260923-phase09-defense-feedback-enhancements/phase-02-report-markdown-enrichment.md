# Phase 02 — Report Markdown Enrichment (Bổ Sung Báo Cáo Học Thuật)

> **Kế hoạch cha:** [plan.md](./plan.md)  
> **Người phụ trách:** Hoàng Cao Sơn (Chương 1, 2) · Bùi Thị Mỷ Cẩm (Chương 3) · Đặng Chí Thanh (Chương 4, 5)  
> **File tác vụ:** `assignments/Final/draft/scam-detection/reports/report/report-source.md`  
> **Trạng thái:** `ready`

---

## 🎯 Nội Dung Cần Bổ Sung Từng Chương Theo Chỉ Đạo Của Thầy Thăng

### Chương 1 — Đặt Vấn Đề
- [ ] **Phân định rõ ranh giới bài toán**: Nêu bật sự khác biệt bản chất giữa **Phát hiện tin nhắn lừa đảo thao túng tâm lý (Social Engineering Phishing)** nhắm vào người cao tuổi vs **Kiểm chứng tin giả báo chí (Fake News Verification)** (dựa trên nhận xét của thầy Thăng: tin giả có nguồn kiểm chứng, lừa đảo dựa trên hành vi và ngữ cảnh bất thường).
- [ ] Số liệu thống kê thực tế từ Bộ Công an, Cục An toàn thông tin năm 2025–2026 về thiệt hại của NCT.
- [ ] 4 thách thức kỹ thuật tiếng Việt: thanh điệu, teencode, thiếu benchmark, và chi phí đánh đổi của việc bỏ sót (FN).

### Chương 2 — Các Phương Pháp Tiếp Cận
- [ ] Bảng so sánh toàn diện 4 hướng tiếp cận: Hệ luật (Rule-based), Học máy truyền thống (ML), Mô hình ngôn ngữ lớn (LLM), và Transformer tiếng Việt (PhoBERT).
- [ ] Lý giải thuyết phục tại sao nhóm chọn Học máy kết hợp Trích xuất đặc trưng chuyên biệt (nhẹ, inference <50ms, chạy offline an toàn cho người cao tuổi, giải thích trực quan với SHAP).

### Chương 3 — Phương Pháp Đề Xuất
- [ ] Sơ đồ kiến trúc luồng dữ liệu Đầu vào – Đầu ra (Input/Output System Flowchart) từ văn bản thô đến phân loại bẫy tâm lý.
- [ ] Mô tả chi tiết 5 bước tiền xử lý: Chuẩn hóa Unicode NFC, 160 quy tắc teencode, tách từ PyVi, lọc bỏ ký tự đặc biệt, loại bỏ stop words chuyên dụng.
- [ ] Trình bày giải pháp chống Mất cân bằng dữ liệu: Công thức toán hàm mất mát có trọng số (Cost-sensitive loss function, `scale_pos_weight = 4.22`), phân tầng Stratified K-Fold và lý giải vì sao không dùng SMOTE cho văn bản tiếng Việt.

### Chương 4 — Thực Nghiệm & Đánh Giá
- [ ] Trình bày công thức toán học tường minh của các metric: Accuracy, Precision, Recall, F1-Score, ROC-AUC, công thức TF-IDF.
- [ ] **Bảng Thực nghiệm Đối chứng 1 (Ablation on Preprocessing)**: Raw Text vs Preprocessed Text.
- [ ] **Bảng Thực nghiệm Đối chứng 2 (Ablation on Feature Spaces)**: Chỉ TF-IDF 5.000 vs Chỉ 15 Features vs Kết hợp 5.015.
- [ ] Bảng so sánh 4 mô hình học máy đã nghiệm thu (XGBoost F1=0.9535, SVM F1=0.9474, RF F1=0.9425, NB F1=0.8864).
- [ ] Chèn các biểu đồ 300 DPI: ROC Curves, Precision-Recall Curves, Ma trận nhầm lẫn, SHAP Beeswarm và Top-20 từ khóa kích hoạt bẫy tâm lý.
- [ ] **Phân tích sai số (Error Analysis — Mục 4.5)**: Mổ xẻ chi tiết ca biên đe dọa trực diện cuối buổi *"Cướp đây, đưa hết tiền đây!"* (mô hình báo 4.1% nguy cơ - an toàn). Phân tích rõ nguyên nhân do:
  1. *Lệch phân phối kịch bản (Domain Gap)*: Dữ liệu tập trung vào lừa đảo thao túng tâm lý / phi bạo lực qua mạng (Social Engineering), thiếu hụt tội phạm cưỡng đoạt tài sản bạo lực ngoài đời thực (Physical Extortion).
  2. *Hạn chế của Unigram*: Các từ đơn lẻ `tiền`, `đưa`, `đây` xuất hiện phổ biến trong tin nhắn giao dịch thông thường, làm loãng trọng số rủi ro khi không có mồi nhử URL/tài khoản.

### Chương 5 — Kết Luận & Hướng Phát Triển
- [ ] Khẳng định tính toàn vẹn của quy trình Zero Data Leakage (Fit duy nhất trên Train, Transform sang Test).
- [ ] **Định hướng giải pháp mở rộng theo lời Thầy Thăng**:
  - Mở rộng N-gram range lên `(1, 2)` và `(1, 3)` cho TF-IDF 5.000 chiều để bắt trọn các cụm từ nối tiếp mang tính đe dọa cưỡng bức như `"cướp đây"`, `"đưa hết tiền"`, `"chuyển tiền ngay"`.
  - Bổ sung nhóm đặc trưng từ khóa cưỡng bức trực diện (`imperative_threat`) vào không gian đặc trưng tâm lý.
  - Ứng dụng mô hình ngữ cảnh Transformer (PhoBERT) với cơ chế Self-Attention để bắt trọn ngữ nghĩa câu ngắn.
  - Nhận diện lừa đảo giọng nói deepfake đa phương thức.
- [ ] Danh mục Tài liệu tham khảo: Bổ sung đủ ≥ 15 tài liệu chuẩn IEEE/APA.
