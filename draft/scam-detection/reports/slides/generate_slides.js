/**
 * generate_slides.js — CS114 Final Phase 09 PPT Template
 * Skill: uit:powerpoint-slides (PptxGenJS + Navy-Blue Gradient Theme)
 * Theme: Đồng bộ với Streamlit Demo App (Navy→Blue header, White content, Red alert, Amber warning)
 *
 * Branch: feat/phase-09-ppt-template
 * Owner: Bùi Thị Mỷ Cẩm (25730013) — Cẩm completes this template
 * Reviewer: Đặng Chí Thanh (25730067)
 *
 * TODO for Cẩm:
 *   1. Fill in slide content following SLIDE_OUTLINE.md
 *   2. Add diagrams.json pipeline diagram
 *   3. Verify all figure paths exist in ../figures/
 *   4. Run: node generate_slides.js
 *   5. Run OMML + Transitions injection scripts
 *   6. Open PR against main → tag @25730067
 *
 * Figures available in ../figures/:
 *   - label_distribution.png
 *   - scam_category_distribution.png
 *   - roc_curves_comparison.png
 *   - precision_recall_curves.png
 *   - shap_summary.png
 *   - confusion_matrices_all.png
 *   - learning_curves_summary.png
 *   - demo_03_scam_detection_verdict.png
 *   - (+ 25 more in figures/)
 */

const PptxGenJS = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

// ─── THEME: Navy-Blue Gradient (Đồng bộ Streamlit Demo App) ─────────────────
// App colors: header gradient #0B2545→#1E5FC2, CTA blue #1e40af,
//             alert red #dc2626, warning amber #F59E0B, bg #f1f5f9
const T = {
  coverBg: "0B2545",       // Deep Navy — khớp header app (từ gradient)
  coverBg2: "1E5FC2",      // Blue — điểm cuối gradient header app
  contentBg: "FFFFFF",     // Pure White content slides
  sectionBg: "0B2545",     // Navy divider slides
  accent: "1E5FC2",        // Primary Blue — khớp CTA button app
  accentDark: "1e40af",    // Deep Blue — khớp màu chữ link app
  accentRed: "DC2626",     // Alert Red — khớp nút cảnh báo app (Gọi 156/113)
  accentAmber: "F59E0B",   // Amber Warning — khớp risk meter app
  text: "1F2937",          // Near-black body text
  textLight: "FFFFFF",     // White text on dark slides
  textMuted: "6B7280",     // Muted gray
  contentSubBg: "F1F5F9",  // Xám nhạt — khớp background tổng thể app
  positive: "15803D",      // Green metrics — khớp "Trực tuyến 24/7" badge
  neutral: "6B7280",
};

// ─── TYPOGRAPHY ──────────────────────────────────────────────────────────────
const F = {
  cover: { size: 32, bold: true, color: T.textLight, font: "Georgia" },
  coverSub: { size: 14, color: T.textLight, font: "Calibri" },   // Trắng trên Navy
  sectionTitle: { size: 28, bold: true, color: T.textLight, font: "Georgia" },
  titleBar: { size: 18, bold: true, color: T.text, font: "Georgia" },
  body: { size: 14, color: T.text, font: "Calibri" },
  bodySmall: { size: 12, color: T.text, font: "Calibri" },
  caption: { size: 10, color: T.textMuted, font: "Calibri", italic: true },
  cardTitle: { size: 14, bold: true, color: T.text, font: "Calibri" },
  tblHead: { size: 12, bold: true, color: T.textLight, font: "Calibri" },
  tblCell: { size: 11, color: T.text, font: "Calibri" },
  stat: { size: 36, bold: true, color: T.accent, font: "Georgia" },
};

// ─── LAYOUT CONSTANTS (16:9) ──────────────────────────────────────────────────
const SW = 10, SH = 5.625, M = 0.5;
const CW = SW - 2 * M;   // Content width: 9"
const CY = 1.1;           // Content area start Y (below header)
const CH = SH - CY - M;   // Content height: ~3.975"

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_16x9";
pptx.title = "CS114 Final — Vietnamese Elderly Scam Detection";
pptx.subject = "Phase 09 Defense Presentation";
pptx.author = "Nhóm 10 — Đặng Chí Thanh, Bùi Thị Mỷ Cẩm, Hoàng Cao Sơn";
pptx.company = "UIT — ĐHQG-HCM";

// Figure base path (relative to this script)
const FIG = path.join(__dirname, "../figures");

