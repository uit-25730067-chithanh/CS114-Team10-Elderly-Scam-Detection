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
| Sprint | Sprint 1 |

---

## 👥 Bảng Trạng thái Thành viên (Individual Progress Tracking)

> 📌 **Nguyên tắc đồng sở hữu:** Phase 01 là giai đoạn chung của cả nhóm. Mỗi thành viên chịu trách nhiệm độc lập cho phần dữ liệu của mình. Khi hoàn thành, thành viên (hoặc AI của thành viên đó) cập nhật dòng tiến độ tương ứng và điền minh chứng vào [Evidence Section](#evidence-section-điền-sau-khi-làm).

| Thành viên | Phụ trách dữ liệu | Mục tiêu mẫu | Đã thu thập | Minh chứng nguồn gốc | Trạng thái |
|---|---|:---:|:---:|---|:---:|
| **Hoàng Cao Sơn** | Lừa đảo: Quyền lực (`fear_authority`) & Cấp cứu (`family_emergency`) | ≥ 500 mẫu | 0 / 500 | ⬜ Chưa có | ⏳ `not-started` |
| **Bùi Thị Mỷ Cẩm** | Lừa đảo: Sức khỏe (`health_gift`) & Dịch vụ công (`public_service`) | ≥ 500 mẫu | 0 / 500 | ⬜ Chưa có | ⏳ `not-started` |
| **Đặng Chí Thanh** *(PM)* | Bình thường (`none`): SMS viễn thông, ngân hàng, sinh hoạt đời thường | ≥ 500 mẫu | 0 / 500 | ⬜ Chưa có | ⏳ `not-started` |
| **TỔNG CỘNG** | **Toàn bộ dataset Phase 01** | **≥ 1.500 mẫu** | **0 / 1.500** | **100% có URL / Ảnh Drive** | ⏳ `not-started` |

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
- [ ] Cẩm: Cài đặt môi trường Python cá nhân theo `requirements.txt`
- [ ] Cẩm: Thu thập đủ **≥ 500 mẫu lừa đảo** thuộc 2 nhóm `health_gift` (Sức khỏe/Quà tặng) & `public_service` (Dịch vụ công/VNeID)
- [ ] Cẩm: 100% mẫu lừa đảo thu thập có đính kèm `source_url` (link bài báo chính thống hoặc link ảnh Drive)
- [ ] Cẩm: Đánh dấu hoàn thành trên Bảng trạng thái thành viên

### 3. Nhiệm vụ của Đặng Chí Thanh (Trưởng nhóm / PM)
- [ ] Thanh: Thu thập đủ **≥ 500 mẫu tin nhắn bình thường** (`label=0`, `scam_category='none'`) từ SMS nhà mạng, ngân hàng, sinh hoạt
- [ ] Thanh: Tải ảnh chụp màn hình tin nhắn thực tế vào thư mục Google Drive [`CS114_Evidence_Vault`](https://drive.google.com/drive/folders/1YuXfFBHMWfpafBgykXKCzKDjqKAyE9DL)
- [ ] Thanh: Kiểm tra chéo (Cross-review) dữ liệu của Sơn và Cẩm, rà soát nhãn nhất quán
- [ ] Thanh: Export Google Sheet thành file `data/raw/dataset.csv` (bảng mã `utf-8-sig`)
- [ ] Thanh: Chạy script `python3 draft/scam-detection/data/scripts/data_validation.py --file draft/scam-detection/data/raw/dataset.csv` pass 100%
- [ ] Thanh: Thực hiện Stratified 80/20 Train/Test split và lưu trữ artifacts
- [ ] Thanh: Đánh dấu hoàn thành trên Bảng trạng thái thành viên

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
- Số mẫu lừa đảo đã nạp vào Sheet: `... / 500`
- Tỷ lệ có `source_url`: `... %`
- Ngày ký duyệt hoàn thành: `...`

### 2. Minh chứng Bùi Thị Mỷ Cẩm:
- Số mẫu lừa đảo đã nạp vào Sheet: `... / 500`
- Tỷ lệ có `source_url`: `... %`
- Ngày ký duyệt hoàn thành: `...`

### 3. Minh chứng Đặng Chí Thanh:
- Số mẫu bình thường đã nạp vào Sheet: `... / 500`
- Ảnh chụp màn hình đã lưu trong `CS114_Evidence_Vault`: `... ảnh`
- Ngày ký duyệt hoàn thành: `...`

### 4. Kết quả chạy script kiểm định (`data_validation.py`):
```text
(Chưa thực hiện — dán output terminal thực tế vào đây khi nghiệm thu)
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Không đủ mẫu | Medium | High | Data augmentation + mở rộng nguồn |
| Class imbalance nặng | Medium | Medium | SMOTE/Oversampling ở phase sau |
| Chất lượng gán nhãn kém | Low | High | Cross-review giữa 2 người |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add data/raw/dataset.csv data/scripts/data_validation.py data/scripts/data_scraper.py
git commit -m "feat(phase01): dataset 1500+ samples collected and validated"
```
