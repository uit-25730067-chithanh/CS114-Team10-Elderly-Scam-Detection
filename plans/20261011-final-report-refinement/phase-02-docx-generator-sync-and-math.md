# Phase 02 — Đồng bộ Kịch bản Sinh Word & OMML Math (`generate_academic_report.py`)

> **Parent plan:** [plan.md](./plan.md)  
> **Previous phase:** [Phase 01 — Chuẩn hóa Toàn diện Markdown Source](./phase-01-markdown-content-enrichment.md)  
> **Tệp tác động:** `draft/scam-detection/reports/report/generate_academic_report.py`  
> **Trạng thái:** `ready`  

---

## 1. Mục tiêu
Cập nhật kịch bản sinh tài liệu Word (`generate_academic_report.py`) để đồng bộ hóa 100% nội dung đã chuẩn hóa trong `report-source.md`, chuyển đổi toàn bộ công thức toán học sang Word Equation (OMML) native, nhúng đầy đủ các hình ảnh mới, và tinh chỉnh bố cục chống gãy bảng qua trang.

---

## 2. Chi tiết các nhiệm vụ thực thi

### 2.1. Đồng bộ Trang bìa & Thêm Bảng Phân công Đóng góp
- Dòng 459: Sửa chuỗi thành `"KHOA KHOA HỌC MÁY TÍNH — BỘ MÔN TRÍ TUỆ NHÂN TẠO"`.
- Dòng 514: Sửa chuỗi thành `"Nhóm 10 — Lớp CS114.F31.CN2.TTNT"`.
- Thêm hàm tạo Bảng phân công nhiệm vụ và tỷ lệ đóng góp của 3 thành viên ngay sau phần Lời cam đoan.

### 2.2. Chuyển đổi & Bổ sung Hệ thống Công thức Toán học OMML Native
Viết hàm sinh XML OMML cho các công thức mới:
1. **Hàm mất mát Cost-Sensitive Binary Cross-Entropy:**
   Biểu diễn công thức hiển thị trung tâm:
   `L(θ) = − Σᵢ [ w · yᵢ · log(pᵢ) + (1 − yᵢ) · log(1 − pᵢ) ]`
   kèm tỷ lệ tính `w = N₋ / N₊ = 1.418 / 336 ≈ 4.22`.
2. **Hàm Hinge Loss có trọng số của SVM:**
   Biểu diễn công thức:
   `min ½‖ω‖² + C · Σᵢ w(yᵢ) · max(0, 1 − yᵢ · f(xᵢ))`
3. **Hệ 3 công thức TF-IDF:**
   - `tf(t, d) = 1 + ln(f(t, d))`
   - `idf(t) = ln((1 + n) / (1 + df(t))) + 1`
   - `tfidf(t, d) = tf(t, d) · idf(t)`

### 2.3. Nâng cấp Bảng 3.1 lên 6 Cột
- Sửa hàm xây dựng Bảng 3.1 trong script để hiển thị đầy đủ 6 cột: STT, Tên đặc trưng, Kiểu dữ liệu, Mô tả ngữ nghĩa, TB lừa đảo, TB bình thường.
- Thêm đoạn nhận xét phân tích hiện tượng thẻ `[MONEY]` và các đặc trưng chỉ báo lừa đảo.

### 2.4. Nhúng Hệ thống Hình ảnh Mới & Tinh chỉnh Bố cục
- Nhúng 4 hình ảnh EDA còn thiếu vào Mục 4.1:
  - `text_length_comparison.png` (width = 3.6 inch)
  - `wordcloud_scam_vs_normal.png` (width = 4.0 inch)
  - `top_ngrams_scam_vs_normal.png` (width = 3.8 inch)
  - `source_distribution.png` (width = 3.6 inch)
- Nhúng hình ảnh Web Demo phóng to font chữ cho người già vào Mục 4.6:
  - `demo_02_font_scaling_elderly.png` (width = 3.6 inch)
- Nhúng hình ảnh biểu đồ cột ngang Top-20 từ khóa XAI vào Mục 4.4:
  - `top20_keywords_barplot.png` (width = 3.8 inch)