// ─── HELPER: Header bar (add to every content slide) ─────────────────────────
function addHeader(slide, title, section) {
  // Top accent bar (Navy-Blue gradient via solid Navy — PptxGenJS gradient workaround)
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: SW, h: 0.55,
    fill: { color: T.coverBg },
  });
  // Thin blue accent line at bottom of header bar
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0.55, w: SW, h: 0.035,
    fill: { color: T.accent },
  });
  // University label (left, white on Navy)
  slide.addText("UIT — CS114", {
    x: M, y: 0.08, w: 2.5, h: 0.38,
    fontSize: 10, color: "BFDBFE", font: "Calibri",  // light blue tint
  });
  // Navigation pill (right, white on Navy)
  if (section) {
    slide.addText(section, {
      x: 4.11, y: 0.08, w: 5.39, h: 0.38,
      fontSize: 10, color: "BFDBFE", font: "Calibri", align: "right",
    });
  }
  // Slide title (below header bar, dark text on white)
  slide.addText(title, {
    x: M, y: 0.65, w: CW, h: 0.45,
    ...F.titleBar, shrinkText: true,
  });
}

// ─── HELPER: Accent card ──────────────────────────────────────────────────────
function addCard(slide, x, y, w, h, title, bodyLines, opts = {}) {
  const fillColor = opts.fill || T.contentSubBg;   // #F1F5F9 — khớp app bg
  const borderColor = opts.border || T.accent;       // Blue border mặc định
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: fillColor }, line: { color: borderColor, width: 0.5 } });
  // Accent bar left (Blue — khớp app left-border style)
  slide.addShape(pptx.ShapeType.rect, { x, y, w: 0.06, h, fill: { color: borderColor } });
  const px = x + 0.15, pw = w - 0.25;
  // Title
  slide.addText(title, { x: px, y: y + 0.08, w: pw, h: 0.35, fontSize: F.cardTitle.size, bold: true, color: opts.titleColor || T.accentDark, font: "Calibri", shrinkText: true });
  // Body
  const bodyText = bodyLines.map(l => ({ text: l, options: { breakLine: true } }));
  slide.addText(bodyText, { x: px, y: y + 0.45, w: pw, h: h - 0.55, fontSize: F.body.size, color: opts.bodyColor || T.text, font: "Calibri", shrinkText: true, margin: [2, 0, 4, 0] });
}

// ─── SLIDE 1: COVER (Navy→Blue gradient — khớp app header) ──────────────────
(function slide01_cover() {
  const slide = pptx.addSlide();
  slide.background = { color: T.coverBg };  // Deep Navy #0B2545

  // Blue gradient strip (simulates app header gradient)
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 0, w: SW, h: SH,
    fill: { type: "solid", color: T.coverBg },
  });
  // Subtle blue overlay bottom half (gradient effect)
  slide.addShape(pptx.ShapeType.rect, {
    x: 0, y: 2.8, w: SW, h: 2.825,
    fill: { color: "102E5E" },   // Mid Navy — transition
  });

  // TODO Cẩm: Add UIT shield logo if available
  // slide.addImage({ path: path.join(__dirname, "../../../../docs/assets/logo_uit.png"), x: M, y: 0.15, w: 1.2, h: 0.6 });

  // Shield emoji label (khớp 🛡️ trong app)
  slide.addText("🛡️", { x: M, y: 0.9, w: CW, h: 0.6, fontSize: 36, align: "center" });

  slide.addText("PHÁT HIỆN TIN NHẮN LỪA ĐẢO\nNHẮM VÀO NGƯỜI CAO TUỔI", {
    x: M, y: 1.5, w: CW, h: 1.4,
    fontSize: 28, bold: true, color: T.textLight, font: "Georgia",
    align: "center", shrinkText: true,
  });
  slide.addText("Vietnamese Elderly Scam Detection", {
    x: M, y: 2.95, w: CW, h: 0.35,
    fontSize: 13, color: "BFDBFE", font: "Calibri", align: "center", italic: true,
  });
  // Divider (Blue accent — khớp app CTA button color)
  slide.addShape(pptx.ShapeType.rect, { x: 2.5, y: 3.35, w: 5, h: 0.04, fill: { color: T.accent } });
  slide.addText("CS114 — Máy học  |  Nhóm 10  |  ThS. Cáp Phạm Đình Thăng", {
    x: M, y: 3.45, w: CW, h: 0.35, fontSize: 12, color: "93C5FD", font: "Calibri", align: "center",
  });
  slide.addText("Đặng Chí Thanh (25730067)  ·  Bùi Thị Mỷ Cẩm (25730013)  ·  Hoàng Cao Sơn (25730061)", {
    x: M, y: 3.85, w: CW, h: 0.35, fontSize: 11, color: T.textLight, font: "Calibri", align: "center",
  });
  slide.addText("23/09/2026  |  UIT — ĐHQG-HCM", {
    x: M, y: 4.25, w: CW, h: 0.3, fontSize: 10, color: "6B7280", font: "Calibri", align: "center",
  });

  slide.addNotes("SLIDE 1 — COVER\n- Người trình bày đầu tiên: Đặng Chí Thanh (PM)\n- Giới thiệu tên đề tài và các thành viên\n- Nhấn mạnh: đề tài bảo vệ người cao tuổi khỏi lừa đảo tin nhắn tiếng Việt");
})();

