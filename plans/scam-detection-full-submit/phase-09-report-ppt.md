# Phase 09 — Report & PPT

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 08 — Demo UI](./phase-08-demo-ui.md)  
**Next phase:** [Phase 10 — Submit Package](./phase-10-submit-package.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Cả nhóm** |
| Priority | P1 |
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 8–12h |
| Sprint | Sprint 2–3 Fast-Track (14/09 – 22/09/2026) |

## Context

Viết báo cáo Word và slide PPT theo chuẩn yêu cầu CS114 của thầy Thăng. Nội dung phải dựa trên kết quả thực nghiệm (evidence-based).

## Report Structure (Word .docx)

Theo yêu cầu trong [README.md](../../README.md):

### Chương 1 — Đặt vấn đề

- Giới thiệu đề tài, bối cảnh lừa đảo NCT tại VN 2026
- Các khó khăn và thách thức
- Ý nghĩa thực tiễn

### Chương 2 — Các phương pháp tiếp cận

- Khảo sát các công trình liên quan (Related Works)
- So sánh các hướng tiếp cận: Rule-based vs ML vs Deep Learning
- Lý do chọn hướng ML + NLP tiếng Việt

### Chương 3 — Phương pháp nhóm chọn

- Pipeline tiền xử lý tiếng Việt
- Feature Engineering (TF-IDF + auxiliary)
- Mô tả 3+ models: NB, RF/XGB, SVM
- Kiến trúc tổng thể hệ thống

### Chương 4 — Thực nghiệm

#### 4.1. Dataset
- Mô tả dataset tự thu thập
- Phân bố class, scam categories
- Data augmentation (nếu có)

#### 4.2. Phương pháp đánh giá
- Metrics: Accuracy, Precision, Recall, F1, AUC-ROC
- K-Fold Cross Validation
- Train/Val/Test split strategy

#### 4.3. Kết quả đạt được
- Bảng so sánh tất cả models
- Confusion Matrix
- ROC Curves
- Learning Curves (Train vs Val — Overfitting)
- Precision-Recall Curves
- Top-20 từ khóa cảnh báo

### Chương 5 — Kết luận và Hướng phát triển

- Tóm tắt kết quả chính
- Hạn chế
- Hướng phát triển: PhoBERT, multimodal, mobile app

### Tài liệu tham khảo

- Định dạng IEEE hoặc APA
- Tối thiểu 10 tài liệu

## Slide PPT (15 phút)

| Slide # | Nội dung | Thời gian |
|---------|---------|-----------|
| 1 | Title slide | 30s |
| 2 | Đặt vấn đề & Ý nghĩa | 1.5 phút |
| 3-4 | Pipeline & Phương pháp | 3 phút |
| 5-6 | Dataset & Feature Engineering | 2 phút |
| 7-10 | Kết quả thực nghiệm (bảng, biểu đồ) | 4 phút |
| 11-12 | Demo UI screenshots | 2 phút |
| 13 | Kết luận & Hướng phát triển | 1 phút |
| 14 | Q&A | 1 phút |

## Fast-Track Tasks (Báo cáo sớm 23/09/2026)

- [ ] **Sprint 2 (14/09 – 18/09):** Viết sớm Báo cáo Word Chương 1 (Đặt vấn đề), Chương 2 (Khảo sát) + Chương 3 (Phương pháp) + Chuẩn bị khung Slide PPT 15 phút
- [ ] **Sprint 3 (19/09 – 20/09):** Báo cáo Word Chương 4 (Thực nghiệm — tích hợp số liệu từ Phase 07) + Chương 5 (Kết luận) + Hoàn thiện Slide PPT (14–16 slides)
- [ ] **Sprint 3 (21/09 – 22/09):** Diễn tập thuyết trình (≤15 phút) cả nhóm + Chuẩn bị câu hỏi Q&A phản biện của thầy Thăng
- [ ] **D-Day (23/09/2026):** Thuyết trình chính thức trước giảng viên ThS. Cáp Phạm Đình Thăng

## Checklist

- [ ] Chương 1 — Đặt vấn đề (≥2 trang)
- [ ] Chương 2 — Phương pháp tiếp cận (≥3 trang)
- [ ] Chương 3 — Phương pháp nhóm chọn (≥4 trang)
- [ ] Chương 4.1 — Dataset description
- [ ] Chương 4.2 — Phương pháp đánh giá
- [ ] Chương 4.3 — Kết quả (bảng + biểu đồ)
- [ ] Chương 5 — Kết luận & Hướng phát triển
- [ ] Tài liệu tham khảo (≥10 refs)
- [ ] File Word đúng định dạng (.docx)
- [ ] File PDF exported
- [ ] PPT 14-16 slides
- [ ] PPT có biểu đồ, screenshots demo
- [ ] Diễn tập thuyết trình ≤15 phút

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Word report | ≥15 trang, đầy đủ 5 chương |
| PPT | 14-16 slides, ≤15 phút |
| Figures embedded | Tất cả biểu đồ từ Phase 07 |
| References | ≥10 tài liệu tham khảo |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add submit/DOCS/ submit/SLIDES/
git commit -m "feat(phase09): report Word + PPT complete"
```
