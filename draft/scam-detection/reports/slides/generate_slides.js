/**
 * generate_slides.js — CS114 Final Phase 09 PPT
 * Skill: uit:powerpoint-slides (PptxGenJS + Navy-Blue Theme)
 * Theme: Đồng bộ với Streamlit Demo App (Navy→Blue header, White content, Red alert, Amber warning)
 *
 * Branch: feat/phase-09-ppt-template
 * Owner: Bùi Thị Mỷ Cẩm (25730013) — Cẩm completes this template
 * Reviewer: Đặng Chí Thanh (25730067)
 *
 * Nguyên tắc số liệu (Hard Rule 37): mọi chỉ số mô hình đọc TRỰC TIẾP từ
 * ../../models/*_metrics.json (log huấn luyện) — không gõ tay. FN/FP suy ra từ Recall/Precision
 * trên tập test 439 mẫu (355 bình thường + 84 lừa đảo).
 *
 * Chạy:
 *   npm install pptxgenjs --no-save --no-package-lock   (một lần, trong thư mục này)
 *   node generate_slides.js
 *
 * Figures dùng từ ../figures/: label_distribution, scam_category_distribution, roc_curves_comparison,
 *   precision_recall_curves, shap_summary, demo_03_scam_detection_verdict, confusion_matrices_all,
 *   learning_curves_summary  (mọi ảnh được đặt theo ĐÚNG tỉ lệ gốc — không kéo giãn).
 */

const PptxGenJS = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

// ─── THEME: Navy-Blue (Đồng bộ Streamlit Demo App) ──────────────────────────
// App colors: header gradient #0B2545→#1E5FC2, CTA blue #1e40af,
//             alert red #dc2626, warning amber #F59E0B, bg #f1f5f9
const T = {
  coverBg: "0B2545",       // Deep Navy — khớp header app (từ gradient)
  coverBg2: "1E5FC2",      // Blue — điểm cuối gradient header app
  contentBg: "FFFFFF",     // Pure White content slides
  sectionBg: "0B2545",     // Navy divider slides
  accent: "1E5FC2",        // Primary Blue — khớp CTA button app
  accentDark: "1E40AF",    // Deep Blue — khớp màu chữ link app
  accentRed: "DC2626",     // Alert Red — khớp nút cảnh báo app (Gọi 156/113)
  accentAmber: "F59E0B",   // Amber Warning — khớp risk meter app
  text: "1F2937",          // Near-black body text
  textLight: "FFFFFF",     // White text on dark slides
  textMuted: "6B7280",     // Muted gray (chỉ dùng trên nền sáng)
  onDarkSoft: "93C5FD",    // Chữ phụ trên nền Navy — tương phản ≥ 4.5:1 (WCAG AA)
  onDarkMuted: "CBD5E1",   // Chữ chú thích trên nền Navy
  contentSubBg: "F1F5F9",  // Xám nhạt — khớp background tổng thể app
  infoBg: "EFF6FF",        // Xanh nhạt cho thẻ thông tin
  amberBg: "FEF3C7",       // Vàng nhạt cho thẻ lưu ý
  positive: "15803D",      // Green metrics — khớp "Trực tuyến 24/7" badge
  neutral: "6B7280",
};

// ─── TYPOGRAPHY (PptxGenJS dùng `fontFace`/`fontSize`, KHÔNG phải `font`/`size`; Cambria thay Georgia vì Georgia thiếu glyph tiếng Việt) ─────────
const F = {
  cover: { fontSize: 32, bold: true, color: T.textLight, fontFace: "Cambria" },
  coverSub: { fontSize: 14, color: T.textLight, fontFace: "Calibri" },
  sectionTitle: { fontSize: 36, bold: true, color: T.textLight, fontFace: "Cambria" },
  titleBar: { fontSize: 18, bold: true, color: T.text, fontFace: "Cambria" },
  body: { fontSize: 14, color: T.text, fontFace: "Calibri" },
  bodySmall: { fontSize: 12, color: T.text, fontFace: "Calibri" },
  caption: { fontSize: 10, color: T.textMuted, fontFace: "Calibri", italic: true },
  cardTitle: { fontSize: 14, bold: true, color: T.text, fontFace: "Calibri" },
  tblHead: { fontSize: 12, bold: true, color: T.textLight, fontFace: "Calibri" },
  tblCell: { fontSize: 12, color: T.text, fontFace: "Calibri" },
  stat: { fontSize: 40, bold: true, color: T.accent, fontFace: "Cambria" },
};

// ─── LAYOUT CONSTANTS (16:9) ──────────────────────────────────────────────────
const SW = 10, SH = 5.625, M = 0.5;
const CW = SW - 2 * M;   // Content width: 9"
const CY = 1.1;           // Content area start Y (below header)
const BOTTOM = SH - M;    // 5.125" — mọi phần tử phải có y + h ≤ BOTTOM (Hard Rule 21)

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_16x9";
pptx.title = "CS114 Final — Vietnamese Elderly Scam Detection";
pptx.subject = "Phase 09 Defense Presentation";
pptx.author = "Nhóm 10 — Đặng Chí Thanh, Bùi Thị Mỷ Cẩm, Hoàng Cao Sơn";
pptx.company = "UIT — ĐHQG-HCM";

// Đường dẫn (tương đối với script này)
const FIG = path.join(__dirname, "../figures");
const MODELS = path.join(__dirname, "../../models");

// ─── SỐ LIỆU: đọc từ log huấn luyện ──────────────────────────────────────────
const TEST_POS = 84;        // số mẫu lừa đảo trong tập test (y_test: 355 bình thường + 84 lừa đảo)
const TEST_NEG = 355;
function loadMetrics(file) {
  const raw = fs.readFileSync(path.join(MODELS, file), "utf8").replace(/^﻿/, "");
  const d = JSON.parse(raw);
  const t = d.test_metrics;
  for (const k of ["accuracy", "precision", "recall", "f1", "roc_auc"]) {
    if (typeof t[k] !== "number") throw new Error(`${file}: thiếu test_metrics.${k}`);
  }
  const tp = Math.round(t.recall * TEST_POS);
  return { ...t, tp, fn: TEST_POS - tp, fp: Math.round(tp * (1 / t.precision - 1)), raw: d };
}
const MET = {
  xgb: loadMetrics("xgboost_metrics.json"),
  svm: loadMetrics("svm_metrics.json"),
  rf: loadMetrics("random_forest_metrics.json"),
  nb: loadMetrics("naive_bayes_metrics.json"),
};
const pct = (v) => (v * 100).toFixed(2) + "%";

