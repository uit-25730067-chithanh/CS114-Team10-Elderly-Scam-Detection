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
│       │   ├── preprocessing/   ✅ text_cleaner, tokenizer, feature_extractor (Phase 02 Passed)
│       │   ├── models/          🚀 naive_bayes, random_forest, xgboost, svm (Phase 04-06 Active)
│       │   ├── evaluation/      ⏳ metrics_calculator, plot_roc_curve, model_comparator (Phase 07)
│       │   ├── utils/           ✅ helpers.py, constants (RANDOM_STATE=42, TEST_SIZE=0.2)
│       │   ├── feature_engineering.py        ✅ Zero-leakage pipeline (Phase 03 Passed)
│       │   ├── feature_engineering_config.py ✅ Hằng số TF-IDF & đặc trưng (Phase 03 Passed)
│       │   ├── eda_plots_part1.py            ✅ Biểu đồ nhãn, bẫy tâm lý, độ dài, wordcloud
│       │   ├── eda_plots_part2.py            ✅ Biểu đồ n-grams, tương quan, nguồn dữ liệu
│       │   └── eda_visualizations.py         ✅ EDA Orchestrator (7 figures @ 300 DPI)
│       ├── notebooks/      ← Jupyter notebooks (01-preprocessing, 02-eda, 03–06 models)
│       ├── data/
│       │   ├── raw/        ← dataset.csv gốc (2.193 mẫu thực tế, 100% Zero Synthetic Text)
│       │   └── processed/  ← dataset_preprocessed.csv, X_train.pkl (1754×5015), X_test.pkl (439×5015), y_train.pkl, y_test.pkl, tfidf_vectorizer.pkl, aux_scaler.pkl, feature_names.json
│       ├── models/         ← Trained model files (.pkl, .json)
│       ├── docs/           ← Tài liệu kỹ thuật nội bộ (roadmap, architecture, pdr, code-standards)
│       ├── reports/        ← Kết quả, biểu đồ 7 figures @ 300 DPI
│       ├── demo/           ← Streamlit/Gradio web app
│       └── requirements.txt
├── plans/             ← Implementation plans (phase-based 00..10)
└── submit/            ← Bản nộp cuối (trống cho đến khi nộp bài)
```

---

## Current State (2026-09-15 — Sprint 2 Active Modeling Mode)

| Component | Status |
|-----------|--------|
| Project scaffold | ✅ Done — folder structure, docs, environment setup |
| `BRAINSTORM.md` | ✅ Done — đề tài đã chọn, hợp đồng đầu ra đã cập nhật báo cáo sớm 23/09 |
| Phase 00 (Env & Data Setup) | ✅ Passed — `requirements.txt`, `dataset_template.csv`, `verify_final.py` |
| `src/utils/` | ✅ Done — `helpers.py`, `constants`, `set_seeds()` reproducibility |
| `draft/scam-detection/README.md` | ✅ Done — workspace developer guide đầy đủ |
| Phase 01 (Data Collection & Labeling) | ✅ Passed — Cả 3 thành viên hoàn thành và merge PR (#7, #9, #10); 100% Zero Synthetic Text; 0% rò rỉ PII; 7 tầng kiểm toán pass |
| Dataset (`dataset.csv`) | ✅ Done — Hợp nhất 2.193 mẫu thực tế (1.773 normal + 420 scam qua 4 nhóm bẫy tâm lý); 100% provenance URLs; `data_validation.py` PASSED |
| `src/preprocessing/` | ✅ Passed (Phase 02) — text_cleaner (Unicode NFC, modern underthesea tone), teencode_dictionary (160 teencode, 22 leet-speak patterns, 50+ unaccented compounds), tokenizer (pyvi), stopwords (domain guard), pipeline (15 auxiliary features) |
| Preprocessed Data (`dataset_preprocessed.csv`) | ✅ Passed (Phase 02) — 2.193 dòng, 24 cột (8 cột raw + text_cleaned + 15 features), 0 nulls, 0 empty strings |
| `notebooks/01_preprocessing.ipynb` | ✅ Passed (Phase 02) — Chạy end-to-end với đầy đủ bảng biểu & biểu đồ phân tách Scam vs Normal |
| `notebooks/02_eda.ipynb` | ✅ Passed (Phase 03) — Chạy end-to-end với 7 biểu đồ phân tích sâu & bảng số liệu chi tiết |
| Phase 03 (EDA & Feature Engineering) | ✅ Passed (15/09/2026) — Zero-leakage TF-IDF+aux pipeline; X_train (1754×5015), X_test (439×5015); 7 EDA figures @ 300 DPI; 34 tests PASS |
| Phase 04 (Naive Bayes Baseline) | 🚀 Sprint 2 Active (15/09 – 16/09) — Cẩm nạp ma trận Phase 03 để huấn luyện & phân tích Overfitting |
| Phase 05 (Random Forest & XGBoost) | 🚀 Sprint 2 Active (15/09 – 16/09) — Sơn (RF) và Cẩm (XGBoost) huấn luyện & hypertuning |
| `src/models/` | 🚀 Sprint 2 Active (15/09 – 17/09) — naive_bayes, random_forest, xgboost, svm |
| `src/evaluation/` | ⏳ Sprint 3 Fast-Track (18/09 – 19/09) — metrics, plots, comparator, XAI SHAP |
| Notebooks (03-06) | ⏳ Sprint 2-3 Fast-Track (15/09 – 19/09) — phân công rõ ràng cho 3 thành viên |
| Demo UI (Streamlit) | ⏳ Sprint 2-3 Fast-Track (16/09 shell → 20/09 integrated) — app.py + components |
| Báo cáo Word & Slide PPT | ⏳ Sprint 2-3 Fast-Track (15/09 Ch 1-3 → 20/09 Ch 4-5 & PPT → 21-22/09 diễn tập) |
| Đóng gói ZIP & Báo cáo | ⏳ Milestone 22/09 đóng gói → **18:30 ngày 23/09/2026 Thuyết trình luân phiên qua MS Teams** |

> **Verdict (15/09): Phase 02 (Tiền xử lý văn bản tiếng Việt & Trích xuất đặc trưng phụ) đã HOÀN THÀNH 100% XUẤT SẮC (21/21 tests passed; 2.193 mẫu được làm sạch và trích xuất 15 đặc trưng phụ; notebook 01_preprocessing.ipynb hoàn tất nhẹ nhàng 39.5 KB; dataset_preprocessed.csv 24 cột sẵn sàng). Kích hoạt Phase 03: EDA & Feature Engineering.**

> **Verdict (15/09): Phase 03 (EDA & Zero-Leakage Feature Engineering) đã HOÀN THÀNH 100% XUẤT SẮC. Đã phát hiện và sửa triệt để lỗi rò rỉ dữ liệu (data leakage) trong bản nháp cũ. Pipeline mới: Stratified Split 80/20 ĐẦU TIÊN → TF-IDF & Scaler fit CHỈ trên train → transform test. X_train (1754×5015) và X_test (439×5015) đã xuất. 34/34 tests PASSED. 7 EDA figures @ 300 DPI. Cẩm (Phase 04/NB, Phase 06/SVM) và Sơn (Phase 05/RF) có thể bắt đầu train model ngay bây giờ.**

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

> **BẮT BUỘC cho mọi AI agent và thành viên (Thanh, Cẩm, Sơn) sau khi triển khai xong 1 task hoặc 1 phase.**
> Repository này (`CS114-Team10-Elderly-Scam-Detection`) là một dự án hoàn toàn độc lập, tự chứa (self-contained). Mọi đường dẫn và quy tắc dưới đây áp dụng trực tiếp từ thư mục gốc của repository này.

### 1. Phân định hai cấp độ đồng bộ tài liệu

*   **Cấp 1 — Task-Level Sync (Vi mô — Trong từng đầu việc nhỏ):**
    1. Đánh dấu `[x]` vào checkbox todo trong file kế hoạch phase (`plans/scam-detection-full-submit/phase-XX-*.md`).
    2. Commit atomic bằng Conventional Commit (ví dụ: `feat(phase04): train naive bayes baseline`).
    3. Tuyệt đối **KHÔNG** cập nhật lan tràn sang `AGENTS.md`, `project-roadmap.md` hoặc `plan.md` khi phase chưa hoàn thành trọn vẹn.
*   **Cấp 2 — Phase-Level Sync (Vĩ mô — Khi hoàn thành trọn vẹn 1 Phase):**
    *   Bắt buộc thực thi đồng bộ theo **Ma trận 10 Tài liệu Nội bộ (Internal Documentation Matrix)** bên dưới trước khi mở PR.

### 2. Ma trận 10 Tài liệu Bắt buộc Đồng bộ Nội bộ Repo (Internal Documentation Matrix)

| STT | Nhóm tài liệu | File đích | Điều kiện & Nội dung cập nhật bắt buộc |
|:---:|---|---|---|
| 1 | Kế hoạch chi tiết | `plans/scam-detection-full-submit/phase-XX-*.md` | Điền số liệu output thực tế vào mục `## Evidence`, viết `## Summary` sau triển khai, tick 100% checklist. |
| 2 | Kế hoạch tổng thể | `plans/scam-detection-full-submit/plan.md` | Đổi status Phase từ `in-progress` sang `passed` ✅, cập nhật ngày hoàn thành `updated: YYYY-MM-DD`. |
| 3 | Lộ trình & Phân công | `draft/scam-detection/docs/project-roadmap.md` | Cập nhật tiến độ biểu đồ Mermaid Gantt, đánh dấu hoàn thành trong bảng Sprint task của 3 thành viên. |
| 4 | Bối cảnh điều phối AI | `AGENTS.md` (file này) | Cập nhật bảng `Current State`, bổ sung khối `Verdict` kết quả thực nghiệm, cập nhật `Next Actions`. |
| 5 | Kiến trúc hệ thống | `draft/scam-detection/docs/system-architecture.md` | Cập nhật sơ đồ luồng dữ liệu, bảng không gian đặc trưng hoặc bảng artifacts nếu có thay đổi kỹ thuật. |
| 6 | Technical Registries | `draft/scam-detection/{data,models,notebooks,reports}/README.md` | Đăng ký artifacts mới:<br>• `models/README.md`: Đăng ký tên model, hyperparams, 5 metrics (Acc, Prec, Rec, F1, ROC-AUC), file path.<br>• `data/processed/README.md`: Đăng ký schema 24 cột hoặc ma trận `.pkl` mới.<br>• `notebooks/README.md`: Xác nhận notebook 01–06 chạy hoàn tất, đã dọn sạch output cells (stripped outputs < 50MB).<br>• `reports/figures/README.md`: Đăng ký biểu đồ mới (300 DPI) kèm chú giải học thuật. |
| 7 | Cổng thông tin nhóm | `README.md` & `draft/scam-detection/README.md` | Cập nhật trạng thái pipeline và bảng tiến độ Sprint tổng thể. |
| 8 | Đề cương báo cáo | `plans/scam-detection-full-submit/phase-09-report-ppt.md` | Nạp ngay số liệu định lượng mới (metrics, bảng so sánh) vào outline Chương 4 để chuẩn bị xuất Word/Slide. |
| 9 | Đóng gói nộp bài | `submit/README.md` | Rà soát danh mục artifacts cần đóng gói vào ZIP `25730067-25730013-25730061.zip`. |
| 10 | Pull Request chuẩn UIT | GitHub Pull Request | Mở PR theo đúng quy chuẩn: Tiêu đề Title Case không prefix, Body Tiếng Việt danh sách gạch đầu dòng lồng nhau, kết thúc bằng `- Xác minh kiểm định thực nghiệm:`. |

