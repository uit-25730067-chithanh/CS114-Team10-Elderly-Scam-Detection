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

## Context

Dự án cần tự thu thập và gán nhãn ≥1500 mẫu tin nhắn tiếng Việt (lừa đảo + bình thường). Khác với CS106 dùng dataset Kaggle sẵn, CS114 yêu cầu xây dựng dataset thủ công phù hợp bối cảnh Việt Nam.

## Requirements

- Tối thiểu **1500 mẫu**, lý tưởng 2000-3000 mẫu
- Tỷ lệ class: ~40-50% Lừa đảo / 50-60% Bình thường
- Gán nhãn `scam_category` cho mọi mẫu lừa đảo
- Mỗi mẫu phải có `source` rõ ràng (truy xuất được)

## Nguồn thu thập

### Mẫu Lừa đảo (`label = 1`)

| Nguồn | URL / Mô tả | Ước tính mẫu |
|-------|-------------|--------------|
| Bộ Công an — Cục ATTT | chongthurac.vn, canhsat.vn | 200-300 |
| Báo Dân Trí | dantri.com.vn — mục Pháp luật | 100-200 |
| VnExpress | vnexpress.net — mục Pháp luật | 100-200 |
| Tuổi Trẻ Online | tuoitre.vn — cảnh báo lừa đảo | 100-150 |
| Facebook/Zalo groups | Hội nhóm cảnh báo lừa đảo | 200-300 |
| Data Augmentation | Hoán đổi tên riêng, số tiền, số ĐT | 200-400 |

### Mẫu Bình thường (`label = 0`)

| Nguồn | Mô tả | Ước tính mẫu |
|-------|-------|--------------|
| Tin nhắn nhà mạng | Thông báo cước, khuyến mãi data | 200-300 |
| Tin nhắn ngân hàng | Biến động số dư, OTP (che số) | 150-200 |
| Tin nhắn gia đình | Hỏi thăm sức khỏe, nhắc lịch | 200-300 |
| CSKH dịch vụ | Lịch khám bệnh, hóa đơn điện nước | 100-200 |

## Cấu trúc Dataset

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

## Implementation Steps

### Step 1 — Tạo Google Sheet thu thập

Tạo bảng tính Google Sheet chia sẻ nhóm, columns: `id | text | label | scam_category | source | collector_name | notes`

### Step 2 — Phân chia thu thập

Mỗi thành viên chịu trách nhiệm 1-2 nguồn, thu thập ≥300 mẫu/người.

### Step 3 — Data Augmentation

```python
# Ý tưởng augmentation đơn giản:
# - Thay đổi tên riêng: "Nguyễn Văn A" → "Trần Văn B"
# - Thay đổi số tiền: "500 triệu" → "200 triệu"
# - Thay đổi tên ngân hàng: "Vietcombank" → "BIDV"
# - Thay đổi số điện thoại
```

### Step 4 — Export & Validate

- Export Google Sheet → `dataset.csv`
- Chạy script validate:
  - Không có dòng trùng lặp
  - Mọi label ∈ {0, 1}
  - Mọi scam_category hợp lệ
  - Không có text rỗng

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

## Checklist

- [ ] Google Sheet tạo và chia sẻ nhóm
- [ ] Thu thập ≥750 mẫu lừa đảo (label=1)
- [ ] Thu thập ≥750 mẫu bình thường (label=0)
- [ ] Mọi mẫu lừa đảo có `scam_category` hợp lệ
- [ ] Mọi mẫu có `source` rõ ràng
- [ ] Không có duplicates
- [ ] Export `data/raw/dataset.csv` thành công
- [ ] Validation script pass 100%
- [ ] Train/Test split saved

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Total samples ≥ 1500 | `df.shape[0] >= 1500` |
| Class balance | `df['label'].value_counts()` reasonable ratio |
| Categories covered | All 4 scam categories present |
| No empty text | `df['text'].str.len().min() > 0` |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
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
git add data/raw/dataset.csv src/data_validation.py
git commit -m "feat(phase01): dataset 1500+ samples collected and validated"
```
