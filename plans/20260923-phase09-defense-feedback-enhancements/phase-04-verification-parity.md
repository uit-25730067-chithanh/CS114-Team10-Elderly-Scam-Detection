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
  - Khắc phục đường dẫn `PROJECT_ROOT` động trong `generate_academic_report.py`, bảo đảm khả năng thực thi độc lập trên mọi hệ điều hành.
  - Loại bỏ hoàn toàn lỗi chính tả ("báo vệ") và văn phong rò rỉ chỉ đạo cá nhân của giáo viên tại Mục 1.2, đưa về chuẩn mực văn phong nghiên cứu khoa học.
  - Chuẩn hóa số lượng mẫu tuyệt đối thành **2.193 mẫu thực tế** (1.773 tin bình thường, 420 tin lừa đảo).
  - Đồng bộ bảng Mục lục (TOC) trong file Word/PDF khớp chính xác 100% với độ dài 34 trang của tài liệu.
- [x] **Sẵn sàng Merge PR #31**:
  - Toàn bộ 4 Phase của kế hoạch cải tiến báo cáo theo góp ý Buổi 8 đã hoàn tất và kiểm chứng đầy đủ.
  - Sẵn sàng tích hợp nhánh `feat/phase-09-defense-feedback-enhancements` vào `main`.
