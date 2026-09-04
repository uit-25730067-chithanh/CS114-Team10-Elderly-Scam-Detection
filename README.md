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
│       ├── data/                  ← Dataset (raw: template + processed: TF-IDF)
│       ├── demo/                  ← Demo UI (Streamlit)
│       ├── docs/                  ← Tài liệu kỹ thuật kiến trúc, tiêu chuẩn mã
│       ├── notebooks/             ← Jupyter notebooks (01–06)
│       ├── reports/               ← Kết quả, biểu đồ figures
│       ├── src/                   ← Source code Python (utils, preprocessing, models, eval)
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

## 📊 Tiến độ

> Nhóm Data & Pipeline (Thanh) tập trung preprocessing & feature engineering. Nhóm Modeling (Cẩm, Sơn) triển khai song song từ Sprint 2. Cả nhóm cùng làm Báo cáo & PPT từ Sprint 2.

| Sprint | Người | Task | Trạng thái |
|--------|-------|------|-----------|
| **Sprint 1** (06/9 – 15/9) | **Thanh** | Setup repo, utils, template, requirements.txt, verify_final.py | ✅ Done (Phase 00 passed) |
| | **Sơn** | Lập bảng thu thập, phân loại 4 nhóm bẫy tâm lý | 🔲 |
| | **Cả nhóm** | Thu thập ≥500 mẫu / người | 🔲 |
| **Sprint 2** (15/9 – 25/9) | **Thanh** | Text preprocessing pipeline (Unicode, tokenize, TF-IDF) | 🔲 |
| | **Thanh** | EDA notebook + Word Cloud + figures | 🔲 |
| | **Cẩm** | Naive Bayes baseline + Learning Curves | 🔲 |
| | **Sơn** | Random Forest training + hypertuning | 🔲 |
| | **Cả nhóm** | Báo cáo Word: Chương 1 (Đặt vấn đề) + Chương 2 (Khảo sát) | 🔲 |
| **Sprint 3** (25/9 – 05/10) | **Cẩm** | XGBoost + SVM training + Evaluation scripts | 🔲 |
| | **Sơn** | Demo UI Streamlit shell | 🔲 |
| | **Thanh** | Evaluation tổng hợp + XAI top-20 keywords | 🔲 |
| | **Cả nhóm** | Báo cáo Word: Chương 3 (Phương pháp) + PPT layout | 🔲 |
| **Sprint 4** (05/10 – 13/10) | **Sơn** | Tích hợp model vào Demo UI | 🔲 |
| | **Cả nhóm** | Báo cáo Word: Chương 4–5 + Hoàn thiện PPT + Diễn tập | 🔲 |
| | **Thanh** | Đóng gói ZIP + Nộp bài (13/10) | 🔲 |

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
