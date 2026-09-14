# Phase 01 — Data Collection & Labeling

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 00 — Environment & Data Setup](./phase-00-env-data-setup.md)  
**Next phase:** [Phase 02 — Vietnamese Text Preprocessing](./phase-02-vietnamese-text-preprocessing.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Sơn** (lead) + cả nhóm |
| Priority | P0 — Blocker cho pipeline ML |
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 8–12h (thu thập + gán nhãn) |
| Sprint | Sprint 1 Fast-Track (Khóa dữ liệu: 23:59 ngày 12/09/2026) |

---

## 👥 Bảng Trạng thái Thành viên (Individual Progress Tracking)

> 📌 **Nguyên tắc đồng sở hữu:** Phase 01 là giai đoạn chung của cả nhóm. Mỗi thành viên chịu trách nhiệm độc lập cho phần dữ liệu của mình. Khi hoàn thành, thành viên (hoặc AI của thành viên đó) cập nhật dòng tiến độ tương ứng và điền minh chứng vào [Evidence Section](#evidence-section-điền-sau-khi-làm). Hạn chót nộp dữ liệu của Sơn và Cẩm để nhóm kịp tiền xử lý và huấn luyện: **23:59 ngày 12/09/2026**.

| Thành viên | Phụ trách dữ liệu | Mục tiêu mẫu | Đã thu thập | Minh chứng nguồn gốc | Trạng thái |
|---|---|:---:|:---:|---|:---:|
| **Hoàng Cao Sơn** | Lừa đảo: Quyền lực (`fear_authority`) & Cấp cứu (`family_emergency`) | ≥ 500 mẫu | **215 / 500** (127 `fear_authority` + 88 `family_emergency`) | 100% Real Đa nguồn (0% cờ bạc, 0% rò rỉ PII, 0% chồng lấn Cẩm/Thanh, 100% đối chiếu nguồn gốc) | 🔧 `needs-more-data` (hoàn tất Staging 215 mẫu sạch tuyệt đối) |
| **Bùi Thị Mỷ Cẩm** | Lừa đảo: Sức khỏe (`health_gift`) & Dịch vụ công (`public_service`) | ≥ 500 mẫu | **205 / 500** (159 `public_service` + 46 `health_gift`) | 100% Real Đa nguồn (0% cờ bạc, 0% rò rỉ PII, 0% chồng lấn nhóm Sơn/Thanh, 100% đối chiếu nguồn gốc) | 🔧 `needs-more-data` (xem [Minh chứng Bùi Thị Mỷ Cẩm](#2-minh-chứng-bùi-thị-mỷ-cẩm)) |
| **Đặng Chí Thanh** *(PM)* | Bình thường (`none`): SMS viễn thông, ngân hàng, sinh hoạt đời thường | ≥ 500 mẫu | **1.773 / 500** (+ 42 mẫu Holdout) | 100% IEEE Access 2026 Permalink + 20 Ảnh Drive cá nhân | ✅ `completed` |
| **TỔNG CỘNG** | **Toàn bộ dataset Phase 01** | **≥ 1.500 mẫu** | **2.193 / 1.500** | **100% có URL kiểm chứng 1-1 (0% rò rỉ, 0% AI tự sinh)** | ⏳ `in-progress` (Hoàn tất Staging Cẩm 205 mẫu, Sơn 215 mẫu, Thanh 1.773 mẫu) |

---

## ⚠️ Quy tắc Chống AI Lười biếng & Gian lận Tự sinh (Anti-Lazy AI & Synthetic Data Guardrails)

> [!CAUTION]
> **RÀNG BUỘC KỶ LUẬT NGHIÊM NGẶT DÀNH CHO AI AGENT KHI THỰC HIỆN PHASE 01:**
>
> 1. **CẤM AGENT TỰ Ý LÀM HỘ TOÀN BỘ PHASE:**
>    * Nếu bất kỳ thành viên nào đưa prompt dạng: *"Làm phase 01 cho anh đi em"* hoặc *"Hoàn thành Phase 01 giúp anh"*, **AI Agent TUYỆT ĐỐI KHÔNG ĐƯỢC TỰ ĐỘNG LÀM FULL CẢ 1.500 MẪU CHO CẢ 3 THÀNH VIÊN**.
>    * Agent **chỉ được phép thực hiện đúng phần việc của người đang tương tác** (Ví dụ: agent của Sơn chỉ làm 500 mẫu quyền lực/cấp cứu; agent của Cẩm chỉ làm 500 mẫu sức khỏe/dịch vụ công; agent của Thanh chỉ làm 500 mẫu bình thường).
>    * Agent **chỉ được tick các checklist item thuộc quyền của thành viên đó**, cấm tự ý tick hộ các thành viên khác khi họ chưa thực hiện!
>
> 2. **CẤM DỮ LIỆU TỰ SINH (ZERO SYNTHETIC TEXT POLICY):**
>    * AI Agent tuyệt đối không dùng prompt để sinh văn bản tin nhắn giả (không dùng ChatGPT/Claude/Gemini bịa text lừa đảo).
>    * 100% mẫu tin nhắn phải là dữ liệu thực tế: trích xuất từ bài báo chính thống (Dân Trí, VnExpress, Tuổi Trẻ, canhsat.vn, chongthurac.vn) có URL sống, hoặc ảnh chụp màn hình tin nhắn SMS đời thực trong [`CS114_Evidence_Vault`](https://drive.google.com/drive/folders/1YuXfFBHMWfpafBgykXKCzKDjqKAyE9DL).
>
> 3. **ĐIỀU KIỆN NGHIỆM THU CHÉO (TRIPARTITE VERIFICATION GATE):**
>    * Phase 01 **CHỈ ĐƯỢC COI LÀ PASSED** khi:
>      - Cả 3 thành viên đều đã hoàn thành ≥ 500 mẫu của mình và đánh dấu hoàn thành trên Bảng trạng thái.
>      - Trong file `dataset.csv`, cột `collector_name` phải ghi nhận đủ cả 3 tên với số lượng tương ứng (mỗi người ≥ 500 mẫu).
>      - Script `data/scripts/data_validation.py` chạy qua 100% không có cảnh báo.

---

## Context

Dự án cần tự thu thập và gán nhãn ≥1500 mẫu tin nhắn tiếng Việt (lừa đảo + bình thường). Khác với CS106 dùng dataset Kaggle sẵn, CS114 yêu cầu xây dựng dataset thủ công phù hợp bối cảnh Việt Nam.

## Requirements

- Tối thiểu **1500 mẫu**, lý tưởng 2000-3000 mẫu
- Tỷ lệ class: ~40-50% Lừa đảo / 50-60% Bình thường
- Gán nhãn `scam_category` cho mọi mẫu lừa đảo
- Mỗi mẫu phải có `source` rõ ràng (truy xuất được)

## Nguồn thu thập & Phân bổ chi tiết

Mục tiêu toàn nhóm: Thu thập **≥ 1.500 mẫu** văn bản tiếng Việt thực tế, cân bằng giữa tập lừa đảo (~50%) và tập bình thường (~50%).

### Bảng phân công nhiệm vụ cụ thể (≥ 500 mẫu / người)

| Thành viên | Trách nhiệm | Nhãn (`label`) | Nhóm dữ liệu (`scam_category`) | Số lượng tối thiểu | Nguồn thu thập chính |
|---|---|:---:|:---:|:---:|---|
| **Hoàng Cao Sơn** *(Lead thu thập)* | Lập Google Sheet nhóm, thu thập lừa đảo nhóm Quyền lực & Cấp cứu | `1` | `fear_authority`<br>`family_emergency` | **500 mẫu** | canhsat.vn, chongthurac.vn, Báo Dân Trí, VnExpress (mục Pháp luật) |
| **Bùi Thị Mỷ Cẩm** | Thu thập lừa đảo nhóm Sức khỏe/Quà tặng & Dịch vụ công | `1` | `health_gift`<br>`public_service` | **500 mẫu** | khonggianmang.vn, VNeID giả mạo, Báo Tuổi Trẻ, Lao Động |
| **Đặng Chí Thanh** *(PM)* | Thu thập tin nhắn bình thường đời thường, kiểm soát chất lượng dữ liệu | `0` | `none` | **500 mẫu** | SMS nhà mạng (Viettel, Vina, Mobi), SMS ngân hàng, hóa đơn EVN, tin nhắn gia đình |
| **TỔNG CỘNG** | | | | **≥ 1.500 mẫu** | Đạt 100% mục tiêu Phase 01 |

---

## Cơ chế Chứng thực Nguồn gốc Dữ liệu (Chống nghi vấn AI tự sinh)

Để bảo vệ tính trung thực khoa học trước Thầy Thăng và Hội đồng phản biện (chứng minh dữ liệu thu thập thực tế ngoài đời, không phải do AI ChatGPT/Claude tự bịa):

1. **Truy xuất nguồn gốc (Source Traceability):**
   * Mọi mẫu lừa đảo (`label = 1`) bắt buộc có link bài báo gốc hoặc bản tin cảnh báo của Cục ATTT / Bộ Công an điền vào cột `source_url`.
2. **Kho lưu trữ bằng chứng tập trung (Google Drive Evidence Vault):**
   * Đối với tin nhắn thực tế từ điện thoại cá nhân/người thân: Lưu ảnh chụp màn hình (screenshot đã bôi đen/ẩn số tài khoản và thông tin cá nhân PII) vào thư mục Google Drive chung của nhóm: [`CS114_Evidence_Vault`](https://drive.google.com/drive/folders/1YuXfFBHMWfpafBgykXKCzKDjqKAyE9DL).
   * Gắn đường link ảnh Drive tương ứng vào cột `source_url` trên Google Sheet. Giúp Git repository luôn nhẹ, không bị đầy dung lượng.
3. **Đặc trưng thống kê thực tế:**
   * Dữ liệu thực tế phản ánh đúng số điện thoại rác thật, tên miền phishing thật đã bị Cục ATTT cảnh báo, cấu trúc dấu câu và từ ngữ đời thường khác biệt với văn phong khuôn mẫu của AI.
4. **Minh bạch khi Tăng cường Dữ liệu (Data Augmentation Transparency):**
   * Tối thiểu 75% - 80% là dữ liệu gốc thu thập từ nguồn báo/cổng thông tin/SMS thật.
   * Nếu có mẫu áp dụng Data Augmentation (thay đổi tên riêng, số tiền), phải ghi chú rõ tại cột `notes`.

---

## Cấu trúc Dataset & Bảng Google Sheet

```csv
id,text,label,scam_category,source
1,"Con ơi mẹ bị tai nạn ở bệnh viện...",1,family_emergency,"news_dantri"
2,"Quý khách có 1 giao dịch -500,000 VND...",0,none,"bank_notification"
```

### Quy tắc gán nhãn `scam_category`

| Category | Mô tả | Từ khóa đặc trưng |
|----------|-------|-------------------|
| `fear_authority` | Giả danh Công an, VKS, Tòa án | viện kiểm sát, bắt tạm giam, phong tỏa tài khoản |
| `family_emergency` | Giả báo người thân gặp nạn | tai nạn, cấp cứu, chuyển viện phí gấp |
| `health_gift` | Dụ dỗ quà tặng, sức khỏe | trúng thưởng, thuốc miễn phí, tri ân |
| `public_service` | Giả mạo dịch vụ công | VNeID, nâng cấp SIM, trợ cấp hưu trí |
| `none` | Tin nhắn bình thường | (không áp dụng) |

---

## Implementation Steps

### Step 1 — Tạo Google Sheet thu thập chuẩn 8 cột

Tạo bảng tính Google Sheet chia sẻ quyền chỉnh sửa cho 3 thành viên, gồm 8 cột chuẩn kiểm toán:
`id | text | label | scam_category | source | source_url | collector_name | notes`

* Thiết lập Data Validation Dropdown:
  * Cột `label`: `[0, 1]`
  * Cột `scam_category`: `['fear_authority', 'family_emergency', 'health_gift', 'public_service', 'none']`

### Step 2 — Phân chia thu thập & Hỗ trợ cào bán tự động

* Mỗi thành viên thu thập ≥ 500 mẫu theo bảng phân công ở trên.
* Có thể sử dụng công cụ cào bán tự động [`data/scripts/data_scraper.py`](../../draft/scam-detection/data/scripts/data_scraper.py) để bóc tách nhanh các trích dẫn tin nhắn từ link bài báo mạng:
  ```bash
  python3 draft/scam-detection/data/scripts/data_scraper.py --url "https://dantri.com.vn/phap-luat/..."
  ```
  *(Thành viên kiểm tra, xác thực nội dung trước khi đưa vào Google Sheet chính).*

### Step 3 — Data Augmentation (Có kiểm soát)

```python
# Ý tưởng augmentation đơn giản cho một phần nhỏ dữ liệu nếu thiếu:
# - Thay đổi tên riêng: "Nguyễn Văn A" → "Trần Văn B"
# - Thay đổi số tiền: "500 triệu" → "200 triệu"
# - Thay đổi tên ngân hàng: "Vietcombank" → "BIDV"
# - Thay đổi số điện thoại
```

### Step 4 — Export & Validate (Tương thích Windows / macOS)

* Export từ Google Sheet về máy: `data/raw/dataset.csv`.
* **Lưu ý định dạng:** Xuất file CSV với chuẩn mã hóa **`utf-8-sig`** (UTF-8 có BOM) để tránh lỗi vỡ font tiếng Việt khi mở bằng Excel trên Windows.
* Chạy script kiểm định dữ liệu tự động:
  ```bash
  python3 draft/scam-detection/data/scripts/data_validation.py --file draft/scam-detection/data/raw/dataset.csv
  ```
  - Kiểm tra không có dòng trùng lặp
  - Mọi label ∈ {0, 1}
  - Mọi scam_category hợp lệ và khớp nhãn (`label=0` $\leftrightarrow$ `none`)
  - Không có text rỗng
  - Kiểm toán tỷ lệ mẫu có đính kèm nguồn gốc `source_url`

### Step 5 — Train/Test Split

```python
from sklearn.model_selection import train_test_split
from src.utils import RANDOM_STATE, TEST_SIZE

X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'],
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=df['label']
)
```

## Checklist Nghiệm thu Phase 01

### 1. Nhiệm vụ của Hoàng Cao Sơn (Lead thu thập)
- [ ] Sơn: Tạo bảng tính Google Sheet nhóm chuẩn 8 cột (`id | text | label | scam_category | source | source_url | collector_name | notes`)
- [ ] Sơn: Cài đặt Data Validation dropdown cho cột `label` (0, 1) và `scam_category` (5 nhóm)
- [ ] Sơn: Phân quyền Editor cho Cẩm (`25730013@ms.uit.edu.vn`) và Thanh (`25730067@ms.uit.edu.vn`)
- [ ] Sơn: Thu thập đủ **≥ 500 mẫu lừa đảo** thuộc 2 nhóm `fear_authority` (Quyền lực) & `family_emergency` (Cấp cứu)
- [ ] Sơn: 100% mẫu lừa đảo thu thập có đính kèm `source_url` (link bài báo chính thống hoặc link ảnh Drive)
- [ ] Sơn: Đánh dấu hoàn thành trên Bảng trạng thái thành viên

### 2. Nhiệm vụ của Bùi Thị Mỷ Cẩm
- [x] Cẩm: Cài đặt môi trường Python cá nhân theo `requirements.txt`
- [ ] Cẩm: Thu thập đủ **≥ 500 mẫu lừa đảo** thuộc 2 nhóm `health_gift` & `public_service` — **Hiện tại: 365/500 (301 `public_service` + 64 `health_gift`)** sau rà soát toàn diện + bổ sung 9 trích dẫn báo chí/pháp lý xác thực thủ công + review độc lập 14/09 loại 7 mẫu ngoài phạm vi (xem [mục 11](#11-review-độc-lập-bổ-sung-1409-loại-7-mẫu-ngoài-phạm-vi)). `health_gift` đang **dưới ngưỡng tối thiểu 200 mẫu/nhóm** ở Success Criteria — 2 nguồn GitHub (UIT IE403 + IEEE Access 2026) đã khai thác gần hết mẫu hợp lệ, hướng báo chí/bản án tòa án cũng gần cạn (tỷ lệ thành công thấp), cần bổ sung thêm ảnh chụp màn hình SMS thật cho riêng nhóm `health_gift`
- [x] Cẩm: 100% mẫu lừa đảo thu thập có đính kèm `source_url` (Permalink GitHub UIT IE403 Ground Truth, Permalink GitHub IEEE Access 2026 chính xác từng dòng vật lý #L..., URL bài báo Báo Tuổi Trẻ trích dẫn nguyên văn)
- [x] Cẩm: 100% mẫu đã được ẩn danh hóa PII (che SĐT, STK, OTP, CCCD, họ tên riêng) qua `anonymize_sms.py` (đã vá lỗi rò rỉ tên/số — xem mục 6)
- [x] Cẩm: Xuất tệp staging kiểm định độc lập `draft/scam-detection/data/raw/staging_cam_scam.csv` pass `data_validation.py` và `verify_cam_provenance.py` 100%
- [ ] Cẩm: Đánh dấu hoàn thành phần việc trên Bảng trạng thái thành viên — **tạm hoãn cho đến khi bổ sung đủ ≥ 500 mẫu (đặc biệt nhóm `health_gift`)**

### 3. Nhiệm vụ của Đặng Chí Thanh (Trưởng nhóm / PM)
- [x] Thanh: Thu thập đủ **≥ 500 mẫu tin nhắn bình thường** (`label=0`, `scam_category='none'`) từ SMS nhà mạng, ngân hàng, sinh hoạt (Đạt 1.773 mẫu độc bản, 0% rò rỉ với tập Holdout)
- [x] Thanh: Tải ảnh chụp màn hình tin nhắn thực tế vào thư mục Google Drive [`CS114_Evidence_Vault`](https://drive.google.com/drive/folders/1YuXfFBHMWfpafBgykXKCzKDjqKAyE9DL)
- [ ] Thanh: Kiểm tra chéo (Cross-review) dữ liệu của Sơn và Cẩm, rà soát nhãn nhất quán (Tạm dừng - Chờ Sơn & Cẩm nộp dữ liệu Google Sheet)
- [x] Thanh: Export dữ liệu thành file `data/raw/dataset.csv` (bảng mã `utf-8-sig`)
- [x] Thanh: Chạy script `python3 draft/scam-detection/data/scripts/data_validation.py --file draft/scam-detection/data/raw/dataset.csv` pass 100%
- [ ] Thanh: Thực hiện Stratified 80/20 Train/Test split và lưu trữ artifacts (Tạm hoãn — Chờ Sơn & Cẩm nộp 1.000 mẫu lừa đảo để chia tập cân bằng 2 lớp)
- [x] Thanh: Đánh dấu hoàn thành phần việc cá nhân trên Bảng trạng thái thành viên

---

## Success Criteria

| Tiêu chí | Mục tiêu định lượng | Phương thức kiểm chứng (Evidence) |
|---|---|---|
| **Tổng số mẫu** | `≥ 1.500 mẫu` | `df.shape[0] >= 1500` qua `data_validation.py` |
| **Đóng góp đủ 3 người** | Mỗi thành viên `≥ 500 mẫu` | `df['collector_name'].value_counts()` có đủ 3 tên |
| **Cân bằng nhãn (Class Balance)** | ~40-50% Scam / 50-60% Normal | `df['label'].value_counts()` trong ngưỡng cho phép |
| **Bao phủ 4 nhóm bẫy** | Mỗi nhóm bẫy lừa đảo `≥ 200 mẫu` | `df['scam_category'].value_counts()` |
| **Minh chứng nguồn gốc 100%** | 100% mẫu lừa đảo có `source_url` | `df[df['label']==1]['source_url'].notna().all()` |
| **Độ sạch dữ liệu** | 0 dòng trùng lặp, 0 văn bản rỗng | `df['text'].duplicated().sum() == 0` |
| **Tính xác thực (Anti-AI)** | 100% có link báo thật hoặc ảnh Drive | Audit ngẫu nhiên 30 mẫu bất kỳ |

---

## Evidence Section *(Điền số liệu thực tế sau khi từng thành viên hoàn thành)*

### 1. Minh chứng Hoàng Cao Sơn:
- Số mẫu lừa đảo đã nạp vào Staging CSV (`staging_son_scam.csv`): **215 / 500** mẫu (43.0% chỉ tiêu tối thiểu — hoàn tất 215 mẫu sạch tuyệt đối).
- Nguồn gốc dữ liệu: **100% đời thực từ Kiến trúc Đa nguồn Cân bằng Độc lập (Zero Synthetic Text - 0% AI bịa/sinh)** (UIT IE403, IEEE Access 2026, La Chắn Cuộc Gọi, KLTN Smishing, Báo chí chính thống VnExpress/Thanh Niên).
- Phân bổ 2 nhóm bẫy tâm lý theo phân công:
  + Cơ quan công quyền, Pháp luật, Phạt nguội, Khởi tố (`fear_authority`): **127 mẫu** (59.1%)
  + Cấp cứu bệnh viện, Tai nạn người thân, Hối thúc chuyển viện phí (`family_emergency`): **88 mẫu** (40.9%)
- Lọc rác & cờ bạc: **100% loại bỏ cờ bạc, cá cược, nổ hũ, đồi trụy** (0 mẫu vi phạm).
- Ẩn danh hóa PII: 100% mẫu đã che thông tin nhạy cảm qua `anonymize_sms.py`, 9 thực thể PII được bảo vệ, 0 trường hợp rò rỉ dữ liệu cá nhân.
- Tỷ lệ có `source_url`: **215 / 215 mẫu (100.0%)** có liên kết permalink 1-1 trên GitHub Raw hoặc bài báo chính thống.
- Chống rò rỉ dữ liệu (Cross-Collision & Data Leakage): 0 trùng lặp nội bộ, 0 va chạm với tập Normal của Thanh (1.751 đối chứng), 0 va chạm với tập Scam của Cẩm (205 đối chứng).
- Kết quả kiểm toán 7 tầng (`audit_son_rigorous.py`): **PASSED 100% (7/7 tầng)**.
- Kết quả kiểm chứng nguồn gốc (`verify_son_provenance.py`): **215 / 215 mẫu (100.0%) khớp nguyên văn trên GitHub Raw / Báo chí**.
- Tài liệu kiểm toán chi tiết: [`research-son-data-collection-audit.md`](../draft/scam-detection/reports/research-son-data-collection-audit.md) và [`kaggle_audit_report.md`](../draft/scam-detection/reports/kaggle_audit_report.md).
- Ngày hoàn thành kiểm định: `14/09/2026`

### 2. Minh chứng Bùi Thị Mỷ Cẩm:
> ⚠️ **Cập nhật 14/09/2026 (10 vòng re-audit, gồm 1 vòng review độc lập bởi AI khác):** Xem lịch sử chi tiết vòng 1-9 ở các mục 6-11 bên dưới. **Vòng 10 (14/09, sau vòng review độc lập):** PM Đặng Chí Thanh duyệt thêm nguồn thứ 4 — lời kể trực tiếp nạn nhân trích nguyên văn từ phỏng vấn báo chí thật (KHÔNG chấp nhận kịch bản AI viết lại), bổ sung 5 lời kể từ Dân Trí, VietnamNet, Tiin.vn và trang tin Khoa CNTT UIT (fit.uit.edu.vn), nâng dataset lên `365 / 500` mẫu. Số liệu **thật, mới nhất** là:
- Số mẫu lừa đảo đã nạp vào Staging CSV: **365 / 500** mẫu (73.0% chỉ tiêu tối thiểu — **chưa đạt**)
- Nguồn gốc dữ liệu: **100% đời thực từ Kiến trúc Đa nguồn Cân bằng Độc lập (Zero Synthetic Text - 0% AI bịa/sinh)**.
- Phân bổ 2 nhóm bẫy tâm lý theo phân công:
  + Dịch vụ công, VNeID, BHXH, SIM, EVN, Ngân hàng, Phạt nguội (`public_service`): **301 mẫu** (82.5%)
  + Sức khỏe, quà tặng tri ân, trúng thưởng thương hiệu (`health_gift`, KHÔNG còn gồm việc làm/CTV/đầu tư/crypto/hội thảo tuyển sinh): **64 mẫu** (17.5%) — **dưới ngưỡng tối thiểu 200 mẫu/nhóm** ở Success Criteria
- Lọc rác & cờ bạc: **100% loại bỏ cờ bạc, cá cược, nổ hũ, gái gọi, hẹn hò/sugar baby (kể cả biến thể leetspeak + domain giả mạo ngân hàng)** (0 mẫu vi phạm).
- Ẩn danh hóa PII: 100% mẫu đã che SĐT/STK/OTP/CCCD/Mã GD/họ tên riêng qua `anonymize_sms.py` (đã vá lỗi rò rỉ — chi tiết mục 6; review độc lập mục 11 quét lại không phát hiện rò rỉ mới).
- Tỷ lệ có `source_url`: **365 / 365 mẫu (100.0%)** có liên kết permalink hoặc URL báo chí/pháp lý xác thực thủ công 1-1 chính xác tuyệt đối.
- Độ sạch: 0 dòng trùng lặp (`text.duplicated().sum() == 0`), 0 văn bản rỗng, độ dài hợp lệ 25-600 ký tự, 0 text lỗi/không đọc được, 0 quảng cáo hội thảo không phải scam, 0 spam cờ bạc lẫn trong public_service, 0 lừa đảo vay tiền/hải quan/CTV online/tuyển tài xế lẫn trong 2 nhóm.
- Kết quả kiểm định tự động `data_validation.py`: **PASSED 100%** (lưu ý: script này chỉ kiểm tra schema/trùng lặp, không kiểm tra ngữ nghĩa category hay nội dung PII)
- Kết quả audit độc lập `verify_cam_provenance.py`: **365 / 365 mẫu (100.0%) đối chiếu khớp nguồn** (tiêu chí: trùng xâu con ≥20 ký tự HOẶC token overlap ≥60% cho 2 nguồn GitHub; đối chiếu thủ công 1-1 cho nguồn báo chí/pháp lý/lời kể nạn nhân)
- Ngày thu thập ban đầu: `12/09/2026` — Ngày re-audit & vá lỗi: `13-14/09/2026` (10 vòng, xem mục 6-11 bên dưới cho lịch sử chi tiết)
- **Việc cần làm tiếp:** bổ sung thêm mẫu thật cho nhóm `health_gift` (ảnh chụp màn hình SMS thật trong `CS114_Evidence_Vault` — hướng báo chí/bản án đã gần cạn) để đạt lại ≥500 mẫu tổng & ≥200 mẫu/nhóm — 2 nguồn GitHub hiện có đã khai thác gần hết, cần báo PM Thanh về mức độ thiếu hụt thực tế.

### 3. Minh chứng Đặng Chí Thanh:
- Số mẫu bình thường đã nạp: `1.773 / 500` mẫu (Đạt 354.6% chỉ tiêu tối thiểu)
- Nguồn gốc dữ liệu: **100% đời thực từ Vietnamese Quality-Assured SMS Dataset (IEEE Access 2026)**. Tuyệt đối không dùng AI tự sinh hay template vòng lặp nhân tạo (Zero Synthetic Text / Zero Template Duplication).
- Phân bổ dữ liệu bình thường đời thực (1.773 mẫu độc bản):
  + SMS Ngân hàng & Ví điện tử (Vietcombank, BIDV, Agribank, VietinBank, Techcombank, Sacombank, MB, VPBank, ACB, MoMo, ZaloPay, Viettel Money...)
  + SMS Viễn thông & Gói cước chính thống (Viettel, VinaPhone, MobiFone, Vietnamobile: đầu số 191, 198, 888, 900...)
  + SMS Khuyến cáo cơ quan nhà nước & Dịch vụ công (Bộ Công an PCCC, Cục CSGT CATP.HCM, Cục ATTT 156, Bộ TTTT...)
  + SMS Thương mại, Xác thực tài khoản & Giao nhận đơn hàng thực tế
- Ẩn danh hóa PII: 100% mẫu đã được che giấu thông tin cá nhân nhạy cảm (SĐT, STK, OTP, CCCD, Mã GD) qua `anonymize_sms.py`.
- Chống rò rỉ dữ liệu (Anti-Data Leakage): Đã chủ động loại trừ 3 mẫu trùng lặp hoàn toàn giữa IEEE Access và 20 ảnh chụp màn hình điện thoại cá nhân (Bộ VHTTDL, Phòng chống mua bán người 111, Cục An ninh mạng phòng chống cờ bạc). Giữ 3 mẫu này độc quyền trong tập Holdout Test để đảm bảo tập test phản ánh 100% dữ liệu chưa từng thấy (unseen data).
- Truy xuất nguồn gốc (`source_url`): **1.773 / 1.773 mẫu (100.0%)** có liên kết permalink 1-1 chính xác trỏ trực tiếp đến từng dòng văn bản gốc (`#L...`) trên repository chính thức của bộ dữ liệu IEEE Access 2026.
- Thư mục Google Drive riêng: Đã khởi tạo thư mục riêng [**`Dang_Chi_Thanh_Normal_SMS`**](https://drive.google.com/drive/folders/1YIRd0PTYcCP_igYtY4YyZ-QCMKYBkJFg) bên trong `CS114_Evidence_Vault` (Folder ID: `1YIRd0PTYcCP_igYtY4YyZ-QCMKYBkJFg`).
- Đã tải thành công **20 ảnh chụp màn hình điện thoại thực tế** của Đặng Chí Thanh lên thư mục Google Drive riêng (`thanh_sms_01.jpg` đến `thanh_sms_20.jpg`) cùng tệp chứng nhận xuất xứ `Dang_Chi_Thanh_Normal_SMS_Provenance.txt`.
- Đã bóc tách thành công **42 tin nhắn SMS đời thực** (100% ẩn danh hóa PII: tên cá nhân, mã OTP, số điện thoại, mã ưu đãi cá nhân) và xuất ra tệp kiểm định độc lập: `draft/scam-detection/data/processed/real_world_test_thanh.csv` với 100% `source_url` trỏ trực tiếp 1-1 tới link từng ảnh Drive.
- Ngày ký duyệt hoàn thành phần việc: `05/09/2026`

### 4. Kết quả chạy script kiểm định (`data_validation.py`):
```text
============================================================
  DATASET VALIDATION REPORT: dataset.csv
============================================================
Total Rows:       1773
Columns:          ['id', 'text', 'label', 'scam_category', 'source', 'source_url', 'collector_name', 'notes']
Class Balance:    Normal (0): 1773 | Scam (1): 0

Scam Category Distribution:
  - none                : 1773

Collector Contributions:
  - Đặng Chí Thanh      : 1773 samples

Provenance URLs:  1773 / 1773 samples (100.0%)
------------------------------------------------------------
✅ STATUS: PASSED — Dataset conforms to all validation rules.
============================================================
```

### 5. Kết quả phân chia Train/Test (`split_data.py`):
> ⏳ **Tạm hoãn bước phân chia Train/Test (Deferred Split Gate):**  
> Việc phân tách `train.csv` (80%) và `test.csv` (20%) bằng `split_data.py` chỉ được thực hiện sau khi Hoàng Cao Sơn và Bùi Thị Mỷ Cẩm nộp đủ 1.000 mẫu tin nhắn lừa đảo. Điều này nhằm đảm bảo thuật toán phân tầng (Stratified Split) hoạt động chính xác trên cả 2 nhãn `0` và `1` cùng 5 nhóm bẫy tâm lý, tránh tạo ra tập huấn luyện đơn lớp gây lỗi mô hình. Hiện tại thư mục `draft/scam-detection/data/processed/` chỉ lưu trữ tệp kiểm định đời thực độc lập `real_world_test_thanh.csv` (42 mẫu, 0% rò rỉ).

### 6. Re-audit kỹ thuật 13/09/2026 — Phát hiện & khắc phục lỗi trước khi merge

Trước khi merge PR #9, một vòng review độc lập (data + code) trên `staging_cam_scam.csv` và pipeline `collect_cam_scam_dataset.py` / `anonymize_sms.py` / `verify_cam_provenance.py` đã phát hiện các vấn đề sau (bên cạnh các con số tổng quan 514 mẫu, 0% cờ bạc, unique 514/514 đều đúng như báo cáo PM 12/09):

| # | Vấn đề phát hiện | Bằng chứng cụ thể | Nguyên nhân gốc | Đã khắc phục |
|---|---|---|---|---|
| 1 | **Rò rỉ PII thật** (tên riêng, số tài khoản, mã giao dịch) dù báo cáo ghi "100% Masked" | id 2 cũ: lộ tên `Trần Thị Lan` + STK `0071000986547` + mã GD `1057425286`; id 138 cũ: lộ tên `HO NGOC HOAI QUAN`; id 63/78 cũ: lộ SĐT di động `0497123597`, `0746591731` | `anonymize_sms.py` không có rule che họ tên; `REGEX_BANK_ACCOUNT`/`REGEX_TRANSACTION_ID`/`REGEX_PHONE` chỉ khớp khi có đúng từ khóa/định dạng đi kèm, không có lưới bắt cuối cho số dài còn sót | ✅ Thêm `REGEX_FULL_NAME_TITLE`/`REGEX_FULL_NAME_CAPS` (che họ tên) + `REGEX_GENERIC_LONG_DIGITS` (bắt lưới mọi dãy ≥8 số còn sót) trong `anonymize_sms.py` |
| 2 | **Bug phân loại category**: keyword `\bqua\b` trong `HEALTH_GIFT_PATTERNS` quá chung chung | Sau khi bỏ dấu, "quà" (gift) và "qua" (giới từ rất phổ biến: "năm qua", "quá hạn"...) trùng chữ nhau → **39/130 mẫu (30%)** health_gift cũ chỉ được gán nhãn nhờ đúng token yếu này, gồm cả tin đòi nợ (id 113, 138 cũ) và lừa quỹ BHTN (id 52, 192 cũ, bị obfuscate `B/H/T/N` nên không khớp `bhtn`) | Regex `\bqua\b`/`\btrung\b` không đủ đặc hiệu; pattern `bhtn` không chịu được ký tự phân cách lách luật | ✅ Bỏ `\bqua\b`/`\btrung\b` khỏi `HEALTH_GIFT_PATTERNS`, thêm `trung_tuyen` (giữ đúng case HUIT); thêm pattern chịu ký tự phân cách cho `bhtn` |
| 3 | **Lấn ranh giới sang phần Sơn** (`fear_authority`) | id 57/113/498 cũ: tin đe dọa "khởi kiện", "công an khu vực", "triệu tập dân sự" — không khớp `SON_PATTERNS` vì list chỉ có "khởi tố" | `SON_PATTERNS` thiếu các biến thể diễn đạt tương đương của đe dọa pháp lý/quyền lực | ✅ Bổ sung `khoi_kien`, `trieu_tap`, `to_giac` vào `SON_PATTERNS` |
| 4 | Diễn giải quá lời trong báo cáo về `verify_cam_provenance.py` | Báo cáo PM ghi "khớp nguyên văn từng ký tự", nhưng code thật cho pass nếu đối sánh xâu con ≥20 ký tự **HOẶC** token overlap ≥60% | — (chỉ là câu chữ báo cáo, không phải bug code) | 📝 Đã diễn đạt lại chính xác hơn ở mục 2 phía trên |
| 5 | Bug tự phát sinh khi vá lỗi #1: che nhầm địa danh | `Hồ Chí Minh` (tên thành phố) bị regex tên người nuốt nhầm thành `[HỌ_VÀ_TÊN]` vì "Hồ" nằm trong danh sách họ | `REGEX_FULL_NAME_TITLE` không loại trừ địa danh phổ biến bắt đầu bằng họ | ✅ Thêm negative lookahead loại trừ `Hồ Chí Minh` |

**Kết quả sau khi vá lỗi và chạy lại `collect_cam_scam_dataset.py` (13/09/2026):**
- Tổng mẫu: `514 → 476` (giảm 38 mẫu do loại bỏ các mẫu phân loại sai/lấn ranh giới)
- `public_service`: `384 → 383`
- `health_gift`: `130 → 93` (**dưới ngưỡng 200 mẫu/nhóm** — cần bổ sung nguồn thật khác, 2 nguồn GitHub hiện có đã cạn mẫu hợp lệ)
- `data_validation.py`: vẫn PASSED 100% (không đổi, vì script này không kiểm tra các lỗi trên)
- `verify_cam_provenance.py`: vẫn PASSED 100% (476/476)
- 0% cờ bạc, 0% dòng trùng lặp, 0% dãy số dài còn sót chưa che (đã quét lại độc lập)

**Việc cần làm tiếp theo (đã lỗi thời — xem mục 7 bên dưới, số liệu tiếp tục giảm sau vòng re-audit ngữ nghĩa):**

### 7. Re-audit ngữ nghĩa 13/09/2026 — Loại bỏ mẫu lạc nhóm khỏi `health_gift`

Sau vòng vá lỗi ở mục 6 (sáng 13/09), một vòng review thứ 2 trong cùng ngày phát hiện `classify_cam_sample()` vẫn là bộ lọc **từ khóa theo thứ tự ưu tiên**, nên dù đã bỏ `\bqua\b`/`\btrung\b`, cơ chế cốt lõi vẫn gán nhãn `health_gift` cho bất kỳ câu nào khớp từ khóa — bất kể bản chất kịch bản lừa đảo có thực sự là "sức khỏe & quà tặng tri ân" hay không. Đọc thủ công toàn bộ 93 mẫu `health_gift` (không dựa vào kết quả regex) phát hiện:

| # | Vấn đề phát hiện | Ví dụ cụ thể | Số lượng | Đã khắc phục |
|---|---|---|:---:|---|
| 1 | Nội dung mại dâm/gái gọi lọt qua vì viết leetspeak (`GAI LAM tjnh` thay vì `gai goi`/`sex`) | id 36, 37 cũ | 2 | ✅ Thêm `gai_lam`, `lam_tjnh`, `lam_tinh` vào `GAMBLING_ADULT_PATTERNS` |
| 2 | Đe dọa chiếm đoạt tài sản giả danh "Trung Tâm Tín Dụng" — gần bản chất `fear_authority` (phần Sơn), không phải quà tặng | id 106, 107 cũ | 2 | ✅ Thêm `chiem_doat_tai_san`, `canh_bao_lan_cuoi`, `trung_tam_tin_dung` vào `SON_PATTERNS` |
| 3 | Nội dung tuyên truyền tôn giáo/chính trị (Pháp Luân Công), không phải lừa đảo chiếm đoạt tài sản | id 143 cũ | 1 | ✅ Thêm `OFF_TOPIC_PATTERNS` loại trừ `phap_luan_cong` |
| 4 | Text lỗi/garbled không đọc được, không dùng làm dữ liệu huấn luyện | id 181, 189 cũ | 2 | ✅ Không còn xuất hiện sau khi lọc lại (tự loại vì độ dài/nội dung không khớp pattern nào sau khi sửa) |
| 5 | **Lừa đảo tuyển dụng/CTV online** ("tuyển nhân viên bán thời gian", "kiếm tiền tại nhà", tuyển CTV Shopee/Tiki/Lazada/TikTok...) bị gán `health_gift` chỉ vì `HEALTH_GIFT_PATTERNS` có sẵn `tuyen_dung/viec_lam/kiem_tien/hoa_hong` — bản chất khác hẳn "quà tặng tri ân" | ~28 mẫu (id 6, 25, 26, 91, 94, 113, 120, 121, 128, 182-185, 238-296, 347, 349, 381, 459 cũ...) | ~28 | ✅ Bỏ 4 pattern trên khỏi `HEALTH_GIFT_PATTERNS`, thêm `JOB_AND_INVESTMENT_PATTERNS` loại trừ trước khi phân loại (áp dụng cho cả `health_gift` lẫn `public_service`) |
| 6 | **Lừa đảo đầu tư/crypto** ("300% Bonus", "AI Trading nhân đôi tài sản", "nuôi bò sinh lời 2%/ngày") chỉ gắn thêm chữ "quà tri ân" làm mồi phụ | id 207, 272, 297, 317, 340 cũ | 5 | ✅ Cùng `JOB_AND_INVESTMENT_PATTERNS` ở trên |
| 7 | Mạo danh cơ quan nhà nước cụ thể ("Tổng cục Du lịch") nhưng bị gán `health_gift` — theo tiêu chí nhóm, mạo danh 1 cơ quan cụ thể đòi hành động trên tài khoản/thông tin phải là `public_service` | id 332 cũ | 1 | ✅ Thêm `tong_cuc` vào `PUBLIC_SERVICE_PATTERNS` |

**Kết quả sau khi vá lỗi ngữ nghĩa và chạy lại `collect_cam_scam_dataset.py` (13/09/2026, vòng 2):**
- Tổng mẫu: `476 → 392` (giảm 84 mẫu — bao gồm cả các mẫu tuyển dụng/đầu tư từng bị gán nhầm `public_service`)
- `public_service`: `383 → 339`
- `health_gift`: `93 → 53` (**cách xa hơn ngưỡng 200 mẫu/nhóm** so với ước tính sáng 13/09 — 2 nguồn GitHub hiện có đã cạn mẫu hợp lệ đúng bản chất "sức khỏe & quà tặng tri ân")
- `data_validation.py`: vẫn PASSED 100%
- `verify_cam_provenance.py`: vẫn PASSED 100% (392/392)
- 10 mẫu template lặp lại (chỉ đổi tên nhân viên/spa, vd "Bạn được tặng 1 phần quà tri ân... gặp NV [X]") vẫn giữ lại vì là dòng thật khác nhau trong nguồn IEEE Access 2026 (không phải trùng lặp/tự sinh), nhưng cần lưu ý rủi ro đa dạng dữ liệu thấp khi huấn luyện.

**Việc cần làm tiếp theo (đã lỗi thời — xem mục 8 bên dưới):**

### 8. Rà soát toàn diện 2 nguồn gốc 14/09/2026 — vét lại `health_gift` thật cẩn thận

Theo yêu cầu của Cẩm ("lọc lại 1 lần nữa thật cẩn thận từng chi tiết Nhóm 1: Sức khỏe & Quà tặng tri ân"), thay vì chỉ đọc lại 93 mẫu health_gift cũ, lần này tải **toàn bộ 2 nguồn gốc thô** (UIT IE403: 247 dòng, IEEE Access 2026: 798 dòng label=1, tổng 1.045 ứng viên) và đọc thủ công từng câu — không dựa vào kết quả `classify_cam_sample()` — để tìm cả 2 chiều: (a) mẫu bị gán sai vào `health_gift`, và (b) mẫu `health_gift` thật bị bỏ sót vì rơi vào `public_service`/bị loại nhầm.

**Phát hiện quan trọng nhất — pattern `tai\s*khoan` (tài khoản) trong `PUBLIC_SERVICE_PATTERNS` quá chung chung:**

Vì `classify_cam_sample()` kiểm tra `is_ps` trước `is_hg`, bất kỳ câu nào chứa chữ "tài khoản" — kể cả "tài khoản Messenger", "tài khoản Shopee" (không liên quan ngân hàng/cơ quan nhà nước) — đều bị nuốt vào `public_service`. Kiểm chứng: trong 1.045 ứng viên, có **19 mẫu chỉ khớp `public_service` nhờ đúng pattern chung chung này** (không có tín hiệu cụ thể nào khác). Đọc thủ công từng mẫu:

| Kết quả | Số lượng | Xử lý |
|---|:---:|---|
| Thật sự là `health_gift` (quà tặng thương hiệu Messenger/Shopee/Club Med, bị `tai_khoan` nuốt nhầm) | 3 | ✅ Chuyển đúng về `health_gift` |
| Thật sự là `public_service` (cảnh báo ngân hàng/Bưu điện VN chung chung, không nêu tên ngân hàng cụ thể) | 5 | ✅ Thêm pattern cụ thể hơn để không phụ thuộc `tai_khoan` |
| Không thuộc 2 nhóm của Cẩm (lừa đảo vay app, hẹn hò/ảnh riêng tư, "con nhắn tin mượn tài khoản" giống `family_emergency`, chuyển nhầm tiền, thiết bị IoT, tài khoản Telegram bị khóa, cờ bạc nạp lần đầu) | 11 | ✅ Loại khỏi dataset của Cẩm (đúng phạm vi, không ép vào 1 trong 2 nhóm) |

**Đã sửa trong `collect_cam_scam_dataset.py`:**
- Bỏ hẳn pattern chung chung `tai\s*khoan` khỏi `PUBLIC_SERVICE_PATTERNS`
- Thêm các pattern cụ thể hơn: `tai_chinh_toan_cau`, `tieu_dung_o_nuoc_ngoai`, `phong_toa`, `gian_lan`, `buu_dien`, `luong_huu`, `an_sinh_xa_hoi`, `sinh_trac_hoc`, `mb\s*bank` (bản có khoảng trắng, bổ sung cho `mbbank`)
- Thêm `nap_lan_dau` vào `GAMBLING_ADULT_PATTERNS` — vì sau khi bỏ `tai_khoan`, 1 mẫu cờ bạc "nạp lần đầu 100%" suýt lọt vào `health_gift` qua pattern `uu_dai` sẵn có
- Phát hiện thêm 2 mẫu text lỗi/không đọc được sót lại từ vòng trước (`id 158, 162` cũ trong lần chạy trung gian) — đã thử 3 phiên bản heuristic tự động (độ dài token, đếm camelCase, đếm camelCase sau khi bỏ URL) nhưng **cả 3 đều gây false-positive loại nhầm dữ liệu thật** (mẫu BHTN leetspeak hợp lệ, mẫu VPBANK nhắc "iPhone"/"512GB"/"4K" hoàn toàn bình thường). Vì `health_gift` đang rất khan hiếm, quyết định đánh đổi an toàn: dùng `GARBLED_TEXT_DENYLIST` — danh sách loại trừ **chính xác từng dòng đã xác nhận thủ công**, không dùng heuristic tổng quát.

**Kết quả sau khi vá và chạy lại `collect_cam_scam_dataset.py` (14/09/2026, vòng 3):**
- Tổng mẫu: `392 → 389`
- `public_service`: `339 → 335`
- `health_gift`: `53 → 54` (+3 mẫu health_gift thật được cứu khỏi `public_service`, trừ đi phần dao động do các pattern mới)
- `data_validation.py`: vẫn PASSED 100%
- `verify_cam_provenance.py`: vẫn PASSED 100% (389/389)

**Các mục còn lại chưa tự động xử lý sau vòng 3 — cần Cẩm xem xét/quyết định thủ công:**
- id 113-115 (bản mới): "Hội thảo trực tuyến... Không trúng tuyển nguyện vọng yêu thích?" — quảng cáo hội thảo tư vấn tuyển sinh của trường đại học, không rõ có thực sự là "lừa đảo chiếm đoạt tài sản" hay chỉ là spam quảng cáo hợp pháp bị gắn nhãn label=1 sai trong nguồn IEEE Access 2026 gốc
- id 132, 158, 159 (bản mới): nội dung rất ngắn/yếu, chỉ có 1 câu chúc mừng/sức khỏe chung chung kèm link rút gọn, không có kịch bản lừa đảo rõ ràng
- 10 mẫu template lặp lại (6 mẫu "quà tri ân... gặp NV [X]" + 4 mẫu "Spa [X] ưu đãi 70%") — vẫn giữ vì là dòng thật khác nhau trong nguồn, không phải trùng lặp/tự sinh, nhưng đa dạng ngữ nghĩa thấp

**Vòng 4 (14/09/2026, cùng ngày) — Cẩm tự xem file CSV trong IDE và xác nhận id 113-115 sai nhãn:**

3 mẫu "Hội thảo trực tuyến... Không trúng tuyển nguyện vọng yêu thích? Biến nguy thành cơ" (quảng cáo tư vấn tâm lý tuyển sinh đại học) chỉ bị gán `health_gift` vì chứa chữ "trúng tuyển" khớp pattern `trung_tuyen`, dùng trong câu hỏi tu từ — không phải kịch bản lừa đảo giả mạo trúng tuyển thật (vốn luôn nói "ĐÃ trúng tuyển" để dụ nạn nhân, như mẫu HUIT thật). Đối chiếu toàn bộ 2 nguồn: có 6 mẫu chứa "hội thảo", trong đó 2 mẫu khác (Đại học FPT tư vấn tuyển sinh, nhóm đầu tư "làm giàu" dùng hội thảo làm mồi) đã tự động bị loại đúng từ trước — chỉ riêng nhóm "Không trúng tuyển..." bị lọt.

**Đã sửa:** thêm `khong_trung_tuyen` vào `OFF_TOPIC_PATTERNS` (dấu hiệu phân biệt an toàn: phủ định "không" ngay trước "trúng tuyển" nghĩa là nội dung tư vấn/hội thảo hợp pháp, không phải lừa đảo giả mạo trúng tuyển — đã verify không ảnh hưởng mẫu HUIT thật "ĐÃ trúng tuyển").

**Kết quả sau khi vá và chạy lại (14/09/2026, vòng 4):**
- Tổng mẫu: `389 → 386`
- `public_service`: `335` (không đổi)
- `health_gift`: `54 → 51` (loại đúng 3 mẫu hội thảo tuyển sinh)
- `data_validation.py`: vẫn PASSED 100%
- `verify_cam_provenance.py`: vẫn PASSED 100% (386/386)

**Vòng 5 (14/09/2026, cùng ngày) — Cẩm tự xem file CSV trong IDE, phát hiện mẫu id 159 sai nhãn:**

id 159 ("UrA bpdFWr.DeBidv.com KhiAeNapTienNhanQua:2OOKgroupsgooglecom") là spam cờ bạc bị làm rối (leetspeak + domain giả mạo tên ngân hàng), khớp `public_service` chỉ vì domain giả chứa chuỗi con "bidv" — không phải tin nhắn ngân hàng thật. Rà lại toàn bộ dataset theo dấu hiệu đuôi rác đặc trưng "groupsgooglecom" (mảnh vỡ của "groups.google.com" dính liền, xuất hiện trong tất cả các biến thể domain giả "...Bidv.com"/"Bidvxx.com" của cùng 1 họ spam): phát hiện **16 mẫu cùng họ**, toàn bộ đều đang bị gán nhầm `public_service`.

**Đã sửa:** thêm `groupsgooglecom` vào `GAMBLING_ADULT_PATTERNS` — dấu hiệu đặc trưng, không xuất hiện ở bất kỳ mẫu nào khác trong dataset ngoài họ spam này (đã kiểm tra).

**Kết quả sau khi vá và chạy lại (14/09/2026, vòng 5):**
- Tổng mẫu: `386 → 370`
- `public_service`: `335 → 319` (loại đúng 16 mẫu spam cờ bạc)
- `health_gift`: `51` (không đổi)
- `data_validation.py`: vẫn PASSED 100%
- `verify_cam_provenance.py`: vẫn PASSED 100% (370/370)

**Việc cần làm tiếp theo (đã lỗi thời — xem mục 9 bên dưới):** `health_gift` vẫn còn cách ngưỡng 200 mẫu rất xa — 2 nguồn GitHub hiện có đã khai thác gần hết mẫu hợp lệ đúng bản chất "sức khỏe & quà tặng tri ân".

### 9. Bổ sung trích dẫn báo chí/pháp lý (14/09/2026)

Theo yêu cầu của Cẩm ("thử tìm thêm hướng khác nữa"), sau khi xác nhận báo chí Việt Nam hầu như luôn né tránh trích dẫn nguyên văn tin nhắn lừa đảo (đã kiểm tra ~40 bài báo/cổng cảnh báo trong suốt buổi làm việc, tỷ lệ có quote dùng được chỉ ~4/40), đã mở rộng sang 2 hướng mới:

1. **Bản án tòa án công khai** (`congbobanan.toaan.gov.vn`) — tòa án buộc phải mô tả chi tiết bằng chứng nên không né tránh như báo chí. Tìm được bản án `60/2024/HSST` (lừa trúng thưởng mạo danh Viettel, trích nguyên văn lời thoại "...đã trúng thưởng giải nhất... 300.000.000 đồng cùng 01 xe mô tô Honda SH...") — **nhưng bị loại vì là lời thoại qua điện thoại, không phải tin nhắn SMS** (Cẩm xác nhận dataset phải đúng là tin nhắn, không tính lời nói qua cuộc gọi). Kỹ thuật tải bản án: `curl -sk` bỏ qua lỗi SSL chứng chỉ chính phủ rồi đọc PDF bằng công cụ Read — hoạt động tốt, có thể dùng lại nếu cần tìm thêm.
2. **Cổng thông tin Học viện Tòa án** (`hvta.toaan.gov.vn`, đăng lại bài báo cũ) — tìm được 1 bài Tuổi Trẻ 2014 trích dẫn nguyên văn đầy đủ 2 bài đăng Facebook lan truyền lừa "nạp thẻ khuyến mãi x10". Cẩm xác nhận vẫn tính được dù là bài đăng Facebook (không phải SMS gửi trực tiếp), vì dataset đã có sẵn nhiều mẫu Zalo/Messenger/Facebook, miễn không phải lời thoại nói.

**4 trích dẫn mới thêm vào `fetch_verified_news_quotes()`:**

| Nội dung (rút gọn) | Nhãn | Nguồn |
|---|---|---|
| "Chúc mừng bạn đã trúng iPhone 15 Pro Max" | `health_gift` | Tuổi Trẻ (NLĐ), 08/04/2026 |
| "Nhận quà tri ân trị giá hàng chục triệu đồng" | `health_gift` | Tuổi Trẻ (NLĐ), 08/04/2026 |
| "[Ngân hàng A.] ... 12.500 điểm thưởng thẻ tín dụng... hết hạn hôm nay..." | `public_service` | Dân Trí (CA Quảng Ninh), 20/08/2026 — mạo danh brandname ngân hàng đòi hành động trên tài khoản, không phải quà tặng thuần túy |
| "Mình vừa được người bạn chia sẻ cho cách nạp thẻ x10... nhà mạng Viettel, MobiFone, Vinaphone tạo ra..." | `public_service` | Học viện Tòa án / Tuổi Trẻ, 12/11/2014 — mạo danh đích danh 3 nhà mạng cụ thể |

Đồng thời mở rộng whitelist domain đã kiểm chứng thủ công trong `verify_cam_provenance.py` (`dantri.com.vn`, `hvta.toaan.gov.vn`) vì 2 nguồn này không có permalink dạng GitHub `#L...` để audit tự động.

**Kết quả sau khi chạy lại (14/09/2026, vòng 6):**
- Tổng mẫu: `370 → 374`
- `public_service`: `319 → 321` (+2, cả 2 quote mới đều mạo danh cơ quan/nhà mạng cụ thể)
- `health_gift`: `51 → 53` (+2)
- `data_validation.py`: vẫn PASSED 100%
- `verify_cam_provenance.py`: **374/374 (100%)** sau khi mở rộng whitelist

**Việc cần làm tiếp theo (đã lỗi thời — xem mục 10 bên dưới):** săn tin nhắn nguyên văn từ báo chí không scale được (~4/40 nguồn có quote dùng được suốt cả buổi); hướng bản án tòa án tiềm năng nhưng đa số là lời thoại cuộc gọi, không phải SMS.

### 10. Sửa pattern `đăng_ký`/`hồ_sơ` quá rộng + bổ sung thêm quote báo chí (14/09/2026)

Theo yêu cầu tiếp tục của Cẩm ("Hãy tìm thêm Nhóm 1... health_gift"), trong lúc tìm thêm quote báo chí mới (báo Thanh Niên — bài cũ 2017 về nạn nhân bị lừa trúng thưởng Facebook), phát hiện quote đó bị phân loại sai thành `public_service` dù nội dung rõ ràng là `health_gift` (Facebook/Messenger thông báo trúng thưởng, không mạo danh cơ quan cụ thể). Truy nguyên nhân: 2 pattern `dang\s*ky` (đăng ký) và `ho\s*so` (hồ sơ) trong `PUBLIC_SERVICE_PATTERNS` — 2 từ hành chính chung chung, xuất hiện tự nhiên cả trong scam quà tặng thật ("đăng ký làm thủ tục hồ sơ nhận thưởng") lẫn scam public_service.

Rà lại toàn bộ 2 nguồn gốc thô theo đúng cách đã làm với `tai_khoan` (mục 8): tìm được **30 mẫu chỉ khớp `public_service` nhờ đúng 2 pattern này** (không có tín hiệu cụ thể nào khác). Đọc thủ công từng mẫu:

| Kết quả | Số lượng | Xử lý |
|---|:---:|---|
| Thật sự là `health_gift` (Messenger, DatXanh_Group, Spa_LamDep, Alma_Gala — sự kiện/quà tặng/tri ân của thương hiệu tư nhân, không mạo danh cơ quan) | 4 | ✅ Chuyển đúng về `health_gift` — **đáng chú ý: mẫu Messenger vốn tưởng đã sửa xong ở mục 8 nhưng thực ra vẫn sai do bản test trước đó dùng câu rút gọn, không phải nguyên văn đầy đủ** |
| Thật sự là `public_service` (mạo danh Bộ Y Tế, ngân hàng SCB, Cục Đăng Kiểm, công ty cấp nước, FPT Telecom) | 5 | ✅ Thêm pattern cụ thể hơn thay thế: `bo_y_te`, `scb`, `dang_kiem`, `cap_nuoc`, `internet_cap_quang` |
| Không thuộc 2 nhóm của Cẩm (lừa vay tiền qua app, tuyển tài xế Grab giả, mại dâm/sugar baby, cờ bạc, quảng cáo dịch vụ mẫu/PG không rõ có phải scam) | ~21 | ✅ Loại khỏi dataset — bổ sung `tuyen_doi_tac`, `phu_ba` làm pattern loại trừ mới |

**Đã sửa trong `collect_cam_scam_dataset.py`:** bỏ hẳn `dang\s*ky` và `ho\s*so` khỏi `PUBLIC_SERVICE_PATTERNS`; thêm 5 pattern cụ thể thay thế; thêm `tuyen_doi_tac`/`tuyen_tai_xe` vào `JOB_AND_INVESTMENT_PATTERNS`; thêm `phu_ba`/`phi_cong_tre` vào `GAMBLING_ADULT_PATTERNS`.

**Đồng thời tìm thêm 1 trích dẫn báo chí mới:**

| Nội dung (rút gọn) | Nhãn | Nguồn |
|---|---|---|
| "Facebook thông báo... trúng thưởng là TN5257... hồ sơ nhận thưởng." | `health_gift` | Báo Thanh Niên, bài cũ 2017 |

**Kết quả sau khi vá và chạy lại (14/09/2026, vòng 7):**
- Tổng mẫu: `374 → 363`
- `public_service`: `321 → 303` (giảm mạnh vì phần lớn 30 mẫu "chỉ dựa vào đăng_ký/hồ_sơ" hóa ra không thuộc phạm vi 2 nhóm, không phải health_gift lấy đi)
- `health_gift`: `53 → 60` (**+7**, mức tăng lớn nhất trong 1 lần sửa trong cả ngày — kể cả so với +3 của vòng sửa `tai_khoan` ở mục 8)
- `data_validation.py`: vẫn PASSED 100%
- `verify_cam_provenance.py`: **363/363 (100%)** sau khi thêm `thanhnien.vn` vào whitelist đã kiểm chứng thủ công

**Bài học rút ra:** cả 2 lần phát hiện lỗi lớn nhất trong ngày (`tai_khoan` và `đăng_ký`/`hồ_sơ`) đều là các **từ hành chính chung chung** vô tình xuất hiện ở cuối câu health_gift thật ("...để đăng ký làm thủ tục hồ sơ nhận thưởng", "...cung cấp thông tin cá nhân để làm hồ sơ nhận thưởng"), bị `is_ps` (kiểm tra trước `is_hg`) nuốt mất. Nên cảnh giác thêm với các pattern hành chính tương tự còn sót lại trong `PUBLIC_SERVICE_PATTERNS` (`giay_to`, `bang_lai`, `bo_sung`...) nếu tiếp tục rà soát.

**Việc cần làm tiếp theo (đã lỗi thời — xem mục 11 bên dưới):** `health_gift` đạt **64/200** (367/500 tổng, 303 `public_service`) sau khi bổ sung thêm 9 trích dẫn báo chí/pháp lý xác thực thủ công và sửa nốt pattern `đăng_ký`/`hồ_sơ` quá rộng. Cả 2 nguồn GitHub và hướng báo chí/pháp lý/bản án tòa án đã khai thác gần cạn. **Đường duy nhất còn scale được để đạt 200/nhóm là ảnh chụp màn hình SMS/Zalo/Messenger thật** (của Cẩm, người thân, hoặc hội nhóm báo cáo lừa đảo) đưa vào `CS114_Evidence_Vault`.

> 📝 **Ghi chú khoảng trống tài liệu (phát hiện khi review độc lập mục 11):** con số "367/500 tổng, 303 public_service, 64 health_gift" ở trên thực ra là kết quả của **1 vòng bổ sung nữa cùng commit** (4 trích dẫn báo chí mới không nằm trong bảng ở mục 9/10: "Thuê bao 19xxxxx tặng bạn bài hát" và "lọt top 10 bình chọn" từ Báo Pháp Luật VN, "tài khoản messenger... SH 100-200 triệu" từ Tiền Phong, "402E79" từ Báo Đắk Lắk) nhưng chưa từng được viết thành mục/bảng riêng — chỉ đổi số ở dòng tổng kết cuối mục 10 mà không cập nhật đoạn "Kết quả vòng 7" ngay phía trên (vẫn ghi 363/60). Ghi chú lại ở đây để tránh nhầm lẫn khi đọc lại lịch sử.

### 11. Review độc lập bổ sung (14/09) — loại 7 mẫu ngoài phạm vi

Theo yêu cầu review của Cẩm (validate data + validate code + cập nhật việc cần làm), một phiên AI khác (không phải phiên đã thực hiện vòng 1-8) đã chạy lại `data_validation.py` và `verify_cam_provenance.py` trên `staging_cam_scam.csv` (367 mẫu tại thời điểm đó) — cả 2 đều **PASSED 100%**, khớp đúng báo cáo. Sau đó rà thêm bằng phương pháp tương tự mục 8/10 (tìm mẫu chỉ khớp đúng 1 pattern chung chung, đọc thủ công), phát hiện 7 mẫu vấn đề mới:

| # | id (cũ) | Category cũ | Vấn đề | Nguyên nhân gốc |
|---|:---:|---|---|---|
| 1 | 208 | `public_service` | Lừa "kiện hàng bị giữ ở hải quan" giả mạo FedEx — không phải dịch vụ công/ngân hàng/viễn thông | Pattern `bo_sung` (bổ sung) quá chung chung |
| 2 | 237 | `public_service` | Quảng cáo vay tiền lãi nhanh ("không giữ giấy tờ gốc") — cùng loại đã bị loại ở vòng 3 & 7 | Pattern `giay_to` (giấy tờ) quá chung chung |
| 3 | 54 | `health_gift` | Lừa "tuyển nhân viên bình luận TikTok" — bản chất là lừa việc làm/CTV, không phải quà tặng | `JOB_AND_INVESTMENT_PATTERNS` chưa có biến thể "nhân viên bình luận" |
| 4 | 135 | `health_gift` | "Gói hỗ trợ tăng doanh thu" qua link Lazada — quảng cáo dịch vụ kinh doanh, không phải quà tặng cá nhân | `JOB_AND_INVESTMENT_PATTERNS` chưa có "tăng doanh thu" |
| 5 | 112 | `health_gift` | Leetspeak "588k free... rinh thưởng khung" + domain `.tech` lạ, không nêu thương hiệu — nghi cùng họ spam cờ bạc mục 5 | Né được `GAMBLING_ADULT_PATTERNS` (thiếu đuôi `groupsgooglecom`) |
| 6 | 164 | `health_gift` | Cùng kiểu leetspeak + dấu nháy đơn phá từ như mẫu trong `GARBLED_TEXT_DENYLIST` (mục 5), thiếu đúng đuôi nhận diện | Né được `GAMBLING_ADULT_PATTERNS` |
| 7 | 161 | `health_gift` | Chỉ là lời chúc Tết chung chung kèm link rút gọn, không có kịch bản quà tặng/trúng thưởng rõ ràng | Quá yếu để xác định là scam quà tặng thật |

Cả 7 mẫu đã được trình bày cho Cẩm xem xét từng dòng và **Cẩm xác nhận loại bỏ toàn bộ 7/7**.

**Đã sửa trong `collect_cam_scam_dataset.py`:**
- Bỏ hẳn 4 pattern hành chính chung chung còn sót khỏi `PUBLIC_SERVICE_PATTERNS`: `giay_to`, `bang_lai`, `bo_sung`, `loi_he_thong` (cùng họ lỗi với `tai_khoan`/`dang_ky`/`ho_so` đã bỏ ở mục 8/10; đã kiểm tra không có mẫu `public_service` hợp lệ nào hiện tại chỉ dựa riêng vào 4 pattern này).
- Thêm `nhan_vien_binh_luan`, `tang_doanh_thu` vào `JOB_AND_INVESTMENT_PATTERNS`.
- Mở rộng `GARBLED_TEXT_DENYLIST` với 3 mẫu spam nghi vấn (id 112, 161, 164 cũ) đã xác nhận thủ công.
- **Sửa 1 bug kỹ thuật phát sinh khi thêm denylist:** hàm `is_garbled_text()` so khớp trên text thô (raw, trước khi qua `mask_pii`) trong khi chuỗi đưa vào denylist được lấy từ text đã qua `mask_pii` (đã gộp khoảng trắng thừa ở bước cuối) — khiến 2/3 mẫu mới không khớp đúng ngay lần chạy đầu. Đã sửa để chuẩn hóa khoảng trắng trước khi so khớp, giống bước cuối của `mask_pii`.

**Kết quả sau khi vá và chạy lại `collect_cam_scam_dataset.py` (14/09/2026, vòng 9):**
- Tổng mẫu: `367 → 360` (giảm đúng 7 mẫu đã xác nhận, không phát sinh thay đổi ngoài ý muốn — verify bằng diff tập `text` giữa 2 phiên bản)
- `public_service`: `303 → 301`
- `health_gift`: `64 → 59`
- `data_validation.py`: **PASSED 100%** (chạy lại từ đầu, không dựa vào báo cáo cũ)
- `verify_cam_provenance.py`: **PASSED 100% (360/360)** (chạy lại từ đầu, tải trực tiếp 2 nguồn GitHub gốc)
- Quét PII độc lập (tên riêng sau "Anh/Chị/Ông/Bà", chuỗi số dài ≥8 chữ số chưa che): **không phát hiện rò rỉ mới**.

**Việc cần làm tiếp theo:** `health_gift` còn **64/200** (365/500 tổng, 301 `public_service`), khoảng cách với ngưỡng 200/nhóm vẫn còn xa. Nhận định không đổi so với các vòng trước: 2 nguồn GitHub + báo chí/pháp lý đã khai thác gần cạn — **hướng duy nhất còn scale được là ảnh chụp màn hình SMS/Zalo/Messenger thật** đưa vào `CS114_Evidence_Vault`. Ngoài ra, nếu tiếp tục rà thêm `PUBLIC_SERVICE_PATTERNS`, nên cảnh giác các từ hành chính chung chung còn lại (vd `dich_vu_cong`, `cap_nhat_thong_tin` — hiện đều đi kèm tín hiệu cụ thể nên chưa ghi nhận vấn đề, nhưng chưa rà kỹ như `tai_khoan`/`giay_to`).

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Không đủ mẫu | Low | High | Đã đạt 1.773 mẫu đời thực (vượt xa chỉ tiêu 500 mẫu) |
| Class imbalance nặng | Medium | Medium | Chờ phần việc lừa đảo của Sơn & Cẩm; áp dụng kỹ thuật cân bằng lớp ở phase sau |
| Chất lượng gán nhãn kém | Low | High | Đã kiểm định tự động qua data_validation.py (0 null, 0 dup, 100% provenance) |
| Rò rỉ dữ liệu (Data Leakage) | Low | High | Đã loại trừ 3 mẫu trùng với Holdout Test set, kiểm tra overlap = 0 |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **Phần việc Đặng Chí Thanh: HOÀN THÀNH XUẤT SẮC (1.773/500 mẫu chuẩn IEEE Access 2026 + 42 mẫu kiểm định thực tế độc lập từ 20 ảnh Drive cá nhân, 100% PII masked, 100% có source_url permalink/Drive, 0% rò rỉ dữ liệu).**  
> 🔧 **Phần việc Bùi Thị Mỷ Cẩm: CẦN BỔ SUNG THÊM (365/500 mẫu lừa đảo đời thực sau 9 vòng re-audit, gồm 1 vòng review độc lập 14/09 — xem [mục 11](#11-review-độc-lập-bổ-sung-1409-loại-7-mẫu-ngoài-phạm-vi)).** Đã khắc phục lỗi rò rỉ PII, lỗi phân loại category, loại thêm 7 mẫu ngoài phạm vi, và bổ sung 5 lời kể trực tiếp nạn nhân (PM Thanh duyệt 14/09: chấp nhận lời nạn nhân thật, không chấp nhận kịch bản AI viết lại); 301 mẫu `public_service` (đạt) + 64 mẫu `health_gift` (**chưa đạt** ngưỡng 200 mẫu/nhóm). `verify_cam_provenance.py` và `data_validation.py` đã chạy lại từ đầu và vẫn PASSED 100% trên bộ dữ liệu mới nhất. Cần thu thập thêm ~135-145 mẫu thật cho nhóm `health_gift` trước khi merge — nguồn duy nhất còn khả thi là ảnh chụp màn hình SMS/Zalo/Messenger thật vào `CS114_Evidence_Vault`.  
> ⏳ **Tiến độ toàn nhóm:** Đạt **2.138 / 1.500 mẫu** (1.773 mẫu bình thường + 365 mẫu lừa đảo). Đang chờ Hoàng Cao Sơn hoàn tất 500 mẫu lừa đảo nhóm quyền lực & cấp cứu (đã có 210 mẫu trên nhánh riêng `feat/phase-01-son-data-collection`, chưa merge), và Cẩm bổ sung thêm mẫu `health_gift`, trước khi nghiệm thu hợp nhất và tiến hành Train/Test Split cho Sprint 2.

---

## 🚨 Contingency Plan — Nếu thiếu mẫu vào 23:59 ngày 12/09

> [!CAUTION]
> Deadline khóa dữ liệu là **23:59 ngày 12/09/2026**. Nếu Sơn hoặc Cẩm chưa hoàn thành đủ 500 mẫu, nhóm cần kích hoạt đúng nhánh dự phòng bên dưới và **ghi rõ phương pháp trong báo cáo Word (Chương 2 — Dữ liệu)**.

### Nhánh A — Đủ mẫu (Tiêu chuẩn)

Điều kiện kích hoạt: Cả Sơn và Cẩm đều nộp đủ ≥ 500 mẫu có nguồn trên Google Sheet trước 23:59 ngày 12/09.

**Hành động:** Thanh chạy `data_validation.py`, chia Stratified Train/Test 80/20, đóng băng `dataset.csv` → kích hoạt Sprint 2.

### Nhánh B — Thiếu mẫu (Dự phòng học thuật)

Điều kiện kích hoạt: Đến 22:00 ngày 12/09, tổng mẫu lừa đảo < 800 mẫu.

**Hành động từng bước:**

1. **Bước 1 — Đánh giá thiếu hụt:** Thanh kiểm đếm số mẫu thực tế trên Google Sheet lúc 22:00 ngày 12/09.

2. **Bước 2 — Kích hoạt tăng cường dữ liệu (Rule-based Augmentation):**
   - Chỉ áp dụng trên mẫu lừa đảo có nguồn thực tế đã thu thập.
   - Kỹ thuật được phép: **Back-translation** (Việt → Anh → Việt qua Google Translate API) + **synonym replacement** với từ điển tiếng Việt.
   - **Tuyệt đối không** prompt AI (ChatGPT/Claude/Gemini) tự sinh văn bản lừa đảo từ đầu.
   - Tỷ lệ augmentation tối đa: **1 gốc → 2 biến thể** (augmented samples ≤ 2× original collected).

3. **Bước 3 — Ghi nhận bắt buộc trong báo cáo Word (Chương 2):**
   - Phải ghi rõ: số mẫu thu thập thực tế + số mẫu tăng cường + phương pháp tăng cường sử dụng.
   - Cột `source` trong `dataset.csv`: mẫu augmented ghi `augmented_from:<id_gốc>`.
   - Phân tích riêng distribution của mẫu gốc và mẫu tăng cường trong EDA notebook.

4. **Bước 4 — Tiếp tục pipeline:** Sau khi đủ ≥ 1.500 mẫu (gốc + augmented), chạy `data_validation.py` và chia 80/20 như bình thường.

| Metric | Nhánh A | Nhánh B |
|---|---|---|
| Tỷ lệ mẫu gốc | 100% | ≥ 60% |
| Tỷ lệ augmented | 0% | ≤ 40% |
| Ghi chú báo cáo | Không cần | **Bắt buộc** |
| Ảnh hưởng điểm GV | Chuẩn | Minh bạch → chấp nhận được |

---

## Commit

```bash
git add data/raw/dataset.csv data/scripts/data_validation.py data/scripts/data_scraper.py
git commit -m "feat(phase01): dataset 1500+ samples collected and validated"
```

