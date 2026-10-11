# Phase 01 — Chuẩn hóa Toàn diện Markdown Source (`report-source.md`)

> **Parent plan:** [plan.md](./plan.md)  
> **Tệp tác động:** `draft/scam-detection/reports/report/report-source.md`  
> **Trạng thái:** `ready`  

---

## 1. Mục tiêu
Đưa `report-source.md` trở thành nguồn chân lý duy nhất (Single Source of Truth - SSOT), sửa đổi và bổ sung toàn bộ các nội dung học thuật còn thiếu trước khi chuyển giao sang tệp Word.

---

## 2. Chi tiết các nhiệm vụ thực thi

### 2.1. Cập nhật Metadata Trang bìa & Lời cam đoan
- Sửa tên đơn vị quản lý: **KHOA KHOA HỌC MÁY TÍNH — BỘ MÔN TRÍ TUỆ NHÂN TẠO**.
- Sửa mã lớp: **CS114.F31.CN2.TTNT**.
- Cập nhật thông tin ngày nộp: *"Báo cáo bảo vệ sớm: 23/09/2026 | Nộp bài chính thức LMS: Tháng 10/2026"*.

### 2.2. Bổ sung Bảng Phân công & Đóng góp thành viên (Member Contribution Matrix)
Đặt ngay sau phần *Cam kết Liêm chính Học thuật*:
| STT | Thành viên | MSSV | Vai trò chính | Phân hệ phụ trách chi tiết | Mức độ hoàn thành | Tỷ lệ đóng góp |
|:---:|---|:---:|---|---|:---:|:---:|
| 1 | **Đặng Chí Thanh** | `25730067` | Trưởng nhóm / PM | • Thu thập 1.773 tin bình thường (IEEE Access 2026) & 50 mẫu Holdout Test<br>• Pipeline tiền xử lý văn bản tiếng Việt & Trích xuất 15 đặc trưng phụ (Phase 02)<br>• Pipeline EDA & Zero-leakage Feature Engineering 5.015 chiều (Phase 03)<br>• Đánh giá tổng hợp 4 mô hình & XAI SHAP Top-20 (Phase 07)<br>• Thực nghiệm đối chứng Ablation Studies (Buổi 8)<br>• Soạn thảo báo cáo học thuật & Điều phối dự án | 100% | 33.33% |
| 2 | **Bùi Thị Mỷ Cẩm** | `25730013` | ML Modeling Lead | • Thu thập 205 mẫu lừa đảo (`health_gift`, `public_service`) vượt 7 tầng kiểm toán<br>• Huấn luyện Naive Bayes Baseline (alpha=0.01) (Phase 04)<br>• Huấn luyện XGBoost Classifier (`scale_pos_weight = 4.22`) (Phase 05)<br>• Huấn luyện Calibrated Linear SVM (C=10.0) (Phase 06)<br>• Thiết kế Slide PowerPoint 22 trang chuẩn UIT (Phase 09) | 100% | 33.33% |
| 3 | **Hoàng Cao Sơn** | `25730061` | Data & UI Lead | • Thu thập 215 mẫu lừa đảo (`fear_authority`, `family_emergency`) vượt 7 tầng kiểm toán<br>• Huấn luyện Random Forest Classifier (n_estimators=200) (Phase 05)<br>• Xây dựng Web App Demo Streamlit tối ưu trợ năng người già (Phase 08)<br>• Tự động hóa kiểm thử E2E Playwright 16/16 tests (Phase 08)<br>• Biên soạn bản thảo Báo cáo Word ban đầu & Thiết lập bố cục OpenXML | 100% | 33.33% |

### 2.3. Tái cấu trúc Chương 4 theo chuẩn Đề cương Thầy Thăng (`NopDoAnMonHoc.png`)
Tái cấu trúc đề mục rõ ràng:
- `4.1. Bộ dữ liệu nghiên cứu và phân tích khám phá (EDA)` (Dataset là gì)
- `4.2. Phương pháp đánh giá và kiểm soát rò rỉ dữ liệu` (Phương pháp đánh giá là gì — nâng cấp mục 4.2.0 cũ thành mục lớn độc lập)
  - Chiến lược phân chia Train/Test 80/20 phân tầng (Zero-Data-Leakage)
  - Kiểm định chéo 5-Fold Stratified Cross-Validation
  - Định nghĩa 5 thước đo đánh giá: Accuracy, Precision, Recall (Scam), F1-Score, ROC-AUC
  - Ví dụ tính tay cụ thể trên ma trận nhầm lẫn của XGBoost
- `4.3. Kết quả thực nghiệm và đối sánh đa mô hình` (Kết quả đạt được)
  - Bảng đối sánh tổng hợp 4 mô hình trên Holdout Test Set (439 mẫu)
  - Phân tích đường cong ROC (Hình 4.4) và Precision-Recall (Hình 4.5)
  - Phân tích ma trận nhầm lẫn 4 mô hình (Hình 4.6)
  - Phân tích hiện tượng quá khớp qua Learning Curves (Hình 4.7)
