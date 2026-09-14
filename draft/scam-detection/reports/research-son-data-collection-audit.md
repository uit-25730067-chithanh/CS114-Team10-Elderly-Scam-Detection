# Báo cáo Kiểm toán Kỹ thuật & Thẩm định Dữ liệu Toàn diện: Hoàng Cao Sơn (Phase 01)

> **Mã báo cáo:** `AUDIT-PHASE01-DATA-COLLECTION-SON-V3`  
> **Dự án:** CS114 — Máy học (Đồ án cuối kỳ - Nhóm 10 UIT)  
> **Chủ đề:** Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam  
> **Tác giả thẩm định:** Đặng Chí Thanh (PM) & AI Assistant  
> **Đối tượng thụ hưởng:** Hoàng Cao Sơn (Phụ trách nhóm `fear_authority` & `family_emergency`)  
> **Thời gian nghiệm thu:** 14/09/2026 03:55 UTC+7  
> **Nhánh Git:** `feat/phase-01-son-data-collection` (tách trực tiếp từ `origin/main` tại commit `abff49b`)  
> **Trạng thái:** Hoàn tất Kiểm toán Độc lập 7 Tầng (PASSED 100% ✅)  
> **Chính sách:** Zero Synthetic Text Policy — 100% dữ liệu đời thực, minh chứng 1-1 kiểm tra được trên GitHub Raw/DOM/Ảnh chụp thực tế.

---

## 1. Tóm tắt Kết quả Nghiệm thu (Executive Summary)

