# 📊 Slide Outline — CS114 Final: Vietnamese Elderly Scam Detection

> **Template mẫu Phase 09 — Bàn giao Cẩm tạo PR và hoàn thiện**
>
> Skill: `uit:powerpoint-slides` | Branch: `feat/phase-09-ppt-template`
> Người review: Đặng Chí Thanh (PM)

---

## 🎯 Phase 1 Interview — Thông số đầu vào (Đã xác định)

| Câu hỏi | Câu trả lời |
|---------|-------------|
| **Thời lượng thuyết trình?** | 15 phút (luân phiên 3 thành viên) |
| **Đối tượng nghe?** | ThS. Cáp Phạm Đình Thăng + lớp CS114.F31.CN2.TTNT |
| **Theme?** | **Navy-Blue Gradient** — đồng bộ Streamlit Demo App (`#0B2545→#1E5FC2` header, White content, Red alert, Amber risk) |
| **Speaker Notes?** | Có — 3-5 gạch đầu dòng/slide |
| **Script file?** | `generate_slides.js` → `phase09_presentation.pptx` |
| **Slides mục tiêu?** | 15 nội dung + 1 divider appendix + 3 backup = 19 tổng |

---

## 📐 Phase 2 — Cấu trúc Slides

### BLOCK 1: MỞ ĐẦU (3 slides)

#### Slide 1 — Cover (layout: `title`)
- Tiêu đề: Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi
- Subtitle: CS114 — Máy học | Nhóm 10 | ThS. Cáp Phạm Đình Thăng
- Thành viên: Đặng Chí Thanh (25730067) · Bùi Thị Mỷ Cẩm (25730013) · Hoàng Cao Sơn (25730061)
- Visual: UIT logo + dark navy background + gold accent

#### Slide 2 — Bối cảnh & Vấn đề (layout: `stat-callout`)
- Câu hỏi mở: "Tại sao người cao tuổi dễ bị lừa đảo qua tin nhắn hơn?"
- Big stat cards: 420 mẫu lừa đảo | 4 nhóm bẫy tâm lý | 100% Zero Synthetic Text

#### Slide 3 — Mục tiêu & Đóng góp (layout: `icon-grid`)
- 4 ô mục tiêu: So sánh 4 model | F1>=88% Recall>=92% | SHAP XAI | Demo Streamlit

---

### BLOCK 2: DỮ LIỆU & PHƯƠNG PHÁP (4 slides)

#### Slide 4 — Section Divider: Dữ liệu & Phương pháp (layout: `section-divider`)

#### Slide 5 — Dataset 2.193 mẫu (layout: `text-left-image-right`)
- Trái: 2.193 mẫu | 80/20 Split | 7 tầng kiểm toán | 3 thành viên
- Phải: figures/label_distribution.png

#### Slide 6 — 4 Nhóm Bẫy Tâm lý (layout: `two-column`)
- Trái: scam_category_distribution.png
- Phải: Bảng 4 nhóm (Quyền lực 127 | Gia đình 88 | Quà tặng 46 | Dịch vụ công 159)

#### Slide 7 — Pipeline Tiền xử lý & Feature Engineering (layout: `full-diagram`)
- Graphviz LR: Input -> Unicode NFC -> 160 Teencode -> PyVi -> TF-IDF 5000 -> 15 Aux -> X(5015)
- Cards: TF-IDF params + Zero-leakage note

---

### BLOCK 3: MÔ HÌNH & KẾT QUẢ (4 slides)

#### Slide 8 — Section Divider: Mô hình & Kết quả (layout: `section-divider`)

#### Slide 9 — Tổng quan 4 Mô hình (layout: `table-with-insight`)
| Mô hình | Accuracy | Recall | F1 | ROC-AUC |
|---------|----------|--------|----|---------|
| XGBoost ⭐ | 98.18% | 97.62% | 95.35% | 99.84% |
| SVM Linear | 97.95% | 96.43% | 94.74% | 99.86% |
| Random Forest | 97.72% | 97.62% | 94.25% | 99.77% |
| Naive Bayes | 95.44% | 92.86% | 88.64% | 99.11% |
- Insight: XGBoost best overall — FN=2 (chỉ bỏ lọt 2/42 tin lừa đảo)