// ─── SLIDE 2: BỐI CẢNH & VẤN ĐỀ ─────────────────────────────────────────────
(function slide02_context() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Bối cảnh & Vấn đề", "Giới thiệu");

  // TODO Cẩm: Add 3 stat callout cards
  const stats = [
    { title: "2.193 Mẫu Thực Tế", body: ["Thu thập từ báo chí, SMS thực,", "KLTN, IEEE Access 2026"] },
    { title: "4 Nhóm Bẫy Tâm lý", body: ["Quyền lực · Gia đình", "Quà tặng · Dịch vụ công"] },
    { title: "Zero Synthetic Text", body: ["100% văn bản đời thực", "0% AI tự sinh, 7 tầng kiểm toán"] },
  ];
  stats.forEach((s, i) => {
    const x = M + i * 3.0, y = CY + 0.3, w = 2.8, h = 1.4;
    addCard(slide, x, y, w, h, s.title, s.body);
  });

  // Opening question
  slide.addText('"Tại sao người cao tuổi dễ bị lừa đảo qua tin nhắn hơn?"', {
    x: M, y: CY + 2.0, w: CW, h: 0.6,
    fontSize: 16, bold: true, color: T.text, font: "Georgia",
    align: "center", italic: true, shrinkText: true,
  });

  slide.addNotes("SLIDE 2 — BỐI CẢNH\n- Mở bằng câu hỏi gây suy nghĩ\n- Nêu quy mô dataset: 2.193 mẫu thực tế, zero AI-generated\n- 4 nhóm bẫy tâm lý — đây là đóng góp học thuật chính của nhóm\n- Chuyển sang: Mục tiêu nghiên cứu");
})();

// ─── SLIDE 3: MỤC TIÊU ────────────────────────────────────────────────────────
(function slide03_objectives() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Mục tiêu & Đóng góp của Nhóm", "Giới thiệu");

  const goals = [
    { title: "So sánh 4 Mô hình ML", body: ["Naive Bayes · Random Forest", "XGBoost · SVM Linear"], icon: "🎯" },
    { title: "Vượt chỉ tiêu kỹ thuật", body: ["F1 ≥ 88% · Recall ≥ 92%", "4 mô hình đều đạt mục tiêu"], icon: "📊" },
    { title: "Giải thích AI (XAI)", body: ["SHAP Beeswarm Analysis", "Top-20 từ khóa cảnh báo"], icon: "🧠" },
    { title: "Demo Streamlit", body: ["Ứng dụng đời thực", "Trợ năng người cao tuổi"], icon: "🖥️" },
  ];

  goals.forEach((g, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = M + col * 4.5, y = CY + 0.2 + row * 1.85, w = 4.2, h = 1.65;
    addCard(slide, x, y, w, h, `${g.icon}  ${g.title}`, g.body);
  });

  slide.addNotes("SLIDE 3 — MỤC TIÊU\n- Đọc nhanh 4 mục tiêu\n- Nhấn: cả 4 mô hình đều vượt chỉ tiêu đề ra\n- Chuyển sang: Phần Dữ liệu");
})();

// ─── SLIDE 4: SECTION DIVIDER — Dữ liệu ─────────────────────────────────────
(function slide04_divider_data() {
  const slide = pptx.addSlide();
  slide.background = { color: T.sectionBg };
  slide.addText("Dữ liệu &\nPhương pháp", {
    x: M, y: 1.5, w: CW, h: 2.2,
    fontSize: 36, bold: true, color: T.textLight, font: "Georgia", align: "center", shrinkText: true,
  });
  slide.addText("Thu thập  ·  Tiền xử lý  ·  Feature Engineering", {
    x: M, y: 3.8, w: CW, h: 0.4,
    fontSize: 14, color: T.accent, font: "Calibri", align: "center",
  });
  slide.addShape(pptx.ShapeType.rect, { x: 3, y: 3.7, w: 4, h: 0.03, fill: { color: T.accent } });
})();

