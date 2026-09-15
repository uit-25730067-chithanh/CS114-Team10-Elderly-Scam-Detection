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
| Status | `passed` ✅ |
| Review | ✅ Đã nghiệm thu & kiểm thử 100% |
| Estimated effort | 3–4h |
| Sprint | Sprint 2 Fast-Track (15/09/2026) |

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

- [x] Unicode normalization (NFC) hoạt động
- [x] Teencode dictionary ≥30 entries (60 entries thực tế)
- [x] Auxiliary features extracted (phone, url, money, urgency, authority, length, exclamation, uppercase)
- [x] `pyvi` tokenizer hoạt động (`ViTokenizer`)
- [x] Stopwords list ≥50 words (80+ words với whitelist bảo vệ từ khóa lừa đảo)
- [x] `data/processed/dataset_preprocessed.csv` saved (2.193 dòng, 19 cột)
- [x] Notebook `01_preprocessing.ipynb` chạy end-to-end có đầy đủ visual cell outputs
- [x] Không có text_cleaned rỗng sau preprocessing (0/2.193 dòng rỗng)

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| All texts preprocessed | `df['text_cleaned'].notna().all()` → `True` (2.193/2.193 mẫu) |
| Tokenization works | Compound words joined: "công_an", "tài_khoản", "chuyển_khoản", "bộ_công_an" |
| Auxiliary features | DataFrame has 10 feature columns: `num_phone_numbers`, `num_urls`, `num_money_mentions`, `has_urgent_words`, `num_authority_words`, `text_length`, `num_words`, `num_exclamation`, `num_question`, `num_uppercase_words` |
| No data loss | Raw: 2.193 dòng → Processed: 2.193 dòng (100% bảo toàn) |

## Evidence Section *(điền sau khi làm)*

```text
=== Phase 02 Execution Evidence ===
- Date: 2026-09-15
- Module structure:
  * src/preprocessing/text_cleaner.py (146 lines, NFC Unicode + 60-entry TEENCODE_DICT)
  * src/preprocessing/tokenizer.py (49 lines, PyVi ViTokenizer wrapper)
  * src/preprocessing/stopwords.py (54 lines, 80+ grammatical stopwords, domain protection)
  * src/preprocessing/pipeline.py (100 lines, 10 auxiliary features + TextPreprocessor)
  * src/preprocessing/__init__.py (45 lines)
- Unit tests:
  * draft/scam-detection/tests/test_preprocessing.py: 13/13 PASSED in 1.44s
- Data validation:
  * Ingested: draft/scam-detection/data/raw/dataset.csv (2,193 rows)
  * Output: draft/scam-detection/data/processed/dataset_preprocessed.csv (2,193 rows, 19 columns, 1.5MB)
  * df['text_cleaned'].notna().all(): True
  * (df['text_cleaned'].str.strip() == '').sum(): 0
- Notebook:
  * draft/scam-detection/notebooks/01_preprocessing.ipynb: 15 cells (7 code cells) executed with 100% populated outputs, statistical plots, and comparative tables.
- System integrity:
  * python3 verify_final.py: PASSED (code 0)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **HOÀN THÀNH 100% XUẤT SẮC**:
> - Đã xây dựng hoàn chỉnh gói xử lý ngôn ngữ tự nhiên tiếng Việt chuyên biệt cho bài toán phát hiện tin nhắn lừa đảo tại `src/preprocessing/`.
> - Tách từ tiếng Việt qua `pyvi` kết hợp giữ nguyên các từ khóa cảm xúc/thao túng then chốt (`công_an`, `phong_tỏa`, `bắt_giam`, `tiền`, `triệu`, `khẩn_cấp`).
> - Trích xuất 10 đặc trưng phụ mang tính chỉ báo cao (tỷ lệ URL, số điện thoại, số tiền, từ ngữ khẩn cấp ở nhóm Scam cao vượt trội so với Normal).
> - Tạo lập và chạy thành công Notebook `01_preprocessing.ipynb` với đầy đủ kết quả trực quan.
> - Đã xuất tập dữ liệu tiền xử lý chuẩn hóa `data/processed/dataset_preprocessed.csv` sẵn sàng chuyển giao sang **Phase 03: EDA & Feature Engineering**.

## Commit

```bash
git add src/preprocessing/ data/processed/ notebooks/01_preprocessing.ipynb tests/
git commit -m "feat(phase02): vietnamese text preprocessing pipeline"
```
