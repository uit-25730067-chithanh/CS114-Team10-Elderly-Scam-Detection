# Báo cáo Quản lý Dự án: Làm sạch Dữ liệu Cẩm & Tối ưu Gemini PR Code Review

**Dự án:** Nhận diện Tin nhắn Lừa đảo Người cao tuổi (CS114 - Nhóm 10)  
**Thời gian:** 12/09/2026 22:00 UTC+7  
**Tác giả:** Đặng Chí Thanh (PM) | Hỗ trợ thành viên: Bùi Thị Mỷ Cẩm  
**Tham chiếu PR:** Pull Request #9 (`feat/phase-01-cam-data-collection`)

---

## 1. Tóm tắt Bối cảnh & Vấn đề Phát hiện

| Thành phần | Vấn đề phát hiện | Tác động kỹ thuật | Giải pháp thực hiện |
|---|---|---|---|
| **Dữ liệu `staging_cam_scam.csv`** | Phân loại fallback khiến ~20-30 mẫu cờ bạc, bắn cá, game bài (VNX0S0, 8DAY, JILI...) lọt vào nhãn `public_service`. | Gây nhiễu nhãn (Label Noise), sai lệch mô tả cam kết của PR #9. | Xây dựng bộ lọc biểu thức chính quy đa tầng chuẩn hóa không dấu, loại bỏ 100% cờ bạc, chỉ giữ đúng `public_service` và `health_gift`. |
| **Workflow `gemini-review.yml`** | Không cấu hình loại trừ `.csv`, `.tsv`, `.jsonl` trong git diff. Thiếu `safetySettings` trong API payload. | Diff 80.000 ký tự tin nhắn thô khiến Gemini kích hoạt bộ lọc Safety Filter ngắt cụt nội dung tại mục `### 🔍`. | Bổ sung `.csv`, `.tsv`, `.jsonl` vào `EXCLUDE_EXTENSIONS`, thêm `safetySettings` `BLOCK_NONE`, log `finishReason`, bật `workflow_dispatch`. |

---

## 2. Kết quả Đo lường Dữ liệu Sau Làm sạch

| Chỉ số | Trước xử lý | Sau xử lý (Clean) | Biến thiên | Trạng thái nghiệm thu |
|---|:---:|:---:|:---:|:---:|
| **Tổng số mẫu lừa đảo** | 530 | **514** | -16 mẫu rác | ✅ Đạt 102.8% chỉ tiêu (≥ 500 mẫu) |
| **Mẫu Cờ bạc / Cá cược / Adult** | 42 | **0** | -42 | ✅ 100% sạch cờ bạc & cá cược |
| **Mẫu Quyền lực & Cấp cứu (Sơn)** | 0 | **0** | 0 | ✅ Phân định ranh giới tuyệt đối 100% |
| **Bẫy Dịch vụ công (`public_service`)** | 471 (lẫn cờ bạc) | **384** (chuẩn hóa) | -87 | ✅ Khớp 100% ngữ nghĩa dịch vụ công |
| **Bẫy Sức khỏe / Quà tặng (`health_gift`)** | 59 | **130** | +71 | ✅ Mở rộng độ phủ từ nguồn IEEE |
| **Minh chứng 1-1 (`source_url` #L...)** | 530 / 530 (100%) | **514 / 514 (100%)** | 0 sai lệch | ✅ Pass `verify_cam_provenance.py` 100% |
| **Kiểm định chuẩn `data_validation.py`** | PASSED | **PASSED** | Chuẩn schema | ✅ Không duplicate, không PII, 0% rò rỉ |

---

## 3. Cập nhật Kỹ thuật Workflow Gemini Code Review

1. **Loại trừ dữ liệu bảng thô:** `.csv`, `.tsv`, `.jsonl` được bỏ qua trong `git diff`. Gemini chỉ tập trung rà soát mã nguồn logic (`.py`, `.yml`) và tài liệu (`.md`).
2. **Khai thông bộ lọc an toàn:** Thêm `safetySettings` (`BLOCK_NONE`) cho 4 danh mục nhạy cảm (Harassment, Hate Speech, Sexually Explicit, Dangerous Content) để mô hình có thể thẩm định các kịch bản tấn công mạng / lừa đảo mà không bị API ngắt ngang.
3. **Giám sát trạng thái:** Bổ sung logging `finishReason` của candidate Gemini.
4. **Hỗ trợ chạy thủ công:** Thêm sự kiện `workflow_dispatch` để tiện kích hoạt qua `gh workflow run`.

---

## 4. Trạng thái Tiến độ Toàn nhóm (Phase 01)

| Thành viên | Nhiệm vụ | Chỉ tiêu | Đã hoàn thành | Tiến độ | Ghi chú |
|---|---|:---:|:---:|:---:|---|
| **Đặng Chí Thanh** | Dữ liệu bình thường (`label=0`) | ≥ 500 | 1.773 (+ 42 Holdout) | 354.6% | Đã nghiệm thu độc lập |
| **Bùi Thị Mỷ Cẩm** | Lừa đảo Sức khỏe & Dịch vụ công | ≥ 500 | **514** | 102.8% | Hoàn tất sạch 100%, sẵn sàng merge |
| **Hoàng Cao Sơn** | Lừa đảo Quyền lực & Cấp cứu | ≥ 500 | 0 | 0.0% | ⏳ Chờ Sơn nộp trước 23:59 đêm nay |
| **Toàn nhóm** | Dataset gộp Phase 01 | ≥ 1.500 | **2.287** | 152.5% | Sẵn sàng đóng gói khi Sơn hoàn tất |

---

## 5. Câu hỏi Chưa giải quyết (Unresolved Questions)

1. **Tiến độ của Hoàng Cao Sơn:** Sơn hiện chưa cập nhật 500 mẫu thuộc 2 nhóm `fear_authority` và `family_emergency`. Nếu trước 23:59 đêm nay Sơn gặp khó khăn kỹ thuật tương tự Cẩm, PM có cần kích hoạt Contingency Plan (Nhánh B) hoặc chạy pipeline hỗ trợ Sơn tương tự hay không?