// ─── SLIDE 5: DATASET ─────────────────────────────────────────────────────────
(function slide05_dataset() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Dataset: 2.193 Mẫu Thực Tế", "Dữ liệu & Phương pháp");

  const figPath = path.join(FIG, "label_distribution.png");
  if (fs.existsSync(figPath)) {
    // TODO Cẩm: Verify aspect ratio of label_distribution.png
    slide.addImage({ path: figPath, x: 5.4, y: CY + 0.1, w: 4.0, h: 3.4 });
  }

  const bullets = [
    "2.193 mẫu | Stratified Split 80/20",
    "Label 0 — Bình thường: 1.773 mẫu",
    "Label 1 — Lừa đảo: 420 mẫu (4.2:1)",
    "7 tầng kiểm toán: 0% PII, 0% synthetic",
    "3 thành viên: Thanh (1.773) · Sơn (215) · Cẩm (205)",
    "Train: 1.754 | Test: 439 (Holdout 50 ảnh thực)",
  ];
  slide.addText(bullets.map(b => ({ text: b, options: { bullet: true, breakLine: true } })), {
    x: M, y: CY + 0.2, w: 4.6, h: CH - 0.3,
    fontSize: F.body.size, color: T.text, font: "Calibri", shrinkText: true, margin: [2, 0, 4, 0],
  });

  slide.addNotes("SLIDE 5 — DATASET\n- Nhấn mạnh Zero Synthetic Text (100% đời thực)\n- 7 tầng kiểm toán nghiêm ngặt\n- 3 thành viên thu thập độc lập\n- Chuyển sang: phân loại 4 nhóm bẫy tâm lý");
})();

// ─── SLIDE 6: 4 NHÓM BẪY TÂM LÝ ──────────────────────────────────────────────
(function slide06_scam_categories() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "4 Nhóm Bẫy Tâm lý trong Dataset", "Dữ liệu & Phương pháp");

  const figPath = path.join(FIG, "scam_category_distribution.png");
  if (fs.existsSync(figPath)) {
    slide.addImage({ path: figPath, x: M, y: CY + 0.1, w: 4.2, h: 3.4 });
  }

  // Table right side
  const rows = [
    [{ text: "Nhóm bẫy tâm lý", options: { bold: true, ...F.tblHead, fill: { color: T.coverBg } } },
     { text: "Mẫu", options: { bold: true, ...F.tblHead, fill: { color: T.coverBg } } },
     { text: "Kịch bản tiêu biểu", options: { bold: true, ...F.tblHead, fill: { color: T.coverBg } } }],
    ["Đe dọa quyền lực", "127", "Giả cảnh sát / tòa án"],
    ["Khẩn cấp gia đình", "88", "Con cháu tai nạn, cần tiền"],
    ["Dụ dỗ quà tặng", "46", "Trúng thưởng, ưu đãi sức khỏe"],
    ["Giả dịch vụ công", "159", "BHXH, điện lực giả mạo"],
  ];
  slide.addTable(rows, {
    x: 5.0, y: CY + 0.3, w: 4.5,
    fontSize: F.tblCell.size, font: "Calibri",
    border: { pt: 0.5, color: T.accent },
    rowH: 0.55,
  });

  slide.addNotes("SLIDE 6 — NHÓM BẪY TÂM LÝ\n- 4 pattern lừa đảo NCT được phát hiện trong data\n- Đe dọa quyền lực (127) và Dịch vụ công (159) chiếm đa số\n- Nhóm Quà tặng (46) ít nhưng rất tinh vi\n- Chuyển sang: pipeline kỹ thuật");
})();

// ─── SLIDE 7: PIPELINE ────────────────────────────────────────────────────────
(function slide07_pipeline() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Pipeline Tiền xử lý & Feature Engineering", "Dữ liệu & Phương pháp");

  // TODO Cẩm: Add rendered pipeline diagram from diagrams.json (Graphviz LR)
  // slide.addImage({ path: "diagrams/pipeline_flow.png", x: M, y: CY + 0.1, w: CW, h: 2.2 });

  // Placeholder cards for pipeline steps
  const steps = [
    { title: "1. Unicode NFC", body: ["Chuẩn hóa ký tự tiếng Việt"] },
    { title: "2. 160 Teencode", body: ["Từ viết tắt → từ chuẩn"] },
    { title: "3. PyVi Tokenizer", body: ["Tách từ tiếng Việt"] },
    { title: "4. TF-IDF", body: ["5.000 từ | ngram(1,2)"] },
    { title: "5. 15 Aux Features", body: ["urgency_score, caps_ratio..."] },
  ];

  steps.forEach((s, i) => {
    const x = M + i * 1.82, y = CY + 0.2, w = 1.72, h = 1.5;
    addCard(slide, x, y, w, h, s.title, s.body);
    // Arrow between steps
    if (i < steps.length - 1) {
      slide.addShape(pptx.ShapeType.rightArrow, {
        x: x + 1.73, y: y + 0.6, w: 0.09, h: 0.3,
        fill: { color: T.accent },
      });
    }
  });

  // Zero-leakage note card
  addCard(slide, M, CY + 1.85, CW, 1.0,
    "Zero-Leakage Protocol",
    ["fit() chỉ trên X_train  →  transform() trên Train + Test",
     "Tránh data leakage: vectorizer & scaler không được thấy Test set"],
    { fill: "FEF3C7" }
  );

  slide.addNotes("SLIDE 7 — PIPELINE\n- Giải thích ngắn gọn 5 bước\n- Nhấn mạnh Zero-Leakage: không train vectorizer trên test data\n- Feature vector cuối: 5.015 chiều (5.000 TF-IDF + 15 Aux)\n- Chuyển sang: phần Mô hình");
})();