// ─── HELPERS ─────────────────────────────────────────────────────────────────
function pngSize(file) {
  const b = fs.readFileSync(file).subarray(0, 24);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

// Đặt ảnh vào hộp (x,y,boxW,boxH) theo đúng tỉ lệ gốc, căn giữa (Hard Rule 32). Trả về khung thực tế.
function addFigure(slide, file, x, y, boxW, boxH, opts = {}) {
  const p = path.join(FIG, file);
  if (!fs.existsSync(p)) { console.warn(`⚠️  Thiếu figure: ${file}`); return null; }
  const { w: pw, h: ph } = pngSize(p);
  const ratio = pw / ph;
  let w = boxW, h = w / ratio;
  if (h > boxH) { h = boxH; w = h * ratio; }
  const fx = opts.alignLeft ? x : x + (boxW - w) / 2;
  const fy = opts.alignTop ? y : y + (boxH - h) / 2;
  slide.addImage({ path: p, x: fx, y: fy, w, h });
  return { x: fx, y: fy, w, h };
}

// Header bar (mọi slide nội dung)
function addHeader(slide, title, section) {
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: SW, h: 0.55, fill: { color: T.coverBg } });
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0.55, w: SW, h: 0.035, fill: { color: T.accent } });
  slide.addText("UIT — CS114", { x: M, y: 0.08, w: 2.5, h: 0.38, fontSize: 10, color: "BFDBFE", fontFace: "Calibri" });
  if (section) {
    slide.addText(section, { x: 4.11, y: 0.08, w: 5.39, h: 0.38, fontSize: 10, color: "BFDBFE", fontFace: "Calibri", align: "right" });
  }
  slide.addText(title, { x: M, y: 0.65, w: CW, h: 0.45, ...F.titleBar, shrinkText: true });
}

// Thẻ có viền trái nhấn màu. opts: fill, border, titleColor, bodyColor, titleSize, bodySize, bullet, spacing
function addCard(slide, x, y, w, h, title, bodyLines, opts = {}) {
  const border = opts.border || T.accent;
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: opts.fill || T.contentSubBg }, line: { color: border, width: 0.5 } });
  slide.addShape(pptx.ShapeType.rect, { x, y, w: 0.06, h, fill: { color: border } });
  const px = x + 0.15, pw = w - 0.25;
  slide.addText(title, {
    x: px, y: y + 0.08, w: pw, h: 0.35, fontSize: opts.titleSize || F.cardTitle.fontSize, bold: true,
    color: opts.titleColor || T.accentDark, fontFace: "Calibri", shrinkText: true,
  });
  const body = bodyLines.map((l) => ({
    text: l,
    options: { breakLine: true, paraSpaceAfter: opts.spacing ?? 4, ...(opts.bullet ? { bullet: { indent: 14 } } : {}) },
  }));
  slide.addText(body, {
    x: px, y: y + 0.45, w: pw, h: h - 0.55, fontSize: opts.bodySize || F.body.fontSize,
    color: opts.bodyColor || T.text, fontFace: "Calibri", valign: "top", shrinkText: true, margin: [2, 0, 4, 0],
  });
}

// Thẻ số liệu lớn (stat-callout)
function addStat(slide, x, y, w, h, num, label, sub) {
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: T.contentSubBg }, line: { color: T.accent, width: 0.5 } });
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h: 0.06, fill: { color: T.accent } });
  slide.addText(num, { x: x + 0.15, y: y + 0.15, w: w - 0.3, h: 0.75, ...F.stat, align: "center", valign: "middle", shrinkText: true });
  slide.addText(label, { x: x + 0.15, y: y + 0.92, w: w - 0.3, h: 0.35, fontSize: 15, bold: true, color: T.text, fontFace: "Calibri", align: "center", shrinkText: true });
  slide.addText(sub, { x: x + 0.15, y: y + 1.3, w: w - 0.3, h: h - 1.4, fontSize: 12, color: T.textMuted, fontFace: "Calibri", align: "center", valign: "top", shrinkText: true });
}

// Dải nhấn một dòng (kết luận / takeaway)
function addCallout(slide, x, y, w, h, text, opts = {}) {
  const border = opts.border || T.accent;
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: opts.fill || T.infoBg }, line: { color: border, width: 0.5 } });
  slide.addShape(pptx.ShapeType.rect, { x, y, w: 0.06, h, fill: { color: border } });
  slide.addText(text, {
    x: x + 0.2, y, w: w - 0.3, h, fontSize: opts.size || 13, color: T.text, fontFace: "Calibri",
    bold: !!opts.bold, valign: "middle", shrinkText: true, margin: [2, 0, 2, 0],
  });
}

// Slide phân đoạn (Navy) — bố cục thống nhất cho cả 4 divider
function addDivider(title, subtitle, notes) {
  const slide = pptx.addSlide();
  slide.background = { color: T.sectionBg };
  slide.addText(title, { x: M, y: 1.25, w: CW, h: 1.95, ...F.sectionTitle, align: "center", valign: "middle", shrinkText: true });
  slide.addShape(pptx.ShapeType.rect, { x: 2.5, y: 3.4, w: 5, h: 0.04, fill: { color: T.accent } });
  slide.addText(subtitle, { x: M, y: 3.6, w: CW, h: 0.4, fontSize: 14, color: T.onDarkSoft, fontFace: "Calibri", align: "center" });
  if (notes) slide.addNotes(notes);
  return slide;
}

