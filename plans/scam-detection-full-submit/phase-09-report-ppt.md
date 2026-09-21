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

## Branches & Templates bàn giao

| Branch | Owner | File template cốt lõi | Trạng thái |
|--------|-------|----------------------|-----------|
| `feat/phase-09-ppt-template` | **Cẩm** tạo PR | [`SLIDE_OUTLINE.md`](../../draft/scam-detection/reports/slides/SLIDE_OUTLINE.md) · [`generate_slides.js`](../../draft/scam-detection/reports/slides/generate_slides.js) | Template ready ✅ — chờ Cẩm hoàn thiện |
| `feat/phase-09-report-template` | **Sơn** tạo PR | [`REPORT_OUTLINE.md`](../../draft/scam-detection/reports/report/REPORT_OUTLINE.md) · [`report-source.md`](../../draft/scam-detection/reports/report/report-source.md) · [`report-meta.yaml`](../../draft/scam-detection/reports/report/report-meta.yaml) | Template ready ✅ — chờ Sơn hoàn thiện |

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

- **Hệ thống 28 biểu đồ trực quan hóa chuẩn 300 DPI (`draft/scam-detection/reports/figures/`):**
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

## Slide PPT (19 slides — 15 phút)

| Slide # | Loại slide | Nội dung chính | Thời lượng | Phụ trách |
|:---:|---|---|:---:|---|
| **1** | Title | Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào NCT | 30s | Đặng Chí Thanh |
| **2** | Stat callout | Bối cảnh & Vấn đề (420 mẫu lừa đảo, 4 nhóm bẫy tâm lý, Zero Synthetic Text) | 1.5 phút | Đặng Chí Thanh |
| **3** | Icon grid | Mục tiêu & Đóng góp (4 models, F1≥88%, SHAP XAI, Web Demo) | 1.5 phút | Đặng Chí Thanh |
| **4** | Section divider | Divider: Dữ liệu & Phương pháp | 15s | Đặng Chí Thanh |
| **5** | Text + Image | Dataset 2.193 mẫu thực tế (80/20 Stratified Split, 7 tầng kiểm toán) | 1.5 phút | Đặng Chí Thanh |
| **6** | Two-column | 4 nhóm bẫy tâm lý (Quyền lực 127, Gia đình 88, Quà tặng 46, Dịch vụ công 159) | 1.5 phút | Đặng Chí Thanh |
| **7** | Full diagram | Pipeline tiền xử lý tiếng Việt & Không gian vector 5.015 chiều | 1.5 phút | Đặng Chí Thanh |
| **8** | Section divider | Divider: Mô hình & Kết quả thực nghiệm | 15s | Bùi Thị Mỷ Cẩm |
| **9** | Table comparison | Bảng so sánh hiệu năng 4 mô hình (XGBoost F1=0.9535, Linear SVM F1=0.9474) | 1.5 phút | Bùi Thị Mỷ Cẩm |
| **10** | Two-column image | ROC Curves & Precision-Recall Curves đa mô hình (AUC 0.9911 → 0.9986) | 1.5 phút | Bùi Thị Mỷ Cẩm |
| **11** | Image + text | Confusion Matrix & Phân tích sai số (XGBoost FN=2, SVM FN=3) | 1 phút | Bùi Thị Mỷ Cẩm |
| **12** | Two-column image | Explainable AI: SHAP Beeswarm & Top-20 từ khóa bẫy tâm lý đồng thuận | 1.5 phút | Bùi Thị Mỷ Cẩm |
| **13** | Section divider | Divider: Ứng dụng & Trình diễn | 15s | Hoàng Cao Sơn |
| **14** | Multi-image demo | Streamlit Web App Demo & Tính năng trợ năng người cao tuổi (Hotline 156/113) | 2 phút | Hoàng Cao Sơn |
| **15** | Two-column | Kết luận & Hướng phát triển (PhoBERT, Mobile App) | 1 phút | Hoàng Cao Sơn |
| **16** | Section divider | Divider: Phụ lục & Backup Slides | — | Cả nhóm |
| **17** | Diagram/Card | Backup 1: Chi tiết kiến trúc Pipeline & 15 đặc trưng phụ | Q&A | Cả nhóm |
| **18** | Table | Backup 2: Chi tiết siêu tham số và không gian Tuning | Q&A | Cả nhóm |
| **19** | Closing | Backup 3: Lời cảm ơn, Q&A & Thông tin liên hệ | Q&A | Cả nhóm |