// ─── SLIDE 8: SECTION DIVIDER — Mô hình ─────────────────────────────────────
(function slide08_divider_models() {
  const slide = pptx.addSlide();
  slide.background = { color: T.sectionBg };  // Navy
  slide.addText("Mô hình &\nKết quả", {
    x: M, y: 1.5, w: CW, h: 2.0,
    fontSize: 36, bold: true, color: T.textLight, font: "Georgia", align: "center", shrinkText: true,
  });
  slide.addText("Naive Bayes  ·  Random Forest  ·  XGBoost  ·  SVM Linear", {
    x: M, y: 3.65, w: CW, h: 0.4,
    fontSize: 13, color: "93C5FD", font: "Calibri", align: "center",  // Light Blue text
  });
  slide.addShape(pptx.ShapeType.rect, { x: 2, y: 3.57, w: 6, h: 0.04, fill: { color: T.accent } });
})();

// ─── SLIDE 9: MODEL COMPARISON TABLE ─────────────────────────────────────────
(function slide09_model_comparison() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "So sánh 4 Mô hình Machine Learning", "Mô hình & Kết quả");

  const rows = [
    // Header
    [{ text: "Mô hình", options: { bold: true, color: T.textLight, fill: { color: T.coverBg }, fontSize: 12 } },
     { text: "Accuracy", options: { bold: true, color: T.textLight, fill: { color: T.coverBg }, fontSize: 12 } },
     { text: "Precision", options: { bold: true, color: T.textLight, fill: { color: T.coverBg }, fontSize: 12 } },
     { text: "Recall", options: { bold: true, color: T.textLight, fill: { color: T.coverBg }, fontSize: 12 } },
     { text: "F1", options: { bold: true, color: T.textLight, fill: { color: T.coverBg }, fontSize: 12 } },
     { text: "ROC-AUC", options: { bold: true, color: T.textLight, fill: { color: T.coverBg }, fontSize: 12 } }],
    // XGBoost — best
    [{ text: "XGBoost ⭐", options: { bold: true, fill: { color: "FEF9EC" }, fontSize: 11 } },
     { text: "98.18%", options: { bold: true, color: T.positive, fontSize: 11 } },
     { text: "93.18%", options: { bold: true, color: T.positive, fontSize: 11 } },
     { text: "97.62%", options: { bold: true, color: T.positive, fontSize: 11 } },
     { text: "95.35%", options: { bold: true, color: T.positive, fontSize: 11 } },
     { text: "99.84%", options: { bold: true, color: T.positive, fontSize: 11 } }],
    ["SVM Linear", "97.95%", "93.10%", "96.43%", "94.74%", "99.86%"],
    ["Random Forest", "97.72%", "91.11%", "97.62%", "94.25%", "99.77%"],
    [{ text: "Naive Bayes", options: { color: T.textMuted, fontSize: 11 } },
     { text: "95.44%", options: { color: T.textMuted, fontSize: 11 } },
     { text: "84.78%", options: { color: T.textMuted, fontSize: 11 } },
     { text: "92.86%", options: { color: T.textMuted, fontSize: 11 } },
     { text: "88.64%", options: { color: T.textMuted, fontSize: 11 } },
     { text: "99.11%", options: { color: T.textMuted, fontSize: 11 } }],
  ];
  slide.addTable(rows, {
    x: M, y: CY + 0.1, w: CW,
    fontSize: 11, font: "Calibri",
    border: { pt: 0.5, color: T.accent },
    rowH: 0.55,
  });

  // Insight card (Amber warning — khớp risk meter app)
  addCard(slide, M, CY + 2.65, CW, 0.9,
    "Kết luận: XGBoost — Mô hình tốt nhất tổng thể",
    ["FN=2 (chỉ bỏ lọt 2 tin lừa đảo trên 42 mẫu test lừa đảo)",
     "Tất cả 4 mô hình vượt chỉ tiêu: F1 ≥ 88%, Recall ≥ 92%"],
    { fill: "FEF3C7", border: T.accentAmber }
  );

  slide.addNotes("SLIDE 9 — MODEL TABLE\n- XGBoost best overall: F1=95.35%, Recall=97.62%\n- SVM có ROC-AUC cao nhất (99.86%) nhưng F1 thấp hơn XGBoost\n- Naive Bayes vẫn đạt F1=88.64% — solid baseline\n- Nhấn: tất cả đều vượt chỉ tiêu GV yêu cầu");
})();