// ─── SLIDE 1: COVER ──────────────────────────────────────────────────────────
(function slide01_cover() {
  const slide = pptx.addSlide();
  slide.background = { color: T.coverBg };
  // Nửa dưới tối hơn một tông — tạo chiều sâu (bắt đầu sau tiêu đề để không chồng lên chữ)
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 2.8, w: SW, h: SH - 2.8, fill: { color: "102E5E" } });

  slide.addText("🛡️", { x: M, y: 0.75, w: CW, h: 0.6, fontSize: 36, align: "center" });
  slide.addText("PHÁT HIỆN TIN NHẮN LỪA ĐẢO\nNHẮM VÀO NGƯỜI CAO TUỔI", {
    x: M, y: 1.42, w: CW, h: 1.28, fontSize: 28, bold: true, color: T.textLight, fontFace: "Cambria",
    align: "center", valign: "middle", shrinkText: true,
  });
  slide.addText("Vietnamese Elderly Scam Detection", {
    x: M, y: 2.95, w: CW, h: 0.35, fontSize: 13, color: "BFDBFE", fontFace: "Calibri", align: "center", italic: true,
  });
  slide.addShape(pptx.ShapeType.rect, { x: 2.5, y: 3.4, w: 5, h: 0.04, fill: { color: T.accent } });
  slide.addText("CS114 — Máy học  |  Nhóm 10  |  ThS. Cáp Phạm Đình Thăng", {
    x: M, y: 3.55, w: CW, h: 0.35, fontSize: 12, color: T.onDarkSoft, fontFace: "Calibri", align: "center",
  });
  slide.addText("Đặng Chí Thanh (25730067)  ·  Bùi Thị Mỷ Cẩm (25730013)  ·  Hoàng Cao Sơn (25730061)", {
    x: M, y: 3.95, w: CW, h: 0.35, fontSize: 12, color: T.textLight, fontFace: "Calibri", align: "center", shrinkText: true,
  });
  slide.addText("23/09/2026  |  UIT — ĐHQG-HCM", {
    x: M, y: 4.4, w: CW, h: 0.3, fontSize: 11, color: T.onDarkMuted, fontFace: "Calibri", align: "center",
  });

  slide.addNotes("SLIDE 1 — COVER\n- Người trình bày đầu tiên: Đặng Chí Thanh (PM)\n- Giới thiệu tên đề tài và các thành viên\n- Nhấn mạnh: đề tài bảo vệ người cao tuổi khỏi lừa đảo tin nhắn tiếng Việt");
})();

// ─── SLIDE 2: BỐI CẢNH & VẤN ĐỀ ─────────────────────────────────────────────
(function slide02_context() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Bối cảnh & Vấn đề", "Giới thiệu");

  const stats = [
    { num: "2.193", label: "Mẫu tin nhắn thực tế", sub: "1.773 bình thường · 420 lừa đảo\n100% có URL nguồn truy vết" },
    { num: "4", label: "Nhóm bẫy tâm lý", sub: "Quyền lực · Gia đình\nQuà tặng · Dịch vụ công" },
    { num: "0%", label: "Văn bản do AI tự sinh", sub: "100% tin nhắn đời thực\nKiểm toán 7 tầng · 0% PII" },
  ];
  stats.forEach((s, i) => addStat(slide, M + i * 3.1, CY + 0.15, 2.8, 2.05, s.num, s.label, s.sub));

  // Câu hỏi mở đầu + định hướng bài toán
  slide.addShape(pptx.ShapeType.rect, { x: M, y: 3.6, w: CW, h: 1.45, fill: { color: T.infoBg }, line: { color: T.accent, width: 0.5 } });
  slide.addShape(pptx.ShapeType.rect, { x: M, y: 3.6, w: 0.06, h: 1.45, fill: { color: T.accent } });
  slide.addText("“Tại sao người cao tuổi dễ bị lừa đảo qua tin nhắn hơn?”", {
    x: M + 0.25, y: 3.68, w: CW - 0.4, h: 0.65, fontSize: 18, bold: true, italic: true, color: T.text, fontFace: "Cambria",
    align: "center", valign: "middle", shrinkText: true,
  });
  slide.addText("Bài toán: phát hiện sớm tin nhắn thao túng tâm lý — ưu tiên không bỏ lọt (Recall), vì bỏ sót nguy hiểm hơn báo nhầm.", {
    x: M + 0.25, y: 4.38, w: CW - 0.4, h: 0.6, fontSize: 13, color: T.textMuted, fontFace: "Calibri", align: "center", valign: "middle", shrinkText: true,
  });

  slide.addNotes("SLIDE 2 — BỐI CẢNH\n- Mở bằng câu hỏi gây suy nghĩ\n- Nêu quy mô dataset: 2.193 mẫu thực tế, zero AI-generated\n- 4 nhóm bẫy tâm lý — đây là đóng góp học thuật chính của nhóm\n- Bài toán ưu tiên Recall vì bỏ lọt tin lừa đảo nguy hiểm hơn báo nhầm\n- Chuyển sang: Mục tiêu nghiên cứu");
})();

// ─── SLIDE 3: MỤC TIÊU ────────────────────────────────────────────────────────
(function slide03_objectives() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Mục tiêu & Đóng góp của Nhóm", "Giới thiệu");

  const goals = [
    { title: "So sánh 4 mô hình ML", body: ["Naive Bayes · Random Forest", "XGBoost · SVM Linear", "Cùng tập test 439 mẫu (stratified 80/20)"] },
    { title: "Vượt chỉ tiêu kỹ thuật", body: ["F1 ≥ 88% · Recall ≥ 92%", "Cả 4 mô hình đều đạt", "Ưu tiên Recall: bỏ lọt nguy hiểm hơn"] },
    { title: "Giải thích AI (XAI)", body: ["SHAP Beeswarm trên XGBoost", "Top-20 từ khóa cảnh báo đồng thuận", "Trả lời: vì sao tin này bị coi là lừa đảo?"] },
    { title: "Demo Streamlit cho người cao tuổi", body: ["Chữ 100–150%, hotline 156/113 một chạm", "Dán tin nhắn → tự động phân tích", "16/16 kiểm thử E2E Playwright"] },
  ];
  goals.forEach((g, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    addCard(slide, M + col * 4.6, CY + 0.15 + row * 1.95, 4.4, 1.8, g.title, g.body, { titleSize: 16, bodySize: 15, bullet: true, spacing: 8 });
  });

  slide.addNotes("SLIDE 3 — MỤC TIÊU\n- Đọc nhanh 4 mục tiêu\n- Nhấn: cả 4 mô hình đều vượt chỉ tiêu đề ra\n- Chuyển sang: Phần Dữ liệu");
})();

// ─── SLIDE 4: SECTION DIVIDER — Dữ liệu ─────────────────────────────────────
addDivider("Dữ liệu &\nPhương pháp", "Thu thập  ·  Tiền xử lý  ·  Feature Engineering");

