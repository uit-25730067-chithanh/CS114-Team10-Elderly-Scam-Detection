---
title: Refinement and Hard Review of Presentation Slides
date: 2026-09-21
summary: Tong hop 4 quyet dinh ky thuat va 5 chi dao nang cap bo 22 slide thuyet trinh giua Thanh va Cam
---

# Refinement and Hard Review of Presentation Slides (Phase 09)

## What happened
Trong quá trình hoàn thiện bộ slide bảo vệ đồ án cuối kỳ CS114 (18:30 23/09/2026), Bùi Thị Mỷ Cẩm (PPT Lead) đã tự động hóa việc sinh 20 slide bằng PptxGenJS (`generate_slides.js`) và bàn giao cho Đặng Chí Thanh (PM / Reviewer) kèm 4 vấn đề kỹ thuật còn vướng mắc:
1. Độ lệch ROC-AUC của Random Forest giữa log Phase 05 (99.76%) và biểu đồ ROC Phase 07 (99.77%).
2. Giá trị `alpha` của Naive Bayes bị ghi sai `0.5` trong `metrics_calculator.py` và tác giả ghi nhầm thành Thanh thay vì Cẩm.
3. Tài liệu tham khảo [4] trích dẫn bài IEEE Access 2026 chưa có DOI/tập chính thức.
4. Nguy cơ lỗi tệp PowerPoint nếu dùng script XML injection tạo hiệu ứng chuyển slide.

## Decisions & Outcomes
Thanh và Cẩm đã thống nhất giải quyết dứt điểm 4 vấn đề kỹ thuật và áp dụng 5 chỉ đạo nâng cấp:
1. **Chốt ROC-AUC Random Forest 99.77%:** Tính toán lại trên tập test thực tế đạt 0.997652... Đồng bộ `random_forest_metrics.json` để Slide 9 và 10 khớp 100%.
2. **Chuẩn hóa Naive Bayes alpha=0.01 & Tác giả Cẩm:** Sửa triệt để 4 vị trí mã nguồn (`metrics_calculator.py`, `model_comparison.csv`, `README.md`, `demo/app.py`).
3. **Liêm chính trích dẫn khoa học:** Gỡ bỏ định dạng trích dẫn giả, thay bằng link repo GitHub bộ dữ liệu SMS gốc và nguồn bổ sung.
4. **Hiệu ứng native an toàn:** Giữ slide nguyên bản, sử dụng Fade 0.3s native trên PowerPoint thay vì can thiệp XML.
5. **Nâng cấp toàn diện lên bộ 22 slide (PR #26):** Thêm Header/Footer nhận diện UIT và đánh số trang `NN / 22`, Slide Agenda 5 phần, chuẩn hóa tên đề tài, sắp xếp 15 tài liệu tham khảo 2 cột theo vòng đời nghiên cứu (PR #26 merged).
6. **Thực nghiệm Ablation & Chuẩn bị Q&A (PR #27):** Kiểm chứng loại bỏ các thẻ ẩn danh `[MONEY]`, `[NUMBER]` (F1 XGBoost giữ vững 0.9425), đính chính 4 luận điểm phản biện Q&A và hoàn thiện kịch bản 15 phút.

## Reference Reports
- Báo cáo thẩm định slide: `draft/scam-detection/reports/research-cam-phase09-ppt-slides-audit.md` (88/100 A-)
- Vòng đời tài liệu tham khảo: `draft/scam-detection/reports/research-cam-phase09-references-lifecycle.md`
- Kịch bản thuyết trình & Q&A: `draft/scam-detection/reports/slides/scripts/script.md`

> Historical work record — not durable authority. Prefer docs/specs/ADRs for current decisions.