// ─── SLIDE 10: ROC & PR CURVES ────────────────────────────────────────────────
(function slide10_curves() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "ROC Curves & Precision-Recall Curves", "Mô hình & Kết quả");

  const rocPath = path.join(FIG, "roc_curves_comparison.png");
  const prPath = path.join(FIG, "precision_recall_curves.png");
  if (fs.existsSync(rocPath)) {
    slide.addImage({ path: rocPath, x: M, y: CY + 0.1, w: 4.3, h: 3.5 });
    slide.addText("(a) ROC Curves — Tất cả AUC ≥ 99%", {
      x: M, y: CY + 3.65, w: 4.3, h: 0.25, ...F.caption, align: "center",
    });
  }
  if (fs.existsSync(prPath)) {
    slide.addImage({ path: prPath, x: 5.2, y: CY + 0.1, w: 4.3, h: 3.5 });
    slide.addText("(b) Precision-Recall Curves", {
      x: 5.2, y: CY + 3.65, w: 4.3, h: 0.25, ...F.caption, align: "center",
    });
  }

  slide.addNotes("SLIDE 10 — ROC & PR\n- ROC-AUC ≥ 99% cho tất cả: chứng minh model chất lượng cao\n- PR curve: XGBoost và SVM có precision cao ở recall cao\n- Chuyển sang: SHAP giải thích model");
})();

// ─── SLIDE 11: SHAP XAI ───────────────────────────────────────────────────────
(function slide11_shap() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Giải thích Mô hình — SHAP Analysis (XAI)", "Mô hình & Kết quả");

  const shapPath = path.join(FIG, "shap_summary.png");
  if (fs.existsSync(shapPath)) {
    slide.addImage({ path: shapPath, x: 4.8, y: CY + 0.1, w: 4.7, h: 3.6 });
  }

  const bullets = [
    "Top từ khóa kích hoạt cảnh báo:",
    "  → \"chuyển khoản\", \"khẩn cấp\", \"xác nhận\"",
    "  → \"phạt\", \"bảo hiểm\", \"cục thuế\"",
    "urgency_score là auxiliary feature quan trọng nhất",
    "Màu đỏ → push toward Scam (label 1)",
    "Màu xanh → push toward Normal (label 0)",
    "SHAP giải thích từng quyết định — không phải blackbox",
  ];
  slide.addText(bullets.map(b => ({ text: b, options: { bullet: !b.startsWith("  "), breakLine: true } })), {
    x: M, y: CY + 0.2, w: 4.3, h: CH - 0.3,
    fontSize: F.body.size, color: T.text, font: "Calibri", shrinkText: true,
  });

  slide.addNotes("SLIDE 11 — SHAP XAI\n- Đây là điểm học thuật quan trọng nhất: giải thích được model\n- urgency_score là feature tổng hợp nhóm tự thiết kế\n- SHAP giúp phát hiện từ khóa tâm lý học ẩn trong tin nhắn\n- Chuyển sang: Demo ứng dụng");
})();

// ─── SLIDE 12: SECTION DIVIDER — Demo ────────────────────────────────────────
(function slide12_divider_demo() {
  const slide = pptx.addSlide();
  slide.background = { color: T.sectionBg };
  slide.addText("Demo Ứng dụng &\nKết luận", {
    x: M, y: 1.5, w: CW, h: 2.0,
    fontSize: 36, bold: true, color: T.textLight, font: "Georgia", align: "center", shrinkText: true,
  });
  slide.addText("Streamlit Web App  ·  Kết quả  ·  Hướng phát triển", {
    x: M, y: 3.65, w: CW, h: 0.4,
    fontSize: 13, color: T.accent, font: "Calibri", align: "center",
  });
  slide.addShape(pptx.ShapeType.rect, { x: 2, y: 3.57, w: 6, h: 0.03, fill: { color: T.accent } });
})();

// ─── SLIDE 13: DEMO UI ────────────────────────────────────────────────────────
(function slide13_demo() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Demo: Streamlit Web Application", "Demo & Kết luận");

  const demoPath = path.join(FIG, "demo_03_scam_detection_verdict.png");
  if (fs.existsSync(demoPath)) {
    // Demo screenshot center-left
    slide.addImage({ path: demoPath, x: M, y: CY + 0.1, w: 5.5, h: 3.6 });
  }

  const features = [
    "4 mô hình trong 1 ứng dụng (Model Catalog)",
    "Font lớn ≥16px — trợ năng người cao tuổi",
    "Responsive trên mobile & desktop",
    "Real-time prediction trong < 1 giây",
    "SHAP explanation cho từng kết quả",
    "16/16 Playwright E2E tests PASSED",
  ];
  slide.addText(features.map(f => ({ text: f, options: { bullet: true, breakLine: true } })), {
    x: 6.0, y: CY + 0.3, w: 3.5, h: CH - 0.4,
    fontSize: 12, color: T.text, font: "Calibri", shrinkText: true,
  });

  slide.addNotes("SLIDE 13 — DEMO\n- Nếu cho phép: live demo trực tiếp streamlit app\n- Nếu không: dùng screenshot này\n- Nhấn: accessibility cho người cao tuổi (font lớn)\n- Chuyển sang: Kết luận");
})();

