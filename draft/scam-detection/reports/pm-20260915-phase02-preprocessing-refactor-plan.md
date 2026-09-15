# Project Management Report: Phase 02 Preprocessing Pipeline Refactoring & Data-Driven Enhancement

- **Project:** CS114 Final Project — Elderly Scam Detection (Nhóm 10)
- **Author:** Đặng Chí Thanh (PM / Phụ trách Phase 02)
- **Date:** 15/09/2026
- **Tracking ID:** `PM-PHASE-02-REFACTOR`

---

## 1. Context & Motivation

Sau phản hồi của Lead review, việc thẩm định lại toàn bộ 2.193 dòng dữ liệu thực tế cho thấy pipeline ban đầu cần được nâng cấp toàn diện từ mức "khung kỹ thuật cơ bản" lên mức "hệ thống tiền xử lý NLP chuyên sâu đạt chuẩn học thuật":
- Khắc phục tình trạng bỏ sót 5 dạng nhãn thực thể ẩn danh (`[MONEY]`, `[ĐƯỜNG_DẪN]`, `[MÃ_OTP]`, `[SỐ_ĐIỆN_THOẠI]`, `[NUMBER]`).
- Xử lý triệt để các kỹ thuật lẩn tránh chữ cái/số (Leet-speak: `0` thay `o`, `!` thay `i`, `j` thay `i`) trong tin nhắn lừa đảo.
- Hóa giải hiện tượng phân mảnh từ ghép trong 45.0% mẫu tin nhắn không dấu.
- Mở rộng từ điển viết tắt từ 60 lên trên 160 mục ánh xạ chuyên ngành.
- Chuẩn hóa vị trí dấu thanh theo quy tắc ngữ âm học chuẩn mới qua `underthesea.text_normalize`.

---

## 2. Work Breakdown Structure (WBS) & Task Matrix

| Task ID | Component | Mô tả công việc chi tiết | Target Deliverable | Trạng thái |
|---------|-----------|--------------------------|---------------------|------------|
| **T-02.1** | `text_cleaner.py` | Tích hợp De-obfuscation Leet-speak (`th0ng ba0`, `d!eu k!en`, `t!en`), khử lặp ký tự (`nhaaa` → `nha`), chuẩn hóa dấu thanh chuẩn mới qua `underthesea` + NFC | Code nâng cấp, < 200 dòng | ⏳ Đang triển khai |
| **T-02.2** | `text_cleaner.py` | Mở rộng `TEENCODE_DICT` lên 160+ mục từ vựng (viễn thông, ngân hàng, công quyền, mạng xã hội, tiếng lóng) | Từ điển 160+ entries | ⏳ Đang triển khai |
| **T-02.3** | `tokenizer.py` | Bổ sung cơ chế nối từ ghép không dấu (unaccented phrase joining: `tai khoan` → `tai_khoan`, `cong an` → `cong_an`) trước khi chuyển giao cho `pyvi.ViTokenizer` | Tokenizer thích ứng | ⏳ Đang triển khai |
| **T-02.4** | `pipeline.py` | Nâng cấp bộ trích xuất đặc trưng phụ từ 10 lên 14 chỉ số, bao quát 100% các nhãn ẩn danh `[MONEY]`, `[ĐƯỜNG_DẪN]`, `[MÃ_OTP]`, `[SỐ_ĐIỆN_THOẠI]` | 14 cột đặc trưng phụ | ⏳ Đang triển khai |
| **T-02.5** | `tests/` | Mở rộng bộ kiểm thử tự động `test_preprocessing.py` từ 13 lên 20+ test cases bao phủ leet-speak, masked tokens, unaccented phrases | Test suite 100% pass | ⏳ Đang triển khai |
| **T-02.6** | `data/processed/` | Tái xử lý toàn bộ 2.193 dòng dữ liệu, kiểm toán tính toàn vẹn 0 nulls, 0 chuỗi rỗng | `dataset_preprocessed.csv` mới | ⏳ Đang triển khai |
| **T-02.7** | `notebooks/` | Cập nhật script khởi tạo và chạy lại `01_preprocessing.ipynb` phản ánh các phân tích leet-speak, masked entities và 14 đặc trưng phụ | Notebook executed | ⏳ Đang triển khai |
| **T-02.8** | Documentation | Cập nhật báo cáo nghiên cứu `research-thanh-phase02-vietnamese-preprocessing-audit.md` và `phase-02-vietnamese-text-preprocessing.md` | Báo cáo đồng bộ | ⏳ Đang triển khai |
| **T-02.9** | Git & PR | Chia nhỏ commit theo chuẩn Conventional Commits, push lên branch `feat/phase-02-vietnamese-text-preprocessing` và cập nhật PR #12 | PR #12 updated | ⏳ Đang triển khai |

---

## 3. Timeline & Execution Roadmap

- **Thời gian thực hiện**: 15/09/2026.
- **Tiêu chí nghiệm thu (Gate Criteria)**:
  1. `pytest` vượt qua 100% kiểm thử (≥ 20 test cases).
  2. `python3 verify_final.py` exit code 0.
  3. `dataset_preprocessed.csv` bảo toàn chính xác 2.193 dòng, 23 cột (gồm 14 cột đặc trưng phụ + metadata + cleaned text).
  4. Notebook `01_preprocessing.ipynb` chạy có đầy đủ outputs hình ảnh biểu đồ thống kê chuyên sâu.
  5. Đẩy code lên PR #12 và vượt qua kiểm định CI.

---

## Unresolved Questions
- Không có câu hỏi nào chưa được giải quyết.
