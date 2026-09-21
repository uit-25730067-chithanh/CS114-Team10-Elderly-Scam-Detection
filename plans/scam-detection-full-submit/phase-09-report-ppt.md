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
| Review | 🟡 Khối Slide & Kịch bản hoàn tất (PR #26 merged, PR #27 open); Báo cáo Word đang hoàn thiện |
| Estimated effort | 8–12h |
| Sprint | Sprint 2–3 Fast-Track (15/09 – 22/09/2026) |

## Branches & Templates bàn giao

| Branch | Owner | File template cốt lõi | Trạng thái |
|--------|-------|----------------------|-----------|
| `feat/phase-09-ppt-template` | **Cẩm** tạo PR | [`SLIDE_OUTLINE.md`](../../draft/scam-detection/reports/slides/SLIDE_OUTLINE.md) · [`generate_slides.js`](../../draft/scam-detection/reports/slides/generate_slides.js) | Hoàn tất ✅ — PR #26 đã merge vào main (22 slide, 3.4 MB PPTX/PDF) |
| `feat/phase-09-presentation-script` | **Thanh** tạo PR | [`script.md`](../../draft/scam-detection/reports/slides/scripts/script.md) (51 KB) | Hoàn tất ✅ — PR #27 kịch bản 15p chuẩn WPM & 10 chủ đề Q&A |
| `feat/phase-09-report-template` | **Sơn** tạo PR | `REPORT_OUTLINE.md` · `report-source.md` · `report-meta.yaml` | Đang triển khai 🟡 — Sơn biên soạn 5 chương trên branch |

## Context

Viết báo cáo Word và slide PPT theo chuẩn yêu cầu CS114 của thầy Thăng. Nội dung phải dựa trên kết quả thực nghiệm (evidence-based).

## Report Structure (Word .docx)

Theo yêu cầu trong [README.md](../../README.md):

### Chương 1 — Đặt vấn đề
- Giới thiệu đề tài, bối cảnh lừa đảo trực tuyến nhắm vào người cao tuổi tại VN 2025–2026.
- Các khó khăn và thách thức (thiếu hụt dữ liệu thực tế, kỹ thuật thao túng tâm lý tinh vi).
- Ý nghĩa thực tiễn và mục tiêu đề tài.
- *Nguồn tham chiếu đề xuất:* [phase-01-thanh-normal-dataset.md](./phase-01-thanh-normal-dataset.md), Báo cáo Cục An toàn thông tin, Cổng TTĐT Bộ Công an.

### Chương 2 — Các phương pháp tiếp cận
- Khảo sát các công trình liên quan (Related Works) về phát hiện SMS/Email phishing, tin nhắn rác tiếng Việt.
- So sánh các hướng tiếp cận: Rule-based (heuristic/regex) vs Machine Learning truyền thống vs Deep Learning / Transformers (PhoBERT).
- Lý do chọn hướng Machine Learning kết hợp trích xuất đặc trưng NLP tiếng Việt (nhẹ, inference <50ms, giải thích minh bạch với SHAP cho người cao tuổi).

### Chương 3 — Phương pháp nhóm chọn
- Pipeline tiền xử lý tiếng Việt: Chuẩn hóa Unicode NFC, Regex 160 teencode rules, PyVi word segmentation (tham chiếu [phase-02-preprocess-vietnamese.md](./phase-02-preprocess-vietnamese.md)).
- Trích xuất đặc trưng: TF-IDF 5.000 n-grams (1,2) + 15 đặc trưng phụ (auxiliary) = Không gian 5.015 chiều; Zero-leakage StandardScaler (tham chiếu [phase-03-feature-engineering.md](./phase-03-feature-engineering.md)).
- Mô tả 4 mô hình: MultinomialNB ([phase-04](./phase-04-model-naive-bayes.md)), Random Forest & XGBoost ([phase-05](./phase-05-model-rf-xgboost.md)), Calibrated Linear SVM ([phase-06](./phase-06-model-svm-phobert.md)).
- Kiến trúc tổng thể hệ thống từ đầu vào tin nhắn thô đến phân loại bẫy tâm lý.

### Chương 4 — Thực nghiệm

#### 4.1. Dataset & Phân tích Khám phá (EDA)
- Mô tả bộ dữ liệu 2.193 mẫu thực tế (100% Zero Synthetic Text, 0% rò rỉ PII, 7 tầng kiểm toán).
- Phân bố 4 nhóm bẫy tâm lý: Đe dọa quyền lực (127), Thúc ép khẩn cấp gia đình (88), Dụ dỗ quà tặng sức khỏe (46), Giả mạo dịch vụ công (159).
- Chiến lược phân chia dữ liệu Zero-Leakage: Stratified Split 80/20 (1.754 Train / 439 Test).
- 7 biểu đồ trực quan hóa khám phá dữ liệu chuẩn 300 DPI (`draft/scam-detection/reports/figures/`):
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

- **Hệ thống 28 biểu đồ trực quan hóa mô hình chuẩn 300 DPI (kết hợp 4 ảnh demo ở Mục 4.4 tạo thành hệ thống 32 hình ảnh chuẩn của dự án tại `draft/scam-detection/reports/figures/`):**
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
- 4 Ảnh chụp màn hình nghiệm thu chuẩn 300 DPI (`draft/scam-detection/reports/figures/`):
  1. `demo_01_initial_layout.png` — Bố cục tổng thể Desktop Workbench hai cột.
  2. `demo_02_font_scaling_elderly.png` — Chế độ phóng đại cỡ chữ 150% cho người cao tuổi.
  3. `demo_03_scam_detection_verdict.png` — Cảnh báo bẫy lừa đảo đe dọa quyền lực và Hotline 156.
  4. `demo_04_mobile_responsive.png` — Giao diện co dãn mượt mà trên điện thoại di động (390×844 px).

### Chương 5 — Kết luận và Hướng phát triển
- Tóm tắt kết quả chính: Bộ dataset 2.193 mẫu 100% thực tế, pipeline 5.015 chiều, XGBoost đạt F1=0.9535 và Recall=97.62%, Web demo hoàn chỉnh.
- Hạn chế: Kích thước dữ liệu bẫy quà tặng sức khỏe còn khiêm tốn (46 mẫu); chưa tích hợp mô hình ngôn ngữ lớn (LLM) để đàm thoại trực tiếp.
- Hướng phát triển: PhoBERT finetuning, phát hiện đa phương thức (multimodal audio/voice call), ứng dụng di động Flutter/React Native.

### Tài liệu tham khảo (Chuẩn IEEE — ≥10 tài liệu đề xuất)
1. T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining*, 2016, pp. 785–794.
2. L. Breiman, "Random forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
3. C. Cortes and V. Vapnik, "Support-vector networks," *Machine Learning*, vol. 20, no. 3, pp. 273–297, 1995.
4. S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2017, pp. 4765–4774.
5. F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *J. Mach. Learn. Res.*, vol. 12, pp. 2825–2830, 2011.
6. D. Q. Nguyen and A. T. Nguyen, "PhoBERT: Pre-trained language models for Vietnamese," in *Findings of EMNLP*, 2020, pp. 1037–1042.
7. T. Fawcett, "An introduction to ROC analysis," *Pattern Recognit. Lett.*, vol. 27, no. 8, pp. 861–874, 2006.
8. Cục An toàn thông tin — Bộ TT&TT, "Báo cáo thường niên tình hình an toàn thông tin mạng và lừa đảo trực tuyến tại Việt Nam," Hà Nội, 2025.
9. Cục Cảnh sát hình sự — Bộ Công an, "Cẩm nang nhận diện và phòng ngừa các thủ đoạn lừa đảo chiếm đoạt tài sản trên không gian mạng," 2025–2026.
10. A. K. Jain, "Data clustering: 50 years beyond K-means," *Pattern Recognit. Lett.*, vol. 31, no. 8, pp. 651–666, 2010.

## Slide PPT (22 slides — 15 phút)

| Slide # | Loại slide | Nội dung chính | Thời lượng | Phụ trách |
|:---:|---|---|:---:|---|
| **1** | Title | Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào NCT | 30s | Đặng Chí Thanh |
| **2** | Agenda | Lộ trình báo cáo 5 phần & Phụ lục Q&A | 20s | Đặng Chí Thanh |
| **3** | Stat callout | PHẦN 1: Bối cảnh lừa đảo NCT tại VN 2026 (420 mẫu lừa đảo, Zero Synthetic Text) | 1.5 phút | Đặng Chí Thanh |
| **4** | Icon grid | PHẦN 1: Mục tiêu đề tài & 4 đóng góp chính (F1≥88%, Recall≥92%, XAI, Demo) | 1.5 phút | Đặng Chí Thanh |
| **5** | Section divider | Divider PHẦN 2: Dữ liệu & Phương pháp tiếp cận | 15s | Đặng Chí Thanh |
| **6** | Text + Image | PHẦN 2: Bộ dữ liệu 2.193 mẫu thực tế (Stratified 80/20, 7 tầng kiểm toán) | 1.5 phút | Đặng Chí Thanh |
| **7** | Two-column | PHẦN 2: Cơ cấu 4 nhóm bẫy tâm lý (Dịch vụ công, Quyền lực, Gia đình, Quà tặng) | 1.5 phút | Đặng Chí Thanh |
| **8** | Full diagram | PHẦN 2: Pipeline tiền xử lý tiếng Việt & Không gian vector 5.015 chiều | 1.5 phút | Đặng Chí Thanh |
| **9** | Section divider | Divider PHẦN 3: Mô hình hóa & Kết quả thực nghiệm | 15s | Bùi Thị Mỷ Cẩm |
| **10** | Table comparison | PHẦN 3: Bảng so sánh 4 mô hình (XGBoost F1=0.9535, Linear SVM F1=0.9474) | 1.5 phút | Bùi Thị Mỷ Cẩm |
| **11** | Two-column image | PHẦN 3: Đường cong ROC & Precision-Recall lồng ghép (AUC 0.9911 → 0.9986) | 1.5 phút | Bùi Thị Mỷ Cẩm |
| **12** | Two-column image | PHẦN 3: Giải thích mô hình XAI với SHAP Beeswarm & Top từ khóa quan trọng | 1.5 phút | Bùi Thị Mỷ Cẩm |
| **13** | Section divider | Divider PHẦN 4: Ứng dụng thực tế & Giao diện Demo | 15s | Hoàng Cao Sơn |
| **14** | Multi-image demo | PHẦN 4: Streamlit Web App Split-View Workbench & Trợ năng NCT (Hotline 156/113) | 2 phút | Hoàng Cao Sơn |
| **15** | Section divider | Divider PHẦN 5: Kết luận & Hướng phát triển | 15s | Hoàng Cao Sơn |
| **16** | Two-column | PHẦN 5: Kết luận, Đóng góp chính & Hạn chế đề tài | 1.5 phút | Hoàng Cao Sơn |
| **17** | References (2-col)| PHẦN 5: 15 Tài liệu tham khảo theo chu trình vòng đời đề tài | 1 phút | Hoàng Cao Sơn |
| **18** | Closing | PHẦN 5: Lời cảm ơn chuẩn UIT, Thông tin liên hệ & Q&A | 30s | Hoàng Cao Sơn |
| **19** | Section divider | Divider PHỤ LỤC: Backup Slides & Phản biện kỹ thuật | Q&A | Cả nhóm |
| **20** | Table | Backup 1: Chi tiết Siêu tham số và Không gian Tuning | Q&A | Cả nhóm |
| **21** | Image + text | Backup 2: Ma trận nhầm lẫn 2×2 chi tiết 4 mô hình (XGB FN=2, SVM FN=3) | Q&A | Cả nhóm |
| **22** | Image + text | Backup 3: Đường cong học tập 5-fold CV kiểm soát quá khớp | Q&A | Cả nhóm |

## Fast-Track Tasks (Báo cáo sớm 23/09/2026)

- [x] **Sprint 2 (15/09 – 18/09):** Khung Slide PPT, hoàn tất huấn luyện 4 mô hình và trích xuất bảng metrics
- [x] **Sprint 3 (19/09 – 21/09):** Hoàn thiện Slide PPT 22 trang (PR #26 merged) + Kịch bản thuyết trình 15p & 10 chủ đề Q&A (PR #27)
- [ ] **Sprint 3 (21/09 – 22/09):** Báo cáo Word Chương 1–5 (Sơn lead) + Diễn tập thuyết trình (≤15 phút) cả nhóm
- [ ] **D-Day (18:30 23/09/2026):** Thuyết trình trực tuyến MS Teams, luân phiên cả 3 thành viên trước ThS. Cáp Phạm Đình Thăng

## Checklist

- [ ] Chương 1 — Đặt vấn đề (≥2 trang)
- [ ] Chương 2 — Phương pháp tiếp cận (≥3 trang)
- [ ] Chương 3 — Phương pháp nhóm chọn (≥4 trang)
- [ ] Chương 4.1 — Dataset description
- [ ] Chương 4.2 — Phương pháp đánh giá
- [ ] Chương 4.3 — Kết quả (bảng + biểu đồ)
- [ ] Chương 5 — Kết luận & Hướng phát triển
- [ ] Tài liệu tham khảo (≥10 refs IEEE)
- [ ] File Word đúng định dạng (.docx)
- [ ] File PDF exported
- [x] PPT 22 slides (15 chính + 1 Agenda + 5 dividers + 3 backup) — `phase09_presentation.pptx` (3.4 MB) & PDF, merged qua PR #26
- [x] Kịch bản thuyết trình bảo vệ 15 phút (`script.md`, 51 KB) bám sát 22 slide, phân vai chuẩn WPM & 10 chủ đề Q&A (PR #27)
- [x] PPT có biểu đồ, screenshots demo
- [ ] Diễn tập thuyết trình ≤15 phút

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Word report | ≥15 trang, đầy đủ 5 chương |
| PPT | 22 slides (15 chính + 1 Agenda + 5 dividers + 3 backup), ≤15 phút |
| Figures embedded | Tất cả 32 biểu đồ từ Phase 03–08 (`draft/scam-detection/reports/figures/`) |
| References | 15 tài liệu tham khảo theo vòng đời đề tài chuẩn IEEE/APA |

## Evidence Section

```
[✓] Branch checked out & pulled: feat/phase-09-ppt-template (commit 597ce72)
[✓] Generator Script: draft/scam-detection/reports/slides/generate_slides.js (883 lines PptxGenJS)
[✓] Presentation Deck: draft/scam-detection/reports/slides/phase09_presentation.pptx (3.4 MB, 22 slides)
[✓] Overlap Checker: .agents/skills/powerpoint-slides/scripts/check_overlaps.py -> OK: no overlap or boundary issues found (0 critical, 0 major, 0 warnings)
[✓] Typography & Bounds Audit: Cambria / Calibri, 0 overflow elements, max_bottom <= 5.56" (SH = 5.625", footer y=5.18, h=0.36)
[✓] Research Audit Document: draft/scam-detection/reports/research-cam-phase09-ppt-slides-audit.md (88/100 A-) & research-cam-phase09-references-lifecycle.md
[✓] Work History Journal: plans/journals/2026-09-21-refinement-and-hard-review-of-presentation-slides.md
[✓] 10 Q&A Defenses for ThS. Cáp Phạm Đình Thăng prepared & evidence-backed
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> 🟢 **PPT Template Finalized (22 Slides):** Đã hoàn tất kiểm toán chuyên sâu và tinh chỉnh hoàn thiện bộ 22 slide của em Cẩm. Đã xử lý triệt để 4 quyết định kỹ thuật (RF ROC-AUC 99.77%, NB alpha=0.01 & Cẩm là tác giả Phase 04, gỡ citation giả, giữ nguyên bản transition native), áp dụng trọn vẹn 5 chỉ đạo nâng cấp (Header/Footer/Số trang NN/22, Agenda 2 cột 5 phần, 15 tài liệu tham khảo theo vòng đời 2 cột, Lời cảm ơn chuẩn UIT). Bố cục đã được kiểm định qua `check_overlaps.py` đạt chuẩn sạch 100% không lỗi tràn lề. Đã xuất bản PDF phục vụ quan sát trực quan. Sẵn sàng nghiệm thu và bảo vệ.

## Commit

```bash
git add draft/scam-detection/reports/slides/ draft/scam-detection/reports/report/
git commit -m "feat(phase09): report Word + PPT complete"
```