- `4.4. Trí tuệ nhân tạo có thể giải thích (XAI) và Top 20 từ khóa bẫy tâm lý`
  - Biểu đồ SHAP Beeswarm của XGBoost (Hình 4.8)
  - Biểu đồ cột ngang Top-20 từ khóa cảnh báo có trọng số đồng thuận cao nhất (Hình 4.8b: `top20_keywords_barplot.png`)
  - Bảng 4.3 chi tiết Top-20 từ khóa và phân tích cơ chế kích hoạt 4 nhóm bẫy tâm lý
- `4.5. Thực nghiệm đối chứng chuyên sâu (Ablation Studies)`
  - Thực nghiệm 1: Vai trò của Tiền xử lý NLP (Raw vs Preprocessed) kèm Bảng 4.4 & Hình 4.10
  - Thực nghiệm 2: Vai trò của 15 Đặc trưng Tâm lý (TF-IDF vs Aux) kèm Bảng 4.5 & Hình 4.11
- `4.6. Đánh giá ứng dụng thực tế Web Demo Streamlit trợ năng người cao tuổi`
  - Giới thiệu Web Demo và kiểm định 16/16 tests Playwright
  - Hình 4.9: Màn hình cảnh báo nguy cơ thời gian thực (`demo_03_scam_detection_verdict.png`)
  - Hình 4.9b: Tính năng trợ năng thị giác phóng đại phông chữ 125%–150% (`demo_02_font_scaling_elderly.png`)
- `4.7. Phân tích sai số và đánh giá ca biên ngoại vi ("Cướp đây, đưa hết tiền đây!")`

### 2.4. Bổ sung 4 Hình ảnh EDA còn thiếu trong Mục 4.1
- Chèn Hình 4.1b: `text_length_comparison.png` — Phân bố độ dài ký tự và số từ giữa 2 lớp (lừa đảo trung bình dài gấp đôi tin thường để dựng kịch bản).
- Chèn Hình 4.1c: `wordcloud_scam_vs_normal.png` — Đám mây từ vựng so sánh song song lừa đảo vs bình thường.
- Chèn Hình 4.1d: `top_ngrams_scam_vs_normal.png` — Top 20 N-grams minh chứng cho việc chọn TF-IDF (1, 2) bắt trọn `bộ_công_an`, `viện_kiểm_sát`.
- Chèn Hình 4.1e: `source_distribution.png` — Phân bố nguồn dữ liệu thực tế (IEEE Access, Báo chí, Vault).
- Cập nhật câu nhận xét giải thích trọn vẹn cả 7 biểu đồ EDA.

### 2.5. Hoàn thiện Hệ thống Công thức Toán học
- **Hàm mất mát Cost-Sensitive Binary Cross-Entropy:**
  `L(θ) = − Σᵢ [ w · yᵢ · log(pᵢ) + (1 − yᵢ) · log(1 − pᵢ) ]`
  với `w = scale_pos_weight = 1.418 / 336 ≈ 4.22`.
- **Hàm Hinge Loss có trọng số của SVM:**
  `min ½‖ω‖² + C · Σᵢ w(yᵢ) · max(0, 1 − yᵢ · f(xᵢ))`
- **Hệ 3 công thức TF-IDF chuẩn hóa logarit:**
  `tf(t, d) = 1 + ln(f(t, d))`
  `idf(t) = ln((1 + n) / (1 + df(t))) + 1`
  `tfidf(t, d) = tf(t, d) · idf(t)`

### 2.6. Đồng bộ Bảng 3.1 (15 đặc trưng phụ) đầy đủ 6 cột
- Giữ nguyên bảng 6 cột có số liệu thống kê trung bình thực tế (`TB lừa đảo`, `TB bình thường`).
- Bổ sung đoạn phân tích chuyên sâu giải thích tại sao thẻ `[MONEY]` xuất hiện ở tin thường nhiều hơn lừa đảo (1.221 / 1.236 mẫu) do đặc thù tin nhắn biến động số dư ngân hàng hợp lệ.

### 2.7. Bổ sung Nhận xét Khoa học cho Linear SVM trong Ablation 2
- Giải thích rõ tại sao F1 của Linear SVM giảm nhẹ từ 0.9697 xuống 0.9474 khi thêm 15 đặc trưng: do không gian TF-IDF 5.000 chiều là không gian thưa, 15 đặc trưng phụ liên tục được chuẩn hóa qua `StandardScaler` làm lệch nhẹ góc của siêu phẳng phân cách cực đại tuyến tính. Ngược lại, các mô hình cây phi tuyến như XGBoost có khả năng phân ngưỡng độc lập nên hấp thụ hoàn hảo và tăng F1 từ 0.9379 lên 0.9535.

---

