# AGENTS.md — CS114 Final Project Context

> Agent context file. Cung cấp ngữ cảnh cho AI assistants làm việc với project này.

---

## Project Identity

- **Course:** CS114 — Machine Learning (Máy học), UIT ĐHQG-HCM
- **Instructor:** ThS. Cáp Phạm Đình Thăng
- **Assignment:** Final — Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi
- **Repository:** [`uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection`](https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection)
- **SSH Remote:** `git@github.com-uit:uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection.git`
- **Deadline:** 13/10/2026 (LMS) | Báo cáo: 15 phút/nhóm
- **Group:** Nhóm 10 | 3 thành viên:
  - **Đặng Chí Thanh** — MSSV: `25730067` (Trưởng nhóm / PM) — `25730067@ms.uit.edu.vn`
  - **Bùi Thị Mỷ Cẩm** — MSSV: `25730013` (ML Modeling) — `25730013@ms.uit.edu.vn`
  - **Hoàng Cao Sơn** — MSSV: `25730061` (Data Collection & Demo UI) — `25730061@ms.uit.edu.vn`

---

## Directory Layout

```
. (CS114-Team10-Elderly-Scam-Detection/)
├── docs/              ← Đề bài gốc + hướng dẫn từ GV
├── AGENTS.md          ← File này — context cho AI agents
├── BRAINSTORM.md      ← Brainstorm & Specification gốc
├── draft/
│   └── scam-detection/    ← Working project
│       ├── src/            ← Python source code
│       │   ├── preprocessing/   ⏳ text_cleaner, tokenizer, feature_extractor
│       │   ├── models/          ⏳ naive_bayes_model, random_forest_model, svm_model
│       │   ├── evaluation/      ⏳ metrics_calculator, plot_roc_curve, model_comparator
│       │   └── utils/           ⏳ helpers.py, constants (RANDOM_STATE=42, TEST_SIZE=0.2)
│       ├── notebooks/      ← Jupyter notebooks
│       ├── data/
│       │   ├── raw/        ← dataset.csv gốc (KHÔNG commit git nếu > 50MB)
│       │   └── processed/  ← Vectorized features, splits (TF-IDF matrices, etc.)
│       ├── models/         ← Trained model files (.pkl, .json)
│       ├── docs/           ← Tài liệu kỹ thuật nội bộ
│       ├── reports/        ← Kết quả, biểu đồ, figures
│       ├── demo/           ← Streamlit/Gradio web app
│       └── requirements.txt
├── plans/             ← Implementation plans (phase-based)
└── submit/            ← Bản nộp cuối (trống cho đến khi nộp bài)
```

---

## Current State (2026-09-04)

| Component | Status |
|-----------|--------|
| Project scaffold | ✅ Done — folder structure, docs, environment setup |
| `BRAINSTORM.md` | ✅ Done — đề tài đã chọn, specification đã ký hợp đồng đầu ra |
| Phase 00 (Env & Data Setup) | ⏳ Sprint 1 Target — pending implementation |
| `src/utils/` | ⏳ Sprint 1 Target |
| `draft/scam-detection/README.md` | ⏳ Sprint 1 Target |
| Dataset (`dataset.csv`) | ⏳ Sprint 1 Target (06/9 – 15/9) — cần thu thập >= 1,500 mẫu |
| `src/preprocessing/` | ⏳ Sprint 2 Target — text_cleaner, tokenizer, feature_extractor |
| `src/models/` | ⏳ Sprint 2-3 Target — naive_bayes, random_forest/xgboost, svm |
| `src/evaluation/` | ⏳ Sprint 3 Target — metrics, plots, comparator, XAI |
| Notebooks (01-06) | ⏳ Sprint 2-3 Target — phân công rõ ràng cho 3 thành viên |
| Demo UI (Streamlit) | ⏳ Sprint 3-4 Target — app.py + components |
| Báo cáo Word & Slide PPT | ⏳ Sprint 2-4 Target — triển khai song song theo sprint |

> **Verdict (04/09): Khởi tạo repository hoàn tất. Sẵn sàng thực hiện Phase 00 (Môi trường & Khung dữ liệu).**

---

## Conventions (follow these when writing code)