// ─── SLIDE 5: DATASET ─────────────────────────────────────────────────────────
(function slide05_dataset() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Dataset: 2.193 Mẫu Thực Tế", "Dữ liệu & Phương pháp");

  const bullets = [
    "2.193 mẫu · Stratified Split 80/20",
    "Bình thường (label 0): 1.773 mẫu",
    "Lừa đảo (label 1): 420 mẫu — tỉ lệ 4.2:1",
    "Kiểm toán 7 tầng: 0% PII, 0% văn bản tổng hợp",
    "Thu thập độc lập: Thanh 1.773 · Sơn 215 · Cẩm 205",
    "Train 1.754 · Test 439 (355 bình thường + 84 lừa đảo)",
  ];
  slide.addText(bullets.map((b) => ({ text: b, options: { bullet: { indent: 14 }, breakLine: true, paraSpaceAfter: 7 } })), {
    x: M, y: CY + 0.15, w: 4.75, h: 2.85, fontSize: 15, color: T.text, fontFace: "Calibri", valign: "top", shrinkText: true, margin: [2, 0, 4, 0],
  });

  const fig = addFigure(slide, "label_distribution.png", 5.4, CY + 0.15, 4.1, 2.75);
  if (fig) slide.addText("Phân bố nhãn (train + test)", { x: 5.4, y: fig.y + fig.h + 0.08, w: 4.1, h: 0.25, ...F.caption, align: "center" });

  addCallout(slide, M, 4.3, CW, 0.75,
    "Mất cân bằng 4.2:1 → đánh giá bằng Recall / F1 thay vì Accuracy; XGBoost bù bằng scale_pos_weight = " +
    MET.xgb.raw.scale_pos_weight.toFixed(2), { fill: T.amberBg, border: T.accentAmber, size: 14, bold: true });

  slide.addNotes("SLIDE 5 — DATASET\n- Nhấn mạnh Zero Synthetic Text (100% đời thực)\n- 7 tầng kiểm toán nghiêm ngặt\n- 3 thành viên thu thập độc lập\n- Mất cân bằng lớp 4.2:1 nên dùng Recall/F1, không dùng Accuracy\n- Chuyển sang: phân loại 4 nhóm bẫy tâm lý");
})();

// ─── SLIDE 6: 4 NHÓM BẪY TÂM LÝ ──────────────────────────────────────────────
(function slide06_scam_categories() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "4 Nhóm Bẫy Tâm lý trong Dataset", "Dữ liệu & Phương pháp");

  const fig = addFigure(slide, "scam_category_distribution.png", M, CY + 0.15, 4.4, 2.5);
  if (fig) slide.addText("Số mẫu lừa đảo theo nhóm bẫy tâm lý", { x: M, y: fig.y + fig.h + 0.08, w: 4.4, h: 0.25, ...F.caption, align: "center" });

  const head = (t, align) => ({ text: t, options: { ...F.tblHead, fill: { color: T.coverBg }, align } });
  const rows = [
    [head("Nhóm bẫy tâm lý", "left"), head("Mẫu", "center"), head("Kịch bản tiêu biểu", "left")],
    ["Đe dọa quyền lực", { text: "127", options: { align: "center", bold: true } }, "Giả cảnh sát / tòa án"],
    ["Khẩn cấp gia đình", { text: "88", options: { align: "center", bold: true } }, "Con cháu tai nạn, cần tiền"],
    ["Dụ dỗ quà tặng", { text: "46", options: { align: "center", bold: true } }, "Trúng thưởng, ưu đãi sức khỏe"],
    ["Giả dịch vụ công", { text: "159", options: { align: "center", bold: true } }, "BHXH, điện lực giả mạo"],
  ];
  slide.addTable(rows, {
    x: 5.1, y: CY + 0.15, w: 4.4, colW: [1.6, 0.6, 2.2], rowH: [0.42, 0.52, 0.52, 0.52, 0.52],
    fontSize: F.tblCell.fontSize, fontFace: "Calibri", color: T.text, valign: "middle", border: { pt: 0.5, color: T.accent },
  });

  addCallout(slide, M, 4.0, CW, 1.05,
    "Tổng 420 mẫu lừa đảo. Giả dịch vụ công (159) và Đe dọa quyền lực (127) chiếm 68%; nhóm Quà tặng (46) ít nhất nhưng tinh vi nhất — mỗi nhóm khai thác một điểm yếu tâm lý khác nhau.",
    { size: 14 });

  slide.addNotes("SLIDE 6 — NHÓM BẪY TÂM LÝ\n- 4 pattern lừa đảo NCT được phát hiện trong data\n- Giả dịch vụ công (159) và Đe dọa quyền lực (127) chiếm 68% (286/420)\n- Nhóm Quà tặng (46) ít nhưng rất tinh vi\n- Chuyển sang: pipeline kỹ thuật");
})();

// ─── SLIDE 7: PIPELINE ────────────────────────────────────────────────────────
(function slide07_pipeline() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Pipeline Tiền xử lý & Feature Engineering", "Dữ liệu & Phương pháp");

  const steps = [
    { title: "1. Unicode NFC", body: ["Chuẩn hóa ký tự", "tiếng Việt"] },
    { title: "2. Teencode", body: ["160 từ viết tắt", "+ 22 mẫu leet"] },
    { title: "3. Tách từ (PyVi)", body: ["Ghép âm tiết", "thành từ"] },
    { title: "4. TF-IDF", body: ["5.000 đặc trưng", "n-gram (1, 2)"] },
    { title: "5. Đặc trưng phụ", body: ["15 đặc trưng:", "URL, SĐT, tiền, OTP"] },
  ];
  const cw = 1.66, gap = (CW - 5 * cw) / 4;
  steps.forEach((s, i) => {
    const x = M + i * (cw + gap), y = CY + 0.15;
    addCard(slide, x, y, cw, 1.55, s.title, s.body, { titleSize: 13, bodySize: 13, spacing: 3 });
    if (i < steps.length - 1) {
      slide.addShape(pptx.ShapeType.rightArrow, { x: x + cw + 0.01, y: y + 0.65, w: gap - 0.02, h: 0.25, fill: { color: T.accent } });
    }
  });

  // Kết quả pipeline
  slide.addShape(pptx.ShapeType.rect, { x: M, y: 2.95, w: CW, h: 0.5, fill: { color: T.coverBg } });
  slide.addText("→ Vector đầu vào mô hình: 5.015 chiều (5.000 TF-IDF + 15 đặc trưng phụ) · Naive Bayes chỉ dùng 5.000 TF-IDF", {
    x: M + 0.15, y: 2.95, w: CW - 0.3, h: 0.5, fontSize: 13, bold: true, color: T.textLight, fontFace: "Calibri", valign: "middle", shrinkText: true,
  });

  addCard(slide, M, 3.65, CW, 1.4, "Zero-Leakage Protocol",
    ["1. Chia Train/Test (stratified 80/20) TRƯỚC mọi bước học từ dữ liệu",
     "2. fit() TF-IDF & scaler chỉ trên X_train → transform() cho Train và Test",
     "→ Vectorizer & scaler không bao giờ “nhìn thấy” tập Test"],
    { fill: T.amberBg, border: T.accentAmber, titleSize: 15, bodySize: 13, spacing: 3 });

  slide.addNotes("SLIDE 7 — PIPELINE\n- Giải thích ngắn gọn 5 bước\n- Nhấn mạnh Zero-Leakage: chia tập TRƯỚC, fit vectorizer chỉ trên train\n- Feature vector cuối: 5.015 chiều (5.000 TF-IDF + 15 đặc trưng phụ)\n- Naive Bayes chỉ dùng TF-IDF vì đặc trưng phụ có giá trị âm không hợp với MultinomialNB\n- Chuyển sang: phần Mô hình");
})();

