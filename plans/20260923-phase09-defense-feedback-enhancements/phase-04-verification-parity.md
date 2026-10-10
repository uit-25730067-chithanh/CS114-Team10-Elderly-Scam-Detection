# Phase 04 — Verification & Parity (Kiểm Định & Đồng Bộ Dự Án)

> **Kế hoạch cha:** [plan.md](./plan.md)  
> **Người phụ trách:** Đặng Chí Thanh (25730067)  
> **Trạng thái:** `passed` ✅

---

## 🎯 Kết Quả Kiểm Định Toàn Diện

- [x] **Kiểm tra tự động toàn diện**:
  - Chạy `python3 verify_final.py`: **100% PASSED** (cấu trúc thư mục, tệp bắt buộc, 11 phase plan, kiểm toán rò rỉ, mã số SV nhóm 10).
  - Chạy `python3 scripts/validate_assignment.py --id Final`: **100% PASSED**.
  - Chạy test suite `pytest draft/scam-detection/tests/`: **72/72 tests PASSED** (15.56s).
- [x] **Loại bỏ trùng lặp file nhị phân**:
  - Xóa bỏ `docs/DoAnMonHoc.docx` và `docs/DoAnMonHoc.pdf` để tránh nhân đôi 12 MB binary dư thừa; tập trung duy nhất vào bản xuất bản chính thức tại `draft/scam-detection/reports/report/report.docx` và `report.pdf`.
- [x] **Đồng bộ hóa tài liệu & Chuẩn hóa học thuật (Cross-Document Parity)**:
  - Khắc phục đường dẫn `PROJECT_ROOT` động và nạp dữ liệu SSOT trực tiếp từ `ablation_studies.json` trong `generate_academic_report.py`.
  - Khắc phục lỗi đảo nhãn mô hình trên biểu đồ `plot_ablation_figures.py` và xuất lại ảnh 300 DPI (`ablation_preprocessing_comparison.png`).
  - Bổ sung lời dẫn và định danh chuẩn mực cho Bảng 4.3 (Top 20 từ khóa SHAP) trong văn bản báo cáo.
  - Loại bỏ hoàn toàn lỗi chính tả ("báo vệ") và văn phong rò rỉ chỉ đạo cá nhân của giáo viên tại Mục 1.2, đưa về chuẩn mực văn phong nghiên cứu khoa học.
  - Chuẩn hóa số lượng mẫu tuyệt đối thành **2.193 mẫu thực tế** (1.773 tin bình thường, 420 tin lừa đảo).
  - Đồng bộ bảng Mục lục (TOC) trong cả 2 file `report.docx` và `report.pdf` khớp chính xác 100% với độ dài 34 trang thực tế của tài liệu.
- [x] **Sẵn sàng Merge PR #31**:
  - Toàn bộ 4 Phase của kế hoạch cải tiến báo cáo theo góp ý Buổi 8 đã hoàn tất và kiểm chứng đầy đủ.
  - Đã rà soát "vạch lá tìm sâu" và khắc phục triệt để các lỗi Critical / Medium.
  - Sẵn sàng tích hợp nhánh `feat/phase-09-defense-feedback-enhancements` vào `main`.
