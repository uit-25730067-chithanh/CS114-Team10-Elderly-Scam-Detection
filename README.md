# CS114 — Final Project Index

<p align="center">
  <img src="./docs/cover.png" alt="Vietnamese Elderly Scam Detection Cover" width="100%" style="border-radius: 8px;" />
</p>

> **Môn học:** Máy học (CS114) — UIT, ĐHQG-HCM  
> **Đề tài:** Nghiên cứu và Xây dựng Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam  
> **Nhóm:** 10 | **Thành viên:** 3 người  
> **Repository:** [`uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection`](https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection)

---

## 📂 Cấu trúc thư mục

```
. (CS114-Team10-Elderly-Scam-Detection/)
├── docs/                          ← Đề bài gốc từ giảng viên
│   ├── DoAnMonHoc.docx
│   └── DoAnMonHoc.pdf
│
├── draft/                         ← Workspace làm việc của nhóm
│   └── scam-detection/            ← Project chính (đang phát triển)
│       ├── data/                  ← Dataset (raw: 2.193 mẫu thực tế + processed: matrices 1754×5015)
│       ├── demo/                  ← Demo UI (Streamlit)
│       ├── docs/                  ← Tài liệu kỹ thuật kiến trúc, tiêu chuẩn mã, roadmap
│       ├── notebooks/             ← Jupyter notebooks (01-preprocessing, 02-eda, 03–06 models)
│       ├── reports/               ← Kết quả, 20 biểu đồ @ 300 DPI (7 EDA + 7 Model Learning Curves + 6 Multi-Model Comparison/XAI)
│       ├── src/                   ← Source code Python (utils, preprocessing, feature engineering, models, eval)
│       └── requirements.txt       ← Thư viện phụ thuộc
│
├── plans/                         ← Kế hoạch triển khai (11 phases)
│   └── scam-detection-full-submit/
│       ├── plan.md                ← Master plan
│       └── phase-00..10.md        ← Phase files chi tiết
│
├── submit/                        ← Bản nộp chính thức (ZIP cuối)
│   └── (trống — đóng gói khi nộp bài)
│
├── verify_final.py                ← Script tự động kiểm định đồ án Final
├── AGENTS.md                      ← Chỉ dẫn & trạng thái dành cho AI Agent
├── BRAINSTORM.md                  ← Hợp đồng đầu ra & đặc tả đề tài
└── README.md                      ← File này
```

---

## 🎯 Tổng quan dự án

| Thông tin | Chi tiết |
|-----------|---------|
| **Bài toán** | Binary Classification — Phát hiện tin nhắn lừa đảo nhắm vào người cao tuổi |
| **Dataset** | Tự thu thập ≥1500 mẫu tin nhắn tiếng Việt (lừa đảo + bình thường) |
| **Models** | Naive Bayes, Random Forest / XGBoost, SVM (Optional: PhoBERT) |
| **NLP** | Vietnamese text preprocessing (pyvi/underthesea), TF-IDF + auxiliary features |
| **Metrics** | F1-Score ≥ 88%, Recall Scam ≥ 92%, Confusion Matrix, Learning Curves |
| **Demo** | Streamlit Web App — Thanh đo nguy cơ + Bôi đỏ từ khóa + Giải thích bẫy tâm lý |

---

## 👥 Thành viên nhóm

| Người | MSSV | Lớp | Lĩnh vực chính |
|-------|------|-----|---------------|
| **Đặng Chí Thanh** *(đại diện nhóm)* | `25730067` | CS114.F31.CN2.TTNT | Data pipeline: Preprocessing → EDA → Feature Engineering |
| **Bùi Thị Mỷ Cẩm** | `25730013` | CS114.F31.CN2.TTNT | Modeling: NB + XGBoost + SVM |
| **Hoàng Cao Sơn** | `25730061` | CS114.F31.CN2.TTNT | Data Collection + Random Forest + Demo UI |

