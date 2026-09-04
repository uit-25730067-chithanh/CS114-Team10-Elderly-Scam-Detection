# Phase 00 — Environment & Data Setup

**Parent plan:** [plan.md](./plan.md)  
**Next phase:** [Phase 01 — Data Collection & Labeling](./phase-01-data-collection-labeling.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P0 — Blocker cho toàn bộ pipeline |
| Status | `not-started` |
| Review | ⬜ Not reviewed |
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

- [ ] `python -m venv .venv` tạo được venv
- [ ] `pip install -r requirements.txt` không error
- [ ] `src/utils/helpers.py` có `RANDOM_STATE`, `set_seeds()`, `SCAM_CATEGORIES`
- [ ] Tất cả imports (pandas, sklearn, xgboost, pyvi/underthesea) không lỗi
- [ ] `data/raw/dataset_template.csv` tồn tại với header đúng
- [ ] `.gitignore` exclude `*.csv` (trừ template) và `.venv/`

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Venv created | `pip list` shows all packages |
| Vietnamese tokenizer works | `ViTokenizer.tokenize("Xin chào")` returns correct output |
| Utils module works | `from src.utils import RANDOM_STATE` works |
| Dataset template ready | CSV header matches schema |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| underthesea install heavy | Medium | Low | Fallback to pyvi |
| numpy version conflict | Low | Medium | Pin numpy<2.0 |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add src/utils/ data/raw/.gitkeep data/raw/dataset_template.csv requirements.txt
git commit -m "feat(phase00): env setup, utils helpers, dataset template"
```