// ─── SLIDE 8: SECTION DIVIDER — Mô hình ─────────────────────────────────────
addDivider("Mô hình &\nKết quả", "Naive Bayes  ·  Random Forest  ·  XGBoost  ·  SVM Linear");

// ─── SLIDE 9: MODEL COMPARISON TABLE ─────────────────────────────────────────
(function slide09_model_comparison() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "So sánh 4 Mô hình Machine Learning", "Mô hình & Kết quả");

  const models = [
    { name: "XGBoost", m: MET.xgb },
    { name: "SVM Linear", m: MET.svm },
    { name: "Random Forest", m: MET.rf },
    { name: "Naive Bayes", m: MET.nb },
  ];
  const cols = ["accuracy", "precision", "recall", "f1", "roc_auc"];
  const best = {};
  cols.forEach((c) => { best[c] = Math.max(...models.map((r) => Number(r.m[c].toFixed(4)))); });

  const head = (t) => ({ text: t, options: { ...F.tblHead, fill: { color: T.coverBg }, align: t === "Mô hình" ? "left" : "center" } });
  const rows = [
    ["Mô hình", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"].map(head),
    ...models.map((r, i) => {
      const fill = i === 0 ? { color: "FEF9EC" } : undefined;
      const cells = [{ text: i === 0 ? "XGBoost (tốt nhất tổng thể)" : r.name, options: { bold: i === 0, align: "left", ...(fill ? { fill } : {}) } }];
      cols.forEach((c) => {
        const isBest = Number(r.m[c].toFixed(4)) === best[c];
        cells.push({ text: pct(r.m[c]), options: { align: "center", bold: isBest, color: isBest ? T.positive : T.text, ...(fill ? { fill } : {}) } });
      });
      return cells;
    }),
  ];
  slide.addTable(rows, {
    x: M, y: CY + 0.1, w: CW, colW: [2.75, 1.25, 1.25, 1.25, 1.25, 1.25], rowH: [0.42, 0.5, 0.5, 0.5, 0.5],
    fontSize: 13, fontFace: "Calibri", color: T.text, valign: "middle", border: { pt: 0.5, color: T.accent },
  });

  const x = MET.xgb;
  addCard(slide, M, 3.65, CW, 1.05, "Kết luận: XGBoost — mô hình tốt nhất tổng thể",
    [`FN = ${x.fn}: chỉ bỏ lọt ${x.fn}/${TEST_POS} tin lừa đảo trong tập test (Recall ${pct(x.recall)}) · FP = ${x.fp}`,
     "Cả 4 mô hình đều vượt chỉ tiêu F1 ≥ 88% và Recall ≥ 92% · Số in đậm xanh = tốt nhất theo cột"],
    { fill: T.amberBg, border: T.accentAmber, titleSize: 15, bodySize: 13, spacing: 3 });

  slide.addText("Nguồn: models/*_metrics.json · tập test 439 mẫu (355 bình thường, 84 lừa đảo) · XGBoost [1], SVM hiệu chỉnh xác suất [2], scikit-learn [5]", {
    x: M, y: 4.78, w: CW, h: 0.28, ...F.caption, shrinkText: true,
  });

  slide.addNotes(`SLIDE 9 — MODEL TABLE\n- XGBoost best overall: F1=${pct(MET.xgb.f1)}, Recall=${pct(MET.xgb.recall)}\n- SVM có ROC-AUC cao nhất (${pct(MET.svm.roc_auc)}) nhưng F1 thấp hơn XGBoost\n- Naive Bayes vẫn đạt F1=${pct(MET.nb.f1)} — baseline tốt, chỉ dùng TF-IDF\n- Nhấn: tất cả đều vượt chỉ tiêu GV yêu cầu\n- Q&A: ROC-AUC Random Forest = ${pct(MET.rf.roc_auc)} theo log huấn luyện Phase 05 (0.99755); ảnh ROC và model_comparison.csv (tính lại ở Phase 07) ghi 0.9977 — chênh do làm tròn/tính lại\n- Q&A: FN của từng mô hình — XGB ${MET.xgb.fn}, RF ${MET.rf.fn}, SVM ${MET.svm.fn}, NB ${MET.nb.fn}`);
})();

// ─── SLIDE 10: ROC & PR CURVES ────────────────────────────────────────────────
(function slide10_curves() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "ROC Curves & Precision-Recall Curves", "Mô hình & Kết quả");

  const rocAuc = [MET.xgb, MET.svm, MET.rf, MET.nb].map((m) => m.roc_auc);
  const lo = (Math.min(...rocAuc) * 100).toFixed(2), hi = (Math.max(...rocAuc) * 100).toFixed(2);

  const a = addFigure(slide, "roc_curves_comparison.png", M, CY + 0.1, 4.3, 3.0);
  if (a) slide.addText("(a) ROC Curves — tất cả AUC ≥ 99%", { x: M, y: a.y + a.h + 0.08, w: 4.3, h: 0.28, ...F.caption, align: "center" });
  const b = addFigure(slide, "precision_recall_curves.png", 5.2, CY + 0.1, 4.3, 3.0);
  if (b) slide.addText("(b) Precision-Recall Curves — 4 mô hình", { x: 5.2, y: b.y + b.h + 0.08, w: 4.3, h: 0.28, ...F.caption, align: "center" });

  addCallout(slide, M, 4.65, CW, 0.45,
    `ROC-AUC của 4 mô hình: ${lo}% – ${hi}% → cả 4 tách lớp rất tốt; khác biệt nằm ở FN/FP và Precision.`, { size: 13, bold: true });

  slide.addNotes("SLIDE 10 — ROC & PR\n- ROC-AUC ≥ 99% cho tất cả: mô hình tách lớp tốt\n- Vì dữ liệu mất cân bằng (4.2:1) nên PR curve phản ánh sát hơn ROC\n- Chuyển sang: SHAP giải thích model");
})();