> Evaluation, Báo cáo Word và Slide PPT là sản phẩm **chung** — cả nhóm đều đóng góp nội dung theo phần mình thực hiện.

---

## 📊 Tiến độ (3-Sprint Fast-Track — Báo cáo sớm 23/09/2026)

> ⚡ **Chiến lược Báo cáo sớm (Fast-Track):** Nhóm xin báo cáo sớm vào ngày **23/09/2026** (Hạn LMS gốc: 13/10/2026). Đã hoàn tất Sprint 1 và khóa dữ liệu (2.193 mẫu thực tế, 100% Zero Synthetic Text), kích hoạt 4 luồng song song (`--parallels`) Sprint 2 từ 15/09, hoàn tất Báo cáo & Slide ngày 20/09, diễn tập ngày 21–22/09, thuyết trình chính thức ngày **23/09/2026**.

| Sprint | Người | Task | Trạng thái |
|--------|-------|------|-----------|
| **Sprint 1** (06/09 – 14/09)<br>*Hạ tầng & Dữ liệu* | **Thanh** | Setup repo, utils, template, requirements.txt, verify_final.py | ✅ Done (Phase 00 passed) |
| | **Thanh** | Thu thập 1.773 mẫu bình thường, mask PII, 50 mẫu Holdout Test | ✅ Done (PR #7 merged) |
| | **Sơn** | Thu thập 215 mẫu lừa đảo (`fear_authority`, `family_emergency`), 7 tầng kiểm toán | ✅ Done (PR #10 merged) |
| | **Cẩm** | Thu thập 205 mẫu lừa đảo (`health_gift`, `public_service`), 7 tầng kiểm toán | ✅ Done (PR #9 merged) |
| | **Thanh** | Hợp nhất 2.193 mẫu thực tế, chạy `data_validation.py`, khóa `dataset.csv` | ✅ Done (Phase 01 PASSED) |
| **Sprint 2** (15/09 – 18/09)<br>*Song song NLP & Modeling* | **Thanh** | Pipeline tiền xử lý văn bản tiếng Việt (Unicode NFC, regex, pyvi, 160 teencode, 15 aux features) | ✅ Done (Phase 02 PASSED — PR #12 merged) |
| | **Thanh** | EDA notebook + Zero-leakage Feature Pipeline (TF-IDF + Scaler, 7 figures 300 DPI) | ✅ Done (Phase 03 PASSED — PR #13 merged) |
| | **Cẩm** | Naive Bayes baseline + Learning Curves (15/09 – 16/09) | ✅ Done (Phase 04 PASSED — F1=0.8864, PR #15) |
| | **Sơn** | Random Forest training + hypertuning (15/09 – 17/09) | ✅ Done (Phase 05 PASSED — F1=0.9425, Recall=97.62%, PR #16) |
| | **Cẩm** | XGBoost training + tuning (16/09 – 17/09) | ✅ Done (Phase 05 PASSED — F1=0.9535, PR #15) |
| | **Cẩm** | Huấn luyện mô hình [SVM Linear / RBF](./plans/scam-detection-full-submit/phase-06-model-svm-phobert.md) (CalibratedClassifierCV) + Tuning C (17/09 – 18/09) | ✅ Done (Phase 06 PASSED — F1=0.9474, ROC-AUC=0.9986, PR #20) |
| | **Sơn** | Dựng khung Web App Demo Streamlit (shell) | ✅ Done (Phase 08 PASSED — PR #21) |
| | **Cả nhóm** | Báo cáo Word: Chương 1 (Đặt vấn đề) + Chương 2 (Khảo sát) + Chương 3 (Phương pháp) | ⏳ Sẵn sàng triển khai (Phase 09) |
| **Sprint 3** (19/09 – 22/09)<br>*Đánh giá, Demo & Diễn tập* | **Thanh** | [Đánh giá tổng hợp & XAI](./plans/scam-detection-full-submit/phase-07-evaluation-xai.md): So sánh 4 models, ROC-AUC, Confusion Matrix, XAI Top-20 SHAP | ✅ Done (Phase 07 PASSED — Multi-model benchmark, SHAP beeswarm, PR #23) |
| | **Sơn** | Tích hợp Model Catalog vào [Streamlit Demo UI](./plans/scam-detection-full-submit/phase-08-demo-ui.md), kiểm thử giao diện người cao tuổi & E2E Playwright | ✅ Done (Phase 08 PASSED — PR #21) |
| | **Cả nhóm** | [Báo cáo Word & Slide PPT](./plans/scam-detection-full-submit/phase-09-report-ppt.md): Chương 4–5 + Slide 15 phút (14–16 slides) + Diễn tập bấm giờ | 🔲 Sẵn sàng triển khai (Phase 09) |
| | **Thanh** | Pre-flight verification + [Đóng gói ZIP](./plans/scam-detection-full-submit/phase-10-submit-package.md) `25730067-25730013-25730061.zip` (22/09) | 🔲 Sẵn sàng triển khai (Phase 10) |
| **D-Day (18:30 23/09/2026)** | **Cả nhóm** | **Báo cáo trực tuyến MS Teams & Thuyết trình luân phiên trước ThS. Cáp Phạm Đình Thăng** | 🎯 Mục tiêu tối thượng |

---

## 📑 Danh mục 11 Phase thực thi chi tiết (`plans/scam-detection-full-submit/`)

| Phase | Tên Phase | Phụ trách | Trạng thái |
|:---:|---|:---:|:---:|
| 00 | [Phase 00 — Environment & Data Setup](./plans/scam-detection-full-submit/phase-00-env-data-setup.md) | **Thanh** | `passed` ✅ |
| 01 | [Phase 01 — Data Collection & Labeling](./plans/scam-detection-full-submit/phase-01-data-collection-labeling.md) | **Sơn** (lead) + Cả nhóm | `passed` ✅ |
| 02 | [Phase 02 — Vietnamese Text Preprocessing](./plans/scam-detection-full-submit/phase-02-vietnamese-text-preprocessing.md) | **Thanh** | `passed` ✅ |
| 03 | [Phase 03 — EDA & Feature Engineering](./plans/scam-detection-full-submit/phase-03-eda-feature-engineering.md) | **Thanh** | `passed` ✅ |
| 04 | [Phase 04 — Modeling — Naive Bayes Baseline](./plans/scam-detection-full-submit/phase-04-model-naive-bayes.md) | **Cẩm** | `passed` ✅ |
| 05 | [Phase 05 — Modeling — Random Forest & XGBoost](./plans/scam-detection-full-submit/phase-05-model-rf-xgboost.md) | **Sơn** (RF) + **Cẩm** (XGB) | `passed` ✅ |
| 06 | [Phase 06 — Modeling — SVM (Optional: PhoBERT)](./plans/scam-detection-full-submit/phase-06-model-svm-phobert.md) | **Cẩm** | `passed` ✅ |
| 07 | [Phase 07 — Evaluation & XAI](./plans/scam-detection-full-submit/phase-07-evaluation-xai.md) | **Thanh** | `passed` ✅ |
| 08 | [Phase 08 — Demo UI (Streamlit)](./plans/scam-detection-full-submit/phase-08-demo-ui.md) | **Sơn** | `passed` ✅ |
| 09 | [Phase 09 — Report & PPT](./plans/scam-detection-full-submit/phase-09-report-ppt.md) | **Cả nhóm** | `not-started` 🔲 |
| 10 | [Phase 10 — Submit Package](./plans/scam-detection-full-submit/phase-10-submit-package.md) | **Thanh** | `not-started` 🔲 |

---

## 🏆 Bảng so sánh hiệu năng 4 mô hình thực nghiệm (Holdout Test = 439 mẫu)

| Mô hình | Không gian đặc trưng | Hyperparameters chính | Accuracy | Precision | Recall (Lừa đảo) | F1-Score | ROC-AUC | Ghi chú & Đánh giá |
|---|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **XGBoost** | 5.015 (TF-IDF + 15 aux) | `n_est=300, depth=5, lr=0.05, subsample=0.7, colsample=0.8, scale_pos_weight=4.22` | **98.18%** | **93.18%** | **97.62%** | **0.9535** | 0.9984 | Best Overall Model, FN=2, FP=6 (Phase 05 — Cẩm) |
| **SVM Linear** | 5.015 (TF-IDF + 15 aux) | `C=10.0` (CalibratedClassifierCV 5-fold) | 97.95% | **93.10%** | 96.43% | **0.9474** | **0.9986** | Best Linear Model, FN=3, FP=6 (Phase 06 — Cẩm) |
| **Random Forest** | 5.015 (TF-IDF + 15 aux) | `n_est=200, depth=50, split=2, leaf=2, max_feat=0.2` | 97.72% | 91.11% | **97.62%** | 0.9425 | 0.9977 | Best Tree Ensemble, FN=2, FP=8 (Phase 05 — Sơn) |
| **Naive Bayes** | 5.000 (TF-IDF non-negative) | `alpha=0.01` (MultinomialNB) | 95.44% | 84.78% | 92.86% | 0.8864 | 0.9911 | Baseline Model, FN=6, FP=14 (Phase 04 — Cẩm) |

> 🎯 **Chỉ tiêu đề tài CS114:** F1-Score ≥ 88%, Recall Scam ≥ 92%. **Toàn bộ 4 mô hình đều vượt chỉ tiêu**, trong đó **XGBoost** đạt hiệu năng xuất sắc nhất (F1 = 0.9535, Recall = 97.62%, chỉ bỏ sót 2/84 tin nhắn lừa đảo).

---

## 🔗 Links nhanh

- [Đề bài (DOCX)](./docs/DoAnMonHoc.docx)
- [Brainstorm & Spec](./BRAINSTORM.md)
- [Master Plan](./plans/scam-detection-full-submit/plan.md)

---

## I. ĐỀ BÀI & YÊU CẦU CHI TIẾT

### Nội dung

Các nhóm nộp đồ án ở đây. Đặt tên: MSSV1-MSSV2-MSSV3.zip
Thư mục gốc: MSSV1-MSSV2-MSSV3

Thư mục DOCS: file word trình bày

Trình bày về đề tài (đề tài là gì, các khó khăn và thách thức của đề tài, ý nghĩa thực tiễn)
Các phương pháp tiếp cận để giải quyết bài toán này
Phương pháp nhóm chọn để giải quyết bài toán
Thực nghiệm

Dataset là gì
Phương pháp đánh giá là gì
Kết quả đạt được

Kết luận và hướng phát triển
Tài liệu tham khảo

File trình chiếu.
Source code

---

## II. DANH SÁCH TÀI LIỆU LIÊN QUAN

*   **File hướng dẫn đồ án:** `docs/DoAnMonHoc.docx`

---

## III. QUY TRÌNH NỘP BÀI & VERIFY

1.  **Thực hiện:** Hoàn thiện các phase triển khai trong `plans/scam-detection-full-submit/`.
2.  **Kiểm tra tự động (Verify):** Chạy kiểm định toàn diện đồ án:
    ```bash
    python3 verify_final.py
    ```
3.  **Bàn giao:** Cập nhật kết quả vào file `walkthrough.md` trong thư mục này.

---

## 📦 Hướng dẫn nộp bài

Khi hoàn thành, tạo thư mục trong `submit/`:

```
submit/
└── 25730067-25730013-25730061/
    ├── DOCS/                ← Báo cáo Word + PDF
    ├── SLIDES/              ← File PPT
    └── SOURCE/              ← Code + Data + Models + Demo
```

Zip lại: `25730067-25730013-25730061.zip`
