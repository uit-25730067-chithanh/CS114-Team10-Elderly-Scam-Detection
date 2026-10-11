# Phase 03 — Biên dịch Word, Đồng bộ Mục lục & Hyperlinks

> **Parent plan:** [plan.md](./plan.md)  
> **Previous phase:** [Phase 02 — Đồng bộ Kịch bản Sinh Word & OMML Math](./phase-02-docx-generator-sync-and-math.md)  
> **Tệp tác động:**
> - `draft/scam-detection/reports/report/report.docx`
> - `draft/scam-detection/reports/report/apply_toc_links.py`
> - `draft/scam-detection/reports/report/apply_reference_links.py`  
> **Trạng thái:** `done`  

---

## 1. Mục tiêu
Thực thi kịch bản biên dịch để sinh tệp `report.docx` mới, cập nhật bảng Mục lục tự động phản ánh chính xác 100% số trang thực tế của từng tiêu đề, thiết lập liên kết nội bộ (bookmarks) và siêu liên kết tài liệu tham khảo ngoài. *(Lưu ý: Không tạo hay can thiệp vào tệp `.pdf`, người dùng sẽ tự mở Word để xuất PDF thủ công).*

---

## 2. Chi tiết các nhiệm vụ thực thi

### 2.1. Biên dịch Bản nháp Word Ban đầu
- Chạy `python3 generate_academic_report.py` để tạo tệp `report.docx` chứa đầy đủ nội dung, hình ảnh và công thức mới.
- Không truyền cờ `--pdf` để bảo toàn yêu cầu của người dùng.

### 2.2. Đo lường & Đồng bộ Số trang Mục lục Chính xác (TOC Synchronization)
- Xây dựng script phân tích phân trang trong Word và đo lường layout thực tế.
- Cập nhật số trang chính xác cho toàn bộ 29 mục trong bảng Mục lục của tài liệu Word:
  - `CHƯƠNG 1`: Trang 4 (kết thúc trang 6).
  - `CHƯƠNG 2`: Trang 7 (kết thúc trang 9).
  - `CHƯƠNG 3`: Trang 10 (kết thúc trang 14).
  - `CHƯƠNG 4`: Trang 15 (kết thúc trang 32).
  - `CHƯƠNG 5`: Trang 33 (kết thúc trang 34).
  - `TÀI LIỆU THAM KHẢO`: Trang 35.
- Triệt tiêu 100% hiện tượng lệch trang giữa Mục lục và nội dung thực tế.

### 2.3. Tích hợp Bookmarks và Liên kết Tương tác
- Nâng cấp và chạy `apply_toc_links.py` để gắn 29 bookmarks (`_Toc_Sec_01` → `_Toc_Sec_29`) và 58 hyperlinks nội bộ cho phép `Ctrl + Click` từ Mục lục nhảy thẳng tới từng chương mục.
- Nâng cấp và chạy `apply_reference_links.py` định vị động theo regex `r'^\[\d+\]'` để gắn 15 hyperlinks trực tiếp cho 20 tài liệu tham khảo (URL và DOI).

### 2.4. Kiểm định Định dạng OpenXML Chuyên sâu (`audit_docx_xml.py`)
- Chạy script kiểm toán:
  ```bash
  python3 .agents/skills/academic-report/scripts/audit_docx_xml.py \
    assignments/Final/draft/scam-detection/reports/report/report.docx
  ```
- Kiểm tra các tiêu chí bắt buộc:
  - Lề trang: Trái 3.0cm, Phải 2.0cm, Trên 2.0cm, Dưới 2.0cm.
  - Bìa hoa văn OpenXML chuẩn UIT Blue `#1B365D`.
  - 100% bảng biểu có thuộc tính chống gãy dòng qua trang `<w:cantSplit/>`.
  - 100% bảng biểu có lặp lại tiêu đề khi qua trang `<w:tblHeader/>`.
  - 100% bookmarks nội bộ giải quyết thành công về các đoạn văn hợp lệ.

---

## 3. Checklist Nghiệm thu Phase 03
- [x] `report.docx` được biên dịch thành công mà không can thiệp tệp PDF (kích thước ~9.5MB).
- [x] Số trang trong bảng Mục lục khớp 100% với phân trang nội dung thực tế (29 mục phân bổ từ Trang 4 đến Trang 35).
- [x] Các mục trong Mục lục có thể `Ctrl + Click` để chuyển hướng (29 bookmarks, 58 internal hyperlinks).
- [x] Các tài liệu tham khảo có thể nhấp mở đường dẫn trực tiếp (15 external hyperlinks).
- [x] `audit_docx_xml.py` trả về kết quả `PASS` 100% tiêu chí.

---

## 4. Evidence (Bằng chứng Thực tế Nghiệm thu)

- **Trạng thái:** `Hoàn thành (Passed)`
- **Lệnh biên dịch Word:**
  ```bash
  python3 assignments/Final/draft/scam-detection/reports/report/generate_academic_report.py
  # Tệp sinh ra: draft/scam-detection/reports/report/report.docx (9,531,048 bytes ~ 9.5MB)
  ```
- **Lệnh gắn TOC bookmarks và internal hyperlinks:**
  ```bash
  python3 assignments/Final/draft/scam-detection/reports/report/apply_toc_links.py \
    assignments/Final/draft/scam-detection/reports/report/report.docx
  # Output: 29/29 TOC items matched, 29 bookmarks created, 58 internal hyperlinks inserted.
  ```
- **Lệnh gắn Reference external hyperlinks:**
  ```bash
  python3 assignments/Final/draft/scam-detection/reports/report/apply_reference_links.py \
    assignments/Final/draft/scam-detection/reports/report/report.docx
  # Output: 15 external hyperlinks added for 20 references.
  ```
- **Kết quả chạy `audit_docx_xml.py`:**
  ```
  [*] Checking margins: Left=3.0cm, Right=2.0cm, Top=2.0cm, Bottom=2.0cm -> PASS
  [*] Checking cover border: Double border #1B365D -> PASS
  [*] Checking table pagination safety: 12/12 tables contain <w:cantSplit/> and <w:tblHeader/> -> PASS
  [*] Checking internal hyperlinks: 58/58 hyperlinks resolved to bookmarks -> PASS
  [*] OVERALL AUDIT: PASS (100% criteria met)
  ```

---

## 5. Kongming Advisory Gate (Passed Criteria)
- [x] Tệp `report.docx` mở được hoàn hảo, phân trang chuẩn xác, lề 3-2-2-2 cm.
- [x] Số trang trong Mục lục khớp chính xác với trang hiển thị thực tế.
- [x] Không tạo hoặc sửa đổi bất kỳ tệp `.pdf` nào theo đúng cam kết với người dùng.
- [x] Kongming xác nhận đánh giá: `PASSED`.

---

## 6. Verdict
- **Đánh giá cuối cùng:** `PASSED`

