# Phase 03 — DOCX Compilation & Styling (Biên Dịch & Định Dạng Báo Cáo Word)

> **Kế hoạch cha:** [plan.md](./plan.md)  
> **Người phụ trách:** Hoàng Cao Sơn (Lead) · Đặng Chí Thanh (Review)  
> **File cấu hình:** `assignments/Final/draft/scam-detection/reports/report/report-meta.yaml`  
> **Output:** `assignments/Final/draft/scam-detection/reports/report/report.docx` và PDF  
> **Trạng thái:** `ready`

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

- [ ] Tạo / Kiểm tra công cụ biên dịch tự động Markdown → DOCX (tận dụng skill `uit:it005-lab-report` hoặc script Python sử dụng `python-docx`).
- [ ] Chèn chuẩn xác các hình ảnh chất lượng cao 300 DPI từ `draft/scam-detection/reports/figures/`.
- [ ] Đảm bảo các bảng biểu (đặc biệt là 2 bảng Ablation Studies) không bị tràn lề, có tiêu đề bảng phía trên.
- [ ] Xuất file `report.docx` hoàn chỉnh và kiểm tra bố cục trang (đạt độ dài ≥ 20 trang).
