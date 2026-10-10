# Phase 03 — DOCX Compilation & Styling (Biên Dịch & Định Dạng Báo Cáo Word)

> **Kế hoạch cha:** [plan.md](./plan.md)  
> **Người phụ trách:** Hoàng Cao Sơn (Lead) · Đặng Chí Thanh (Review)  
> **File cấu hình:** `assignments/Final/draft/scam-detection/reports/report/report-meta.yaml`  
> **Output:** `draft/scam-detection/reports/report/report.docx` và PDF  
> **Trạng thái:** `passed` ✅

---

## 🎯 Chuẩn Thể Thức Học Thuật UIT

Theo quy định trình bày đồ án và cấu hình tại `report-meta.yaml`:
* **Font chữ**: Times New Roman 13pt (Title 16pt Bold, Heading 1 14pt Bold, Heading 2 13pt Bold).
* **Giãn dòng (Line spacing)**: 1.3 lines, giãn đoạn Before 0pt, After 6pt.
* **Căn lề chuẩn (Margins)**:
  - Lề trái (Left): 3.0 cm (để đóng gáy).
  - Lề phải (Right): 2.0 cm.
  - Lề trên (Top): 2.0 cm.
  - Lề dưới (Bottom): 2.0 cm.
* **Trang bìa (UIT Standard Cover)**:
  - Khung viền hoa văn kép (double border) trang trọng theo chuẩn OpenXML.
  - Logo Trường ĐH Công nghệ Thông tin — ĐHQG-HCM.
  - Tên môn học: **Máy học (CS114.F31.CN2.TTNT)**.
  - Giảng viên hướng dẫn: **ThS. Cáp Phạm Đình Thăng**.
  - Danh sách nhóm 10: Đặng Chí Thanh (25730067), Bùi Thị Mỷ Cẩm (25730013), Hoàng Cao Sơn (25730061).
* **Mục lục tự động**: Danh mục nội dung có số trang dot-leader, Danh mục hình ảnh và Danh mục bảng biểu.

---

## 🛠️ Công Việc Cụ Thể

- [x] Tạo / Kiểm tra công cụ biên dịch tự động Markdown → DOCX (sử dụng script Python `draft/scam-detection/reports/report/generate_academic_report.py` tích hợp `python-docx` và `docx2pdf`).
- [x] Chèn chuẩn xác các hình ảnh chất lượng cao 300 DPI từ `draft/scam-detection/reports/figures/` (tổng cộng 11 hình ảnh biểu đồ và sơ đồ luồng hệ thống).
- [x] Đảm bảo các bảng biểu (Bảng 2.1, 2.2, 4.2, Bảng 4.4 & 4.5 Ablation Studies) không bị tràn lề, có tiêu đề bảng phía trên, căn chỉnh đều đẹp.
- [x] Xuất file `report.docx` (5.7 MB) và biên dịch `report.pdf` (6.2 MB) hoàn chỉnh, kiểm tra bố cục trang đạt chuẩn 34 trang (≥ 30 trang), sao chép đồng bộ vào `docs/DoAnMonHoc.docx` và `docs/DoAnMonHoc.pdf`.