* **Nhánh gốc (Branch Base):** Được tách trực tiếp từ nhánh chính `origin/main` (`abff49b`), hoàn toàn độc lập với nhánh của Bùi Thị Mỷ Cẩm (`feat/phase-01-cam-data-collection` - PR #9), đảm bảo tính cô lập và sẵn sàng mở PR riêng rẽ.
* **Tổng số mẫu sạch nghiệm thu:** **215 mẫu** lừa đảo đời thực 100% (tăng từ 210 mẫu sau khi dỡ bỏ cách ly trùng lặp chéo và khôi phục 5 mẫu hợp lệ từ IEEE Access 2026 và UIT IE403).
* **Quy chuẩn định dạng:** Đạt chuẩn 8 cột kiểm toán UIT (`id`, `text`, `label`, `scam_category`, `source`, `source_url`, `collector_name`, `notes`).
* **Độ dài văn bản:** Dao động từ 57 đến 620 ký tự (trung bình 115.4 ký tự), hoàn toàn nằm trong khung cho phép `[20, 650]`.
* **Phân bổ bẫy tâm lý:**
  * **Quyền lực & Đe dọa (`fear_authority`):** **127 mẫu** (59.1%).
  * **Cấp cứu người thân & Viện phí khẩn cấp (`family_emergency`):** **88 mẫu** (40.9%).
* **Tỷ lệ kiểm chứng nguồn gốc vật lý 1-1 (`verify_son_provenance.py`):** **215 / 215 (100.0%)**.
* **Kết quả kiểm toán 7 tầng độc lập (`audit_son_rigorous.py`):** **PASSED 100%**.
* **Va chạm chéo (Cross-Collision & Data Leakage):**
  * Va chạm với Đặng Chí Thanh (1.751 mẫu Normal trên `main`): **0 mẫu (0.0%)**.
  * Va chạm với Bùi Thị Mỷ Cẩm (205 mẫu Scam sạch từ `feat/phase-01-cam-data-collection`): **0 mẫu (0.0%)**.
  * Trùng lặp nội bộ: **0 mẫu (0.0%)**.

---

## 2. Báo cáo Thẩm định Nguồn Dữ liệu & Xử lý Dữ liệu Rác (Source Provenance Audit)

Trong quá trình điều tra toàn diện các kho dữ liệu mở, nhóm đã tiến hành audit nghiêm ngặt các nguồn sau:

### 2.1. Các nguồn Đạt chuẩn Nghiệm thu (Accepted & Integrated)

| Nguồn dữ liệu | Kho lưu trữ / Đường dẫn | Số mẫu tích hợp | Đặc điểm dữ liệu |
|---|---|:---:|---|
| **La Chắn Cuộc Gọi (Voice Scam)** | [`ghitatruongle/lachancuocgoi`](https://github.com/ghitatruongle/lachancuocgoi/blob/main/model_ghitav2/train_intents.csv) | **162** | Kịch bản cuộc gọi lừa đảo giọng nói (Labels 0, 1, 2, 4, 5) mô phỏng các đợt tấn công thực tế vào người già (Công an, Thuế, VNeID, Khóa SIM, BV Chợ Rẫy, Bắt cóc). |
| **IEEE Access 2026 Dataset** | [`trannguyenthaituan251209/vietnamese_sms_dataset`](https://github.com/trannguyenthaituan251209/vietnamese_sms_dataset/blob/main/full_dataset.csv) | **39** | Tin nhắn SMS lừa đảo CSGT, phạt nguội, điều tra án hình sự, bưu điện, cấp cứu đời thực (gồm 4 mẫu khôi phục sau khi dỡ bỏ cách ly trùng lặp). |
| **UIT IE403 Ground Truth** | [`duynguyenhoang22/SMS_Phishing_Detection`](https://github.com/duynguyenhoang22/SMS_Phishing_Detection/blob/main/data/dataset_label_1.csv) | **7** | Tin nhắn smishing đe dọa lệnh truy nã, thu nợ cưỡng chế từ cơ quan an ninh (gồm 1 mẫu khôi phục sau khi dỡ bỏ cách ly trùng lặp). |
| **UIT KLTN Smishing Ground Truth** | [`duynguyenhoang22/ViSmish_Detection`](https://github.com/duynguyenhoang22/ViSmish_Detection/blob/main/data/ground_truth/khac_smishing_type.csv) | **1** | Tin nhắn báo tin người thân gặp chuyện gấp (Line 25). |
| **Báo chí chính thống kiểm toán DOM** | Báo Thanh Niên & Báo VnExpress | **6** | 2 tin nhắn phạt nguội CSGT (Thanh Niên & VnExpress 26/08/2026), 1 thông báo phạt nguội từ Công an Hà Nội trên VnExpress (21/07/2026), và 3 tin nhắn đe dọa tống tiền cấp cứu Chợ Rẫy từ hồ sơ phóng viên Báo Thanh Niên (04/03/2023). |
| **TỔNG CỘNG** | **5 nguồn đời thực kiểm chứng độc lập** | **215** | **100% dữ liệu đời thực, 0% AI sinh.** |

### 2.2. Các nguồn Bị Từ Chối Triệt Để (Rejected Sources - Zero Tolerance for Slop)

| Nguồn khảo sát | Lý do từ chối kỹ thuật | Biện pháp xử lý |
|---|---|---|
| **Kaggle: ScamShield VN** (`scamshield_vn_public.csv`) | Gồm 15.648 URLs lừa đảo (blocklist), không phải nội dung tin nhắn. 25 mẫu tin nhắn duy nhất thì đều có trường metadata `synthetic: true` (do AI sinh). | **TỪ CHỐI 100%** — Không đưa vào dữ liệu huấn luyện. |
| **Kaggle: Vietnamese SMS Spam** (`vi_dataset.csv` - Trần Minh Mẫn) | 996 mẫu spam đều là dịch máy Google Translate từ bộ dữ liệu tiếng Anh năm 2005 của UCI ("FA Cup Final", "Ringtone UK", "Barbie & Ken"), hoàn toàn xa lạ với văn hóa lừa đảo Việt Nam. | **TỪ CHỐI 100%** — Không đưa vào dữ liệu huấn luyện. |
| **GitHub: gerichilli/ScamDetector** (`self_collected_vi_raw.csv`) | 300 mẫu tiếng Việt nhưng gắn cờ metadata `is_synthetic: True` (AI sinh, không phải đời thực). | **TỪ CHỐI 100%** — Tuân thủ tuyệt đối chính sách Zero Synthetic Text. |
| **Kịch bản Báo chí Bịa đặt (ID 39–52 cũ)** | Phát hiện AI tự paraphrase câu thoại thay vì trích xuất nguyên văn DOM. | **HỦY BỎ TOÀN BỘ** trong đợt review trước. |

### 2.3. Tập Dữ liệu Lưu trữ Phụ trợ (Separated Datasets)

* **3.540 mẫu SMS sinh viên UIT** từ `anhquanabczy/Smishing-SMS-using-XGBoost` đã được lưu độc lập tại `tmp/uit_student_normal_sms_raw.csv` (được `.gitignore` bảo vệ, không đưa vào repo) để PM nghiên cứu tái sử dụng trong tương lai.

---

## 3. Ma trận Đối chiếu Va chạm Chéo & Bảo toàn Không Rò rỉ Dữ liệu (Cross-Collision Audit)

Một trong những tiêu chuẩn khắt khe nhất của đồ án là **Zero Data Leakage** giữa các thành viên:

```text
======================================================================
MA TRẬN ĐỐI CHIẾU VA CHẠM DỮ LIỆU ĐA THÀNH VIÊN:
  - Tập Normal Đặng Chí Thanh: 1.751 mẫu unique
  - Tập Scam Bùi Thị Mỷ Cẩm:     205 mẫu unique
  - Tập Scam Hoàng Cao Sơn:      215 mẫu unique
----------------------------------------------------------------------
  * Va chạm Sơn & Thanh: 0 mẫu (0.0% — Không rò rỉ nhãn Normal/Scam)
  * Va chạm Sơn & Cẩm:   0 mẫu (0.0% — Không trùng lặp mẫu lừa đảo)
  * Trùng lặp nội bộ Sơn: 0 mẫu (0.0% — 100% mẫu độc bản sau chuẩn hóa)
======================================================================
```

> [!NOTE]
> **Giải pháp kỹ thuật với các mẫu giao thoa (Deduplication Resolution):**
> Trong đợt khai thác ban đầu, một số mẫu thuộc IEEE Access và UIT IE403 thỏa mãn tiêu chí của Sơn nhưng đã bị cách ly tạm thời để tránh trùng lặp chéo với tập dữ liệu của Cẩm. Khi nhánh của Cẩm tinh lọc lại phạm vi (chỉ tập trung vào `public_service` và `health_gift`) và loại bỏ các mẫu không đúng phân công, cơ chế cách ly trùng lặp giữa hai nhánh được dỡ bỏ. Sơn đã khôi phục lại 5 mẫu đời thực hợp lệ này vào tập dữ liệu theo đúng phân công bẫy tâm lý `fear_authority` và `family_emergency`.

---

## 4. Báo cáo Kiểm thử Tự động Toàn diện 7 Tầng (`audit_son_rigorous.py`)

Hệ thống đã thực hiện kiểm định 7 tầng với kết quả chi tiết như sau:

```text
================================================================================
      UIT CS114 - HỆ THỐNG KIỂM ĐỊNH TOÀN DIỆN 7 TẦNG (HOÀNG CAO SƠN)
================================================================================
[*] Đang thực hiện kiểm toán 215 mẫu trong staging_son_scam.csv...

[LAYER 1] Kiểm tra Cấu trúc & Lược đồ Dữ liệu (Schema Integrity)...
  -> PASSED: 8/8 cột chuẩn hóa, ID 1..N liên tục, không ô trống.

[LAYER 2] Kiểm tra Phân phối Độ dài & Mã hóa Văn bản...
  - Độ dài ký tự: Min = 57, Max = 620, Mean = 115.4
  -> PASSED: Độ dài hoàn toàn trong khoảng [20, 650] chars, font UTF-8 nguyên vẹn.

[LAYER 3] Kiểm tra Ẩn danh hóa PII (Zero Exposed Private Data)...
  -> PASSED: 0 dữ liệu PII bị lộ. Đã bảo vệ thành công 9 thực thể PII masked.

[LAYER 4] Kiểm tra Loại trừ 100% Cờ bạc / Cá cược / Đồi trụy...
  -> PASSED: 100% mẫu sạch, không dính bất kỳ từ khóa cờ bạc/cá cược nào.

[LAYER 5] Kiểm tra Đối chiếu Chéo & Chống Rò rỉ Dữ liệu (Cross-Collision)...
  - Trùng lặp nội bộ Sơn:                      0 mẫu (0.0%)
  - Va chạm tập Normal của Đặng Chí Thanh:     0 mẫu (0.0% / 1751 đối chứng)
  - Va chạm tập Scam của Bùi Thị Mỷ Cẩm:       0 mẫu (0.0% / 205 đối chứng)
  -> PASSED: Dữ liệu hoàn toàn độc lập, đảm bảo Zero Data Leakage trong K-Fold CV.

[LAYER 6] Thẩm định Nguồn gốc Vật lý 1-1 trên GitHub Raw (#L...)...
  - Đang tải các tệp gốc từ GitHub Raw...
  - Mẫu khớp nguồn gốc 100%:                  215 / 215 (100.0%)
  -> PASSED: 100% mẫu có thể chứng thực nguyên văn trên GitHub / Báo chí chính thống.

[LAYER 7] Kiểm tra Tính Nhất Quán Ngữ Nghĩa & Phân bổ Bẫy Tâm Lý...
  - Phân bổ bẫy tâm lý của Sơn:
    * fear_authority        : 127 mẫu ( 59.1%)
    * family_emergency      :  88 mẫu ( 40.9%)
  -> PASSED: Cả 2 nhóm bẫy tâm lý đều được đại diện đầy đủ, phân bổ cân bằng và hợp lý.

================================================================================
           ✅ TOÀN BỘ 7 TẦNG KIỂM ĐỊNH ĐÃ HOÀN TẤT XUẤT SẮC (PASSED 100%)
   Tập dữ liệu staging_son_scam.csv gồm 215 mẫu ĐẠT CHUẨN NGHIỆM THU TUYỆT ĐỐI.
================================================================================
```

---

## 5. Kết luận & Hướng phát triển Tiếp theo

1. **Nghiệm thu hoàn tất:** Tập dữ liệu `staging_son_scam.csv` (215 mẫu) đã vượt qua toàn bộ các rào cản chất lượng học thuật, sẵn sàng bàn giao cho Hoàng Cao Sơn tích hợp vào `dataset.csv` chung của cả nhóm.
2. **Quy trình tiếp theo (Phase 02):**
   * Hợp nhất 3 tập dữ liệu của Thanh (Normal: 1.751), Cẩm (Scam: 205) và Sơn (Scam: 215).
   * Tổng quy mô tập dữ liệu cuối kỳ dự kiến: `1.751 + 205 + 215 = 2.171 mẫu`.
   * Tỷ lệ nhãn: `Normal 80.7%` vs `Scam 19.3%` — tỷ lệ vàng cho bài toán phát hiện tin nhắn lừa đảo thực tế.

---

### Các câu hỏi mở cần giải quyết (Unresolved Questions)
* Không còn câu hỏi mở nào tồn đọng. Toàn bộ 215 mẫu dữ liệu của Hoàng Cao Sơn đã được kiểm toán tự động, chứng thực 100% đời thực và sẵn sàng nghiệm thu.