#### Slide 10 — ROC & PR Curves (layout: `two-column`)
- Trái: roc_curves_comparison.png | Phải: precision_recall_curves.png

#### Slide 11 — SHAP & XAI (layout: `text-left-image-right`)
- Phải: shap_summary.png
- Trái: Top keywords: "chuyển khoản", "khẩn cấp", "xác nhận" | urgency_score top aux feature

---

### BLOCK 4: DEMO & KẾT LUẬN (4 slides + References + Thank You)

#### Slide 12 — Section Divider: Demo & Kết luận (layout: `section-divider`)

#### Slide 13 — Streamlit Demo UI (layout: `figure-with-text`)
- Figure: demo_03_scam_detection_verdict.png
- Bullets: 4 models | Font lớn NCT | Mobile responsive | Real-time SHAP

#### Slide 14 — Kết luận & Hướng phát triển (layout: `two-column`)
- Đạt được: F1=95.35% | Recall=97.62% | 2193 mẫu Zero Synthetic | Demo live
- Phát triển: PhoBERT | Voice scam | API tích hợp | Dataset 10k+

#### Slide 15 — References (layout: `references`)
- [1] XGBoost: Chen & Guestrin, KDD 2016
- [2] SVM Platt Calibration, 1999
- [3] PhoBERT: Nguyen et al., EMNLP 2020
- [4] Vietnamese SMS Dataset: IEEE Access 2026
- [5] Scikit-learn: Pedregosa et al., JMLR 2011

#### Slide 16 — Thank You (layout: `thank-you`)
- Cảm ơn Thầy và các bạn | Nhóm 10 | 23/09/2026 | UIT-ĐHQG-HCM

---

### BACKUP SLIDES Q&A (3 slides)

#### B1 — Chi tiết siêu tham số (layout: `table`)
- Hyperparameter grid + validation strategy cả 4 mô hình

#### B2 — Confusion Matrices (layout: `figure-with-text`)
- confusion_matrices_all.png — FP/FN phân tích

#### B3 — Learning Curves (layout: `two-column`)
- learning_curves_summary.png — chứng minh không overfit

---

## ❓ Câu hỏi mở cho Cẩm xác nhận khi tạo PR

1. Theme cuối: Sandwich (Navy/Gold) hay Midnight (toàn dark)?
2. Speaker notes: Cẩm điền theo slide outline này hay để các thành viên bổ sung?
3. Logo UIT: Dùng file trong docs/assets/ hay cần tải mới?
4. Transitions: academic preset hay tùy chỉnh thêm?
5. Cover slide: Ghi đủ MSSV hay chỉ tên thành viên?

---

## 🛠️ Workflow Cẩm thực hiện

```bash
# 1. Checkout branch
git checkout feat/phase-09-ppt-template

# 2. Install dependencies
npm install pptxgenjs

# 3. Tạo pipeline diagram
# Viết diagrams.json với graphviz LR pipeline

# 4. Viết generate_slides.js theo outline này

# 5. Compile
node generate_slides.js

# 6. Post-processing
python3 ../../.agents/skills/powerpoint-slides/scripts/inject_omml.py phase09_presentation.pptx formulas.json phase09_presentation.pptx
python3 ../../.agents/skills/powerpoint-slides/scripts/inject_transitions.py phase09_presentation.pptx --preset academic phase09_presentation.pptx

# 7. QA: visual check
python3 ../../.agents/skills/powerpoint-slides/scripts/soffice.py --headless --convert-to pdf --outdir /tmp phase09_presentation.pptx
pdftoppm -png -r 200 /tmp/phase09_presentation.pdf /tmp/slide

# 8. Tạo PR → tag @25730067
```

---

## 📋 PR Checklist (Cẩm điền khi tạo PR)

- [ ] Phase 2 structure plan được Thanh approve trước
- [ ] generate_slides.js chạy không lỗi
- [ ] OMML injection: 0 residual {{MATH:}} placeholders
- [ ] Transitions: academic preset applied
- [ ] QA score >= 90
- [ ] Speaker notes có mặt mọi content slide
- [ ] Tất cả figures embed đúng aspect ratio
- [ ] References slide: 5 bài báo authentic
- [ ] PR title: feat(phase-09): Create CS114 Final Defense Presentation Template
- [ ] PR body: tiếng Việt nested bullets
- [ ] Reviewer: @25730067 (Thanh - PM)
