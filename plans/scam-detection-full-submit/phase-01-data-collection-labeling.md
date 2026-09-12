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
| **Hoàng Cao Sơn** | Lừa đảo: Quyền lực (`fear_authority`) & Cấp cứu (`family_emergency`) | ≥ 500 mẫu | 0 / 500 | ⬜ Chưa có | ⏳ `not-started` (Hạn 12/09) |
| **Bùi Thị Mỷ Cẩm** | Lừa đảo: Sức khỏe (`health_gift`) & Dịch vụ công (`public_service`) | ≥ 500 mẫu | **530 / 500** | 100% Real Đa nguồn: UIT IE403 Ground Truth (241) + IEEE Access (287) + Báo Tuổi Trẻ (2) | ✅ `completed` (Hỗ trợ kỹ thuật từ PM) |
| **Đặng Chí Thanh** *(PM)* | Bình thường (`none`): SMS viễn thông, ngân hàng, sinh hoạt đời thường | ≥ 500 mẫu | **1.773 / 500** (+ 42 mẫu Holdout) | 100% IEEE Access 2026 Permalink + 20 Ảnh Drive cá nhân | ✅ `completed` |
| **TỔNG CỘNG** | **Toàn bộ dataset Phase 01** | **≥ 1.500 mẫu** | **2.303 / 1.500** | **100% có URL kiểm chứng 1-1 (0% rò rỉ, 0% AI tự sinh)** | ⏳ `in-progress` (Khóa dữ liệu 12/09) |

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
- [x] Cẩm: Thu thập đủ **≥ 500 mẫu lừa đảo** thuộc 2 nhóm `health_gift` (59 mẫu) & `public_service` (471 mẫu) qua pipeline đa nguồn bán tự động `collect_cam_scam_dataset.py` (Đạt 530 mẫu - 106.0%, 100% dữ liệu đời thực, 0% AI tự sinh)
- [x] Cẩm: 100% mẫu lừa đảo thu thập có đính kèm `source_url` (241 permalink GitHub UIT IE403 Ground Truth, 287 permalink GitHub IEEE Access 2026 chính xác từng dòng vật lý #L..., 2 URL bài báo Báo Tuổi Trẻ trích dẫn nguyên văn)
- [x] Cẩm: 100% mẫu đã được ẩn danh hóa PII (che SĐT, STK, OTP, CCCD) qua `anonymize_sms.py`
- [x] Cẩm: Xuất tệp staging kiểm định độc lập `draft/scam-detection/data/raw/staging_cam_scam.csv` pass `data_validation.py` và `verify_cam_provenance.py` 100%
- [x] Cẩm: Đánh dấu hoàn thành phần việc trên Bảng trạng thái thành viên

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
- Số mẫu lừa đảo đã nạp vào Sheet: `0 / 500`
- Tỷ lệ có `source_url`: `0.0 %`
- Ngày ký duyệt hoàn thành: `(Chưa thực hiện)`

### 2. Minh chứng Bùi Thị Mỷ Cẩm:
- Số mẫu lừa đảo đã nạp vào Staging CSV: `530 / 500` mẫu (Đạt 106.0% chỉ tiêu tối thiểu)
- Nguồn gốc dữ liệu: **100% đời thực từ Kiến trúc Đa nguồn Cân bằng Độc lập (Zero Synthetic Text - 0% AI bịa/sinh)**.
- Phân bổ đa nguồn độc lập:
  + Nguồn UIT IE403 Ground Truth Smishing Dataset (`duynguyenhoang22`): **241 mẫu (45.5%)** trích xuất từ các điện thoại thực tế của sinh viên UIT, định vị chính xác từng dòng vật lý `#L...` trên GitHub repository.
  + Nguồn Vietnamese Quality-Assured SMS Dataset (`IEEE Access 2026`): **287 mẫu (54.1%)** trích xuất từ dữ liệu SMS lừa đảo đời thực, định vị chính xác dòng vật lý `#L...` trên GitHub repository.
  + Nguồn Báo chí điều tra chính thống (Báo Tuổi Trẻ): **2 mẫu (0.4%)** trích dẫn nguyên văn tin nhắn phạt nguội và mạo danh trường đại học có URL trực tiếp.
- Phân bổ 2 nhóm bẫy tâm lý theo phân công:
  + Dịch vụ công, VNeID, BHXH, SIM, EVN, Ngân hàng, Phạt nguội (`public_service`): **471 mẫu** (88.9%)
  + Sức khỏe, quà tặng tri ân, việc làm, ưu đãi (`health_gift`): **59 mẫu** (11.1%)
- Ẩn danh hóa PII: 100% mẫu đã được che giấu thông tin nhạy cảm qua `anonymize_sms.py`.
- Tỷ lệ có `source_url`: **530 / 530 mẫu (100.0%)** có liên kết permalink 1-1 chính xác tuyệt đối.
- Độ sạch: 0 dòng trùng lặp (`text.duplicated().sum() == 0`), 0 văn bản rỗng, độ dài hợp lệ 25-600 ký tự.
- Kết quả kiểm định tự động `data_validation.py`: **PASSED 100%**
- Kết quả audit độc lập `verify_cam_provenance.py`: **530 / 530 mẫu (100.0%) khớp nguyên văn nguồn gốc**
- Ngày hoàn thành: `12/09/2026`

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

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Không đủ mẫu | Low | High | Đã đạt 1.773 mẫu đời thực (vượt xa chỉ tiêu 500 mẫu) |
| Class imbalance nặng | Medium | Medium | Chờ phần việc lừa đảo của Sơn & Cẩm; áp dụng kỹ thuật cân bằng lớp ở phase sau |
| Chất lượng gán nhãn kém | Low | High | Đã kiểm định tự động qua data_validation.py (0 null, 0 dup, 100% provenance) |
| Rò rỉ dữ liệu (Data Leakage) | Low | High | Đã loại trừ 3 mẫu trùng với Holdout Test set, kiểm tra overlap = 0 |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **Phần việc Đặng Chí Thanh: HOÀN THÀNH XUẤT SẮC (1.773/500 mẫu chuẩn IEEE Access 2026 + 42 mẫu kiểm định thực tế độc lập từ 20 ảnh Drive cá nhân, 100% PII masked, 100% có source_url permalink/Drive, 0% rò rỉ dữ liệu).**  
> ✅ **Phần việc Bùi Thị Mỷ Cẩm: HOÀN THÀNH XUẤT SẮC (530/500 mẫu lừa đảo đời thực 100%: 241 mẫu UIT IE403 Ground Truth + 287 mẫu IEEE Access 2026 + 2 mẫu báo Tuổi Trẻ, 471 mẫu dịch vụ công/VNeID/SIM + 59 mẫu sức khỏe/quà tri ân, 100% PII masked, verify_cam_provenance.py và data_validation.py PASSED 100% ✅).**  
> ⏳ **Tiến độ toàn nhóm:** Đạt **2.303 / 1.500 mẫu** (1.773 mẫu bình thường + 530 mẫu lừa đảo). Hiện đang chờ Hoàng Cao Sơn hoàn tất 500 mẫu lừa đảo nhóm quyền lực & cấp cứu để hoàn thành 100% chỉ tiêu Phase 01 trước 23:59 đêm nay 12/09/2026, nghiệm thu hợp nhất và tiến hành Train/Test Split cho Sprint 2.

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

