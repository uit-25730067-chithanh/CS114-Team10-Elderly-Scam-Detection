# Phase 09 — Report & PPT

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 08 — Demo UI](./phase-08-demo-ui.md)  
**Next phase:** [Phase 10 — Submit Package](./phase-10-submit-package.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **PPT: Cẩm (25730013) · Report: Sơn (25730061) · Review/Merge: Thanh (25730067)** |
| Priority | P1 |
| Status | `in-progress` |
| Review | 🟡 Template branches tạo xong — chờ thành viên tạo PR |
| Estimated effort | 8–12h |
| Sprint | Sprint 2–3 Fast-Track (15/09 – 22/09/2026) |

## Branches (đã tạo — chưa tạo PR)

| Branch | Owner | Mục đích | Trạng thái |
|--------|-------|---------|-----------|
| `feat/phase-09-ppt-template` | **Cẩm** tạo PR | PPT template + `generate_slides.js` | Template ready ✅ — chờ Cẩm hoàn thiện |
| `feat/phase-09-report-template` | **Sơn** tạo PR | Report Markdown template → .docx | Template ready ✅ — chờ Sơn hoàn thiện |

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

#### 4.1. Dataset & Phân tích Khám phá (EDA)
- Mô tả bộ dữ liệu 2.193 mẫu thực tế (100% Zero Synthetic Text, 0% rò rỉ PII, 7 tầng kiểm toán).
- Phân bố 4 nhóm bẫy tâm lý: Đe dọa quyền lực (127), Thúc ép khẩn cấp gia đình (88), Dụ dỗ quà tặng sức khỏe (46), Giả mạo dịch vụ công (159).
- Chiến lược phân chia dữ liệu Zero-Leakage: Stratified Split 80/20 (1.754 Train / 439 Test).
- 7 biểu đồ trực quan hóa khám phá dữ liệu chuẩn 300 DPI (`reports/figures/`):
  1. `label_distribution.png` — Phân bố nhãn & tỷ lệ mất cân bằng (4.2 : 1).
  2. `scam_category_distribution.png` — Cơ cấu 4 nhóm bẫy tâm lý.
  3. `text_length_comparison.png` — Biểu đồ phân bố độ dài ký tự và số lượng từ.
  4. `wordcloud_scam_vs_normal.png` — Đám mây từ vựng phân tách lừa đảo vs tin thường.
  5. `top_ngrams_scam_vs_normal.png` — Top-20 N-grams có tần suất chênh lệch mạnh nhất.
  6. `auxiliary_correlation_heatmap.png` — Ma trận tương quan 15 đặc trưng phụ với nhãn lừa đảo.
  7. `source_distribution.png` — Phân bố các nguồn dữ liệu chính thống.
- Không gian vector đặc trưng: 5.015 chiều (5.000 TF-IDF N-gram 1-2 + 15 đặc trưng phụ qua StandardScaler fit duy nhất trên Train).

#### 4.2. Phương pháp đánh giá
- Metrics: Accuracy, Precision, Recall, F1, AUC-ROC
- K-Fold Cross Validation
- Train/Val/Test split strategy

#### 4.3. Kết quả đạt được (Test Set: 439 mẫu — 355 Normal / 84 Scam)
- **Bảng so sánh hiệu năng các mô hình đã nghiệm thu:**

| Mô hình | Đặc trưng | Hyperparameters | Accuracy | Precision | Recall (Lừa đảo) | F1-Score | ROC-AUC | Ghi chú |
|---|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **XGBoost** | 5.015 (TF-IDF + 15 aux) | `n_est=300, depth=5, lr=0.05, subsample=0.7, colsample=0.8, scale_pos_weight=4.22` | **98.18%** | **93.18%** | **97.62%** | **0.9535** | 0.9984 | Best Overall Model, FN=2, FP=6 (Phase 05 — Cẩm) |
| **SVM Linear** | 5.015 (TF-IDF + 15 aux) | `C=10.0` (CalibratedClassifierCV 5-fold) | 97.95% | **93.10%** | 96.43% | **0.9474** | **0.9986** | Best Linear Model, FN=3, FP=6 (Phase 06 — Cẩm) |
| **Random Forest** | 5.015 (TF-IDF + 15 aux) | `n_est=200, depth=50, split=2, leaf=2, max_feat=0.2` | 97.72% | 91.11% | **97.62%** | 0.9425 | 0.9977 | Best Tree Ensemble, FN=2, FP=8 (Phase 05 — Sơn) |
| **MultinomialNB** | 5.000 (TF-IDF non-negative) | `alpha=0.01` (GridSearchCV 5-fold) | 95.44% | 84.78% | 92.86% | 0.8864 | 0.9911 | Baseline vượt F1≥0.88, FN=6, FP=14 (Phase 04 — Cẩm) |

- **Hệ thống 28 biểu đồ trực quan hóa chuẩn 300 DPI (`reports/figures/`):**
  - **7 Biểu đồ EDA (Phase 03):** `label_distribution.png`, `scam_category_distribution.png`, `text_length_comparison.png`, `wordcloud_scam_vs_normal.png`, `top_ngrams_scam_vs_normal.png`, `auxiliary_correlation_heatmap.png`, `source_distribution.png`.
  - **15 Biểu đồ đơn mô hình (Phase 04–06):** Confusion Matrix, ROC curve, Learning curve, Feature Importance của từng mô hình (NB, RF, XGB, Linear SVM).
  - **6 Biểu đồ so sánh tổng hợp & XAI (Phase 07 — Thanh):**
    - `confusion_matrices_all.png`: Lưới 2×2 ma trận nhầm lẫn so sánh trực tiếp FN/FP của cả 4 mô hình.
    - `roc_curves_comparison.png`: 4 đường cong ROC lồng ghép (AUC: 0.9911 → 0.9986).
    - `precision_recall_curves.png`: 4 đường Precision-Recall chứng minh duy trì Precision > 90% ở Recall > 95%.
    - `learning_curves_summary.png`: Lưới 2×2 đường cong học tập 5-fold CV chứng minh kiểm soát quá khớp tối ưu.
    - `top20_keywords_barplot.png`: Biểu đồ ngang 20 từ khóa kích hoạt bẫy tâm lý có trọng số đồng thuận cao nhất (`money`, `số_tiền`, `viện_phí`, `gấp`, `số_định_danh`).
    - `shap_summary.png`: Biểu đồ SHAP Beeswarm của XGBoost giải thích đóng góp vi mô từng giá trị đặc trưng.

#### 4.4. Ứng dụng Thực tế & Giao diện Web Demo (Phase 08 — Sơn)
- Ứng dụng Streamlit Split-View Workbench tối ưu trợ năng cho người cao tuổi:
  - Phóng đại cỡ chữ linh hoạt 100% – 125% – 150% với tỷ lệ tương phản cao.
  - Tự động phân tích và bôi đỏ từ khóa bẫy tâm lý với regex biên dịch trước (<10ms).
  - Hộp quy tắc sinh tồn "3 KHÔNG & 1 GỌI", Hotline 1-chạm 156 (Cục ATTT) và 113 (Công an).
  - Tích hợp bộ điều phối 4 mô hình học máy (XGBoost F1=0.9535 mặc định, Linear SVM, RF, NB).
  - Tích hợp Web Clipboard API dán 1-chạm và bảo lưu kết quả qua URL query params (`?text=...`).
- 4 Ảnh chụp màn hình nghiệm thu chuẩn 300 DPI (`reports/figures/`):
  1. `demo_01_initial_layout.png` — Bố cục tổng thể Desktop Workbench hai cột.
  2. `demo_02_font_scaling_elderly.png` — Chế độ phóng đại cỡ chữ 150% cho người cao tuổi.
  3. `demo_03_scam_detection_verdict.png` — Cảnh báo bẫy lừa đảo đe dọa quyền lực và Hotline 156.
  4. `demo_04_mobile_responsive.png` — Giao diện co dãn mượt mà trên điện thoại di động (390×844 px).

### Chương 5 — Kết luận và Hướng phát triển

- Tóm tắt kết quả chính
- Hạn chế
- Hướng phát triển: PhoBERT, multimodal, mobile app

### Tài liệu tham khảo

- Định dạng IEEE hoặc APA
- Tối thiểu 10 tài liệu

## Slide PPT (15 phút)

| Slide # | Nội dung | Thời gian | Phụ trách chính |
|---------|---------|-----------|-----------------|
| 1 | Title slide | 30s | Đặng Chí Thanh |
| 2 | Đặt vấn đề & Ý nghĩa | 1.5 phút | Đặng Chí Thanh |
| 3-4 | Pipeline & Phương pháp | 3 phút | Đặng Chí Thanh |
| 5-6 | Dataset & Feature Engineering | 2 phút | Đặng Chí Thanh |
| 7-10 | Kết quả thực nghiệm (bảng, biểu đồ) | 4 phút | Bùi Thị Mỷ Cẩm |
| 11-12 | Demo Web App Streamlit (Screenshots demo_01→04, Trợ năng NCT, Hotline, Đa mô hình) | 2 phút | Hoàng Cao Sơn |
| 13 | Kết luận & Hướng phát triển | 1 phút | Hoàng Cao Sơn |
| 14 | Q&A | 1 phút | Cả nhóm |

## Fast-Track Tasks (Báo cáo sớm 23/09/2026)

- [ ] **Sprint 2 (15/09 – 18/09):** Viết sớm Báo cáo Word Chương 1 (Đặt vấn đề), Chương 2 (Khảo sát) + Chương 3 (Phương pháp) + Chuẩn bị khung Slide PPT 15 phút
- [ ] **Sprint 3 (19/09 – 20/09):** Báo cáo Word Chương 4 (Thực nghiệm — tích hợp số liệu từ Phase 07) + Chương 5 (Kết luận) + Hoàn thiện Slide PPT (14–16 slides)
- [ ] **Sprint 3 (21/09 – 22/09):** Diễn tập thuyết trình (≤15 phút) cả nhóm + Chuẩn bị câu hỏi Q&A phản biện của thầy Thăng
- [ ] **D-Day (18:30 23/09/2026):** Thuyết trình trực tuyến MS Teams, luân phiên cả 3 thành viên trước ThS. Cáp Phạm Đình Thăng

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