// ─── SLIDE 11: SHAP XAI ───────────────────────────────────────────────────────
(function slide11_shap() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Giải thích Mô hình — SHAP Analysis (XAI)", "Mô hình & Kết quả");

  const items = [
    { t: "SHAP TreeExplainer trên XGBoost — không phải “hộp đen”", lvl: 0 },
    { t: "Từ khóa cảnh báo đồng thuận (Top-20 của 4 mô hình):", lvl: 0 },
    { t: "mày, số_định_danh → đe dọa quyền lực", lvl: 1 },
    { t: "gấp, viện_phí → thúc ép khẩn cấp", lvl: 1 },
    { t: "money, liên_hệ 198, thuế → giả mạo tổ chức, đòi tiền", lvl: 1 },
    { t: "Cách đọc biểu đồ: SHAP > 0 đẩy dự đoán về Lừa đảo", lvl: 0 },
    { t: "Màu điểm = giá trị đặc trưng (đỏ cao, xanh thấp)", lvl: 0 },
  ];
  slide.addText(items.map((it) => ({ text: it.t, options: { bullet: { indent: 14 }, indentLevel: it.lvl, breakLine: true, paraSpaceAfter: 6 } })), {
    x: M, y: CY + 0.15, w: 4.5, h: 3.45, fontSize: 14, color: T.text, fontFace: "Calibri", valign: "top", shrinkText: true, margin: [2, 0, 4, 0],
  });

  addFigure(slide, "shap_summary.png", 5.2, CY + 0.1, 4.3, 3.9);
  slide.addText("“money” là token chuẩn hóa cho số tiền trong tin nhắn (bước tiền xử lý).", {
    x: M, y: 4.8, w: 4.5, h: 0.28, ...F.caption, shrinkText: true,
  });

  slide.addNotes("SLIDE 11 — SHAP XAI\n- Điểm học thuật quan trọng: giải thích được vì sao mô hình kết luận lừa đảo\n- Top-20 từ khóa đồng thuận lấy từ xếp hạng của cả 4 mô hình (reports/figures/top20_keywords_barplot.png)\n- 'money' và 'number' là token chuẩn hóa từ bước tiền xử lý\n- Cách đọc SHAP beeswarm: trục ngang là mức đẩy về lớp Lừa đảo; màu là giá trị đặc trưng\n- Chuyển sang: Demo ứng dụng");
})();

// ─── SLIDE 12: SECTION DIVIDER — Demo ────────────────────────────────────────
addDivider("Demo Ứng dụng &\nKết luận", "Streamlit Web App  ·  Kết quả  ·  Hướng phát triển");

// ─── SLIDE 13: DEMO UI ────────────────────────────────────────────────────────
(function slide13_demo() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Demo: Streamlit Web Application", "Demo & Kết luận");

  const fig = addFigure(slide, "demo_03_scam_detection_verdict.png", M, CY + 0.15, 5.4, 3.5);
  if (fig) slide.addText("Kết quả phân tích một tin nhắn lừa đảo trên giao diện demo", { x: M, y: fig.y + fig.h + 0.08, w: 5.4, h: 0.25, ...F.caption, align: "center" });

  const features = [
    "4 mô hình trong 1 ứng dụng (mặc định XGBoost)",
    "Chỉnh cỡ chữ 100% · 125% · 150%",
    "Hotline khẩn cấp 156 / 113 gọi 1 chạm",
    "Dán tin nhắn → tự động phân tích",
    "Trích xuất 15 đặc trưng tâm lý theo thời gian thực",
    "Tối ưu điện thoại · 16/16 kiểm thử E2E Playwright",
  ];
  slide.addText(features.map((f) => ({ text: f, options: { bullet: { indent: 14 }, breakLine: true, paraSpaceAfter: 8 } })), {
    x: 6.2, y: CY + 0.15, w: 3.3, h: 3.8, fontSize: 14, color: T.text, fontFace: "Calibri", valign: "top", shrinkText: true, margin: [2, 0, 4, 0],
  });

  slide.addNotes("SLIDE 13 — DEMO\n- Nếu cho phép: live demo trực tiếp streamlit app (streamlit run demo/app.py)\n- Nếu không: dùng screenshot này\n- Nhấn: trợ năng cho người cao tuổi (chỉnh cỡ chữ, hotline 1 chạm)\n- Chuyển sang: Kết luận");
})();

// ─── SLIDE 14: KẾT LUẬN ──────────────────────────────────────────────────────
(function slide14_conclusion() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Kết luận & Hướng Phát triển", "Demo & Kết luận");

  const achieved = [
    `F1 = ${pct(MET.xgb.f1)} (mục tiêu ≥ 88%)`,
    `Recall = ${pct(MET.xgb.recall)} (mục tiêu ≥ 92%)`,
    "4 mô hình được so sánh (tối thiểu 3)",
    "2.193 mẫu thực tế — Zero Synthetic Text",
    "SHAP XAI — giải thích được quyết định của mô hình",
    "Demo Streamlit hoạt động đầy đủ, thân thiện người cao tuổi",
  ];
  const future = [
    "Tích hợp PhoBERT (BERT tiếng Việt) [3]",
    "Mở rộng sang lừa đảo qua giọng nói",
    "API cho ứng dụng ngân hàng / nhà mạng",
    "Mở rộng dataset lên 10.000+ mẫu",
    "Dashboard giám sát thời gian thực",
  ];
  addCard(slide, M, CY + 0.15, 4.4, 3.8, "Kết quả đạt được", achieved,
    { fill: T.infoBg, border: T.accent, titleSize: 18, bodySize: 16, bullet: true, spacing: 10 });
  addCard(slide, 5.1, CY + 0.15, 4.4, 3.8, "Hướng phát triển", future,
    { fill: "FFFBEB", border: T.accentAmber, titleColor: "B45309", titleSize: 18, bodySize: 16, bullet: true, spacing: 10 });

  slide.addNotes("SLIDE 14 — KẾT LUẬN\n- Nhóm đã hoàn thành đầy đủ các mục tiêu đề ra\n- XGBoost là best model\n- Điểm mạnh: dataset thực tế + XAI giải thích + demo trợ năng\n- Hạn chế trung thực: tập test chỉ có 84 mẫu lừa đảo nên mỗi FN thay đổi Recall ~1.2 điểm\n- Mở ra: tích hợp PhoBERT và mở rộng sang voice scam");
})();

