# Phase 02 — Vietnamese Text Preprocessing

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 01 — Data Collection & Labeling](./phase-01-data-collection-labeling.md)  
**Next phase:** [Phase 03 — EDA & Feature Engineering](./phase-03-eda-feature-engineering.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P1 — Blocker cho feature extraction |
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 3–4h |
| Sprint | Sprint 2 Fast-Track (13/09/2026) |

## Context

Text tiếng Việt có đặc thù riêng cần xử lý: Unicode dựng sẵn vs tổ hợp, teencode, viết tắt, tách từ (word segmentation). Bước tiền xử lý quyết định chất lượng toàn pipeline.

## Requirements

- Chuẩn hóa Unicode tiếng Việt (NFC)
- Loại bỏ URL, số điện thoại (trích xuất thành feature riêng trước khi xóa)
- Xử lý teencode/viết tắt phổ biến
- Tách từ tiếng Việt (word segmentation) bằng `pyvi` hoặc `underthesea`
- Loại bỏ stopwords tiếng Việt
- Lowercase toàn bộ

## Implementation Steps

### Step 1 — Unicode Normalization

```python
import unicodedata

def normalize_unicode(text: str) -> str:
    """Chuẩn hóa Unicode NFC cho tiếng Việt."""
    return unicodedata.normalize("NFC", text)
```

### Step 2 — Feature Extraction (trước khi clean)

Trích xuất đặc trưng phụ **trước** khi loại bỏ:

```python
import re

def extract_auxiliary_features(text: str) -> dict:
    """Trích xuất các đặc trưng phụ từ text gốc."""
    return {
        "num_phone_numbers": len(re.findall(r'\b0\d{9,10}\b', text)),
        "num_urls": len(re.findall(r'https?://\S+', text)),
        "num_money_mentions": len(re.findall(r'\d+\s*(triệu|tỷ|nghìn|ngàn|tr|đ|VND)', text, re.I)),
        "has_urgent_words": int(bool(re.search(r'(gấp|khẩn|ngay lập tức|trong vòng \d+ phút)', text, re.I))),
        "text_length": len(text),
        "num_exclamation": text.count("!"),
    }
```

### Step 3 — Text Cleaning Pipeline

```python
def clean_text(text: str) -> str:
    """Pipeline làm sạch text tiếng Việt."""
    text = normalize_unicode(text)
    text = text.lower()
    # Loại bỏ URL
    text = re.sub(r'https?://\S+', ' ', text)
    # Loại bỏ số điện thoại
    text = re.sub(r'\b0\d{9,10}\b', ' ', text)
    # Loại bỏ email
    text = re.sub(r'\S+@\S+', ' ', text)
    # Xử lý teencode cơ bản
    text = teencode_normalize(text)
    # Loại bỏ ký tự đặc biệt (giữ dấu tiếng Việt)
    text = re.sub(r'[^\w\sàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]', ' ', text)
    # Loại bỏ whitespace thừa
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

### Step 4 — Teencode Dictionary

```python
TEENCODE_DICT = {
    "ko": "không", "k": "không", "kh": "không",
    "dc": "được", "đc": "được",
    "nc": "nước", "ck": "chuyển khoản",
    "tk": "tài khoản", "stk": "số tài khoản",
    "đt": "điện thoại", "sdt": "số điện thoại",
    "tks": "cảm ơn", "bt": "bình thường",
    "ng": "người", "vs": "với",
    "mk": "mình", "bn": "bạn",
    # ... mở rộng thêm
}

def teencode_normalize(text: str) -> str:
    """Thay thế teencode bằng từ chuẩn."""
    words = text.split()
    return " ".join(TEENCODE_DICT.get(w, w) for w in words)
```

### Step 5 — Vietnamese Word Segmentation

```python
from pyvi import ViTokenizer

def segment_vietnamese(text: str) -> str:
    """Tách từ tiếng Việt — ví dụ: 'công an' → 'công_an'."""
    return ViTokenizer.tokenize(text)
```

### Step 6 — Stopword Removal

```python
# Vietnamese stopwords list (subset)
VIETNAMESE_STOPWORDS = {
    "và", "là", "của", "có", "được", "cho", "với", "trong",
    "này", "đó", "để", "từ", "theo", "về", "trên", "đã",
    "những", "các", "một", "cũng", "như", "nhưng", "hay",
    "thì", "mà", "rằng", "nếu", "khi", "tại", "bị", "do",
    # ... mở rộng thêm
}

def remove_stopwords(text: str) -> str:
    """Loại bỏ stopwords tiếng Việt."""
    words = text.split()
    return " ".join(w for w in words if w not in VIETNAMESE_STOPWORDS)
```

### Step 7 — Full Preprocessing Pipeline

```python
def preprocess_pipeline(text: str) -> tuple[str, dict]:
    """
    Full preprocessing pipeline.
    Returns: (cleaned_text, auxiliary_features)
    """
    # Extract features BEFORE cleaning
    aux_features = extract_auxiliary_features(text)
    
    # Clean
    cleaned = clean_text(text)
    
    # Segment
    segmented = segment_vietnamese(cleaned)
    
    # Remove stopwords
    final = remove_stopwords(segmented)
    
    return final, aux_features
```

### Step 8 — Apply & Save

```python
import pandas as pd

df = pd.read_csv("data/raw/dataset.csv")

# Apply preprocessing
results = df['text'].apply(preprocess_pipeline)
df['text_cleaned'] = results.apply(lambda x: x[0])
aux_df = pd.DataFrame(results.apply(lambda x: x[1]).tolist())
df = pd.concat([df, aux_df], axis=1)

# Save
df.to_csv("data/processed/dataset_preprocessed.csv", index=False)
```

## Related Files

```
draft/scam-detection/
├── src/preprocessing/
│   ├── __init__.py
│   ├── text_cleaner.py         ← Unicode, regex, teencode
│   ├── tokenizer.py            ← Vietnamese word segmentation
│   ├── stopwords.py            ← Stopword list & removal
│   └── pipeline.py             ← Full pipeline orchestrator
├── data/processed/
│   └── dataset_preprocessed.csv
└── notebooks/
    └── 01_preprocessing.ipynb   ← Exploration & validation
```

## Checklist

- [ ] Unicode normalization (NFC) hoạt động
- [ ] Teencode dictionary ≥30 entries
- [ ] Auxiliary features extracted (phone, url, money, urgency)
- [ ] `pyvi` hoặc `underthesea` tokenizer hoạt động
- [ ] Stopwords list ≥50 words
- [ ] `data/processed/dataset_preprocessed.csv` saved
- [ ] Notebook `01_preprocessing.ipynb` chạy end-to-end
- [ ] Không có text_cleaned rỗng sau preprocessing

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| All texts preprocessed | `df['text_cleaned'].notna().all()` |
| Tokenization works | Compound words joined: "công_an", "tài_khoản" |
| Auxiliary features | DataFrame has phone/url/money/urgency columns |
| No data loss | Same row count before/after preprocessing |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add src/preprocessing/ data/processed/ notebooks/01_preprocessing.ipynb
git commit -m "feat(phase02): vietnamese text preprocessing pipeline"
```
