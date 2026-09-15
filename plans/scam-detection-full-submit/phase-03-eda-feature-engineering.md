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
| Status | `passed` ✅ |
| Review | ✅ Passed — 34/34 tests; verified via `verify_final.py` |
| Estimated effort | 3–4h |
| Sprint | Sprint 2 Fast-Track (15/09/2026) |
| Actual elapsed | < 1h pipeline + 3h notebook/tests |

## Context

Phân tích khám phá dữ liệu (EDA) để hiểu phân bố, đặc điểm ngôn ngữ lừa đảo, và xây dựng TF-IDF features cho các mô hình ML.

## Implementation Steps

### Step 1 — EDA Notebook ✅

`notebooks/02_eda.ipynb` — 30 cells, executed end-to-end, 29.5 KB (no base64 bloat).

7 biểu đồ phân tích (300 DPI):
1. `label_distribution.png` — Bar chart label 0 vs 1, imbalance ratio 4.2:1
2. `scam_category_distribution.png` — 4 nhóm bẫy tâm lý
3. `text_length_comparison.png` — Histogram phân bố ký tự và số từ
4. `wordcloud_scam_vs_normal.png` — Word cloud tiếng Việt
5. `top_ngrams_scam_vs_normal.png` — Top-20 N-grams phân tách mạnh nhất
6. `auxiliary_correlation_heatmap.png` — Correlation heatmap 15 đặc trưng × nhãn
7. `source_distribution.png` — Phân bố nguồn dữ liệu

### Step 2 — Zero-Leakage Feature Pipeline ✅

**CRITICAL FIX:** Bản nháp plan cũ có lỗi leakage (`tfidf.fit_transform(df['text_cleaned'])` toàn bộ dataset). Đã sửa triệt để — Split FIRST, sau đó mới fit.

```
src/feature_engineering_config.py  (45 lines) — constants
src/feature_engineering.py         (193 lines) — pipeline classes
```

- `DataSplitter`: Stratified 80/20, `random_state=42`, `stratify=y` ✅
- `TextFeatureExtractor`: `TfidfVectorizer(ngram_range=(1,2), max_features=5000, sublinear_tf=True, min_df=2, max_df=0.95)` — `fit_transform` ONLY trên X_train_text ✅
- `AuxiliaryFeatureScaler`: `StandardScaler` fit ONLY trên X_train_aux ✅
- `assemble_feature_matrix()`: `scipy.sparse.hstack([tfidf_matrix, csr_matrix(aux_scaled)])` ✅

### Step 3 — EDA Modules ✅

```
src/eda_plots_part1.py    (152 lines) — label, category, text length, wordcloud
src/eda_plots_part2.py    (122 lines) — n-grams, heatmap, source distribution
src/eda_visualizations.py (103 lines) — orchestrator
```

### Step 4 — Unit Tests ✅

`tests/test_feature_engineering.py` — 13 new tests (34 total: 21 old + 13 new):
- `TestDataSplitter`: split sizes, stratified ratio, no index overlap
- `TestTextFeatureExtractor`: vocabulary from train only, RuntimeError if not fitted, no NaN/Inf
- `TestAuxiliaryFeatureScaler`: scaler stats from train only, RuntimeError if not fitted, no NaN/Inf
- `TestFeatureMatrixShape`: shape (5015), train/test column match
- `TestReproducibility`: bit-identical y_train across 2 runs, identical vocab

## Related Files

```
draft/scam-detection/
├── notebooks/
│   └── 02_eda.ipynb                       ✅ 30 cells, no errors, 29.5 KB
├── src/
│   ├── feature_engineering.py             ✅ 193 lines
│   ├── feature_engineering_config.py      ✅ 45 lines
│   ├── eda_plots_part1.py                 ✅ 152 lines
│   ├── eda_plots_part2.py                 ✅ 122 lines
│   └── eda_visualizations.py              ✅ 103 lines
├── data/processed/
│   ├── X_train.pkl                        ✅ 1251.0 KB
│   ├── X_test.pkl                         ✅ 302.4 KB
│   ├── y_train.pkl                        ✅ 55.6 KB
│   ├── y_test.pkl                         ✅ 14.5 KB
│   ├── tfidf_vectorizer.pkl               ✅ 198.3 KB
│   ├── aux_scaler.pkl                     ✅ 0.9 KB
│   └── feature_names.json                 ✅ 80.5 KB (5015 names)
├── tests/
│   └── test_feature_engineering.py        ✅ 13 tests all PASSED
└── reports/figures/
    ├── label_distribution.png             ✅ 111.1 KB @ 300 DPI
    ├── scam_category_distribution.png     ✅ 158.7 KB @ 300 DPI
    ├── text_length_comparison.png         ✅ 195.7 KB @ 300 DPI
    ├── wordcloud_scam_vs_normal.png       ✅ 2569.0 KB @ 300 DPI
    ├── top_ngrams_scam_vs_normal.png      ✅ 230.8 KB @ 300 DPI
    ├── auxiliary_correlation_heatmap.png  ✅ 709.7 KB @ 300 DPI
    └── source_distribution.png           ✅ 144.6 KB @ 300 DPI
```