// ─── SLIDE 15: REFERENCES ────────────────────────────────────────────────────
(function slide15_references() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Tài liệu tham khảo", "Tham khảo");

  const refs = [
    "[1] T. Chen & C. Guestrin, “XGBoost: A Scalable Tree Boosting System,” KDD 2016.",
    "[2] J. Platt, “Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods,” Advances in Large Margin Classifiers, 1999.",
    "[3] D. Q. Nguyen & A. T. Nguyen, “PhoBERT: Pre-trained Language Models for Vietnamese,” Findings of EMNLP 2020.",
    "[4] Vietnamese Quality-Assured SMS Dataset, IEEE Access 2026 (doi pending) — nguồn dữ liệu tin nhắn bình thường.",
    "[5] F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” JMLR vol. 12, 2011.",
  ];
  const top = CY + 0.15, rowH = (BOTTOM - top - 0.05) / refs.length;
  refs.forEach((ref, i) => {
    slide.addText(ref, {
      x: M, y: top + i * rowH, w: CW, h: rowH - 0.1, fontSize: 14, color: T.text, fontFace: "Calibri",
      valign: "middle", shrinkText: true,
    });
  });

  slide.addNotes("SLIDE 15 — THAM KHẢO\n- [1] XGBoost, [2] hiệu chỉnh xác suất SVM (CalibratedClassifierCV), [3] PhoBERT (hướng phát triển), [4] nguồn dữ liệu bình thường, [5] scikit-learn\n- Q&A: [4] đang chờ DOI — trình bày rõ là nguồn dữ liệu công khai nhóm đã ghi provenance trong dataset");
})();

// ─── SLIDE 16: THANK YOU ─────────────────────────────────────────────────────
(function slide16_thankyou() {
  const slide = pptx.addSlide();
  slide.background = { color: T.coverBg };

  slide.addText("🛡️", { x: M, y: 0.75, w: CW, h: 0.5, fontSize: 32, align: "center" });
  slide.addText("Cảm ơn Thầy và các bạn\nđã lắng nghe!", {
    x: M, y: 1.35, w: CW, h: 1.5, fontSize: 30, bold: true, color: T.textLight, fontFace: "Cambria",
    align: "center", valign: "middle", shrinkText: true,
  });
  slide.addShape(pptx.ShapeType.rect, { x: 2.5, y: 2.95, w: 5, h: 0.04, fill: { color: T.accent } });
  slide.addText("Nhóm 10 — CS114.F31.CN2.TTNT  |  23/09/2026", {
    x: M, y: 3.1, w: CW, h: 0.35, fontSize: 13, color: T.onDarkSoft, fontFace: "Calibri", align: "center",
  });
  const members = [
    "Đặng Chí Thanh  ·  25730067@ms.uit.edu.vn",
    "Bùi Thị Mỷ Cẩm  ·  25730013@ms.uit.edu.vn",
    "Hoàng Cao Sơn  ·  25730061@ms.uit.edu.vn",
  ];
  slide.addText(members.map((m) => ({ text: m, options: { breakLine: true } })), {
    x: M, y: 3.55, w: CW, h: 0.9, fontSize: 12, color: T.textLight, fontFace: "Calibri", align: "center",
  });
  slide.addText("UIT — Trường Đại học Công nghệ Thông tin, ĐHQG-HCM", {
    x: M, y: 4.55, w: CW, h: 0.3, fontSize: 11, color: T.onDarkMuted, fontFace: "Calibri", align: "center",
  });

  slide.addNotes("SLIDE 16 — THANK YOU\n- Mời Thầy và hội đồng đặt câu hỏi\n- Backup slides có: siêu tham số, confusion matrices, learning curves");
})();

// ─── APPENDIX DIVIDER ────────────────────────────────────────────────────────
addDivider("Phụ lục —\nBackup Q&A", "Siêu tham số  ·  Confusion Matrices  ·  Learning Curves");

// ─── BACKUP B1: HYPERPARAMETERS ──────────────────────────────────────────────
(function slideB1_hyperparams() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Backup: Siêu tham số & Chiến lược tinh chỉnh", "Phụ lục");

  const bp = (m) => m.raw.best_params;
  const cv = (m, k) => m.raw[k].toFixed(4);
  const head = (t, align) => ({ text: t, options: { ...F.tblHead, fill: { color: T.coverBg }, align } });
  const rows = [
    [head("Mô hình", "left"), head("Siêu tham số tốt nhất", "left"), head("Tinh chỉnh", "left"), head("CV F1", "center")],
    ["XGBoost",
      `n_estimators=${bp(MET.xgb).n_estimators}, max_depth=${bp(MET.xgb).max_depth}, learning_rate=${bp(MET.xgb).learning_rate}, subsample=${bp(MET.xgb).subsample}, colsample_bytree=${bp(MET.xgb).colsample_bytree}, scale_pos_weight=${MET.xgb.raw.scale_pos_weight.toFixed(2)}`,
      "RandomizedSearchCV\n(n_iter=25, 5-fold)", { text: cv(MET.xgb, "cv_f1_randomsearch"), options: { align: "center" } }],
    ["SVM Linear",
      `C=${bp(MET.svm).estimator__C} (LinearSVC + CalibratedClassifierCV 5-fold)`,
      "GridSearchCV (5-fold)", { text: cv(MET.svm, "cv_f1_gridsearch"), options: { align: "center" } }],
    ["Random Forest",
      `n_estimators=${bp(MET.rf).n_estimators}, max_depth=${bp(MET.rf).max_depth}, min_samples_split=${bp(MET.rf).min_samples_split}, min_samples_leaf=${bp(MET.rf).min_samples_leaf}, max_features=${bp(MET.rf).max_features}`,
      "RandomizedSearchCV\n(n_iter=25, 5-fold)", { text: cv(MET.rf, "cv_f1_randomsearch"), options: { align: "center" } }],
    ["Naive Bayes",
      `alpha=${MET.nb.raw.best_alpha} (MultinomialNB) — chỉ 5.000 đặc trưng TF-IDF`,
      "GridSearchCV (5-fold)", { text: cv(MET.nb, "cv_f1_gridsearch"), options: { align: "center" } }],
  ];
  slide.addTable(rows, {
    x: M, y: CY + 0.15, w: CW, colW: [1.35, 4.15, 2.5, 1.0], rowH: [0.42, 0.85, 0.65, 0.85, 0.65],
    fontSize: 11, fontFace: "Calibri", color: T.text, valign: "middle", border: { pt: 0.5, color: T.accent },
  });
  slide.addText("Nguồn: models/*_metrics.json · CV F1 = điểm F1 trung bình cross-validation trên tập train (1.754 mẫu).", {
    x: M, y: 4.75, w: CW, h: 0.3, ...F.caption, shrinkText: true,
  });

  slide.addNotes("BACKUP B1 — SIÊU THAM SỐ\n- XGBoost và Random Forest: RandomizedSearchCV n_iter=25, 5-fold; SVM và Naive Bayes: GridSearchCV 5-fold\n- Naive Bayes chọn alpha=0.01 và chỉ dùng TF-IDF vì đặc trưng phụ có giá trị âm\n- CV F1 (train) gần với F1 test → mô hình khái quát tốt");
})();