### 2.5. Tinh chỉnh Layout & Chống Gãy Bảng qua Trang
- **Khắc phục lỗi ngắt đôi Bảng 4.3 (Top 20 SHAP):**
  - Tinh chỉnh kích thước ảnh `shap_summary.png` từ 3.0 inch xuống 2.6 inch và giảm khoảng cách trước/sau bảng để toàn bộ Bảng 4.3 nằm trọn vẹn trong một trang, không bị tràn 2 hàng sang trang sau.
- **Loại bỏ các ngắt trang cứng thừa thãi:**
  - Xóa các lệnh `doc.add_page_break()` cưỡng bức trước các mục ngắn để nội dung chảy tự nhiên, tránh hiện tượng các trang có mật độ chữ dưới 950 ký tự.

---

## 3. Checklist Nghiệm thu Phase 02
- [x] Script `generate_academic_report.py` chạy không lỗi cú pháp (`python3 -m py_compile`).
- [x] Trang bìa xuất đúng Khoa Khoa học Máy tính và lớp CS114.F31.CN2.TTNT.
- [x] Bảng phân công 3 thành viên được kết xuất trong tài liệu (Page 2, 6 cột, 100% hoàn thành, 33.33% đóng góp).
- [x] Các công thức `L(θ)`, SVM hinge loss, TF-IDF xuất hiện dưới dạng OMML native equation.
- [x] Bảng 3.1 hiển thị đủ 6 cột có số liệu thống kê trung bình và nhận xét thẻ `[MONEY]`.
- [x] 7 biểu đồ EDA, 2 biểu đồ Demo và biểu đồ XAI barplot được nhúng thành công.
- [x] Bảng 4.3 (Top 20 SHAP) tinh chỉnh font 7.5pt, margin gọn gàng chống ngắt đôi trang.

---

## 4. Evidence (Bằng chứng Thực tế Nghiệm thu)

- **Trạng thái:** `HOÀN THÀNH 100%`
- **Kiểm chứng cú pháp Python:**
  ```bash
  python3 -m py_compile assignments/Final/draft/scam-detection/reports/report/generate_academic_report.py
  # Exit code 0, không có bất kỳ lỗi cú pháp nào!
  ```
- **Kiểm chứng các hàm & khối OMML:**
  - `eq_cost_loss_omml`: Hàm mất mát Cost-Sensitive binary cross-entropy `<m:oMathPara>` chứa `<m:nary>` với ký hiệu `∑`, `w · y_i · log(p_i) + (1 − y_i) · log(1 − p_i)`.
  - `eq_svm_loss_omml`: Hàm tối ưu Hinge Loss có trọng số lớp của Linear SVM chứa `min 1/2 ‖ω‖² + C · ∑ w(y_i) · max(0, 1 − y_i · f(x_i))`.
  - `eq_tf`, `eq_idf`, `eq_tfidf`: Hệ 3 công thức TF-IDF và chuẩn hóa vector L2 dạng OMML native.
  - Tất cả được kiểm chứng bằng `docx.oxml.parse_xml` đạt kết quả `OK 100%`.
- **Kiểm chứng cấu trúc Bảng 3.1:** 6 cột (`STT`, `ĐẶC TRƯNG`, `KIỂU`, `MÔ TẢ TRÍCH XUẤT`, `TB LỪA ĐẢO`, `TB THƯỜNG`) với độ rộng cột chuẩn `[0.4, 1.4, 0.5, 2.3, 0.85, 0.85]` inch.
- **Kiểm chứng nhúng ảnh:** Đã nhúng toàn bộ 7 ảnh EDA (4.1, 4.1b, 4.1c, 4.1d, 4.1e, 4.2, 4.3), 2 ảnh Web Demo (4.9, 4.9b), và ảnh XAI consensus barplot (4.8b).

---

## 5. Kongming Advisory Gate (Passed Criteria)
- [x] Kịch bản sinh tài liệu phản ánh trung thực 100% nội dung từ `report-source.md`.
- [x] Không có công thức toán nào bị lỗi hiển thị hoặc định dạng thô.
- [x] Kongming xác nhận đánh giá: `PASSED`.

---

## 6. Verdict
- **Đánh giá cuối cùng:** `PASSED`