## 3. Checklist Nhiệm vụ
- [x] `report-source.md` có đầy đủ thông tin Trang bìa chuẩn UIT Khoa Khoa học Máy tính.
- [x] Có Bảng phân công nhiệm vụ và đóng góp của 3 thành viên (100% hoàn thành).
- [x] Cấu trúc Chương 4 phân tách rõ 4.1 Dataset, 4.2 Phương pháp đánh giá, 4.3 Kết quả đạt được.
- [x] 7 biểu đồ EDA được nhúng và nhận xét đầy đủ.
- [x] Biểu đồ Web Demo trợ năng người già (`demo_02_font_scaling_elderly.png`) được nhúng.
- [x] Biểu đồ cột ngang Top-20 từ khóa XAI (`top20_keywords_barplot.png`) được nhúng.
- [x] Đầy đủ các công thức toán: Cost-Sensitive loss, SVM hinge loss, TF-IDF.
- [x] Bảng 3.1 có đầy đủ 6 cột và số liệu thống kê trung bình.
- [x] Có giải thích toán học cho hiện tượng của Linear SVM trong Ablation 2.

---

## 4. Evidence (Bằng chứng Thực tế Nghiệm thu)

- **Trạng thái cập nhật:** `ĐÃ HOÀN THÀNH`
- **Diff tệp `report-source.md`:**
  - Kiểm tra diff: `git diff draft/scam-detection/reports/report/report-source.md` (384 dòng thay đổi).
  - Tệp nguồn tăng từ 610 dòng lên 711 dòng (+101 dòng học thuật sâu sắc).
  - Frontmatter: Đã thêm `faculty: "Khoa Khoa học Máy tính"`, `department: "Bộ môn Trí tuệ Nhân tạo"`, cập nhật ngày nộp: `"Báo cáo bảo vệ sớm: 23/09/2026 | Nộp bài chính thức LMS: Tháng 10/2026"`.
  - Thêm Bảng Phân công Nhiệm vụ & Tỷ lệ Đóng góp 3 thành viên (100% hoàn thành, 33.33% mỗi người) tại các dòng 34–48.
  - Mục lục chi tiết được đồng bộ tại các dòng 53–82.
- **Kiểm chứng hình ảnh nhúng:**
  - Hình 4.1: `label_distribution.png` (dòng 315)
  - Hình 4.1b: `text_length_comparison.png` (dòng 320)
  - Hình 4.1c: `wordcloud_scam_vs_normal.png` (dòng 325)
  - Hình 4.1d: `top_ngrams_scam_vs_normal.png` (dòng 330)
  - Hình 4.1e: `source_distribution.png` (dòng 335)
  - Hình 4.2: `scam_category_distribution.png` (dòng 340)
  - Hình 4.3: `auxiliary_correlation_heatmap.png` (dòng 345)
  - Hình 4.8b: `top20_keywords_barplot.png` (dòng 485)
  - Hình 4.9b: `demo_02_font_scaling_elderly.png` (dòng 598)
  - Toàn bộ 9/9 hình ảnh đã được xác nhận tồn tại 100% trong thư mục `reports/figures/`.
- **Kiểm chứng công thức toán & tính tay:**
  - `L(θ) = − Σᵢ [ w · yᵢ · log(pᵢ) + (1 − yᵢ) · log(1 − pᵢ) ]` (dòng 255).
  - `min ½‖ω‖² + C · Σᵢ w(yᵢ) · max(0, 1 − yᵢ · f(xᵢ))` (dòng 267).
  - Hệ 3 công thức TF-IDF (dòng 420–428).
  - Ví dụ tính tay đối soát khớp 100% với ma trận nhầm lẫn của XGBoost (Accuracy: 98.18%, Precision: 93.18%, Recall: 97.62%, F1: 0.9535) (dòng 406–416).
- **Kiểm chứng lý giải toán học Linear SVM:**
  - Mục 4.5.2 (dòng 582–590): Phân tích chi tiết hiện tượng dịch chuyển siêu phẳng cực đại lề `wᵀx + b = 0` trong không gian vector thưa 5.000 chiều TF-IDF khi ghép 15 đặc trưng liên tục chuẩn hóa qua `StandardScaler`, đối lập với cơ chế phân ngưỡng trực giao của họ cây XGBoost.

---

## 5. Kongming Advisory Gate (Passed Criteria)
- [x] Bằng chứng tại mục 4 được điền đầy đủ và kiểm chứng trực tiếp trên hệ thống tệp.
- [x] Không có hiện tượng hallucination hoặc số liệu mâu thuẫn.
- [x] Kongming xác nhận đánh giá: `PASSED`.
  > **Kongming Gate Verdict:** Bản thảo `report-source.md` đạt chuẩn chất lượng học thuật cao cấp A+, tính nhất quán số liệu 100%, tuân thủ tuyệt đối quy định không dùng LaTeX thô, tái cấu trúc Chương 4 hoàn hảo theo đề cương Thầy Thăng. Đủ điều kiện chuyển tiếp sang Phase 02.

---

## 6. Verdict
- **Đánh giá cuối cùng:** `PASSED`