## Fast-Track Tasks (Báo cáo sớm 23/09/2026)

- [ ] **Sprint 2 (15/09 – 18/09):** Viết sớm Báo cáo Word Chương 1 (Đặt vấn đề), Chương 2 (Khảo sát) + Chương 3 (Phương pháp) + Chuẩn bị khung Slide PPT 15 phút
- [ ] **Sprint 3 (19/09 – 20/09):** Báo cáo Word Chương 4 (Thực nghiệm — tích hợp số liệu từ Phase 07) + Chương 5 (Kết luận) + Hoàn thiện Slide PPT (19 slides)
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
- [ ] Tài liệu tham khảo (≥10 refs IEEE)
- [ ] File Word đúng định dạng (.docx)
- [ ] File PDF exported
- [ ] PPT 19 slides (15 chính + 1 divider phụ lục + 3 backup) — *bản hiện tại 22 slide theo chỉ đạo của anh Thanh (Agenda + 5 PHẦN), khác bảng 19 slide ở trên, xem [Ghi chú bàn giao](#ghi-chú-bàn-giao-cho-anh-thanh-ppt--cẩm-21092026)*
- [x] PPT có biểu đồ, screenshots demo
- [ ] Diễn tập thuyết trình ≤15 phút

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Word report | ≥15 trang, đầy đủ 5 chương |
| PPT | 19 slides (15 chính + 1 divider + 3 backup), ≤15 phút |
| Figures embedded | Tất cả biểu đồ từ Phase 07 (`draft/scam-detection/reports/figures/`) |
| References | ≥10 tài liệu tham khảo chuẩn IEEE |

## Ghi chú bàn giao cho anh Thanh (PPT — Cẩm, 21/09/2026)

> Gửi anh Thanh (@25730067, reviewer Phase 09): bộ slide đã dựng xong bản đầu, có **4 vấn đề còn treo** cần anh xem trước khi bảo vệ 18:30 23/09. Chưa sửa gì ở các file dùng chung (README, demo, evaluator) vì cần anh/nhóm đồng ý.

**Trạng thái bộ slide:** `draft/scam-detection/reports/slides/generate_slides.js` → `phase09_presentation.pptx` (commit `1f6770e`, `07b4f2b`). Mọi chỉ số mô hình đọc trực tiếp từ `models/*_metrics.json`; mỗi slide có speaker notes; chưa có hiệu ứng chuyển slide;.

**Khác biệt so với bảng 19 slide ở trên (cần anh duyệt cấu trúc):** bản dựng có **20 slide** = 15 slide chính (có slide Tài liệu tham khảo) + Cảm ơn + divider phụ lục + 3 backup (Siêu tham số, Confusion Matrices, Learning Curves). Confusion Matrix chuyển sang backup; không có backup "Pipeline & 15 đặc trưng phụ" (pipeline nằm ở slide 7).

| # | Vấn đề | Cần anh làm |
|:-:|---|---|
| 1 | **ROC-AUC của Random Forest có 2 giá trị:** log Phase 05 (`random_forest_metrics.json`, raw 0.997552) = **99.76%**; `model_comparison.csv` và ảnh `roc_curves_comparison.png` (Phase 07 tính lại) = **99.77%**. Slide 9 dùng 99.76%, slide 10 hiện ảnh ghi 0.9977. | Chọn 1 giá trị chuẩn cho cả nhóm (anh là owner Phase 07). Slide 9 đã có câu trả lời Q&A trong speaker notes. |
| 2 | **`alpha` của Naive Bayes bị ghi sai `0.5`, giá trị đúng là `0.01`** (xem 4 chỗ bên dưới). | Đồng ý để sửa, sau đó sinh lại CSV bằng `run_full_evaluation.py`. |
| 3 | **Tài liệu tham khảo [4]** "Vietnamese Quality-Assured SMS Dataset, IEEE Access 2026 (doi pending)" là nguồn 1.773 mẫu bình thường — chưa xác minh được bài có tồn tại/đã xuất bản. | Xác minh tên bài, tác giả, link (anh thu thập nhóm dữ liệu này). Nếu không xác minh được: ghi "bộ dữ liệu công khai trên GitHub" kèm link thay vì trích dẫn IEEE. |
| 4 | **Hiệu ứng chuyển slide chưa áp dụng:** `inject_transitions.py` (morph/fracture) chưa kiểm chứng trên PowerPoint thật, có nguy cơ báo "file cần sửa chữa" lúc bảo vệ. | Tùy chọn: mở PowerPoint → chọn tất cả slide → tab Transitions → Fade → Apply To All. |

**Vấn đề 2 — 4 chỗ ghi `alpha=0.5` cần sửa thành `alpha=0.01` (và "Phase 04 — Thanh" thành "Phase 04 — Cẩm"):**

1. `draft/scam-detection/src/evaluation/metrics_calculator.py` dòng 44–45 — **gốc lỗi** (chuỗi gõ cứng trong `MODEL_METADATA`).
2. `draft/scam-detection/reports/model_comparison.csv` dòng 5 — được sinh ra từ mục 1 nên phải sửa mục 1 trước, nếu không lần chạy đánh giá sau sẽ ghi đè.
3. `README.md` (gốc repo) dòng 125 — bảng kết quả.
4. `draft/scam-detection/demo/app.py` dòng 92 — mô tả mô hình hiển thị cho người dùng demo.

Bằng chứng `0.01` đúng: `models/naive_bayes.pkl` lưu `alpha=0.01`; `naive_bayes_metrics.json` có `best_alpha: 0.01`; dựng lại mô hình trên X_train/X_test chỉ cho ra F1 0.8864 / FN=6 / FP=14 với `alpha=0.01` (với `alpha=0.5` F1 chỉ 0.8402, FN=13). Các tài liệu khác (AGENTS.md, plan Phase 04, `models/README.md`, hai báo cáo audit) đều đã ghi 0.01.

## Phản hồi thẩm định & Quyết định của anh Thanh (PM / Reviewer — 21/09/2026)

### 4 Quyết định Kỹ thuật Dứt điểm:
1. **Vấn đề 1 (ROC-AUC RF 99.76% vs 99.77%):** Đã đánh giá lại model artifact `random_forest.pkl` trên test set thực tế cho kết quả `0.99765258...` → **CHỐT 99.77%**. Cập nhật `random_forest_metrics.json` để Slide 9 và Slide 10 đồng nhất 100%.
2. **Vấn đề 2 (Naive Bayes alpha=0.01 & Tác giả Phase 04 — Cẩm):** **ĐỒNG Ý**. Sửa triệt để cả 4 vị trí (`metrics_calculator.py`, `model_comparison.csv`, `README.md`, `demo/app.py`).
3. **Vấn đề 3 (Trích dẫn [4] IEEE Access):** **XÓA BỎ TRÍCH DẪN GIẢ**. Thay bằng trích dẫn dataset thực tế / Báo cáo Cục ATTT trên Slide 15.
4. **Vấn đề 4 (Transitions):** **GIỮ NGUYÊN BẢN (KHÔNG DÙNG SCRIPT HACK XML)** để tránh lỗi file lúc bảo vệ; khi chiếu chỉ cần bật hiệu ứng Fade nhẹ 0.3s trên PowerPoint native.

### Trạng thái xử lý 4 quyết định (Cẩm, 21/09/2026):
1. **ROC-AUC RF — ✅ Đã xử lý:** Slide 9 đọc trực tiếp `random_forest_metrics.json` nên hiển thị **99.77%**, khớp chú thích 0.9977 trong ảnh ROC ở Slide 10. Cẩm tự tính lại `random_forest.pkl` trên tập test cho cùng kết quả `0.9976525821596244`. Đã dựng lại `phase09_presentation.pptx`.
2. **`alpha` Naive Bayes — ✅ Đã xác minh:** sau khi pull, cả 4 vị trí đã là `alpha=0.01`, tác giả Phase 04 là Cẩm; deck vốn đọc `0.01` từ `naive_bayes_metrics.json`.
3. **Trích dẫn [4] — ✅ Đã thay, kèm một hiệu chỉnh cần anh biết:** bỏ chữ "doi pending"; [4] nay trích đúng theo yêu cầu của tác giả bộ dữ liệu, kèm repo GitHub `trannguyenthaituan251209/vietnamese_sms_dataset` (1.944 mẫu: 1.773 bình thường + 171 lừa đảo; CC BY 4.0 theo README). Thêm [6] cho các nguồn bổ sung (249/420 mẫu lừa đảo: `lachancuocgoi`, `SMS_Phishing_Detection`, `ViSmish_Detection`, báo chí/VTV24), và Slide 5 trích dẫn [4], [6]. Không thêm "Báo cáo Cục ATTT" vì chưa có tên báo cáo và đường dẫn để kiểm chứng.
   - *Hiệu chỉnh so với báo cáo thẩm định:* README chính thức của repo bộ dữ liệu có mục Citation yêu cầu trích dẫn bài "Vietnamese SMS Dataset with Quality Assurance" (Tran, Le, Nguyen, Nguyen, Mai; IEEE Access, 2026, không ghi tập/DOI). Nên bài báo không phải placeholder do nhóm tự đặt; điều Cẩm không xác nhận được là bài đã xuất bản hay chưa, vì vậy [4] ghi "chưa có tập/DOI" và speaker notes Slide 15 dặn không khẳng định bài đã xuất bản.
4. **Transitions — ✅ Giữ nguyên:** không dùng script XML; nhắc bật Fade 0.3s (Transitions → Fade → Apply To All) trong speaker notes Slide 1.

### 5 Chỉ đạo Bổ sung & Định hướng Nâng cấp Slide gửi em Cẩm tự hoàn thiện:
1. **Header, Footer & Đánh số trang đồng bộ:** Toàn bộ slide nội dung cần Header (`TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN — ĐHQG-HCM`), Footer (`CS114: Máy học — Nhóm 10 — Báo cáo Đồ án: Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam`) và số trang định dạng `01 / 22`, `02 / 22`...
2. **Thống nhất tên đề tài chuẩn:** "Nghiên cứu và Xây dựng Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam" (loại bỏ hoàn toàn các biến thể như "Gian lận tài chính").
3. **Bổ sung Slide Lộ trình báo cáo (Agenda) & Đánh số phân đoạn:** Thêm Slide 2 Agenda 2 cột (5 phần chính + Phụ lục Q&A) và đánh số rõ ràng `PHẦN 1..5`.
4. **Sắp xếp Tài liệu tham khảo theo vòng đời dữ liệu / dự án:** Xếp 2 cột theo chu trình: Nguồn cào data → Tiền xử lý NLP → Thuật toán Học máy → XAI → Trợ năng Web → PhoBERT.
5. **Chuẩn hóa Lời cảm ơn:** `"CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE BÁO CÁO!"`.
- **Định hướng Slide vs Script:** Slide không cần cắt xén quá ngắn gọn. Slide đóng vai trò là "điểm tựa thị giác" (visual anchor) chứa đủ luận cứ khoa học để bổ trợ cho kịch bản nói (script) của speaker. Transition sẽ hoàn thiện đồng bộ sau cùng.

Toàn văn báo cáo thẩm định chuyên môn và phản biện xem tại:
- [`research-cam-phase09-ppt-slides-audit.md`](../../draft/scam-detection/reports/research-cam-phase09-ppt-slides-audit.md)

### Cập nhật bản 22 slide, trạng thái 5 chỉ đạo và hiệu chỉnh Q&A (Cẩm, 21/09/2026)

**Trạng thái 5 chỉ đạo của anh Thanh (deck `phase09_presentation.pptx`, 22 slide, 3,4 MB):**
1. **Header, footer, số trang — ✅:** header `TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN — ĐHQG-HCM` + nhãn PHẦN bên phải; footer 2 dòng cỡ 10pt đúng nội dung anh yêu cầu; số trang `NN / 22` tự tính theo tổng slide (không gõ tay). Chỉ áp dụng cho 15 slide nội dung; bìa, slide phân đoạn và slide cảm ơn để nền navy toàn khung.
2. **Tên đề tài chuẩn — ✅:** bìa dùng đúng "Nghiên cứu và Xây dựng Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam" (trùng README, BRAINSTORM, cẩm nang bảo vệ); thuộc tính tệp `.pptx` cũng dùng tên này. Cụm "Gian lận tài chính" không xuất hiện ở đâu trong repo.
3. **Agenda và `PHẦN 1..5` — ✅ (22 slide):** Agenda ở slide 2; PHẦN 1 mở đầu bằng Agenda (không cần slide phân đoạn), PHẦN 2–5 mỗi phần có 1 slide phân đoạn (tách "Demo" và "Kết luận" thành hai slide) + 1 slide phân đoạn Phụ lục.
4. **Tài liệu tham khảo 2 cột theo vòng đời — ✅ (15/18 tài liệu lên slide 17):** thứ tự nguồn dữ liệu → tiền xử lý NLP → thuật toán học máy → XAI → trợ năng web → hướng phát triển; mỗi tài liệu đã kiểm chứng qua Crossref, trang gốc tạp chí/hội nghị, W3C, Unicode.org, PyPI và GitHub (bằng chứng: `draft/scam-detection/reports/research-cam-phase09-references-lifecycle.md`). 3 tài liệu để dành cho báo cáo Word: LIBLINEAR, McCallum & Nigam (Naive Bayes), Streamlit. Không thêm "Báo cáo Cục ATTT" vì chưa có tên báo cáo và đường dẫn để kiểm chứng.
   - *Hiệu chỉnh:* trích dẫn Platt đổi sang bản đã xuất bản (chương "Probabilities for SV Machines", MIT Press, 2000, pp. 61–74, DOI 10.7551/mitpress/1113.003.0008; bản thảo 1999 mang tên dài khác); bổ sung số trang cho XGBoost, PhoBERT, scikit-learn.
   - *Đánh số mới theo vòng đời (thay cho số cũ ở các mục phía trên):* [1] bộ dữ liệu SMS chính, [2] nguồn bổ sung, [3] Unicode UAX #15, [4] PyVi, [5] underthesea, [6] TF-IDF, [7] XGBoost, [8] Random Forest, [9] SVM, [10] Platt, [11] scikit-learn, [12] SHAP, [13] TreeExplainer, [14] WCAG 2.1, [15] PhoBERT. Số cũ [4] trong các đoạn trên nay là [1]; số cũ [6] nay là [2]. Các trích dẫn trong slide 6, 8, 10, 12, 14, 16 đã đánh số lại.
5. **Lời cảm ơn — ✅:** `CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE BÁO CÁO!`.
- **Logo UIT ở bìa và slide cảm ơn — ✅:** dùng bộ nhận diện chính thức của trường (`Logo UIT_DHQG_Trang_Transparent.png`, bản trắng có tên ĐHQG-HCM) theo Brand Guideline: logo trắng trên nền tối, đặt giữa phía trên, không kéo giãn, không đổi màu. File nằm ở `draft/scam-detection/reports/slides/assets/`.

**Bản đồ 22 slide và phân vai (giữ phân bổ 14 phút của báo cáo thẩm định, dư ~1 phút):**

| Slide | Nội dung | Trình bày |
|:-:|---|---|
| 1–8 | Bìa · Agenda (≤ 20 giây) · PHẦN 1 (2 slide) · divider PHẦN 2 · Dataset · 4 nhóm bẫy · Pipeline | Thanh — 4:30 |
| 9–12 | divider PHẦN 3 · So sánh mô hình · ROC/PR · SHAP | Cẩm — 5:00 |
| 13–18 | divider PHẦN 4 · Demo · divider PHẦN 5 · Kết luận · Tài liệu tham khảo · Cảm ơn | Sơn — 4:30 |
| 19–22 | divider Phụ lục · Siêu tham số · Confusion Matrix · Learning Curves | Cả nhóm (Q&A) |

Các slide phân đoạn (5, 9, 13, 15, 19) không nói. Số slide trong bảng phân vai của báo cáo thẩm định (Slide 1–7, 8–11, 12–16, 17–20) đã dịch sang bản đồ mới này. Dòng "Presentation Deck ... 20 slides, 2.5 MB" ở mục Evidence bên dưới là số liệu của bản trước; bản hiện tại là 22 slide, 3,4 MB.

**Slide 12 (SHAP) đã sửa theo dữ liệu thật.** Đo trên `dataset_preprocessed.csv` (tỉ lệ tin lừa đảo chung là 19,2%): trong Top-20 từ khóa quan trọng có 9 từ không thiên về lừa đảo (`money` 1,2%, `number` 1,7%, `time` 1,0%, `liên_hệ 198` và `198` 0%, `soạn` 0,4%, `viettel` 0,5%, cùng `doi`, `sẽ` lẫn lộn); các từ `mày`, `gấp`, `viện_phí`, `thuế`, `số_định_danh` thì 100% là tin lừa đảo. Nhiều đặc trưng là **thẻ ẩn danh có sẵn trong bộ dữ liệu gốc**: tin bình thường dùng `[MONEY]`, `[NUMBER]`, `[TIME]`; tin lừa đảo dùng `[ĐƯỜNG_DẪN]`, `[THƯƠNG_HIỆU]`, `[SỐ_TIỀN]`. Thử nghiệm bỏ toàn bộ 453 đặc trưng chứa thẻ rồi huấn luyện lại đúng quy trình notebook (`src/evaluation/ablation_masking_tags.py`, kết quả `reports/ablation_masking_tags.json`; tái lập đúng F1 đã báo cáo): XGBoost F1 0.9535 → 0.9425 (Recall giữ 0.9762), Naive Bayes F1 0.8864 → 0.8503. Nên hiệu năng không chủ yếu do thẻ ẩn danh, nhưng cách gọi "từ khóa cảnh báo bẫy tâm lý" ở Phase 07 cần đổi thành "từ khóa quan trọng".

**Hiệu chỉnh 4 câu Q&A trong báo cáo thẩm định (kiểm chứng với dữ liệu; câu trả lời đề xuất để cả nhóm thống nhất):**
- **Câu 10 (đạo đức, PII):** báo cáo ghi "100% tin lừa đảo lấy từ báo chí" là chưa đúng. Chỉ 13/420 mẫu lừa đảo từ báo chí và video; 407/420 từ các bộ dữ liệu công khai trên GitHub; cả 2.193 dòng đều có `source_url`. *Trả lời:* "Nhóm khử PII 100%; dữ liệu lừa đảo lấy từ nguồn công khai (chủ yếu các bộ dữ liệu SMS trên GitHub, một phần báo chí và video điều tra), mọi mẫu đều có URL nguồn để truy vết."
- **Câu 8 (từ "money"):** báo cáo ghi "regex thay mọi số tiền" là chưa đúng. `money` là thẻ ẩn danh `[MONEY]` có sẵn trong bộ dữ liệu gốc (1.236 dòng thô, 1.221 dòng là tin bình thường); dữ liệu thô không có số tiền thật nào để regex thay. *Trả lời:* "Đó là thẻ che số tiền của bộ dữ liệu gốc, không phải từ tiếng Anh; nó xuất hiện chủ yếu ở tin bình thường nên mô hình dùng như dấu hiệu tin thông báo bình thường. Nhóm đã kiểm tra bằng cách bỏ toàn bộ đặc trưng chứa thẻ ẩn danh, F1 XGBoost chỉ giảm từ 0.9535 xuống 0.9425."
- **Câu 1 (PhoBERT):** con số "<15ms so với >300ms" chưa có phép đo nào trong repo. *Trả lời:* nói định tính (PhoBERT cần GPU, nhóm chưa thử nghiệm trong đồ án; mô hình cổ điển chạy được trên CPU); chỉ nêu số khi đã đo `predict` thật trên máy demo.
- **Câu 7 (teencode):** "tinh lọc từ benchmark NLP chuẩn" không có căn cứ trong mã nguồn. *Trả lời:* "Từ điển do nhóm tự biên soạn (160 mục), cố ý loại các từ đơn mơ hồ để tránh biến đổi sai nghĩa (ghi trong `teencode_dictionary.py`); đặc trưng `has_leet_speak` để mô hình tự học phần còn lại."

**Việc còn lại:** (1) diễn tập bấm giờ ≤ 15 phút theo bản đồ 22 slide; (2) bật Fade 0.3s thủ công trong PowerPoint sau cùng, vì dựng lại `.pptx` bằng script sẽ mất hiệu ứng.
**Chỉnh tay đã đưa vào script:** slide 2 (Agenda) đã bỏ dòng "Trình bày: …" ở các thẻ theo chỉnh sửa trong PowerPoint của Cẩm; script hỗ trợ biến môi trường `PPTX_OUT` để dựng thử ra nơi khác mà không ghi đè file đang chỉnh tay.

## Evidence Section

```
[✓] Branch checked out & pulled: feat/phase-09-ppt-template (commit d54df44)
[✓] Generator Script: draft/scam-detection/reports/slides/generate_slides.js (661 lines PptxGenJS)
[✓] Presentation Deck: draft/scam-detection/reports/slides/phase09_presentation.pptx (2.5 MB, 20 slides)
[✓] Overlap Checker: .agents/skills/powerpoint-slides/scripts/check_overlaps.py -> OK: no overlap or boundary issues found
[✓] Typography & Bounds Audit: Cambria / Calibri, 0 overflow elements, max_bottom <= 5.100" (SH = 5.625")
[✓] Research Audit Document: draft/scam-detection/reports/research-cam-phase09-ppt-slides-audit.md (88/100 A-)
[✓] 10 Q&A Defenses for ThS. Cáp Phạm Đình Thăng prepared & evidence-backed
```

## Phase Summary *(viết sau khi làm — evidence-based)*

> 🟡 **PPT Template Review Complete:** Đã thực hiện kiểm toán chuyên sâu (Hard Review) đối với 20 slide của em Cẩm. Giải quyết dứt điểm 4 vấn đề bàn giao, chuẩn hóa thời lượng thuyết trình 15 phút luân phiên 3 thành viên, thiết lập kịch bản ứng phó 10 câu hỏi phản biện của GV. Chờ áp dụng các bản vá cục bộ và diễn tập thử.

## Commit

```bash
git add draft/scam-detection/reports/slides/ draft/scam-detection/reports/report/
git commit -m "feat(phase09): report Word + PPT complete"
```