// ─── BACKUP B2: CONFUSION MATRICES ───────────────────────────────────────────
(function slideB2_confusion() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Backup: Confusion Matrices — Cả 4 Mô hình", "Phụ lục");

  addFigure(slide, "confusion_matrices_all.png", M, CY + 0.1, 4.8, 3.9);

  const head = (t, align) => ({ text: t, options: { ...F.tblHead, fill: { color: T.coverBg }, align } });
  const num = (v, hi) => ({ text: String(v), options: { align: "center", bold: true, color: hi ? T.accentRed : T.text } });
  const rows = [
    [head("Mô hình", "left"), head("FN (bỏ lọt)", "center"), head("FP (báo sai)", "center")],
    ["XGBoost", num(MET.xgb.fn), num(MET.xgb.fp)],
    ["SVM Linear", num(MET.svm.fn), num(MET.svm.fp)],
    ["Random Forest", num(MET.rf.fn), num(MET.rf.fp)],
    ["Naive Bayes", num(MET.nb.fn, true), num(MET.nb.fp, true)],
  ];
  slide.addTable(rows, {
    x: 5.5, y: CY + 0.15, w: 4.0, colW: [1.4, 1.2, 1.4], rowH: 0.4,
    fontSize: 12, fontFace: "Calibri", color: T.text, valign: "middle", border: { pt: 0.5, color: T.accent },
  });
  addCard(slide, 5.5, 3.35, 4.0, 1.7, "Cách đọc",
    ["FN = tin lừa đảo bị bỏ lọt — nguy hiểm nhất", "FP = tin bình thường bị báo nhầm", `Tập test: ${TEST_POS} lừa đảo + ${TEST_NEG} bình thường`],
    { titleSize: 14, bodySize: 12, bullet: true, spacing: 3 });

  slide.addNotes("BACKUP B2 — CONFUSION MATRIX\n- FN/FP tính từ Recall/Precision trong log trên tập test 439 mẫu (84 lừa đảo)\n- XGBoost và Random Forest cùng FN nhỏ nhất; Random Forest báo nhầm nhiều hơn (FP cao hơn)\n- Naive Bayes FN và FP cao nhất — vai trò baseline");
})();

// ─── BACKUP B3: LEARNING CURVES ──────────────────────────────────────────────
(function slideB3_learning() {
  const slide = pptx.addSlide();
  slide.background = { color: T.contentBg };
  addHeader(slide, "Backup: Learning Curves — Train vs Validation", "Phụ lục");

  addFigure(slide, "learning_curves_summary.png", M, CY + 0.1, 5.7, 3.9);
  addCard(slide, 6.4, CY + 0.15, 3.1, 3.8, "Nhận định trung thực",
    ["Train F1 ≈ 0.96–1.0, Validation F1 ≈ 0.91–0.96 → còn khoảng cách 3–6 điểm (overfit nhẹ)",
     "Validation F1 của XGBoost, SVM, RF vẫn tăng theo số mẫu → thêm dữ liệu sẽ giúp",
     `CV F1 (~${MET.xgb.raw.cv_f1_randomsearch.toFixed(2)}) sát F1 test (${MET.xgb.f1.toFixed(2)}) → khái quát ổn`],
    { titleSize: 14, bodySize: 12, bullet: true, spacing: 6 });

  slide.addNotes("BACKUP B3 — LEARNING CURVES\n- Không nói 'không overfit': Train F1 gần 1.0 nhưng Validation F1 thấp hơn ~3-6 điểm\n- Điểm tích cực: Validation F1 vẫn đang tăng theo số mẫu (thêm dữ liệu sẽ cải thiện) và F1 test sát CV F1 nên không có dấu hiệu khái quát kém\n- Naive Bayes: Train F1 giảm, Validation tăng dần — hội tụ ~0.91");
})();

// ─── EXPORT ──────────────────────────────────────────────────────────────────
const outputFile = path.join(__dirname, "phase09_presentation.pptx");
pptx.writeFile({ fileName: outputFile })
  .then(() => {
    console.log(`✅ Presentation generated: ${outputFile}`);
    console.log("📝 Next steps (PowerShell, Windows):");
    console.log("   1. Kiểm tra bố cục:   python <skill-root>/scripts/check_overlaps.py phase09_presentation.pptx");
    console.log("   2. Xuất PDF để xem:   python <skill-root>/scripts/soffice.py --headless --convert-to pdf --outdir qa phase09_presentation.pptx");
    console.log("   (Hiệu ứng chuyển slide dạng morph/fracture chưa được kiểm chứng trên PowerPoint — chỉ dùng nếu đã mở thử.)");
  })
  .catch((err) => {
    console.error("❌ Error generating presentation:", err);
    process.exit(1);
  });
