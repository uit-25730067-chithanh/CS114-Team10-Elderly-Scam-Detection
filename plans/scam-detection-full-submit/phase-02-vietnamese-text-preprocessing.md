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
│   ├── teencode_dictionary.py  ← Centralized dictionary & compound mappings
│   ├── text_cleaner.py         ← Unicode NFC, regex, tone marks, deobfuscation
│   ├── tokenizer.py            ← Vietnamese word segmentation & unaccented joiner
│   ├── stopwords.py            ← Stopword list & domain protection whitelist
│   └── pipeline.py             ← Full pipeline orchestrator & 15 aux features
├── data/processed/
│   └── dataset_preprocessed.csv
└── notebooks/
    └── 01_preprocessing.ipynb   ← Exploration & validation (39.5 KB)
```

## Checklist

- [x] Unicode normalization (NFC) hoạt động
- [x] Unicode normalization (NFC) & chuẩn hóa dấu thanh hiện đại (`underthesea.text_normalize`)
- [x] Teencode dictionary mở rộng 160 entries chuẩn xác (0 duplicate keys, loại bỏ từ đa nghĩa gây méo mó ngữ nghĩa)
- [x] De-obfuscation thủ thuật Leet-speak lừa đảo (`th0ng ba0`, `kh0ng`, `kh0a`, `d!eu k!en`, `t!en`)
- [x] Hóa giải 45.0% văn bản không dấu qua cơ chế ghép cụm từ không dấu (`tai_khoan`, `chuyen_khoan`, `vao_cuoc`, `cuoc_goi`)
- [x] Auxiliary features chuyên sâu gồm 15 chỉ báo (URL, SĐT, số tiền, khẩn cấp, quyền lực, tai nạn cấp cứu, quà tặng, OTP, leet-speak, không dấu, độ dài, dấu câu, chữ in hoa)
- [x] Bao quát 100% các nhãn ẩn danh masked entities (`[MONEY]`, `[ĐƯỜNG_DẪN]`, `[MÃ_OTP]`, `[SỐ_ĐIỆN_THOẠI]`)
- [x] `pyvi` tokenizer hoạt động (`ViTokenizer`) kết hợp xử lý cụm từ không dấu
- [x] Stopwords list ≥50 words (80+ words với whitelist bảo vệ từ khóa lừa đảo & nguy cấp `ngay_lập_tức`)
- [x] `data/processed/dataset_preprocessed.csv` saved (2.193 dòng, 24 cột hoàn chỉnh)
- [x] Notebook `01_preprocessing.ipynb` chạy end-to-end (39.5 KB, không bloat base64) có đầy đủ visual cell outputs và bảng biểu chuyên sâu
- [x] Không có text_cleaned rỗng sau preprocessing (0/2.193 dòng rỗng)

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| All texts preprocessed | `df['text_cleaned'].notna().all()` → `True` (2.193/2.193 mẫu) |
| Tokenization works | Compound words joined: "công_an", "tài_khoản", "chuyển_khoản", "tai_khoan", "chuyen_khoan" |
| Auxiliary features | DataFrame has 15 feature columns: `num_urls`, `num_phone_numbers`, `num_money_mentions`, `has_urgent_words`, `num_authority_words`, `has_emergency_words`, `has_gift_words`, `has_otp_request`, `has_leet_speak`, `is_unaccented`, `text_length`, `num_words`, `num_exclamation`, `num_question`, `num_uppercase_words` |
| No data loss | Raw: 2.193 dòng → Processed: 2.193 dòng (100% bảo toàn), 24 cột |

## Evidence Section *(điền sau khi làm)*

```text
=== Phase 02 Execution Evidence (Research-Driven Upgrade & Code Review Curated) ===
- Date: 2026-09-15
- Research Report: draft/scam-detection/reports/research-thanh-phase02-vietnamese-preprocessing-audit.md
- Clean Module Structure (strictly < 150 lines per file, adhering to 200-line rule & DRY):
  * src/preprocessing/teencode_dictionary.py (147 lines, centralized dictionary with 0 key collisions, 22 leet-speak patterns, and 50+ unaccented compounds)
  * src/preprocessing/text_cleaner.py (124 lines, NFC + underthesea tone normalization + deobfuscation)
  * src/preprocessing/tokenizer.py (71 lines, PyVi ViTokenizer + unaccented adaptive joining)
  * src/preprocessing/stopwords.py (54 lines, 80+ grammatical stopwords, domain protection)
  * src/preprocessing/pipeline.py (126 lines, 15 auxiliary features + TextPreprocessor)
  * src/preprocessing/__init__.py (58 lines)