### 3. Quy tắc về .pkl và artifacts

*   `data/raw/dataset.csv` → **Commit nếu < 50MB** (dataset 2.193 mẫu thực tế, 100% Zero Synthetic Text)
*   `data/processed/*.pkl` (TF-IDF matrices, splits) → **Commit luôn** nếu < 50MB
*   `models/vectorizer.pkl`, `models/best_model_bundle.pkl` → **Commit luôn** nếu < 50MB (phục vụ Demo UI và kiểm định)
*   `models/*.pkl` lớn (> 50MB) → **Gitignore** → ghi hướng dẫn reproduce rõ ràng trong `models/README.md`

### 4. Quy chuẩn tạo Pull Request (PR Standards) — BẮT BUỘC

> 📌 **Mọi Agent AI và thành viên khi tạo PR bắt buộc phải tuân theo quy chuẩn:**
> 1. **PR Title**: Viết bằng Tiếng Anh chuẩn **Title Case**, bắt đầu bằng Imperative Verb, **TUYỆT ĐỐI KHÔNG** dùng tiền tố (`feat:`, `chore:`, `fix:`, `docs:`...).
> 2. **PR Body**: Viết bằng **Tiếng Việt**, sử dụng cấu trúc **danh sách gạch đầu dòng lồng nhau (nested bullet points)** súc tích:
>    * Mục lớn: `- [Động từ hành động tóm tắt công việc]:`
>    * Mục con: `  - [Mô tả chi tiết]:` ghi rõ đường dẫn tệp trong backticks (`path/to/file`), hàm được sửa đổi, số liệu kỹ thuật.
>    * Mục cuối cùng luôn là: `- Xác minh kiểm định thực nghiệm:` ghi rõ kết quả kiểm định (`pytest`, test scripts), dung lượng tệp an toàn Git (< 50MB).
>    * **TUYỆT ĐỐI KHÔNG** chèn bảng lớn, checklist `[x]`, hay badges rườm rà vào PR body.
> 3. **Assignee**: Tự gán chính mình `--assignee "@me"`.
> 4. **Lệnh kiểm tra trước khi mở PR:**
>    ```bash
>    python3 verify_final.py
>    ```

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
1. **Luồng A (Dữ liệu & Khóa Dataset — Sơn Lead):** ✅ **HOÀN THÀNH (15/09/2026)**
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

