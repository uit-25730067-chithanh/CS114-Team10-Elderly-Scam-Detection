# Phase 10 — Submit Package

**Parent plan:** [plan.md](./plan.md)  
**Previous phase:** [Phase 09 — Report & PPT](./phase-09-report-ppt.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P0 — Deadline critical |
| Status | `not-started` |
| Review | ⬜ Not reviewed |
| Estimated effort | 1–2h |
| Sprint | Sprint 3 Fast-Track (22/09/2026) |

## Context

Đóng gói tất cả deliverables vào thư mục nộp bài theo đúng cấu trúc yêu cầu CS114. Đóng gói hoàn tất ngày 22/09/2026 để sẵn sàng nộp và thuyết trình ngày 23/09/2026 (Hạn LMS gốc: 13/10/2026 23:59).

## Required Structure (từ README.md)

```
25730067-25730013-25730061/
├── DOCS/
│   ├── DoAnMonHoc.docx        # Báo cáo đầy đủ
│   └── DoAnMonHoc.pdf         # PDF exported
├── SLIDES/
│   └── Presentation_CS114.pptx
├── SOURCE/
│   ├── data/                  # dataset.csv + processed
│   ├── models/                # .pkl files
│   ├── src/                   # Source code
│   ├── notebooks/             # Jupyter notebooks
│   ├── demo/                  # Streamlit app
│   ├── app.py                 # Entry point cho demo
│   ├── requirements.txt
│   └── reports/               # Figures & comparison CSV
└── README.md                  # Hướng dẫn chạy code
```

## Implementation Steps

### Step 1 — Pre-flight Checks

```bash
# Verify tất cả files tồn tại
[ -f submit/DOCS/DoAnMonHoc.docx ] && echo "✅ Word" || echo "❌ Word missing"
[ -f submit/DOCS/DoAnMonHoc.pdf ] && echo "✅ PDF" || echo "❌ PDF missing"
[ -f submit/SLIDES/Presentation_CS114.pptx ] && echo "✅ PPT" || echo "❌ PPT missing"
[ -d draft/scam-detection/src ] && echo "✅ Source" || echo "❌ Source missing"
[ -f draft/scam-detection/data/raw/dataset.csv ] && echo "✅ Dataset" || echo "❌ Dataset missing"
```

### Step 2 — Copy Files to Submit Structure

```bash
SUBMIT_DIR="submit/25730067-25730013-25730061"
mkdir -p "$SUBMIT_DIR"/{DOCS,SLIDES,SOURCE}

# Copy DOCS
cp submit/DOCS/DoAnMonHoc.docx "$SUBMIT_DIR/DOCS/"
cp submit/DOCS/DoAnMonHoc.pdf "$SUBMIT_DIR/DOCS/"

# Copy SLIDES
cp submit/SLIDES/Presentation_CS114.pptx "$SUBMIT_DIR/SLIDES/"

# Copy SOURCE (selective — không copy .venv, __pycache__)
rsync -av --exclude='.venv' --exclude='__pycache__' --exclude='.git' \
    draft/scam-detection/ "$SUBMIT_DIR/SOURCE/"

# Create README cho submit
cp submit/README_SUBMIT.md "$SUBMIT_DIR/README.md"
```

### Step 3 — Create Submit README

```markdown
# Đồ Án Cuối Kỳ CS114 — Machine Learning

## Đề tài
Nghiên cứu và Xây dựng Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam

## Thành viên nhóm
| MSSV | Họ tên | Vai trò |
|------|--------|---------|
| 25730067 | Đặng Chí Thanh | Trưởng nhóm / Data & NLP Lead / Evaluation XAI |
| 25730013 | Bùi Thị Mỷ Cẩm | Modeling Engineer (NB, XGBoost, SVM) |
| 25730061 | Hoàng Cao Sơn | Data Collection Lead, Random Forest, Demo UI |

## Hướng dẫn chạy code

### Cài đặt
\`\`\`bash
cd SOURCE
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\`\`\`

### Chạy Demo
\`\`\`bash
streamlit run demo/app.py
\`\`\`

### Chạy Notebooks
Mở các file trong thư mục `notebooks/` bằng Jupyter Notebook / JupyterLab.
```

### Step 4 — Zip & Verify

```bash
cd submit/
zip -r "25730067-25730013-25730061.zip" "25730067-25730013-25730061/"

# Verify zip content
unzip -l "25730067-25730013-25730061.zip" | head -30
```

### Step 5 — Upload to LMS

Nộp file `25730067-25730013-25730061.zip` lên Moodle LMS trước deadline.

## Checklist

- [ ] Tất cả phases 00–09 đã PASSED
- [ ] DOCS/ có Word + PDF
- [ ] SLIDES/ có PPT
- [ ] SOURCE/ có code, data, models, notebooks, demo
- [ ] SOURCE/requirements.txt đầy đủ
- [ ] README.md hướng dẫn chạy code
- [ ] ZIP file tạo thành công
- [ ] File size reasonable (< 100MB, không có .venv)
- [ ] Test unzip → chạy được
- [ ] Đóng gói ZIP hoàn tất trước **22/09/2026** — sẵn sàng nộp ngay khi báo cáo xong 23/09
- [ ] Upload ZIP lên Moodle LMS: thực hiện sau khi báo cáo 23/09, **trước hạn gốc 13/10/2026 23:59**

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| ZIP structure correct | `unzip -l` matches required structure |
| No junk files | No .venv, __pycache__, .git in ZIP |
| Demo reproducible | Fresh unzip → pip install → streamlit run works |
| Uploaded | LMS submission confirmed |

## Evidence Section *(điền sau khi làm)*

```
(Chưa thực hiện)
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ZIP quá lớn | Medium | Medium | Exclude large files, compress models |
| Missing files | Low | High | Pre-flight checklist |
| LMS upload fail | Low | Critical | Upload 1 ngày trước deadline |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa bắt đầu.

## Commit

```bash
git add submit/
git commit -m "feat(phase10): submit package 25730067-25730013-25730061.zip ready"
```
