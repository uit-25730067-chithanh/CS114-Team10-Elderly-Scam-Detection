# AGENTS.md — CS114 Final Project Context

> Agent context file. Cung cấp ngữ cảnh cho AI assistants làm việc với project này.

---

## Project Identity

- **Course:** CS114 — Machine Learning (Máy học), UIT ĐHQG-HCM
- **Instructor:** ThS. Cáp Phạm Đình Thăng
- **Assignment:** Final — Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi
- **Repository:** [`uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection`](https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection)
- **SSH Remote:** `git@github.com-uit:uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection.git`
- **Deadline & Báo cáo:** 18:30 ngày 23/09/2026 (Báo cáo sớm qua MS Teams | Hạn LMS gốc: 13/10/2026) | Thuyết trình: 15 phút/nhóm (Luân phiên 3 thành viên)
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

## Current State (2026-09-15 — Sprint 2 Kickoff Mode)

| Component | Status |
|-----------|--------|
| Project scaffold | ✅ Done — folder structure, docs, environment setup |
| `BRAINSTORM.md` | ✅ Done — đề tài đã chọn, hợp đồng đầu ra đã cập nhật báo cáo sớm 23/09 |
| Phase 00 (Env & Data Setup) | ✅ Passed — `requirements.txt`, `dataset_template.csv`, `verify_final.py` |
| `src/utils/` | ✅ Done — `helpers.py`, `constants`, `set_seeds()` reproducibility |
| `draft/scam-detection/README.md` | ✅ Done — workspace developer guide đầy đủ |
| Phase 01 (Data Collection & Labeling) | ✅ Passed — Cả 3 thành viên hoàn thành và merge PR (#7, #9, #10); 100% Zero Synthetic Text; 0% rò rỉ PII; 7 tầng kiểm toán pass |
| Dataset (`dataset.csv`) | ✅ Done — Hợp nhất 2.193 mẫu thực tế (1.773 normal + 420 scam qua 4 nhóm bẫy tâm lý); 100% provenance URLs; `data_validation.py` PASSED |
| `src/preprocessing/` | ✅ Passed (Phase 02) — text_cleaner (Unicode NFC, 60+ teencode), tokenizer (pyvi), stopwords (domain guard), pipeline (10 auxiliary features) |
| Preprocessed Data (`dataset_preprocessed.csv`) | ✅ Passed (Phase 02) — 2.193 dòng, 19 cột, 0 nulls, 0 empty strings |
| `notebooks/01_preprocessing.ipynb` | ✅ Passed (Phase 02) — Chạy end-to-end với đầy đủ bảng biểu & biểu đồ so sánh Scam vs Normal |
| `src/models/` | ⏳ Sprint 2 Fast-Track (15/09 – 17/09) — naive_bayes, random_forest, xgboost, svm |
| `src/evaluation/` | ⏳ Sprint 3 Fast-Track (18/09 – 19/09) — metrics, plots, comparator, XAI SHAP |
| Notebooks (01-06) | ⏳ Sprint 2-3 Fast-Track (15/09 – 19/09) — phân công rõ ràng cho 3 thành viên |
| Demo UI (Streamlit) | ⏳ Sprint 2-3 Fast-Track (16/09 shell → 20/09 integrated) — app.py + components |
| Báo cáo Word & Slide PPT | ⏳ Sprint 2-3 Fast-Track (15/09 Ch 1-3 → 20/09 Ch 4-5 & PPT → 21-22/09 diễn tập) |
| Đóng gói ZIP & Báo cáo | ⏳ Milestone 22/09 đóng gói → **18:30 ngày 23/09/2026 Thuyết trình luân phiên qua MS Teams** |

> **Verdict (15/09): Phase 02 (Tiền xử lý văn bản tiếng Việt & Trích xuất đặc trưng phụ) đã HOÀN THÀNH 100% XUẤT SẮC (13/13 tests passed; 2.193 mẫu được làm sạch và trích xuất 10 đặc trưng phụ; notebook 01_preprocessing.ipynb hoàn tất; dataset_preprocessed.csv sẵn sàng). Kích hoạt Phase 03: EDA & Feature Engineering.**

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

[9] Tạo Pull Request (PR) theo chuẩn quy định
    → Title: Tiếng Anh, Title Case, KHÔNG dùng tiền tố commit (không feat/fix/chore)
    → Body: Tóm tắt công việc đã làm trên PR đó, tiếng Việt, các gạch đầu dòng chi tiết
    → Assignee: Tự gán chính mình (--assignee "@me")
```

### Quy chuẩn tạo Pull Request (PR Standards) — BẮT BUỘC

> 📌 **Mọi Agent AI khi tạo PR bắt buộc phải tuân theo khuôn mẫu chuẩn của [PR #1](https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection/pull/1) & [PR #2](https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection/pull/2):**

1. **PR Title (Tiêu đề PR):**
   - Sử dụng **Tiếng Anh** hoàn toàn, viết hoa dạng Title Case.
   - **TUYỆT ĐỐI KHÔNG dùng tiền tố commit message** (KHÔNG dùng `feat:`, `feat(ci):`, `fix:`, `chore:`, `docs:`...).
   - *Ví dụ chuẩn:*
     - ✅ `Setup Development Environment, Utility Helpers, and Dataset Ingestion Template` (PR #1)
     - ✅ `Setup Automated PR Code Review with Google Gemini Flash` (PR #2)
     - ❌ `feat(ci): integrate automated PR code review via Google Gemini Flash` (Sai convention)

2. **PR Body (Nội dung mô tả PR):**
   - Tóm tắt công việc đã làm trên PR bằng **Tiếng Việt**.
   - Trình bày dạng **các gạch đầu dòng phân cấp rõ ràng**:
     - Cấp 1 (`-`): Nhóm đầu việc lớn kèm đường dẫn/file liên quan trong dấu backticks.
     - Cấp 2 (`  -`): Chi tiết kỹ thuật, cấu hình, logic triển khai hoặc tiêu chí nghiệm thu đạt được.
   - Thuật ngữ kỹ thuật, tên thư viện, hàm, biến số, đường dẫn tệp bắt buộc đặt trong dấu code backticks (ví dụ: `requirements.txt`, `RANDOM_STATE = 42`).

3. **Assignee (Người phụ trách):**
   - **Tự assign chính mình** vào PR ngay khi tạo thông qua cờ `--assignee "@me"`.
   - *Mẫu lệnh chuẩn qua GitHub CLI:*
     ```bash
     gh pr create \
       --base main \
       --head <branch-name> \
       --title "<Title In English Without Commit Prefix>" \
       --body-file <path/to/pr_body.md> \
       --assignee "@me"
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

## Next Actions (Sprint 2 Kickoff — Fast-Track 23/09 Mode)
 
> **🚀 Mục tiêu tối thượng: Sẵn sàng bảo vệ đồ án trước GV vào ngày 23/09/2026 (Chỉ còn 8 ngày).**

### 🎯 Phân công luồng thực thi song song (`--parallels`):
1. **Luồng A (Dữ liệu & Khóa Dataset — Thanh Lead):** ✅ **HOÀN THÀNH (15/09/2026)**
   - Đã hợp nhất 2.193 mẫu đời thực độc bản (`staging_thanh_normal.csv`: 1.773, `staging_cam_scam.csv`: 205, `staging_son_scam.csv`: 215).
   - Đạt 100% provenance URLs, 0% PII leak, 0 duplicate, pass `data_validation.py` 100%.
   - Đóng băng `dataset.csv` và chuyển giao sang tiền xử lý.
2. **Luồng B (Tiền xử lý & Feature Engineering — Thanh):** ✅ **HOÀN THÀNH PHASE 02 (15/09/2026)**
   - Triển khai thành công `src/preprocessing/` (`text_cleaner.py`, `tokenizer.py`, `stopwords.py`, `pipeline.py`).
   - Xây dựng thành công `notebooks/01_preprocessing.ipynb` và xuất `data/processed/dataset_preprocessed.csv` (2.193 dòng, 19 cột).
   - Chuyển tiếp sang Phase 03: EDA và trích xuất TF-IDF matrix (N-gram 1-2) + Stratified Train/Test 80/20.
3. **Luồng C (Mô hình hóa ML — Cẩm & Sơn):** ⏳ **KHỞI ĐỘNG (15/09 – 17/09)**
   - Cẩm: Naive Bayes baseline (`notebooks/03_model_naive_bayes.ipynb`) → XGBoost & SVM Linear/RBF (`notebooks/04_model_xgboost.ipynb`, `notebooks/05_model_svm.ipynb`).
   - Sơn: Random Forest (`notebooks/04_model_random_forest.ipynb`).
   - Thanh & Cẩm: Đánh giá XAI, vẽ Learning Curves và trích xuất Top-20 từ khóa SHAP (18/09 – 19/09).
4. **Luồng D (Demo UI — Sơn):** ⏳ **TRIỂN KHAI (16/09 – 18/09)**
   - Dựng khung giao diện Streamlit (`demo/app.py`), thiết kế UX thân thiện với người cao tuổi và tích hợp mô hình.
5. **Luồng E (Báo cáo Word, Slide PPT & Diễn tập — Cả nhóm):** ⏳ **ĐỒNG THỜI (15/09 – 22/09)**
   - Báo cáo Word Chương 1–3: Hoàn thành trước 18/09.
   - Báo cáo Word Chương 4–5: Hoàn thành trước 20/09 ngay khi có kết quả thực nghiệm.
   - Slide PPT 15 phút: Dựng ngày 20/09 – 21/09 theo cẩm nang bảo vệ.
   - Diễn tập bấm giờ (≤15 phút): 21/09 – 22/09.
   - Đóng gói ZIP `25730067-25730013-25730061.zip` vào 22/09/2026.
   - **18:30 ngày 23/09/2026: Thuyết trình luân phiên chính thức với ThS. Cáp Phạm Đình Thăng qua MS Teams!**

