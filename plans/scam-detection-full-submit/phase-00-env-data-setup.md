# Phase 00 — Environment & Data Setup

**Parent plan:** [plan.md](./plan.md)  
**Next phase:** [Phase 01 — Data Collection & Labeling](./phase-01-data-collection-labeling.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P0 — Blocker cho toàn bộ pipeline |
| Status | `passed` |
| Review | ✅ Passed by PM Thanh (2026-09-04) |
| Estimated effort | 1h |
| Sprint | Sprint 1 |

## Context

Cần thiết lập môi trường phát triển hoàn chỉnh cho dự án NLP phát hiện lừa đảo tin nhắn tiếng Việt. Bao gồm cài đặt venv, dependencies, utility modules, và template cho dataset.

## Requirements

- Python 3.10+
- Các thư viện NLP tiếng Việt: `pyvi`, `underthesea` (tách từ)
- ML: `scikit-learn`, `xgboost`, `imbalanced-learn`
- Visualization: `matplotlib`, `seaborn`, `wordcloud`
- Demo: `streamlit`
- XAI: `shap` (nếu dùng)
- `RANDOM_STATE = 42` set trong mọi script

## Key Insights

- Khác CS106 (numerical data), CS114 xử lý **text tiếng Việt** → cần tokenizer riêng
- `underthesea` hoặc `pyvi` cho Vietnamese word segmentation
- Dataset tự thu thập → không cần tải từ Kaggle, nhưng cần template chuẩn

## Related Files

```
draft/scam-detection/
├── requirements.txt          ← Install target
├── data/raw/                 ← Đặt dataset.csv vào đây
│   └── .gitkeep
├── data/processed/           ← Dữ liệu sau tiền xử lý
│   └── .gitkeep
└── src/utils/
    ├── __init__.py
    └── helpers.py            ← Constants + helpers cơ bản
```

## Implementation Steps

### Step 1 — Setup Virtual Environment

```bash
cd draft/scam-detection
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2 — Create `requirements.txt`

```txt
# Core ML
scikit-learn>=1.5
xgboost>=2.0
imbalanced-learn>=0.12

# NLP Vietnamese
pyvi>=0.1
underthesea>=6.8

# Data & Visualization
pandas>=2.2
numpy<2.0
matplotlib>=3.9
seaborn>=0.13
wordcloud>=1.9

# XAI
shap>=0.45

# Demo
streamlit>=1.37

# Utilities
joblib>=1.4
tqdm>=4.66
```

### Step 3 — Create Utility Files

**`src/utils/helpers.py`** — constants và helpers dùng chung:

```python
"""Shared constants and utility helpers for the scam detection project."""
import numpy as np
import random

# ─── Constants ────────────────────────────────────────────────────────────────
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.15
DATA_RAW_PATH = "data/raw/dataset.csv"
DATA_PROCESSED_DIR = "data/processed"

# Scam categories
SCAM_CATEGORIES = [
    "fear_authority",       # Đe dọa / Giả danh quyền lực
    "family_emergency",     # Thúc ép khẩn cấp gia đình
    "health_gift",          # Dụ dỗ sức khỏe / Tri ân
    "public_service",       # Giả mạo dịch vụ công
    "none",                 # Không phải lừa đảo
]

# ─── Reproducibility ──────────────────────────────────────────────────────────

def set_seeds(seed: int = RANDOM_STATE) -> None:
    """Set all random seeds for reproducibility."""
    np.random.seed(seed)
    random.seed(seed)

# ─── Path helpers ─────────────────────────────────────────────────────────────

def get_project_root() -> str:
    """Return the project root directory (scam-detection/)."""
    import os
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Step 4 — Create Dataset Template

Tạo file `data/raw/dataset_template.csv` với header chuẩn:

```csv
id,text,label,scam_category,source
1,"Ví dụ tin nhắn bình thường",0,none,"manual"
2,"Ví dụ tin nhắn lừa đảo giả danh công an",1,fear_authority,"news"
```

### Step 5 — Verify Installation

```python
import pandas as pd
import numpy as np
import sklearn
import xgboost
from pyvi import ViTokenizer
print("All imports OK")
print(f"Pandas: {pd.__version__}")
print(f"Sklearn: {sklearn.__version__}")
```

## Checklist

- [x] Cấu trúc thư mục `draft/scam-detection/` hoàn chỉnh (`data`, `src`, `notebooks`, `reports`, `demo`)
- [x] File `requirements.txt` đầy đủ packages cốt lõi (scikit-learn, xgboost, pyvi, underthesea, shap, streamlit)
- [x] `src/utils/helpers.py` hoàn thiện với `RANDOM_STATE = 42`, `set_seeds()`, `SCAM_CATEGORIES`
- [x] Python package inits (`__init__.py`) được khởi tạo đầy đủ trong `src/` và các subpackages
- [x] `data/raw/dataset_template.csv` tồn tại với header chuẩn `id,text,label,scam_category,source` và 6 mẫu thực tế
- [x] `.gitignore` exclude `*.csv` (ngoại trừ template `!**/data/raw/dataset_template.csv`) và `.venv/`
- [x] Script kiểm định chuyên biệt `verify_final.py` chạy thành công 100%

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Project Structure ready | All directories & essential files exist |
| Requirements specified | `requirements.txt` with ML, NLP, XAI, Streamlit |
| Utils module works | `from src.utils.helpers import RANDOM_STATE` works |
| Dataset template ready | CSV header matches schema with 6 realistic samples |
| Custom verification script | `python3 verify_final.py` passes |

## Evidence Section *(điền sau khi làm)*

```text
=== Running Verification for CS114 Final Project ===
[*] Checking essential directory structure...
[SUCCESS] Directory exists: docs
[SUCCESS] Directory exists: draft/scam-detection
[SUCCESS] Directory exists: draft/scam-detection/src
[SUCCESS] Directory exists: draft/scam-detection/src/utils
[SUCCESS] Directory exists: draft/scam-detection/src/preprocessing
[SUCCESS] Directory exists: draft/scam-detection/src/models
[SUCCESS] Directory exists: draft/scam-detection/src/evaluation
[SUCCESS] Directory exists: draft/scam-detection/data/raw
[SUCCESS] Directory exists: draft/scam-detection/data/processed
[SUCCESS] Directory exists: draft/scam-detection/notebooks
[SUCCESS] Directory exists: draft/scam-detection/reports/figures
[SUCCESS] Directory exists: draft/scam-detection/demo
[SUCCESS] Directory exists: plans/scam-detection-full-submit
[SUCCESS] Directory exists: submit
[*] Checking required files...
[SUCCESS] File exists: README.md
[SUCCESS] File exists: AGENTS.md
[SUCCESS] File exists: BRAINSTORM.md
[SUCCESS] File exists: .gitignore
[SUCCESS] File exists: draft/scam-detection/README.md
[SUCCESS] File exists: draft/scam-detection/requirements.txt
[SUCCESS] File exists: draft/scam-detection/data/raw/dataset_template.csv
[SUCCESS] File exists: draft/scam-detection/src/utils/helpers.py
[SUCCESS] File exists: draft/scam-detection/src/utils/__init__.py
[SUCCESS] File exists: plans/scam-detection-full-submit/plan.md
[*] Checking 11 phase plan specifications...
[SUCCESS] All phase plans (phase-00 to phase-10) found.
[*] Verifying dataset_template.csv schema...
[SUCCESS] Template header matches: 'id,text,label,scam_category,source'
[SUCCESS] Template contains 6 sample rows
[*] Testing Python utils module import...
[SUCCESS] helpers.py imported successfully. RANDOM_STATE=42, Categories=5
[SUCCESS] Target metrics: F1 >= 0.88, Recall >= 0.92
--------------------------------------------------
[SUCCESS] All Final project checks PASSED! Ready for Sprint execution.
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| underthesea install heavy | Medium | Low | Fallback to pyvi (nhẹ, nhanh hơn) |
| numpy version conflict | Low | Medium | Pin numpy<2.0 trong requirements.txt |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **HOÀN THÀNH (04/09/2026):** PM Thanh đã rà soát và thiết lập thành công toàn bộ hạ tầng Phase 00. Đã tạo `requirements.txt`, `dataset_template.csv`, `src/utils/helpers.py`, package inits, `draft/scam-detection/README.md`, và script tự động `verify_final.py`. Chạy kiểm định 100% đạt chuẩn môn học CS114. Sẵn sàng cho Phase 01: Thu thập & Gán nhãn Dataset vào Sprint 1 (06/09).

## Commit

```bash
git add src/utils/ data/raw/.gitkeep data/raw/dataset_template.csv requirements.txt
git commit -m "feat(phase00): env setup, utils helpers, dataset template"
```