- Unit tests:
  * draft/scam-detection/tests/test_preprocessing.py: 21/21 PASSED in 1.67s (including over-normalization regression tests)
- Data validation:
  * Ingested: draft/scam-detection/data/raw/dataset.csv (2,193 rows)
  * Output: draft/scam-detection/data/processed/dataset_preprocessed.csv (2,193 rows, 24 columns, 1.5MB)
  * df['text_cleaned'].notna().all(): True
  * (df['text_cleaned'].str.strip() == '').sum(): 0
- Feature Discrimination Highlights (Scam vs Normal):
  * has_emergency_words: Scam (9.8%) vs Normal (0.2%) — gấp 35 lần
  * has_urgent_words: Scam (19.0%) vs Normal (3.6%) — gấp 5.2 lần
  * num_authority_words: Scam (12.6%) vs Normal (4.1%) — gấp 3 lần
  * has_leet_speak: Scam (2.9%) vs Normal (0.0%) — chỉ xuất hiện ở tin nhắn lừa đảo
  * is_unaccented: Scam (1.7%) vs Normal (55.3%)
- Notebook:
  * draft/scam-detection/notebooks/01_preprocessing.ipynb: 15 cells (7 code cells) executed cleanly (39.5 KB, zero base64 bloat)
- System integrity:
  * python3 verify_final.py: PASSED (code 0)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **HOÀN THÀNH 100% XUẤT SẮC (RESEARCH-DRIVEN & REVIEW CURATED)**:
> - Thực hiện thẩm định toàn diện 2.193 dòng dữ liệu thực tế, phát hiện và hóa giải 4 thách thức lớn: nhãn ẩn danh (hơn 4.000 nhãn `[MONEY]`, `[NUMBER]`, `[ĐƯỜNG_DẪN]`), thủ đoạn leet-speak (`th0ng ba0`, `d!eu k!en`, `t!en`), tính bất đối xứng dấu thanh (45.0% không dấu), và bất cập trong vị trí dấu thanh tiếng Việt.
> - Tiếp thu triệt để phản hồi từ Gemini PR Code Review: Loại bỏ triệt để hiện tượng over-normalization của các từ đa nghĩa (`cuoc` -> `cước`, `ty` -> `cảm ơn`, `the` -> `thẻ`, `vay` -> `khoản vay`), chuyển sang ghép cụm từ cố định an toàn (`vao_cuoc`, `cuoc_goi`, `the_tin_dung`).
> - Gộp và chuẩn hóa kiến trúc mã nguồn theo DRY vào duy nhất `teencode_dictionary.py` (147 dòng), loại bỏ các file thừa; chọn lọc và xóa bỏ các script sinh tạm, file nháp và ảnh nhị phân tĩnh khỏi git tracking; làm sạch notebook (39.5 KB).
> - Đạt 21/21 unit tests pass, bảo đảm dữ liệu `data/processed/dataset_preprocessed.csv` (2.193 dòng, 24 cột) sạch đẹp 100%.

## Commit

```bash
git add src/preprocessing/ data/processed/ notebooks/01_preprocessing.ipynb tests/ reports/ plans/ AGENTS.md README.md
git commit -m "refactor(preprocessing): curate repository deliverables and synchronize phase documentation"
```