// ─── SLIDE 14: KẾT LUẬN ──────────────────────────────────────────────────────
(function slide14_conclusion() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Kết luận & Hướng Phát triển", "Demo & Kết luận");

  const achieved = [
    "✅ F1=95.35% (mục tiêu ≥88%)",
    "✅ Recall=97.62% (mục tiêu ≥92%)",
    "✅ 4 mô hình so sánh (mục tiêu ≥3)",
    "✅ 2.193 mẫu Zero Synthetic Text",
    "✅ Demo Streamlit hoạt động đầy đủ",
    "✅ SHAP XAI — giải thích mô hình",
  ];
  const future = [
    "🔭 Tích hợp PhoBERT (BERT tiếng Việt)",
    "🔭 Mở rộng: Voice scam detection",
    "🔭 API tích hợp app ngân hàng / nhà mạng",
    "🔭 Dataset lớn hơn: 10.000+ mẫu",
    "🔭 Real-time monitoring dashboard",
  ];

  // Kết quả: Blue card (khớp màu chính app)
  addCard(slide, M, CY + 0.1, 4.3, CH - 0.1,
    "Kết quả đạt được", achieved.map(a => a),
    { fill: "EFF6FF", border: T.accent }       // Light blue fill
  );
  // Tương lai: Amber card (khớp risk meter warning color)
  addCard(slide, 5.2, CY + 0.1, 4.3, CH - 0.1,
    "Hướng phát triển", future.map(f => f),
    { fill: "FFFBEB", border: T.accentAmber }  // Light amber fill
  );

  slide.addNotes("SLIDE 14 — KẾT LUẬN\n- Nhóm đã hoàn thành đầy đủ tất cả mục tiêu đề ra\n- XGBoost là best model với F1=95.35%\n- Điểm mạnh: dataset thực tế + XAI giải thích + demo live\n- Mở ra: tích hợp PhoBERT và mở rộng sang voice scam");
})();

// ─── SLIDE 15: REFERENCES ────────────────────────────────────────────────────
(function slide15_references() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Tài liệu tham khảo", "Tham khảo");

  const refs = [
    "[1] T. Chen & C. Guestrin, \"XGBoost: A Scalable Tree Boosting System,\" KDD 2016.",
    "[2] J. Platt, \"Probabilistic Outputs for SVMs,\" Advances in Large Margin Classifiers, 1999.",
    "[3] D. Q. Nguyen et al., \"PhoBERT: Pre-trained Language Models for Vietnamese,\" Findings EMNLP 2020.",
    "[4] Vietnamese Quality-Assured SMS Dataset, IEEE Access 2026 (doi pending).",
    "[5] F. Pedregosa et al., \"Scikit-learn: Machine Learning in Python,\" JMLR vol.12, 2011.",
  ];

  const rowH = (CH - 0.3) / refs.length;
  refs.forEach((ref, i) => {
    slide.addText(ref, {
      x: M, y: CY + 0.1 + i * rowH, w: CW, h: rowH,
      fontSize: 12, color: T.text, font: "Calibri",
      valign: "middle", shrinkText: true,
    });
  });
})();

// ─── SLIDE 16: THANK YOU ─────────────────────────────────────────────────────
(function slide16_thankyou() {
  const slide = pptx.addSlide();
  slide.background = { color: T.coverBg };  // Navy — đồng bộ Cover

  slide.addText("🛡️", { x: M, y: 0.8, w: CW, h: 0.55, fontSize: 32, align: "center" });
  slide.addText("Cảm ơn Thầy và các bạn\nđã lắng nghe!", {
    x: M, y: 1.35, w: CW, h: 1.5,
    fontSize: 30, bold: true, color: T.textLight, font: "Georgia", align: "center", shrinkText: true,
  });
  slide.addShape(pptx.ShapeType.rect, { x: 2.5, y: 2.95, w: 5, h: 0.04, fill: { color: T.accent } });

  slide.addText("Nhóm 10 — CS114.F31.CN2.TTNT  |  23/09/2026", {
    x: M, y: 3.05, w: CW, h: 0.35, fontSize: 13, color: "93C5FD", font: "Calibri", align: "center",
  });

  const members = [
    "Đặng Chí Thanh  25730067@ms.uit.edu.vn",
    "Bùi Thị Mỷ Cẩm  25730013@ms.uit.edu.vn",
    "Hoàng Cao Sơn  25730061@ms.uit.edu.vn",
  ];
  slide.addText(members.map(m => ({ text: m, options: { breakLine: true } })), {
    x: M, y: 3.5, w: CW, h: 0.9, fontSize: 12, color: T.textLight, font: "Calibri", align: "center",
  });
  slide.addText("UIT — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM", {
    x: M, y: 4.5, w: CW, h: 0.3, fontSize: 10, color: "6B7280", font: "Calibri", align: "center",
  });

  slide.addNotes("SLIDE 16 — THANK YOU\n- Mời Thầy và hội đồng đặt câu hỏi\n- Backup slides có: hyperparameters, confusion matrices, learning curves");
})();

