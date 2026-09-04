# Phase 03 — EDA & Feature Engineering

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 02 — Vietnamese Text Preprocessing](./phase-02-vietnamese-text-preprocessing.md)  
**Next phase:** [Phase 04 — Modeling — Naive Bayes Baseline](./phase-04-model-naive-bayes.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P1 |
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 3–4h |
| Sprint | Sprint 2 |

## Context

Phân tích khám phá dữ liệu (EDA) để hiểu phân bố, đặc điểm ngôn ngữ lừa đảo, và xây dựng TF-IDF features cho các mô hình ML.

## Implementation Steps

### Step 1 — EDA Notebook

Tạo `notebooks/02_eda.ipynb` với các phân tích:

1. **Phân bố label**: Bar chart `label=0` vs `label=1`
2. **Phân bố scam_category**: Bar chart 4 categories
3. **Phân bố độ dài text**: Histogram so sánh scam vs normal
4. **Word Cloud**: Riêng cho class lừa đảo vs bình thường
5. **Top-20 từ phổ biến** mỗi class
6. **Correlation** auxiliary features vs label
7. **Phân bố source**: Kiểm tra diversity

### Step 2 — TF-IDF Feature Extraction

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from src.utils import RANDOM_STATE

# TF-IDF with n-gram (1,2)
tfidf = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
)

X_tfidf = tfidf.fit_transform(df['text_cleaned'])
```

### Step 3 — Combine Features

```python
import scipy.sparse as sp

# Kết hợp TF-IDF + auxiliary features
aux_features = df[['num_phone_numbers', 'num_urls', 'num_money_mentions',
                    'has_urgent_words', 'text_length', 'num_exclamation']].values
X_combined = sp.hstack([X_tfidf, sp.csr_matrix(aux_features)])
```

### Step 4 — Save Artifacts

```python
import joblib

joblib.dump(tfidf, "data/processed/tfidf_vectorizer.pkl")
joblib.dump(X_combined, "data/processed/X_features.pkl")
joblib.dump(df['label'].values, "data/processed/y_labels.pkl")
```

## Related Files

```
draft/scam-detection/
├── notebooks/
│   └── 02_eda.ipynb
├── src/
│   └── feature_engineering.py
├── data/processed/
│   ├── tfidf_vectorizer.pkl
│   ├── X_features.pkl
│   └── y_labels.pkl
└── reports/figures/
    ├── label_distribution.png
    ├── scam_category_distribution.png
    ├── text_length_histogram.png
    ├── wordcloud_scam.png
    └── wordcloud_normal.png
```

## Checklist

- [ ] EDA notebook hoàn chỉnh với ≥7 visualizations
- [ ] Word Cloud cho cả 2 class
- [ ] TF-IDF vectorizer fit trên training set
- [ ] Combined features (TF-IDF + auxiliary) saved
- [ ] Tất cả figures saved vào `reports/figures/`
- [ ] Notebook chạy end-to-end không lỗi

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| TF-IDF matrix shape | `(n_samples, ≤5000)` |
| Combined features | TF-IDF + 6 auxiliary features |
| Figures exported | ≥5 PNG files in reports/figures/ |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add notebooks/02_eda.ipynb src/feature_engineering.py reports/figures/
git commit -m "feat(phase03): EDA complete, TF-IDF + auxiliary features saved"
```
