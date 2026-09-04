---
title: "CS114 Final — Scam Detection Full Implementation to Submit"
description: "End-to-end implementation plan: từ code rỗng đến bản nộp hoàn chỉnh, chia theo phase độc lập có validation gate"
status: in-progress
priority: P1
effort: ~40h (nhóm 10 — 3 người)
branch: main
tags: [cs114, scam-detection, academic, python, ml, nlp, submit]
created: 2026-09-04
updated: 2026-09-04
sprints: 4 sprints | Bắt đầu ~06/9 | Deadline 13/10/2026
---

# Plan: CS114 Final — Vietnamese Elderly Scam Detection Full Submit

## Mục tiêu

Từ skeleton ban đầu → hoàn thiện từng phase có kiểm định nghiêm ngặt:
`25730067-25730013-25730061.zip` với đủ: code, notebooks, báo cáo Word, PPT, demo Streamlit.

## Sprint Timeline

| Sprint | Thời gian | Mục tiêu chính |
|--------|----------|---------------|
| **Sprint 1** | 06/9 – 15/9 | Setup repo + Scaffold (Phase 00 Passed ✅), Thu thập & Gán nhãn Dataset (Phase 01) |
| **Sprint 2** | 15/9 – 25/9 | Tiền xử lý tiếng Việt, EDA, Feature Engineering, Huấn luyện Naive Bayes baseline |
| **Sprint 3** | 25/9 – 05/10 | Huấn luyện RF/XGBoost + SVM, Evaluation & So sánh, Demo UI shell |
| **Sprint 4** | 05/10 – 13/10 | XAI/SHAP, Demo tích hợp model, Báo cáo & PPT hoàn thiện, Đóng gói nộp bài |

## Constraints

- Dataset: `dataset.csv` — tự thu thập 1500-3000 mẫu tiếng Việt, gán nhãn thủ công
- Tech: Python 3.10+, scikit-learn, xgboost, pyvi/underthesea, streamlit
- Không dùng Computer Vision, không làm Fraud Detection ngân hàng (tránh trùng CS106)
- Phase phải passed validation gate trước khi chuyển tiếp
- Tóm lược phase viết **sau khi code xong** (evidence-based, không phải plan)
- `RANDOM_STATE = 42` set trong mọi script

## Phase Overview

| # | Phase | Owner | Sprint | Status | Gate |
|---|-------|-------|--------|--------|------|
| 00 | [Environment & Data Setup](./phase-00-env-data-setup.md) | **Thanh** | Sprint 1 | `passed` ✅ | Venv OK, utils helpers, template CSV ready, verify_final.py passed |
| 01 | [Data Collection & Labeling](./phase-01-data-collection-labeling.md) | **Sơn** (lead) + cả nhóm | Sprint 1 | `not-started` | ≥1500 mẫu, 4 scam categories labeled |
| 02 | [Vietnamese Text Preprocessing](./phase-02-vietnamese-text-preprocessing.md) | **Thanh** | Sprint 2 | `not-started` | Unicode normalized, tokenized, cleaned text |
| 03 | [EDA & Feature Engineering](./phase-03-eda-feature-engineering.md) | **Thanh** | Sprint 2 | `not-started` | TF-IDF matrix saved, EDA notebook complete |
| 04 | [Modeling — Naive Bayes Baseline](./phase-04-model-naive-bayes.md) | **Cẩm** | Sprint 2 | `not-started` | NB trained, baseline metrics recorded |
| 05 | [Modeling — Random Forest & XGBoost](./phase-05-model-rf-xgboost.md) | **Sơn** (RF) + **Cẩm** (XGB) | Sprint 3 | `not-started` | RF+XGB trained, hypertuned, metrics > NB |
| 06 | [Modeling — SVM (Optional: PhoBERT)](./phase-06-model-svm-phobert.md) | **Cẩm** | Sprint 3 | `not-started` | SVM trained, all 3+ models compared |
| 07 | [Evaluation & XAI](./phase-07-evaluation-xai.md) | **Thanh** | Sprint 3–4 | `not-started` | Confusion Matrix, Learning Curves, SHAP top-20 keywords |
| 08 | [Demo UI](./phase-08-demo-ui.md) | **Sơn** (lead) + **Cẩm** | Sprint 3–4 | `not-started` | Streamlit app chạy, model integrated |
| 09 | [Report & PPT](./phase-09-report-ppt.md) | **Cả nhóm** | Sprint 2–4 | `not-started` | Word + PPT hoàn chỉnh theo chuẩn CS114 |
| 10 | [Submit Package](./phase-10-submit-package.md) | **Thanh** | Sprint 4 | `not-started` | 25730067-25730013-25730061.zip đúng cấu trúc |

## Git Convention

- Làm riêng → 1 commit gộp cuối mỗi phase: `feat(phaseXX): <description>`
- Không commit: `data/raw/*.csv`, `.venv/`, `__pycache__/`, `*.pkl > 50MB`

## Validation Rules (áp dụng cho mọi phase)

Một phase được coi là **PASSED** khi:
1. ✅ Tất cả checklist items trong phase file được tick
2. ✅ Evidence section điền đầy đủ (output thực tế, không phải expected)
3. ✅ Summary section viết dựa trên code đã làm (không phải plan)
4. ❌ Nếu bất kỳ item nào FAIL → phase chưa passed, không chuyển tiếp

## Acceptance Criteria (Theo BRAINSTORM.md)

| Criterion | Target |
|-----------|--------|
| F1-Score | ≥ 88% |
| Recall lớp Lừa đảo | ≥ 92% |
| Số mô hình so sánh | ≥ 3 |
| Giải thích mô hình | Top 20 từ khóa cảnh báo (SHAP / Feature Weights) |
| Demo | Streamlit app chạy trên localhost |