## Checklist

- [x] EDA notebook hoàn chỉnh với ≥7 visualizations
- [x] Word Cloud cho cả 2 class
- [x] TF-IDF vectorizer fit trên training set ONLY (Zero-Leakage)
- [x] StandardScaler fit trên training set ONLY (Zero-Leakage)
- [x] Combined features (TF-IDF 5000 + auxiliary 15 = 5015) saved
- [x] Tất cả figures saved vào `reports/figures/` (≥5 PNG @ 300 DPI)
- [x] Notebook chạy end-to-end không lỗi (30/30 cells OK)
- [x] 13 unit tests PASSED (34 total)
- [x] verify_final.py exit code 0
- [x] Mọi src/ file ≤ 200 dòng (modularization compliant)
- [x] 0 credential/secret trong staged files
- [x] 0 file > 50MB

## Success Criteria

| Criterion | Target | Evidence |
|-----------|--------|----------|
| TF-IDF matrix shape | `(n_samples, ≤5000)` | X_train_tfidf: (1754, 5000) ✅ |
| Combined features | TF-IDF + 15 aux = 5015 | X_train: (1754, 5015), X_test: (439, 5015) ✅ |
| Figures exported | ≥5 PNG @ 300 DPI | 7 PNG files in reports/figures/ ✅ |
| Tests | 100% PASS | 34/34 passed in 2.09s ✅ |
| Zero-leakage | No test data in vocab/scaler | Test vocabulary unchanged after transform ✅ |

## Evidence Section *(điền sau khi làm)*

```
=== Pipeline Execution (2026-09-15 14:04) ===
Dataset: data/processed/dataset_preprocessed.csv (2193 rows × 24 cols)
Split: Train=1754, Test=439 (stratified, random_state=42)
  Train scam ratio: 0.1916 (336/1754)
  Test scam ratio:  0.1913 (84/439)

TF-IDF: ngram_range=(1,2), max_features=5000, sublinear_tf=True, min_df=2, max_df=0.95
  Vocabulary size: 5000 unique n-grams
  X_train_tfidf shape: (1754, 5000)
  X_test_tfidf shape:  (439, 5000)

StandardScaler on 15 aux features:
  X_train_aux_scaled: (1754, 15)
  X_test_aux_scaled:  (439, 15)

Final matrices (TF-IDF + Aux):
  X_train: (1754, 5015) — sparse CSR, 1251.0 KB
  X_test:  (439, 5015)  — sparse CSR, 302.4 KB

Exported artifacts (all < 50MB):
  X_train.pkl: 1251.0 KB
  X_test.pkl: 302.4 KB
  y_train.pkl: 55.6 KB
  y_test.pkl: 14.5 KB
  tfidf_vectorizer.pkl: 198.3 KB
  aux_scaler.pkl: 0.9 KB
  feature_names.json: 80.5 KB (5015 names)

EDA: 7 PNG figures @ 300 DPI generated in 2.4s
Notebook: 30/30 cells executed, 0 errors, 29.5 KB

Tests: 34/34 PASSED (13 new + 21 existing) in 2.09s
verify_final.py: exit code 0, all checks PASSED
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **Phase 03 PASSED** (15/09/2026). Đã triển khai thành công toàn bộ EDA Notebook (30 cells, 7 biểu đồ 300 DPI) và Zero-Leakage Feature Engineering Pipeline. **Lỗi nghiêm trọng trong bản nháp cũ** (fit TF-IDF trên toàn bộ dataset trước khi split) đã được phát hiện và sửa triệt để: pipeline mới thực hiện Stratified Split 80/20 ĐẦU TIÊN, rồi mới fit TF-IDF/Scaler CHỈ trên tập Train. Ma trận `X_train (1754×5015)` và `X_test (439×5015)` đã được xuất và sẵn sàng cho các thành viên Phase 04 (Cẩm/NB, SVM), Phase 05 (Sơn/RF). 34/34 unit tests PASSED. Mọi module src/ tuân thủ quy tắc ≤200 dòng.

## Commit

```bash
git add notebooks/02_eda.ipynb src/feature_engineering.py src/feature_engineering_config.py \
    src/eda_visualizations.py src/eda_plots_part1.py src/eda_plots_part2.py \
    reports/figures/ tests/test_feature_engineering.py data/processed/
git commit -m "feat(phase03): EDA complete, zero-leakage TF-IDF+aux pipeline, 7 figures, 34 tests pass"
```