- **Files:** snake_case cho file Python (`text_cleaner.py`, `naive_bayes_model.py`), kebab-case cho các loại file khác
- **Functions/Variables:** snake_case — `clean_text()`, `X_train`, `y_test`
- **Classes:** PascalCase — `ScamDetector`, `TextPreprocessor`
- **Constants:** UPPER_SNAKE_CASE — `RANDOM_STATE = 42`, `TEST_SIZE = 0.2`
- **Random seed:** Always set `RANDOM_STATE = 42`
- **Git:** Do NOT commit `data/raw/*.csv` nếu > 50MB

---

## Pipeline Overview

```
dataset.csv (1,500+ mẫu tin nhắn tiếng Việt)
  → [text_cleaner.py]        Chuẩn hóa Unicode, xóa ký tự rác, xử lý teencode
  → [tokenizer.py]           Tách từ tiếng Việt (underthesea / pyvi)
  → [feature_extractor.py]   TF-IDF (N-gram 1-2) + đặc trưng phụ (URL, SĐT, từ khóa khẩn cấp)
  → [data_splitter.py]       Stratified 80/20 split
  → [naive_bayes_model.py / random_forest_model.py / svm_model.py]
  → [metrics_calculator.py]  F1, ROC-AUC, Precision, Recall
  → [model_comparator.py]    Cross-model comparison table
  → [app.py]                 Streamlit demo — kiểm tra tin nhắn & giải thích bẫy tâm lý
```

**Key design decisions:**
1. **Dữ liệu tiếng Việt** — sử dụng `underthesea` hoặc `pyvi` để tách từ
2. **TF-IDF N-gram 1-2** — trích xuất đặc trưng văn bản chính
3. **Đặc trưng phụ thủ công** — đếm URL, số điện thoại, từ khóa khẩn cấp, từ khóa quyền lực
4. **Stratified split** — maintain tỷ lệ lừa đảo/bình thường trong cả train và test
5. **Recall ưu tiên** — với bài toán lừa đảo, bỏ sót (FN) nguy hiểm hơn báo nhầm (FP)
6. **Mỗi model 1 notebook riêng** — tránh merge conflicts

---

## Data

| Field | Value |
|-------|-------|
| Source | Thu thập thủ công: Bộ Công an, Cục ATTT, báo chí, mạng xã hội |
| Shape | 1,500–3,000 mẫu × 5 cột |
| Features | `id`, `text`, `label`, `scam_category`, `source` |
| Label | label (0=bình thường, 1=lừa đảo) |
| Scam categories | `fear_authority`, `family_emergency`, `health_gift`, `public_service`, `none` |

---

## Team & Responsibilities

> 📌 **Chi tiết tasks theo phase:** [project-roadmap.md](./draft/scam-detection/docs/project-roadmap.md)

| Member | MSSV | Vai trò | Task chính |
|--------|------|---------|-----------|
| **Đặng Chí Thanh** *(Lead/PM)* | `25730067` | Data Pipeline & Evaluation Lead | Pipeline tiền xử lý văn bản tiếng Việt, EDA & trích xuất TF-IDF, đánh giá tổng hợp XAI, đóng gói bài nộp |
| **Bùi Thị Mỷ Cẩm** | `25730013` | Machine Learning Engineer | Huấn luyện Naive Bayes baseline, tối ưu hóa XGBoost, huấn luyện Support Vector Machine (LinearSVC Calibrated) |
| **Hoàng Cao Sơn** | `25730061` | Data Collection & Demo UI Lead | Thiết kế schema thu thập Google Sheet, gán nhãn 4 nhóm bẫy tâm lý, huấn luyện Random Forest, Web Demo Streamlit |
| **Cả nhóm** | — | Báo cáo & Thuyết trình | Thu thập >= 500 mẫu/người, soạn thảo Báo cáo Word (Chương 1–5), Slide PowerPoint 15 phút, diễn tập bảo vệ |

---

## Agent Workflow — Post-Implementation Checklist

> **BẮT BUỘC cho mọi AI agent sau khi implement xong 1 phase.**

### Sau khi code xong, agent phải làm theo thứ tự:

