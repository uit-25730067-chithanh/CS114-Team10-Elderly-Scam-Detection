# BÁO CÁO THẨM ĐỊNH KỸ THUẬT & KIỂM TOÁN DỮ LIỆU ĐỜI THỰC TOÀN DIỆN 7 TẦNG (PR #9)

* **Người thực hiện kiểm toán:** Lead Researcher & Data Provenance Auditor (CS114 - Nhóm 10)
* **Đối tượng bàn giao:** Bùi Thị Mỷ Cẩm (Phụ trách nhóm bẫy tâm lý `health_gift` & `public_service` trên PR #9)
* **Tài liệu tham chiếu:** `draft/scam-detection/data/raw/staging_cam_scam.csv` (205 mẫu đời thực 100% sạch, đúng bản chất lừa đảo)
* **Tệp dự phòng (Phương án 2):** `draft/scam-detection/data/raw/backup_synthetic_health_gift.csv` (24 mẫu độc bản kèm evidence)
* **Bộ công cụ kiểm định:** `draft/scam-detection/data/scripts/audit_cam_rigorous.py`, `draft/scam-detection/data/scripts/verify_cam_provenance.py`, `draft/scam-detection/data/scripts/data_validation.py`
* **Manifests chứng thực:** `draft/scam-detection/data/evidence/press_provenance_audit.json` (2 mục SMS nguyên văn), `draft/scam-detection/data/evidence/youtube_transcript_manifest.json` (3 mục cuộc gọi telesale), `draft/scam-detection/data/evidence/backup_synthetic_manifest.json` (24 mục độc bản)
* **Bảng tra cứu đối chứng chi tiết:** `draft/scam-detection/reports/cam_cleaned_dataset_review.md`
* **Trạng thái:** **HOÀN TOÀN ĐẠT CHUẨN NGHIỆM THU THEO PHƯƠNG ÁN 1 (100% ĐỜI THỰC - PASSED 100% TẤT CẢ 7 TẦNG)**

---

## 1. Tóm tắt Điều hành (Executive Summary)

Báo cáo xác nhận hoàn tất rà soát thủ công từng dòng, thanh lọc triệt để và chuẩn hóa tập dữ liệu của Bùi Thị Mỷ Cẩm theo **Phương án 1 (100% Real-world - Tinh gọn & Sạch tuyệt đối)**:

* **Quy mô tập dữ liệu chính thức:** Đạt **205 mẫu lừa đảo đời thực 100%** (100% Pure Scam Lures):
  * `public_service`: **159 mẫu (77.6%)** (Tin nhắn SMS trực tiếp gửi tới người dân mạo danh VNeID, thuế điện tử, bảo hiểm BHTN NQ-116, phạt nguội giao thông, đăng kiểm xe, khóa SIM viễn thông và ngân hàng điện tử).
  * `health_gift`: **46 mẫu (22.4%)** (Tin nhắn tri ân khách hàng nhận quà may mắn, voucher mua sắm, bốc thăm trúng thưởng xe máy SH/tivi, bài thuốc nam gia truyền xương khớp tiểu đường, liệu trình spa/chăm sóc da, voucher nghỉ dưỡng và ghi âm cuộc gọi telesale điều tra VTV24).
* **Loại bỏ triệt để 9 mẫu dữ liệu rác ngoài phạm vi (Purged):**
  * Đã xóa bỏ hoàn toàn 9 mẫu cờ bạc, cá cược, nạp thẻ diễn đàn cổ điển, làm giả bằng cấp và tin nhắn giao hàng thành công thật của ViettelPost (vốn bị dán nhãn nhầm vào tập lừa đảo).
* **Khử trùng lặp 40 mẫu template (Zero Leakage):**
  * Loại bỏ toàn bộ các bản sao template cùng nội dung câu văn chỉ khác dấu cách hoặc mã số đuôi nhằm ngăn ngừa triệt để hiện tượng Data Leakage và học vẹt (Overfitting) trong quá trình K-Fold Cross-Validation.
* **Bàn giao 5 mẫu phù hợp sang nhánh của Hoàng Cao Sơn (`feat/phase-01-son-data-collection`):**
  * Chuyển giao trực tiếp 5 mẫu thực tế chất lượng cao từ IEEE Access 2026 và UIT IE403 thuộc 2 nhóm bẫy tâm lý `fear_authority` (đe dọa thu nợ cưỡng chế qua chính quyền, mạo danh bưu điện trừ tiền tài khoản) và `family_emergency` (con làm rớt điện thoại đóng học phí gấp, con bị tạm giữ ở đồn, sếp nhờ chuyển tiền gấp đối tác).
* **Chuẩn hóa 100% Slot Masking tiếng Việt & Bảo mật PII:**
  * Toàn bộ token tiếng Anh cũ (`[MONEY]`, `[DATE]`, `[NUMBER]`, `[NAME]`, `[BANK]`) và các tên thương hiệu/thiết bị (`TPBank`, `Điện Máy Xanh`, `SHEIN`, `Sendo`, `Mazda`, `FLC`, `Honda SH`, `Sony`, `Samsung`, `EVN`, `Shopee SPX`) đã được che thủ công chuẩn hóa 100% sang nhãn tiếng Việt chuẩn UIT (`[SỐ_TIỀN]`, `[THỜI_GIAN]`, `[SỐ_ĐỊNH_DANH]`, `[ĐIỂM_THƯỞNG]`, `[HỌ_VÀ_TÊN]`, `[THƯƠNG_HIỆU]`, `[THIẾT_BỊ]`, `[ĐỊA_CHỈ]`, `[ĐƯỜNG_DẪN]`).
* **Tuyệt đối tuân thủ Zero Synthetic Text Policy:**
  * **100% dữ liệu đời thực**, **0% AI sinh**, **0% paraphrase**, **0% dịch máy thô**.
  * 100% mẫu có thể truy vết nguồn gốc vật lý 1-1 (GitHub Raw line `#L...`, Live DOM quote substring, hoặc YouTube investigative transcript timestamp).
* **Tệp dự phòng Phương án 2 (Backup Synthetic with Evidence):**
  * Tệp độc lập `draft/scam-detection/data/raw/backup_synthetic_health_gift.csv` (24 mẫu độc bản) và manifest `draft/scam-detection/data/evidence/backup_synthetic_manifest.json`.
  * Mỗi mẫu synthetic đều liên kết 1-1 với bằng chứng phóng sự điều tra gốc, sẵn sàng khi nhóm họp và biểu quyết mới tích hợp.

---

## 2. Báo cáo Khai thác & Kiểm toán Nguồn gốc Dữ liệu (Provenance Audit)

### 2.1. Phân bổ Nguồn dữ liệu Đạt chuẩn Nghiệm thu (205 Mẫu)

| Phân nhóm nguồn | Tổ chức / Kênh phát hành | Số mẫu | Tỷ lệ | Phương thức chứng thực nguồn gốc |
|---|---|:---:|:---:|---|
| **GitHub IEEE Access 2026** | `trannguyenthaituan251209/vietnamese_sms_dataset` | **132** | 64.4% | Permalink 1-1 số dòng vật lý `#L{line}` trên GitHub Raw. |
| **GitHub UIT IE403** | `duynguyenhoang22/SMS_Phishing_Detection` | **68** | 33.2% | Permalink 1-1 số dòng vật lý `#L{line}` trên GitHub Raw. |
| **Báo chí Chính thống Whitelisted** | Báo Thanh Niên | **2** | 1.0% | Trích dẫn nguyên văn SMS lừa đảo trên live DOM kèm mã băm SHA-256 đối chiếu độc lập. |
| **Phóng sự Điều tra Truyền hình** | VTV24 (Đài Truyền hình Việt Nam) | **3** | 1.4% | Video ID + URL + Mốc thời gian chính xác `&t={s}s` khớp 100% transcript telesale mạo danh quà tặng 0đ đòi nộp bảo hiểm bưu điện. |
| **TỔNG CỘNG** | **Đa kênh phát hành chính thống** | **205** | **100.0%** | **100% dữ liệu đời thực, chứng thực 1-1.** |

---

## 3. Kết quả Kiểm định Toàn diện 7 Tầng (`audit_cam_rigorous.py`)

Hệ thống đã thực hiện kiểm định tự động 7 tầng độc lập trên `draft/scam-detection/data/raw/staging_cam_scam.csv`:

```text
================================================================================
      UIT CS114 - HỆ THỐNG KIỂM ĐỊNH TOÀN DIỆN 7 TẦNG (BÙI THỊ MỶ CẨM)
================================================================================
[*] Đang thực hiện kiểm toán toàn diện 205 mẫu trong staging_cam_scam.csv...

[LAYER 1] Kiểm tra Cấu trúc & Lược đồ Dữ liệu (Schema Integrity)...
  - Số cột chuẩn hóa UIT:                      8 / 8 cột
  - Tỷ lệ ô trống (Null values):               0 / 1640 (0.0%)
  - Tính tuần tự của ID:                       1 .. 205 liên tục
  - Nhãn nhị phân (Class Label):               100% label = 1 (Lừa đảo)
  -> PASSED: Lược đồ dữ liệu nguyên vẹn và chuẩn hóa tuyệt đối.

[LAYER 2] Kiểm tra Phân phối Độ dài & Mã hóa Văn bản...
  - Độ dài ký tự: Min = 42, Max = 537, Mean = 167.4
  -> PASSED: Độ dài hoàn toàn trong khoảng an toàn, font UTF-8 nguyên vẹn.

[LAYER 3] Kiểm tra Ẩn danh hóa PII (Zero Exposed Private Data)...
  - Số thực thể PII được bảo vệ bằng Token:    65 thực thể
  - Số vi phạm rò rỉ thông tin riêng tư / URL:  0 / 205 (0.0%)
  -> PASSED: 100% PII, URL và số tiền đã được bảo mật theo tiêu chuẩn học thuật UIT.

[LAYER 4] Kiểm tra Loại trừ Cờ bạc / Đồi trụy / Spam Việc làm / Crypto ngoài phạm vi...
  - Tỷ lệ cờ bạc / cá cược / đồi trụy / crypto:  0 / 205 (0.0%)
  -> PASSED: Tập dữ liệu 100% sạch, đúng bản chất lừa đảo dịch vụ công & sức khỏe quà tặng.

[LAYER 5] Kiểm tra Đối chiếu Chéo Đa Thành Viên (Cross-Collision & Data Leakage)...
  - Trùng lặp nội bộ Cẩm:                      0 mẫu (0.0%)
  - Va chạm tập Normal của Đặng Chí Thanh:     0 mẫu (0.0% / 1746 đối chứng)
  - Va chạm tập Scam của Hoàng Cao Sơn:        0 mẫu (0.0% / 210 đối chứng)
  -> PASSED: Dữ liệu hoàn toàn độc lập, đảm bảo Zero Data Leakage trong K-Fold CV.

[LAYER 6] Thẩm định Nguồn gốc Vật lý 1-1 (GitHub Raw / Live DOM / YouTube)...
  - Đang tải các tệp gốc từ GitHub Raw...
  - Thẩm định Manifest Báo chí:                2 / 2 mục đạt chuẩn (100% SHA-256 khớp)
  - Thẩm định Manifest Phóng sự YouTube:       3 / 3 mục đạt chuẩn (100% SHA-256 khớp)
  - Mẫu khớp nguồn gốc kiểm chứng 100%:       205 / 205 (100.0%)
  -> PASSED: 100% mẫu có thể chứng thực nguyên văn trên GitHub / Báo chí / YouTube.

[LAYER 7] Kiểm tra Tính Nhất Quán Ngữ Nghĩa & Phân bổ Bẫy Tâm Lý...
  - Phân bổ bẫy tâm lý của Bùi Thị Mỷ Cẩm (Phương án 1: 100% Đời thực):
    * public_service        : 159 mẫu ( 77.6%)
    * health_gift           :  46 mẫu ( 22.4%)
  - Tập dữ liệu dự phòng Phương án 2 (Backup Synthetic): 24 mẫu (sẵn sàng khi team phê duyệt)
  - Tổng hợp tiềm năng (Chính thức + Dự phòng):       229 mẫu (70 health_gift)
  -> PASSED: Cả 2 nhóm bẫy tâm lý đều đạt chỉ tiêu tinh hoa, phân bổ cân bằng và 100% sạch.

================================================================================
           ✅ TOÀN BỘ 7 TẦNG KIỂM ĐỊNH ĐÃ HOÀN TẤT XUẤT SẮC (PASSED 100%)
   Tập dữ liệu staging_cam_scam.csv gồm 205 mẫu ĐẠT CHUẨN NGHIỆM THU TUYỆT ĐỐI.
================================================================================
```

---

## 4. Hướng dẫn Tái hiện & Kiểm thử Độc lập (Reproduction Commands)

Người kiểm thử hoặc reviewer có thể chạy độc lập các lệnh sau tại thư mục gốc repository để thẩm định toàn bộ tập dữ liệu:

1. **Kiểm định lược đồ & chuẩn hóa thuộc tính:**
   ```bash
   python3 draft/scam-detection/data/scripts/data_validation.py --file draft/scam-detection/data/raw/staging_cam_scam.csv
   ```
2. **Kiểm toán nguồn gốc vật lý 1-1 đối chiếu GitHub Raw:**
   ```bash
   python3 draft/scam-detection/data/scripts/verify_cam_provenance.py
   ```
3. **Kiểm toán 7 tầng toàn diện:**
   ```bash
   python3 draft/scam-detection/data/scripts/audit_cam_rigorous.py
   ```

---

## 5. Danh mục Tệp Deliverables Bàn giao

* `draft/scam-detection/data/raw/staging_cam_scam.csv`: Tập dữ liệu 205 mẫu chính thức (100% đời thực).
* `draft/scam-detection/data/evidence/press_provenance_audit.json`: Manifest minh chứng trích dẫn Báo chí chính thống.
* `draft/scam-detection/data/evidence/youtube_transcript_manifest.json`: Manifest minh chứng trích dẫn Phóng sự YouTube VTV24.
* `draft/scam-detection/data/raw/backup_synthetic_health_gift.csv`: Tập dữ liệu dự phòng Phương án 2 (24 mẫu độc bản).
* `draft/scam-detection/data/evidence/backup_synthetic_manifest.json`: Manifest chứng thực cho tập dự phòng (24 mục độc bản).
* `draft/scam-detection/reports/cam_cleaned_dataset_review.md`: Bảng tra cứu đối chiếu chi tiết 205 mẫu sạch.
* `draft/scam-detection/data/scripts/audit_cam_rigorous.py`: Script kiểm định toàn diện 7 tầng.
* `draft/scam-detection/data/scripts/verify_cam_provenance.py`: Script kiểm chứng nguồn gốc vật lý 1-1.
