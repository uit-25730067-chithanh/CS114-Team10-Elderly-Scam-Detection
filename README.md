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
│       ├── reports/               ← Kết quả, 7 biểu đồ EDA figures @ 300 DPI
│       ├── src/                   ← Source code Python (utils, preprocessing, feature engineering, models, eval)
│       ├── requirements.txt       ← Thư viện phụ thuộc
│       └── README.md              ← Hướng dẫn workspace
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
| | **Sơn** | Random Forest training + hypertuning (15/09 – 16/09) | 🚀 Đang thực hiện (Phase 05) |
| | **Cẩm** | XGBoost training + tuning (16/09 – 17/09) | ✅ Done (Phase 05 — F1=0.9535, PR #15) |
| | **Sơn** | Dựng khung Web App Demo Streamlit (shell) | ⏳ Sẵn sàng (Phase 08) |
| | **Cả nhóm** | Báo cáo Word: Chương 1 (Đặt vấn đề) + Chương 2 (Khảo sát) + Chương 3 (Phương pháp) | ⏳ Sẵn sàng (Phase 09) |
| **Sprint 3** (19/09 – 22/09)<br>*Đánh giá, Demo & Diễn tập* | **Thanh** | Đánh giá tổng hợp: So sánh 4 models, ROC-AUC, Confusion Matrix, XAI Top-20 SHAP | 🔲 |
| | **Sơn** | Tích hợp Best Model vào Streamlit Demo UI, kiểm thử giao diện người cao tuổi | 🔲 |
| | **Cả nhóm** | Báo cáo Word: Chương 4 (Thực nghiệm) + Chương 5 (Kết luận) + Tài liệu tham khảo | 🔲 |
| | **Cả nhóm** | Slide PPT 15 phút (14–16 slides) + Diễn tập bấm giờ (≤15 phút) | 🔲 |
| | **Thanh** | Pre-flight verification + Đóng gói `25730067-25730013-25730061.zip` (22/09) | 🔲 |
| **D-Day (18:30 23/09/2026)** | **Cả nhóm** | **Báo cáo trực tuyến MS Teams & Thuyết trình luân phiên trước ThS. Cáp Phạm Đình Thăng** | 🎯 Mục tiêu tối thượng |

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