```
[1] Verify pipeline chạy đúng
    → Chạy lại script chính, kiểm tra output khớp Success Criteria
    → Không claim "done" nếu chưa chạy thực tế

[2] Update phase file (plans/scam-detection-full-submit/phase-XX-*.md)
    → Điền Evidence section bằng output THỰC TẾ
    → Tick [x] tất cả checklist items
    → Viết Summary sau khi code xong

[3] Update plan.md (plans/scam-detection-full-submit/plan.md)
    → Đổi status phase vừa xong: pending → passed ✅
    → Cập nhật field updated: với ngày thực tế

[4] Update AGENTS.md (file này)
    → Cập nhật bảng Current State
    → Cập nhật Next Actions

[5] Update docs/ (nếu architecture/data thay đổi)
    → system-architecture.md: cập nhật pipeline diagram nếu có bước mới
    → project-overview-pdr.md: cập nhật số liệu nếu thay đổi

[6] Update README files (nếu cần)
    → draft/scam-detection/README.md: cập nhật Workflow status
    → Final/README.md: cập nhật Sprint progress

[7] Xử lý artifacts (data, models)
    → Kiểm tra file .pkl nào team cần → đảm bảo KHÔNG bị gitignore
    → Processed data (< ~50MB) → commit luôn để team dùng
    → Model lớn (> 50MB) → để trong gitignore, ghi hướng dẫn reproduce

[8] Commit
    → feat(phaseXX): <mô tả ngắn>  ← code + notebook
    → docs(phaseXX): <mô tả ngắn> ← docs/README riêng nếu nhiều thay đổi
```

### File nào phải update sau mỗi phase

| File | Khi nào cập nhật |
|------|----------------|
| `plans/.../phase-XX-*.md` | Luôn luôn — điền Evidence + Summary |
| `plans/.../plan.md` | Luôn luôn — đổi status + updated date |
| `AGENTS.md` | Luôn luôn — Current State + Next Actions |
| `draft/scam-detection/README.md` | Khi có file mới hoặc workflow thay đổi |
| `Final/README.md` | Khi sprint status thay đổi |
| `docs/system-architecture.md` | Khi pipeline có thêm/bớt bước |

### Quy tắc về .pkl và artifacts

- `data/raw/dataset.csv` → **Commit nếu < 50MB** (dataset tự tạo)
- `data/processed/*.pkl` (TF-IDF matrices, splits) → **Commit luôn** nếu < 50MB
- `models/vectorizer.pkl` → **Commit luôn** (nhỏ, team UI cần)
- `models/*.pkl` lớn → **Gitignore** (thường > 50MB) → ghi hướng dẫn reproduce

---

## Submission Format
 
Final package name: `25730067-25730013-25730061.zip`
 
Contents:
```
25730067-25730013-25730061/
├── DOCS/          ← DoAnMonHoc.docx + DoAnMonHoc.pdf
├── SLIDES/        ← Presentation_CS114.pptx
├── SOURCE/
│   ├── data/      ← dataset.csv và dữ liệu huấn luyện
│   ├── models/    ← File trọng số model đã train (.pkl, .pt)
│   ├── src/       ← Source code tiền xử lý, huấn luyện
│   ├── app.py     ← File chạy Web Demo Streamlit
│   └── requirements.txt
└── README.md      ← Hướng dẫn chạy code
```
 
Place in `Final/submit/` before zipping.

---

## Next Actions
 
> **🚀 Sẵn sàng thực hiện Phase 00 (Môi trường & Khung dữ liệu) khởi động Sprint 1 (06/9 – 15/9).**

### 🎯 Sprint 1 — Kế hoạch hành động cụ thể:
1. **Hoàng Cao Sơn (Lead thu thập):**
   - Thiết lập Google Sheet chia sẻ nhóm theo schema: `id | text | label | scam_category | source | collector_name | notes`.
   - Phụ trách thu thập >= 500 mẫu lừa đảo (nhóm `fear_authority` và `family_emergency`).
2. **Bùi Thị Mỷ Cẩm:**
   - Cài đặt môi trường theo `requirements.txt`.
   - Phụ trách thu thập >= 500 mẫu lừa đảo (nhóm `health_gift` và `public_service`).
3. **Đặng Chí Thanh (PM & Data Lead):**
   - Thu thập >= 500 mẫu tin nhắn bình thường (`none`) từ SMS nhà mạng, ngân hàng, sinh hoạt đời thường.
   - Chuẩn bị sẵn module `src/preprocessing/` cho Sprint 2.
   - Giám sát tiến độ và kiểm tra chất lượng dữ liệu thu thập (tránh trùng lặp, nhãn nhất quán).