// ─── APPENDIX DIVIDER ────────────────────────────────────────────────────────
(function slideApp_divider() {
  const slide = pptx.addSlide();
  slide.background = { color: T.coverBg };
  slide.addText("Phụ lục — Backup Q&A", {
    x: M, y: 2.0, w: CW, h: 1.0,
    fontSize: 28, bold: true, color: T.accent, font: "Georgia", align: "center",
  });
})();

// ─── BACKUP B1: HYPERPARAMETERS ──────────────────────────────────────────────
(function slideB1_hyperparams() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Backup: Chi tiết Siêu tham số (Hyperparameters)", "Phụ lục");

  const rows = [
    [{ text: "Mô hình", options: { bold: true, color: T.textLight, fill: { color: T.coverBg } } },
     { text: "Siêu tham số tốt nhất", options: { bold: true, color: T.textLight, fill: { color: T.coverBg } } },
     { text: "CV Strategy", options: { bold: true, color: T.textLight, fill: { color: T.coverBg } } }],
    ["XGBoost", "n_est=300, depth=5, lr=0.05, subsample=0.7, colsample=0.8, scale_pos_weight=4.22", "GridSearch 5-fold Stratified"],
    ["SVM Linear", "C=10.0 (CalibratedClassifierCV 5-fold)", "5-fold Calibrated CV"],
    ["Random Forest", "n_est=200, depth=50, min_split=2, min_leaf=2, max_feat=0.2", "GridSearch 5-fold"],
    ["Naive Bayes", "alpha=0.5 (MultinomialNB)", "Cross-validated Alpha search"],
  ];
  slide.addTable(rows, {
    x: M, y: CY + 0.1, w: CW,
    fontSize: 10, font: "Calibri",
    border: { pt: 0.5, color: T.accent },
    rowH: 0.65,
  });
})();

// ─── BACKUP B2: CONFUSION MATRICES ───────────────────────────────────────────
(function slideB2_confusion() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Backup: Confusion Matrices — Cả 4 Mô hình", "Phụ lục");

  const cmPath = path.join(FIG, "confusion_matrices_all.png");
  if (fs.existsSync(cmPath)) {
    slide.addImage({ path: cmPath, x: M, y: CY + 0.1, w: 7.0, h: 3.6 });
  }
  addCard(slide, 7.6, CY + 0.5, 1.8, 2.5,
    "Đọc CM",
    ["TN=Bình thường đúng", "FP=Báo sai", "FN=Bỏ lọt lừa đảo", "TP=Bắt đúng", "", "FN cần → tối thiểu!"]
  );
})();

// ─── BACKUP B3: LEARNING CURVES ──────────────────────────────────────────────
(function slideB3_learning() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Backup: Learning Curves — Không Overfit", "Phụ lục");

  const lcPath = path.join(FIG, "learning_curves_summary.png");
  if (fs.existsSync(lcPath)) {
    slide.addImage({ path: lcPath, x: M, y: CY + 0.1, w: 7.0, h: 3.6 });
  }
  slide.addText("Train Score ≈ Val Score → không overfit. Dataset đủ lớn cho 4 mô hình.", {
    x: 7.6, y: CY + 1.5, w: 1.8, h: 1.2,
    fontSize: 10, color: T.text, font: "Calibri", shrinkText: true,
  });
})();

// ─── EXPORT ──────────────────────────────────────────────────────────────────
const outputFile = path.join(__dirname, "phase09_presentation.pptx");
pptx.writeFile({ fileName: outputFile })
  .then(() => {
    console.log(`✅ Presentation generated: ${outputFile}`);
    console.log("📝 Next steps:");
    console.log("   1. OMML injection (if formulas added):");
    console.log("      python3 ../../.agents/skills/powerpoint-slides/scripts/inject_omml.py phase09_presentation.pptx formulas.json phase09_presentation.pptx");
    console.log("   2. Transitions:");
    console.log("      python3 ../../.agents/skills/powerpoint-slides/scripts/inject_transitions.py phase09_presentation.pptx --preset academic phase09_presentation.pptx");
    console.log("   3. Convert to PDF for visual QA:");
    console.log("      python3 ../../.agents/skills/powerpoint-slides/scripts/soffice.py --headless --convert-to pdf --outdir /tmp phase09_presentation.pptx");
    console.log("   4. Create PR → tag @25730067 for review");
  })
  .catch(console.error);
