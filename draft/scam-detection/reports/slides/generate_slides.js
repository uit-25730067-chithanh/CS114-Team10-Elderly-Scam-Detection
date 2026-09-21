/**
 * generate_slides.js — CS114 Final Phase 09 PPT (22 slides)
 * Skill: uit:powerpoint-slides (PptxGenJS + Navy-Blue Theme)
 * Theme: Đồng bộ với Streamlit Demo App (Navy→Blue header, White content, Red alert, Amber warning)
 *
 * Branch: feat/phase-09-ppt-template
 * Owner: Bùi Thị Mỷ Cẩm (25730013) — Reviewer: Đặng Chí Thanh (25730067)
 *
 * Nguyên tắc số liệu (Hard Rule 37): mọi chỉ số mô hình đọc TRỰC TIẾP từ
 * ../../models/*_metrics.json và ../ablation_masking_tags.json (sinh bởi
 * src/evaluation/ablation_masking_tags.py) — không gõ tay. FN/FP suy ra từ Recall/Precision
 * trên tập test 439 mẫu (355 bình thường + 84 lừa đảo).
 *
 * Cấu trúc 22 slide: Bìa · Agenda · PHẦN 1 Giới thiệu (2) · PHẦN 2 Dữ liệu & Phương pháp (divider + 3)
 *   · PHẦN 3 Mô hình & Kết quả (divider + 3) · PHẦN 4 Demo (divider + 1) · PHẦN 5 Kết luận (divider + 1)
 *   · Tham khảo · Cảm ơn · Phụ lục (divider + 3 backup).
 *
 * Chạy:
 *   npm install pptxgenjs --no-save --no-package-lock   (một lần, trong thư mục này)
 *   node generate_slides.js
 *
 * Logo: assets/logo_uit_dhqg_trang.png — bản trắng chính thức của UIT (Brand Guideline: logo trắng trên nền tối;
 *   không kéo giãn, không đổi màu). Mọi ảnh biểu đồ được đặt theo ĐÚNG tỉ lệ gốc.
 */

const PptxGenJS = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

// ─── THEME: Navy-Blue (Đồng bộ Streamlit Demo App) ──────────────────────────
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
const BOTTOM = SH - M;    // 5.125" — nội dung phải có y + h ≤ BOTTOM; footer nằm trong lề dưới (5.16–5.58)

// ─── NỘI DUNG CHUẨN THEO CHỈ ĐẠO CỦA ANH THANH (21/09/2026) ─────────────────
const OFFICIAL_TITLE = "Nghiên cứu và Xây dựng Hệ thống Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam";
const HEADER_TEXT = "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN — ĐHQG-HCM";
const FOOTER_TEXT = "CS114: Máy học — Nhóm 10 — Báo cáo Đồ án: Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam";
const THANKS_TEXT = "CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN\nĐÃ LẮNG NGHE BÁO CÁO!";
const SEC = {
  1: "PHẦN 1 · Giới thiệu",
  2: "PHẦN 2 · Dữ liệu & Phương pháp",
  3: "PHẦN 3 · Mô hình & Kết quả",
  4: "PHẦN 4 · Demo ứng dụng",
  5: "PHẦN 5 · Kết luận & Hướng phát triển",
  ref: "Tài liệu tham khảo",
  app: "Phụ lục",
  agenda: "Lộ trình báo cáo",
};

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_16x9";
pptx.title = OFFICIAL_TITLE;
pptx.subject = "CS114 — Phase 09 Defense Presentation";
pptx.author = "Nhóm 10 — Đặng Chí Thanh, Bùi Thị Mỷ Cẩm, Hoàng Cao Sơn";
pptx.company = "UIT — ĐHQG-HCM";

// Đường dẫn (tương đối với script này)
const FIG = path.join(__dirname, "../figures");
const MODELS = path.join(__dirname, "../../models");
const LOGO = path.join(__dirname, "assets/logo_uit_dhqg_trang.png");
const LOGO_RATIO = 8992 / 1334;   // tỉ lệ gốc của file logo — không được kéo giãn

// ─── SỐ LIỆU: đọc từ log huấn luyện ──────────────────────────────────────────
const TEST_POS = 84;        // số mẫu lừa đảo trong tập test (y_test: 355 bình thường + 84 lừa đảo)
const TEST_NEG = 355;
function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^﻿/, ""));
}
function loadMetrics(file) {
  const d = readJson(path.join(MODELS, file));
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

// Kết quả thử nghiệm bỏ thẻ ẩn danh (python src/evaluation/ablation_masking_tags.py)
const ABL = readJson(path.join(__dirname, "../ablation_masking_tags.json"));
if (!ABL.baseline_matches_reported_xgb_f1) throw new Error("ablation_masking_tags.json: baseline không khớp F1 XGBoost đã báo cáo");
// Phân loại từ khóa Top-20 — kiểm chứng bằng dữ liệu, không gán tay
const KW_SCAM = ["mày", "gấp", "viện_phí", "thuế", "số_định_danh"];
const KW_NORMAL = ["money", "number", "time", "liên_hệ 198", "soạn", "viettel"];
KW_SCAM.forEach((k) => { if (!(ABL.keyword_scam_share[k].scam_share >= 0.99)) throw new Error(`từ khóa ${k} không còn 100% lừa đảo`); });
KW_NORMAL.forEach((k) => { if (!(ABL.keyword_scam_share[k].scam_share <= 0.02)) throw new Error(`từ khóa ${k} không còn ≤2% lừa đảo`); });

// ─── SLIDE REGISTRY (để đánh số trang "NN / TỔNG" và số slide trong speaker notes) ─────────────
const registry = [];
function newSlide(kind) {
  const slide = pptx.addSlide();
  registry.push({ slide, kind });
  slide.__n = registry.length;
  slide.background = { color: kind === "content" ? T.contentBg : T.sectionBg };
  return slide;
}
function note(slide, title, lines) {
  slide.addNotes(`SLIDE ${slide.__n} — ${title}\n` + lines.join("\n"));
}

// ─── HELPERS ─────────────────────────────────────────────────────────────────
function pngSize(file) {
  const b = fs.readFileSync(file).subarray(0, 24);
  const isPng = b.length >= 24 && b.readUInt32BE(0) === 0x89504E47;
  if (!isPng) {
    console.warn(`⚠️ File không đúng định dạng PNG hợp lệ: ${file}`);
    return { w: 1920, h: 1080 };
  }
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

// Logo UIT (bản trắng) — đặt giữa phía trên, đúng tỉ lệ gốc
function addLogo(slide, y, w) {
  if (!fs.existsSync(LOGO)) { console.warn("⚠️  Thiếu logo UIT: assets/logo_uit_dhqg_trang.png"); return; }
  slide.addImage({ path: LOGO, x: (SW - w) / 2, y, w, h: w / LOGO_RATIO });
}

// Header bar (mọi slide nội dung): tên trường bên trái, nhãn PHẦN bên phải
function addHeader(slide, title, section) {
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: SW, h: 0.55, fill: { color: T.coverBg } });
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0.55, w: SW, h: 0.035, fill: { color: T.accent } });
  slide.addText(HEADER_TEXT, { x: M, y: 0.08, w: 4.6, h: 0.38, fontSize: 9, bold: true, color: "BFDBFE", fontFace: "Calibri", valign: "middle" });
  if (section) {
    slide.addText(section, { x: 5.3, y: 0.08, w: 4.2, h: 0.38, fontSize: 10, color: "BFDBFE", fontFace: "Calibri", align: "right", valign: "middle" });
  }
  slide.addText(title, { x: M, y: 0.65, w: CW, h: 0.45, ...F.titleBar, shrinkText: true });
}

// Footer + số trang "NN / TỔNG" cho slide nội dung (nằm trong lề dưới, dưới vùng nội dung ≤ 5.125")
function addFooter(slide, n, total) {
  const pad = (v) => String(v).padStart(2, "0");
  slide.addText(FOOTER_TEXT, {
    x: M, y: 5.22, w: 7.7, h: 0.25, fontSize: 7.2, color: T.textMuted, fontFace: "Calibri", valign: "middle", margin: [0, 0, 0, 0], wrap: false,
  });
  slide.addText(`${pad(n)} / ${pad(total)}`, {
    x: 8.3, y: 5.22, w: 1.2, h: 0.25, fontSize: 9.5, bold: true, color: T.accentDark, fontFace: "Calibri", align: "right", valign: "middle", margin: [0, 0, 0, 0],
  });
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

// Dải nhấn (kết luận / takeaway)
function addCallout(slide, x, y, w, h, text, opts = {}) {
  const border = opts.border || T.accent;
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: opts.fill || T.infoBg }, line: { color: border, width: 0.5 } });
  slide.addShape(pptx.ShapeType.rect, { x, y, w: 0.06, h, fill: { color: border } });
  slide.addText(text, {
    x: x + 0.2, y, w: w - 0.3, h, fontSize: opts.size || 13, color: T.text, fontFace: "Calibri",
    bold: !!opts.bold, valign: "middle", shrinkText: true, margin: [2, 0, 2, 0],
  });
}

// Slide phân đoạn (Navy) — bố cục thống nhất theo phong cách Micro-Agenda
function addDivider(part, title, subtitle, bullets = []) {
  const slide = newSlide("divider");

  // University Header Banner
  slide.addText("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN — ĐHQG-HCM  •  BÁO CÁO ĐỒ ÁN CS114", {
    x: M, y: 0.35, w: CW, h: 0.25,
    fontSize: 9.5, fontFace: "Calibri", color: T.onDarkSoft, align: "center", bold: true,
  });

  // Section Pill Badge
  slide.addShape(pptx.ShapeType.roundRect, {
    x: (SW - 2.4) / 2, y: 0.72, w: 2.4, h: 0.36,
    fill: { color: T.accent },
    line: { color: "60A5FA", width: 1 },
    rectRadius: 0.08,
  });
  slide.addText(part, {
    x: (SW - 2.4) / 2, y: 0.72, w: 2.4, h: 0.36,
    fontSize: 13, fontFace: "Cambria", color: T.textLight, align: "center", bold: true,
  });

  // Section Title
  slide.addText(title, {
    x: M, y: 1.20, w: CW, h: 0.60,
    fontSize: 24, fontFace: "Cambria", color: T.textLight, align: "center", bold: true, shrinkText: true,
  });

  // Accent Underline
  slide.addShape(pptx.ShapeType.line, {
    x: (SW - 2.8) / 2, y: 1.95, w: 2.8, h: 0,
    line: { color: T.accentAmber, width: 2.5 },
  });

  // Micro-agenda Container Box
  if (bullets && bullets.length > 0) {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: M + 0.75, y: 2.18, w: CW - 1.5, h: 2.80,
      fill: { color: "102E5E" },
      line: { color: "3B82F6", width: 1 },
      rectRadius: 0.12,
    });

    const textArr = bullets.map((b, idx) => ({
      text: b,
      options: {
        bullet: true,
        breakLine: idx < bullets.length - 1,
        color: "E2E8F0",
        fontSize: 12,
        fontFace: "Calibri",
        lineSpacingMultiple: 1.25,
        paraSpaceAfter: 9,
      },
    }));

    slide.addText(textArr, {
      x: M + 1.05, y: 2.45, w: CW - 2.1, h: 2.35,
      margin: [2, 4, 2, 4],
      shrinkText: true,
    });
  } else if (subtitle) {
    slide.addText(subtitle, {
      x: M, y: 2.45, w: CW, h: 0.45, fontSize: 14, color: T.onDarkSoft, fontFace: "Calibri", align: "center",
    });
  }

  return slide;
}

// Thẻ Agenda: ô số PHẦN bên trái + tiêu đề, mô tả, người trình bày
function addAgendaCard(slide, x, y, w, h, badgeTop, badgeMain, title, desc) {
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: T.contentSubBg }, line: { color: T.accent, width: 0.5 } });
  slide.addShape(pptx.ShapeType.rect, { x, y, w: 0.85, h, fill: { color: T.accent } });
  slide.addText([
    { text: badgeTop, options: { fontSize: 10, bold: true, breakLine: true } },
    { text: badgeMain, options: { fontSize: badgeMain.length > 2 ? 18 : 30, bold: true, fontFace: "Cambria" } },
  ], { x, y, w: 0.85, h, color: T.textLight, fontFace: "Calibri", align: "center", valign: "middle", margin: [0, 0, 0, 0] });
  const px = x + 1.0, pw = w - 1.1;
  slide.addText(title, { x: px, y: y + 0.1, w: pw, h: 0.4, fontSize: 16, bold: true, color: T.accentDark, fontFace: "Calibri", valign: "middle", shrinkText: true });
  slide.addText(desc, { x: px, y: y + 0.5, w: pw, h: 0.36, fontSize: 12.5, color: T.text, fontFace: "Calibri", valign: "middle", shrinkText: true });
}

// ─── SLIDE 1: BÌA (logo UIT + tên đề tài chuẩn) ──────────────────────────────
(function slide01_cover() {
  const slide = newSlide("cover");

  // Logo UIT tinh chỉnh kích thước thanh lịch (w=3.0", h≈0.445")
  addLogo(slide, 0.40, 3.0);

  // Tên đề tài chính thức đầy đủ — ngắt dòng ngữ nghĩa chuẩn xác, không bẻ từ ghép
  slide.addText("Nghiên cứu và Xây dựng Hệ thống\nPhát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo\nnhắm vào Người cao tuổi tại Việt Nam", {
    x: M, y: 1.15, w: CW, h: 1.30, fontSize: 21, bold: true, color: T.textLight, fontFace: "Cambria",
    align: "center", valign: "middle", shrinkText: true,
  });

  // Phụ đề tiếng Anh tương ứng
  slide.addText("Vietnamese Elderly Scam Message & Psychological Manipulation Detection", {
    x: M, y: 2.55, w: CW, h: 0.35, fontSize: 12.5, color: "93C5FD", fontFace: "Calibri", align: "center", italic: true,
  });

  // Đường kẻ nhấn trung tâm màu vàng Amber
  slide.addShape(pptx.ShapeType.line, {
    x: (SW - 2.8) / 2, y: 3.05, w: 2.8, h: 0,
    line: { color: T.accentAmber, width: 2.0 },
  });

  // Thông tin học phần & GVHD
  slide.addText("Môn học: CS114 — Máy học  •  GVHD: ThS. Cáp Phạm Đình Thăng", {
    x: M, y: 3.22, w: CW, h: 0.30, fontSize: 12.5, color: "E2E8F0", fontFace: "Calibri", align: "center",
  });

  // Nhãn Nhóm sinh viên
  slide.addText("NHÓM SINH VIÊN THỰC HIỆN: NHÓM 10", {
    x: M, y: 3.60, w: CW, h: 0.22, fontSize: 11, bold: true, color: T.accentAmber, fontFace: "Calibri", align: "center",
  });

  // Danh sách thành viên nhóm
  slide.addText("Đặng Chí Thanh (25730067)   •   Bùi Thị Mỷ Cẩm (25730013)   •   Hoàng Cao Sơn (25730061)", {
    x: M, y: 3.88, w: CW, h: 0.30, fontSize: 12.5, bold: true, color: T.textLight, fontFace: "Calibri", align: "center", shrinkText: true,
  });

  // Thời gian & Trường
  slide.addText("KHOA KHOA HỌC MÁY TÍNH  •  TP. HỒ CHÍ MINH, THÁNG 09/2026", {
    x: M, y: 4.40, w: CW, h: 0.30, fontSize: 10.5, color: "94A3B8", fontFace: "Calibri", align: "center",
  });

  note(slide, "BÌA", [
    "- Người trình bày Khối 1 (slide 1–8, ~4 phút 30 giây): Đặng Chí Thanh",
    "- Giới thiệu tên đề tài chuẩn và các thành viên; nhấn mạnh: bảo vệ người cao tuổi khỏi lừa đảo tin nhắn tiếng Việt",
    "- Trước khi chiếu: PowerPoint → chọn tất cả slide → Transitions → Fade (0.3s) → Apply To All. Không dùng script chèn XML (tránh lỗi file)",
    "- Phân bổ 15 phút: Thanh slide 1–8 (4:30) · Cẩm slide 9–12 (5:00) · Sơn slide 13–18 (4:30) · dư ~1 phút. Slide phân đoạn (5, 9, 13, 15, 19) không nói",
  ]);
})();

// ─── SLIDE 2: AGENDA ─────────────────────────────────────────────────────────
(function slide02_agenda() {
  const slide = newSlide("content");
  addHeader(slide, "Lộ trình báo cáo", SEC.agenda);

  const items = [
    ["PHẦN", "1", "Giới thiệu", "Bối cảnh, vấn đề và mục tiêu của nhóm"],
    ["PHẦN", "2", "Dữ liệu & Phương pháp", "2.193 mẫu, 4 nhóm bẫy tâm lý, pipeline tiền xử lý"],
    ["PHẦN", "3", "Mô hình & Kết quả", "So sánh 4 mô hình, ROC/PR, giải thích SHAP"],
    ["PHẦN", "4", "Demo ứng dụng", "Web Streamlit thân thiện với người cao tuổi"],
    ["PHẦN", "5", "Kết luận & Hướng phát triển", "Kết quả, hạn chế đã biết, PhoBERT và voice scam"],
    ["PHỤ LỤC", "Q&A", "Backup trả lời phản biện", "Siêu tham số, Confusion Matrix, Learning Curves"],
  ];
  items.forEach((it, i) => {
    const col = Math.floor(i / 3), row = i % 3;
    addAgendaCard(slide, M + col * 4.6, CY + 0.15 + row * 1.3, 4.4, 1.15, ...it);
  });

  note(slide, "AGENDA", [
    "- Nói không quá 20 giây: đọc nhanh 5 phần và ai trình bày phần nào",
    "- Chuyển sang: PHẦN 1 — Bối cảnh & Vấn đề",
  ]);
})();

// ─── SLIDE 3: BỐI CẢNH & VẤN ĐỀ ─────────────────────────────────────────────
(function slide03_context() {
  const slide = newSlide("content");
  addHeader(slide, "Bối cảnh & Vấn đề", SEC[1]);

  const stats = [
    { num: "2.193", label: "Mẫu tin nhắn thực tế", sub: "1.773 bình thường · 420 lừa đảo\n100% có URL nguồn truy vết" },
    { num: "4", label: "Nhóm bẫy tâm lý", sub: "Quyền lực · Gia đình\nQuà tặng · Dịch vụ công" },
    { num: "0%", label: "Văn bản do AI tự sinh", sub: "100% tin nhắn đời thực\nKiểm toán 7 tầng · 0% PII" },
  ];
  stats.forEach((s, i) => addStat(slide, M + i * 3.1, CY + 0.15, 2.8, 2.05, s.num, s.label, s.sub));

  slide.addShape(pptx.ShapeType.rect, { x: M, y: 3.6, w: CW, h: 1.45, fill: { color: T.infoBg }, line: { color: T.accent, width: 0.5 } });
  slide.addShape(pptx.ShapeType.rect, { x: M, y: 3.6, w: 0.06, h: 1.45, fill: { color: T.accent } });
  slide.addText("“Tại sao người cao tuổi dễ bị lừa đảo qua tin nhắn hơn?”", {
    x: M + 0.25, y: 3.68, w: CW - 0.4, h: 0.65, fontSize: 18, bold: true, italic: true, color: T.text, fontFace: "Cambria",
    align: "center", valign: "middle", shrinkText: true,
  });
  slide.addText("Bài toán: phát hiện sớm tin nhắn thao túng tâm lý — ưu tiên không bỏ lọt (Recall), vì bỏ sót nguy hiểm hơn báo nhầm.", {
    x: M + 0.25, y: 4.38, w: CW - 0.4, h: 0.6, fontSize: 13, color: T.textMuted, fontFace: "Calibri", align: "center", valign: "middle", shrinkText: true,
  });

  note(slide, "BỐI CẢNH", [
    "- Mở bằng câu hỏi gây suy nghĩ",
    "- Quy mô dataset: 2.193 mẫu thực tế; bộ dữ liệu chính công bố là tin nhắn thật, không do AI sinh",
    "- 4 nhóm bẫy tâm lý — đóng góp học thuật chính của nhóm",
    "- Bài toán ưu tiên Recall vì bỏ lọt tin lừa đảo nguy hiểm hơn báo nhầm",
    "- Chuyển sang: mục tiêu nghiên cứu",
  ]);
})();

// ─── SLIDE 4: MỤC TIÊU ────────────────────────────────────────────────────────
(function slide04_objectives() {
  const slide = newSlide("content");
  addHeader(slide, "Mục tiêu & Đóng góp của Nhóm", SEC[1]);

  const goals = [
    { title: "So sánh 4 mô hình ML", body: ["Naive Bayes · Random Forest", "XGBoost · SVM Linear", "Cùng tập test 439 mẫu (stratified 80/20)"] },
    { title: "Vượt chỉ tiêu kỹ thuật", body: ["F1 ≥ 88% · Recall ≥ 92%", "Cả 4 mô hình đều đạt", "Ưu tiên Recall: bỏ lọt nguy hiểm hơn"] },
    { title: "Giải thích AI (XAI)", body: ["SHAP Beeswarm trên XGBoost", "Top-20 từ khóa quan trọng đồng thuận", "Trả lời: vì sao tin này bị coi là lừa đảo?"] },
    { title: "Demo Streamlit cho người cao tuổi", body: ["Chữ 100–150%, hotline 156/113 một chạm", "Dán tin nhắn → tự động phân tích", "16/16 kiểm thử E2E Playwright"] },
  ];
  goals.forEach((g, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    addCard(slide, M + col * 4.6, CY + 0.15 + row * 1.95, 4.4, 1.8, g.title, g.body, { titleSize: 16, bodySize: 15, bullet: true, spacing: 8 });
  });

  note(slide, "MỤC TIÊU", [
    "- Đọc nhanh 4 mục tiêu",
    "- Nhấn: cả 4 mô hình đều vượt chỉ tiêu đề ra",
    "- Chuyển sang: PHẦN 2 — Dữ liệu & Phương pháp",
  ]);
})();

// ─── SLIDE 5: DIVIDER PHẦN 2 ─────────────────────────────────────────────────
addDivider("PHẦN 2", "Dữ liệu & Phương pháp", "Thu thập  ·  Tiền xử lý  ·  Feature Engineering", [
  "Đặc điểm tập dữ liệu: 2.193 mẫu thực tế có nguồn gốc kiểm chứng (Zero Synthetic Text)",
  "Phân loại 4 nhóm bẫy tâm lý phổ biến nhắm vào người cao tuổi tại Việt Nam",
  "Pipeline xử lý ngôn ngữ tự nhiên: Tiền xử lý tiếng Việt, TF-IDF 5.000 từ và 15 đặc trưng miền tâm lý",
  "Quy chuẩn Zero-Leakage: Phân lập tuyệt đối dữ liệu Train/Test trước mọi bước huấn luyện",
]);

// ─── SLIDE 6: DATASET ─────────────────────────────────────────────────────────
(function slide06_dataset() {
  const slide = newSlide("content");
  addHeader(slide, "Dataset: 2.193 Mẫu Thực Tế", SEC[2]);

  const bullets = [
    "2.193 mẫu · Stratified Split 80/20 · nguồn [1], [2]",
    "Bình thường (label 0): 1.773 mẫu",
    "Lừa đảo (label 1): 420 mẫu — tỉ lệ 4.2:1",
    "Kiểm toán 7 tầng: 0% PII, 0% văn bản tổng hợp",
    "Tuyển chọn: Thanh 1.773 · Sơn 215 · Cẩm 205",
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

  note(slide, "DATASET", [
    "- Nhấn mạnh Zero Synthetic Text (100% tin nhắn đời thực)",
    "- 7 tầng kiểm toán; mỗi mẫu có source_url truy vết (bộ dữ liệu SMS công khai trên GitHub + báo chí)",
    "- Cách nói đúng về thu thập: 3 thành viên TUYỂN CHỌN và gán nhãn từ nguồn công khai (Thanh 1.773 bình thường; Sơn 215 và Cẩm 205 lừa đảo), không phải tự soạn tin nhắn",
    "- Mất cân bằng lớp 4.2:1 nên dùng Recall/F1, không dùng Accuracy",
    "- Chuyển sang: 4 nhóm bẫy tâm lý",
  ]);
})();

// ─── SLIDE 7: 4 NHÓM BẪY TÂM LÝ ──────────────────────────────────────────────
(function slide07_scam_categories() {
  const slide = newSlide("content");
  addHeader(slide, "4 Nhóm Bẫy Tâm lý trong Dataset", SEC[2]);

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

  note(slide, "NHÓM BẪY TÂM LÝ", [
    "- 4 pattern lừa đảo nhắm vào người cao tuổi được phát hiện trong dữ liệu",
    "- Giả dịch vụ công (159) và Đe dọa quyền lực (127) chiếm 68% (286/420)",
    "- Nhóm Quà tặng (46) ít nhưng rất tinh vi",
    "- Chuyển sang: pipeline kỹ thuật",
  ]);
})();

// ─── SLIDE 8: PIPELINE ────────────────────────────────────────────────────────
(function slide08_pipeline() {
  const slide = newSlide("content");
  addHeader(slide, "Pipeline Tiền xử lý & Feature Engineering", SEC[2]);

  const steps = [
    { title: "1. Unicode NFC", body: ["NFC [3]", "Dấu thanh [5]"] },
    { title: "2. Teencode", body: ["160 từ viết tắt", "+ 22 mẫu leet"] },
    { title: "3. Tách từ (PyVi)", body: ["Ghép âm tiết", "thành từ [4]"] },
    { title: "4. TF-IDF", body: ["5.000 đặc trưng", "n-gram (1, 2) [6]"] },
    { title: "5. Đặc trưng phụ", body: ["15 đặc trưng:", "URL, SĐT, OTP…"] },
  ];
  const cw = 1.66, gap = (CW - 5 * cw) / 4;
  steps.forEach((s, i) => {
    const x = M + i * (cw + gap), y = CY + 0.15;
    addCard(slide, x, y, cw, 1.55, s.title, s.body, { titleSize: 13, bodySize: 13, spacing: 3 });
    if (i < steps.length - 1) {
      slide.addShape(pptx.ShapeType.rightArrow, { x: x + cw + 0.01, y: y + 0.65, w: gap - 0.02, h: 0.25, fill: { color: T.accent } });
    }
  });

  slide.addShape(pptx.ShapeType.rect, { x: M, y: 2.90, w: CW, h: 0.58, fill: { color: T.coverBg } });
  slide.addText([
    { text: "Không gian đặc trưng vector đầu vào:  ", options: { bold: true, fontSize: 11, color: "93C5FD" } },
    { text: "x = [ TF-IDF(w₁, d), ..., TF-IDF(w₅₀₀₀, d) | f_meta₁, ..., f_meta₁₅ ]ᵀ ∈ ℝ⁵⁰¹⁵\n", options: { bold: true, fontSize: 10, fontFace: "Cambria", color: "FFFFFF" } },
    { text: "• 5.000 đặc trưng từ vựng n-gram + 15 đặc trưng miền tâm lý (URL, OTP, SĐT...)  •  Naive Bayes chỉ dùng 5.000 TF-IDF", options: { fontSize: 9.5, color: "CBD5E1" } }
  ], {
    x: M + 0.15, y: 2.90, w: CW - 0.3, h: 0.58, fontFace: "Calibri", valign: "middle", shrinkText: true,
  });

  addCard(slide, M, 3.65, CW, 1.4, "Zero-Leakage Protocol",
    ["1. Chia Train/Test (stratified 80/20) TRƯỚC mọi bước học từ dữ liệu",
     "2. fit() TF-IDF & scaler chỉ trên X_train → transform() cho Train và Test",
     "→ Vectorizer & scaler không bao giờ “nhìn thấy” tập Test"],
    { fill: T.amberBg, border: T.accentAmber, titleSize: 15, bodySize: 13, spacing: 3 });

  note(slide, "PIPELINE", [
    "- Giải thích ngắn gọn 5 bước",
    "- Nhấn mạnh Zero-Leakage: chia tập TRƯỚC, fit vectorizer chỉ trên train",
    "- Vector cuối: 5.015 chiều (5.000 TF-IDF + 15 đặc trưng phụ)",
    "- Naive Bayes chỉ dùng TF-IDF vì đặc trưng phụ có giá trị âm không hợp với MultinomialNB",
    "- Teencode: từ điển do nhóm tự biên soạn (160 mục), cố ý loại các từ đơn mơ hồ để tránh biến đổi sai nghĩa; đặc trưng has_leet_speak để mô hình tự học phần còn lại",
    "- Chuyển sang: PHẦN 3 — Mô hình & Kết quả (Cẩm trình bày)",
  ]);
})();

// ─── SLIDE 9: DIVIDER PHẦN 3 ─────────────────────────────────────────────────
addDivider("PHẦN 3", "Mô hình & Kết quả", "Naive Bayes  ·  Random Forest  ·  XGBoost  ·  SVM Linear", [
  "Đánh giá và so sánh định lượng 4 mô hình: XGBoost, Random Forest, SVM Linear và Naive Bayes",
  "Phân tích hiệu năng phân lớp: Đường cong ROC Curves & Precision-Recall Curves (AUC ≥ 99%)",
  "Giải thích quyết định mô hình XAI bằng SHAP TreeExplainer: Top-20 đặc trưng phân định lừa đảo",
  "Thử nghiệm loại bỏ thẻ ẩn danh (Ablation Study): Chứng minh tính độc lập, không học vẹt nguồn",
]);

// ─── SLIDE 10: MODEL COMPARISON TABLE ────────────────────────────────────────
(function slide10_model_comparison() {
  const slide = newSlide("content");
  addHeader(slide, "So sánh 4 Mô hình Machine Learning", SEC[3]);

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

  slide.addText("Nguồn: models/*_metrics.json · tập test 439 mẫu (355 bình thường, 84 lừa đảo) · XGBoost [7], Random Forest [8], SVM [9] hiệu chỉnh xác suất [10], scikit-learn [11]", {
    x: M, y: 4.78, w: CW, h: 0.28, ...F.caption, shrinkText: true,
  });

  note(slide, "BẢNG SO SÁNH MÔ HÌNH", [
    "- Người trình bày Khối 2 (slide 9–12, ~5 phút): Bùi Thị Mỷ Cẩm",
    `- XGBoost best overall: F1=${pct(MET.xgb.f1)}, Recall=${pct(MET.xgb.recall)}`,
    `- SVM có ROC-AUC cao nhất (${pct(MET.svm.roc_auc)}) nhưng F1 thấp hơn XGBoost`,
    `- Naive Bayes vẫn đạt F1=${pct(MET.nb.f1)} — baseline tốt, chỉ dùng TF-IDF`,
    "- Nhấn: tất cả đều vượt chỉ tiêu GV yêu cầu",
    `- Q&A: ROC-AUC Random Forest = ${pct(MET.rf.roc_auc)} — anh Thanh đánh giá lại random_forest.pkl trên tập test (0.99765), khớp với ảnh ROC ở slide 11`,
    `- Q&A: FN của từng mô hình — XGB ${MET.xgb.fn}, RF ${MET.rf.fn}, SVM ${MET.svm.fn}, NB ${MET.nb.fn}`,
    "- Q&A: dùng scale_pos_weight thay vì SMOTE để giữ nguyên tắc Zero Synthetic Text (không sinh mẫu giả)",
  ]);
})();

// ─── SLIDE 11: ROC & PR CURVES ────────────────────────────────────────────────
(function slide11_curves() {
  const slide = newSlide("content");
  addHeader(slide, "ROC Curves & Precision-Recall Curves", SEC[3]);

  const rocAuc = [MET.xgb, MET.svm, MET.rf, MET.nb].map((m) => m.roc_auc);
  const lo = (Math.min(...rocAuc) * 100).toFixed(2), hi = (Math.max(...rocAuc) * 100).toFixed(2);

  const a = addFigure(slide, "roc_curves_comparison.png", M, CY + 0.1, 4.3, 3.0);
  if (a) slide.addText("(a) ROC Curves — tất cả AUC ≥ 99%", { x: M, y: a.y + a.h + 0.08, w: 4.3, h: 0.28, ...F.caption, align: "center" });
  const b = addFigure(slide, "precision_recall_curves.png", 5.2, CY + 0.1, 4.3, 3.0);
  if (b) slide.addText("(b) Precision-Recall Curves — 4 mô hình", { x: 5.2, y: b.y + b.h + 0.08, w: 4.3, h: 0.28, ...F.caption, align: "center" });

  addCallout(slide, M, 4.65, CW, 0.45,
    `ROC-AUC của 4 mô hình: ${lo}% – ${hi}% → cả 4 tách lớp rất tốt; khác biệt nằm ở FN/FP và Precision.`, { size: 13, bold: true });

  note(slide, "ROC & PR", [
    "- ROC-AUC ≥ 99% cho tất cả: mô hình tách lớp tốt",
    "- Vì dữ liệu mất cân bằng (4.2:1) nên PR curve phản ánh sát hơn ROC",
    "- Chuyển sang: SHAP giải thích mô hình",
  ]);
})();

// ─── SLIDE 12: SHAP XAI (đã sửa theo dữ liệu thật) ───────────────────────────
(function slide12_shap() {
  const slide = newSlide("content");
  addHeader(slide, "Giải thích Mô hình — SHAP Analysis (XAI)", SEC[3]);

  const items = [
    { t: "SHAP TreeExplainer trên XGBoost [12], [13] — không phải “hộp đen”", lvl: 0 },
    { t: "Top-20 từ khóa quan trọng (đồng thuận 4 mô hình):", lvl: 0 },
    { t: `Thiên về lừa đảo: ${KW_SCAM.join(", ")} (100% tin chứa từ này là lừa đảo)`, lvl: 1 },
    // NBSP giữ "liên_hệ 198" trên cùng một dòng (khóa tra dữ liệu ở trên vẫn dùng dấu cách thường)
    { t: `Thiên về bình thường: ${KW_NORMAL.map((k) => k.replace(" ", " ")).join(", ")} (≤ 2% là lừa đảo)`, lvl: 1 },
    { t: "Lưu ý: money, number, time, đường_dẫn… là thẻ ẩn danh có sẵn trong bộ dữ liệu gốc", lvl: 0 },
    { t: `Bỏ ${ABL.features_removed} đặc trưng chứa thẻ này: F1 XGBoost ${pct(ABL.baseline.xgboost.f1)} → ${pct(ABL.without_tags.xgboost.f1)}, Recall giữ ${pct(ABL.without_tags.xgboost.recall)}`, lvl: 0 },
  ];
  slide.addText(items.map((it) => ({ text: it.t, options: { bullet: { indent: 14 }, indentLevel: it.lvl, breakLine: true, paraSpaceAfter: 5 } })), {
    x: M, y: CY + 0.15, w: 4.45, h: 3.8, fontSize: 13, color: T.text, fontFace: "Calibri", valign: "top", shrinkText: true, margin: [2, 0, 4, 0],
  });

  addFigure(slide, "shap_summary.png", 5.2, CY + 0.1, 4.3, 3.45);
  slide.addText("(c) Phân bố tác động SHAP (TreeExplainer) trên mô hình XGBoost", {
    x: 5.2, y: 4.80, w: 4.3, h: 0.22, ...F.caption, align: "center",
  });

  note(slide, "SHAP XAI", [
    "- Điểm học thuật quan trọng: giải thích được vì sao mô hình kết luận lừa đảo",
    "- Cách đọc SHAP beeswarm: trục ngang là mức đẩy về lớp Lừa đảo (bên phải) hay Bình thường (bên trái); màu là giá trị đặc trưng (đỏ cao, xanh thấp)",
    "- Top-20 xếp theo MỨC QUAN TRỌNG, không phải theo hướng: một nửa số từ thiên về tin BÌNH THƯỜNG (money, number, time, liên_hệ 198, soạn, viettel — tỉ lệ lừa đảo ≤ 2%)",
    "- Q&A 'money là gì?': là thẻ ẩn danh [MONEY] có sẵn trong bộ dữ liệu gốc (che số tiền), KHÔNG phải kết quả regex của nhóm; xuất hiện chủ yếu ở tin bình thường (1.221/1.236 dòng thô)",
    "- Q&A 'mô hình có học vẹt nguồn dữ liệu không?': hai nguồn được ẩn danh bằng thẻ khác nhau (bình thường: [MONEY]/[NUMBER]/[TIME]; lừa đảo: [ĐƯỜNG_DẪN]/[THƯƠNG_HIỆU]/[SỐ_TIỀN]). Kiểm tra: bỏ toàn bộ " + ABL.features_removed + " đặc trưng chứa thẻ rồi huấn luyện lại đúng quy trình notebook — " +
      `XGBoost F1 ${pct(ABL.baseline.xgboost.f1)} → ${pct(ABL.without_tags.xgboost.f1)}, Naive Bayes F1 ${pct(ABL.baseline.naive_bayes.f1)} → ${pct(ABL.without_tags.naive_bayes.f1)} (kết quả: reports/ablation_masking_tags.json)`,
    "- Chuyển sang: PHẦN 4 — Demo (Sơn trình bày)",
  ]);
})();

// ─── SLIDE 13: DIVIDER PHẦN 4 ────────────────────────────────────────────────
addDivider("PHẦN 4", "Demo Ứng dụng", "Streamlit Web App  ·  Trợ năng cho người cao tuổi", [
  "Kiến trúc ứng dụng Streamlit hỗ trợ suy luận thời gian thực với mô hình tối ưu XGBoost",
  "Thiết kế giao diện trợ năng chuyên biệt cho người cao tuổi: Phóng to chữ 150%, tương phản cao WCAG AA",
  "Tích hợp hotline khẩn cấp 156 / 113 gọi một chạm và kiểm thử toàn diện 16/16 kịch bản Playwright",
]);

// ─── SLIDE 14: DEMO UI ────────────────────────────────────────────────────────
(function slide14_demo() {
  const slide = newSlide("content");
  addHeader(slide, "Demo: Streamlit Web Application", SEC[4]);

  const frameW = 5.4, frameH = 3.55;
  const frameX = M, frameY = CY + 0.12;
  // Khung viền công nghệ giả lập trình duyệt (Tech Window Container)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: frameX, y: frameY, w: frameW, h: frameH,
    fill: { color: "0F172A" },
    line: { color: T.accent, width: 1.5 },
    rectRadius: 0.1,
  });
  // Thanh tiêu đề cửa sổ trình duyệt (Browser Header Bar)
  slide.addText("  ● ● ●   https://elderly-scam-guard.uit.edu.vn  •  Streamlit Live Demo", {
    x: frameX, y: frameY, w: frameW, h: 0.28,
    fill: { color: "1E293B" },
    fontSize: 8.5, color: "94A3B8", fontFace: "Calibri", valign: "middle",
  });

  addFigure(slide, "demo_03_scam_detection_verdict.png", frameX + 0.06, frameY + 0.32, frameW - 0.12, frameH - 0.38);
  slide.addText("Giao diện phân tích tin nhắn thời gian thực với trợ năng người cao tuổi", {
    x: frameX, y: frameY + frameH + 0.06, w: frameW, h: 0.22, ...F.caption, align: "center",
  });

  const features = [
    "4 mô hình trong 1 ứng dụng (mặc định XGBoost)",
    "Chỉnh cỡ chữ 100% · 125% · 150%",
    "Tương phản chữ 14.6:1, vượt mức WCAG 2.1 AA (4.5:1) [14]",
    "Hotline khẩn cấp 156 / 113 gọi 1 chạm",
    "Dán tin nhắn → tự động phân tích",
    "Trích xuất 15 đặc trưng tâm lý theo thời gian thực",
    "Tối ưu điện thoại · 16/16 kiểm thử E2E Playwright",
  ];
  slide.addText(features.map((f) => ({ text: f, options: { bullet: { indent: 14 }, breakLine: true, paraSpaceAfter: 5 } })), {
    x: 6.2, y: CY + 0.15, w: 3.3, h: 3.8, fontSize: 13.5, color: T.text, fontFace: "Calibri", valign: "top", shrinkText: true, margin: [2, 0, 4, 0],
  });

  note(slide, "DEMO", [
    "- Người trình bày Khối 3 (slide 13–18, ~4 phút 30 giây): Hoàng Cao Sơn — 60 giây live demo hoặc dùng screenshot",
    "- Nếu cho phép: live demo trực tiếp (streamlit run demo/app.py)",
    "- Nhấn: trợ năng cho người cao tuổi (chỉnh cỡ chữ, hotline 1 chạm)",
    "- Chuyển sang: PHẦN 5 — Kết luận",
  ]);
})();

// ─── SLIDE 15: DIVIDER PHẦN 5 ────────────────────────────────────────────────
addDivider("PHẦN 5", "Kết luận & Hướng phát triển", "Kết quả  ·  Hạn chế đã biết  ·  Hướng mở rộng", [
  "Tổng kết các đóng góp chính và đối chiếu mức độ hoàn thành so với mục tiêu đề ra",
  "Nhìn nhận khách quan các hạn chế nghiên cứu về quy mô tập test và phân bố nhãn",
  "Lộ trình mở rộng: Tích hợp mô hình ngôn ngữ lớn PhoBERT và phát hiện lừa đảo qua giọng nói",
]);

// ─── SLIDE 16: KẾT LUẬN ──────────────────────────────────────────────────────
(function slide16_conclusion() {
  const slide = newSlide("content");
  addHeader(slide, "Kết luận & Hướng Phát triển", SEC[5]);

  const achieved = [
    `F1 = ${pct(MET.xgb.f1)} (mục tiêu ≥ 88%)`,
    `Recall = ${pct(MET.xgb.recall)} (mục tiêu ≥ 92%)`,
    "So sánh 4 mô hình (tối thiểu 3)",
    "2.193 mẫu thực tế, Zero Synthetic Text",
    "SHAP XAI giải thích quyết định",
    "Demo thân thiện người cao tuổi",
  ];
  const future = [
    "Tích hợp PhoBERT (BERT tiếng Việt) [15]",
    "Mở rộng sang lừa đảo qua giọng nói",
    "API cho ứng dụng ngân hàng / nhà mạng",
    "Mở rộng dataset lên 10.000+ mẫu",
    "Dashboard giám sát thời gian thực",
  ];
  addCard(slide, M, CY + 0.15, 4.4, 3.05, "Kết quả đạt được", achieved,
    { fill: T.infoBg, border: T.accent, titleSize: 18, bodySize: 15, bullet: true, spacing: 6 });
  addCard(slide, 5.1, CY + 0.15, 4.4, 3.05, "Hướng phát triển", future,
    { fill: "FFFBEB", border: T.accentAmber, titleColor: "B45309", titleSize: 18, bodySize: 15, bullet: true, spacing: 6 });

  addCallout(slide, M, 4.4, CW, 0.65,
    `Hạn chế đã biết: tập test chỉ có ${TEST_POS} tin lừa đảo (mỗi FN làm Recall đổi ~1.2 điểm); dữ liệu gộp từ nhiều nguồn ẩn danh khác kiểu thẻ — bỏ toàn bộ thẻ, F1 XGBoost ${pct(ABL.baseline.xgboost.f1)} → ${pct(ABL.without_tags.xgboost.f1)}.`,
    { fill: T.amberBg, border: T.accentAmber, size: 13 });

  note(slide, "KẾT LUẬN", [
    "- Hoàn thành đầy đủ các mục tiêu đề ra; XGBoost là mô hình tốt nhất",
    "- Điểm mạnh: dữ liệu thực tế có nguồn truy vết + XAI giải thích + demo trợ năng",
    "- Hạn chế trung thực: test chỉ 84 mẫu lừa đảo; hai nguồn dữ liệu ẩn danh bằng thẻ khác nhau (đã kiểm tra bằng thử nghiệm bỏ thẻ, hiệu năng XGBoost giảm ~1 điểm F1)",
    "- Mở ra: PhoBERT (cần GPU, chưa thử nghiệm) và lừa đảo qua giọng nói",
  ]);
})();

// ─── SLIDE 17: TÀI LIỆU THAM KHẢO (2 cột theo vòng đời dự án — chỉ đạo của anh Thanh) ─────────────
(function slide17_references() {
  const slide = newSlide("content");
  addHeader(slide, "Tài liệu tham khảo", SEC.ref);

  // 15/18 tài liệu đã kiểm chứng (Crossref, trang gốc tạp chí/hội nghị, W3C, Unicode, PyPI, GitHub).
  // Bằng chứng và 3 mục để dành cho báo cáo Word: reports/research-cam-phase09-references-lifecycle.md
  const LEFT = [
    { head: "NGUỒN DỮ LIỆU", items: [
      [1, "N. T. T. Tran et al., “Vietnamese SMS Dataset with Quality Assurance,” IEEE Access, 2026 (theo trích dẫn của tác giả; chưa có tập/DOI). GitHub: trannguyenthaituan251209/vietnamese_sms_dataset."],
      [2, "Nguồn bổ sung của tập lừa đảo (249/420 mẫu): GitHub ghitatruongle/lachancuocgoi, duynguyenhoang22/SMS_Phishing_Detection và ViSmish_Detection; báo chí, VTV24 (13 mẫu)."],
    ] },
    { head: "TIỀN XỬ LÝ NLP", items: [
      [3, "Unicode Consortium, “UAX #15: Unicode Normalization Forms,” Unicode 18.0.0, 12 Aug. 2026."],
      [4, "V.-T. Tran, “PyVi: Python Vietnamese Toolkit,” v0.1.1. GitHub: trungtv/pyvi."],
      [5, "Underthesea NLP, “underthesea: Vietnamese NLP Toolkit,” v9.5.0. GitHub: undertheseanlp/underthesea."],
      [6, "G. Salton and C. Buckley, “Term-weighting approaches in automatic text retrieval,” Inf. Process. Manage., 24(5):513–523, 1988."],
    ] },
    { head: "THUẬT TOÁN HỌC MÁY", items: [
      [7, "T. Chen and C. Guestrin, “XGBoost: A scalable tree boosting system,” KDD 2016, pp. 785–794."],
      [8, "L. Breiman, “Random forests,” Mach. Learn., 45(1):5–32, 2001."],
    ] },
  ];
  const RIGHT = [
    { head: "THUẬT TOÁN HỌC MÁY (TIẾP)", items: [
      [9, "C. Cortes and V. Vapnik, “Support-vector networks,” Mach. Learn., 20(3):273–297, 1995."],
      [10, "J. Platt, “Probabilities for SV machines,” in Advances in Large-Margin Classifiers, MIT Press, 2000, pp. 61–74."],
      [11, "F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” JMLR 12:2825–2830, 2011."],
    ] },
    { head: "GIẢI THÍCH MÔ HÌNH (XAI)", items: [
      [12, "S. M. Lundberg and S.-I. Lee, “A unified approach to interpreting model predictions,” NeurIPS 30, 2017."],
      [13, "S. M. Lundberg et al., “From local explanations to global understanding with explainable AI for trees,” Nat. Mach. Intell., 2(1):56–67, 2020."],
    ] },
    { head: "TRỢ NĂNG WEB", items: [
      [14, "W3C, “Web Content Accessibility Guidelines (WCAG) 2.1,” Recommendation, 5 Jun. 2018 (updated 6 May 2025)."],
    ] },
    { head: "HƯỚNG PHÁT TRIỂN", items: [
      [15, "D. Q. Nguyen and A. T. Nguyen, “PhoBERT: Pre-trained language models for Vietnamese,” Findings of EMNLP, 2020, pp. 1037–1042."],
    ] },
  ];
  const runs = (groups) => {
    const out = [];
    groups.forEach((g, gi) => {
      out.push({ text: g.head, options: { bold: true, color: T.accentDark, fontSize: 10, breakLine: true, paraSpaceBefore: gi ? 3 : 0, paraSpaceAfter: 1.5 } });
      g.items.forEach(([n, t]) => {
        out.push({ text: `[${n}] `, options: { bold: true, color: T.accentDark, fontSize: 9.5, paraSpaceAfter: 1.5 } });
        out.push({ text: t, options: { fontSize: 9.5, breakLine: true, paraSpaceAfter: 1.5 } });
      });
    });
    return out;
  };
  const box = { y: CY + 0.08, w: 4.4, h: 3.55, color: T.text, fontFace: "Calibri", valign: "top", margin: [0, 0, 0, 0], lineSpacingMultiple: 0.95 };
  slide.addText(runs(LEFT), { x: M, ...box });
  slide.addText(runs(RIGHT), { x: 5.1, ...box });
  slide.addText("Nguồn trực tuyến truy cập 21/09/2026 · [1] giấy phép CC BY 4.0 theo README · Danh sách đầy đủ 18 tài liệu: báo cáo Word", {
    x: M, y: 4.80, w: CW, h: 0.22, ...F.caption, shrinkText: true,
  });

  note(slide, "THAM KHẢO", [
    "- Thứ tự theo vòng đời dự án: nguồn dữ liệu [1]–[2] → tiền xử lý NLP [3]–[6] → thuật toán học máy [7]–[11] → XAI [12]–[13] → trợ năng web [14] → hướng phát triển [15]",
    "- Q&A về [1]: trích đúng theo yêu cầu của tác giả bộ dữ liệu trong README (bài IEEE Access 2026); nhóm không khẳng định bài đã xuất bản (chưa có tập/DOI). Điều nhóm dùng và kiểm chứng được là bộ dữ liệu công khai trên GitHub (CC BY 4.0), mỗi mẫu có URL truy vết trong dataset.csv",
    "- 1.944/2.193 mẫu (88.7%) đến từ repo [1]; 249 mẫu lừa đảo còn lại từ nguồn [2]",
    "- [10] Platt: trích theo bản đã xuất bản (MIT Press, 2000, pp. 61–74); bản thảo năm 1999 mang tên dài 'Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods'",
    "- Chỉ 15/18 tài liệu lên slide; LIBLINEAR (LinearSVC), McCallum & Nigam (Naive Bayes) và Streamlit nằm trong báo cáo Word. Bằng chứng kiểm chứng: reports/research-cam-phase09-references-lifecycle.md",
    "- Q&A đạo đức/PII: khử PII 100%; dữ liệu lừa đảo lấy từ nguồn công khai (407/420 mẫu từ các bộ dữ liệu GitHub, 13/420 từ báo chí và video điều tra), mọi mẫu có source_url",
  ]);
})();

// ─── SLIDE 18: THANK YOU ─────────────────────────────────────────────────────
(function slide18_thankyou() {
  const slide = newSlide("thanks");
  addLogo(slide, 0.45, 2.8);
  slide.addText(THANKS_TEXT, {
    x: M, y: 1.25, w: CW, h: 1.30, fontSize: 24, bold: true, color: T.textLight, fontFace: "Cambria",
    align: "center", valign: "middle", shrinkText: true,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: (SW - 2.8) / 2, y: 2.80, w: 2.8, h: 0,
    line: { color: T.accentAmber, width: 2.0 },
  });
  slide.addText("Nhóm 10 — CS114.F31.CN2.TTNT  |  Tháng 09/2026", {
    x: M, y: 3.00, w: CW, h: 0.35, fontSize: 13, color: T.onDarkSoft, fontFace: "Calibri", align: "center",
  });
  const members = [
    "Đặng Chí Thanh  ·  25730067@ms.uit.edu.vn",
    "Bùi Thị Mỷ Cẩm  ·  25730013@ms.uit.edu.vn",
    "Hoàng Cao Sơn  ·  25730061@ms.uit.edu.vn",
  ];
  slide.addText(members.map((m) => ({ text: m, options: { breakLine: true } })), {
    x: M, y: 3.45, w: CW, h: 0.9, fontSize: 12.5, color: T.textLight, fontFace: "Calibri", align: "center",
  });
  slide.addText("KHOA KHOA HỌC MÁY TÍNH  •  TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN, ĐHQG-HCM", {
    x: M, y: 4.55, w: CW, h: 0.3, fontSize: 11, color: T.onDarkMuted, fontFace: "Calibri", align: "center",
  });

  note(slide, "CẢM ƠN", [
    "- Mời Thầy và hội đồng đặt câu hỏi",
    "- Backup slides (19–22): siêu tham số, confusion matrices, learning curves",
  ]);
})();

// ─── SLIDE 19: DIVIDER PHỤ LỤC ───────────────────────────────────────────────
addDivider("PHỤ LỤC", "Phụ lục & Backup Q&A", "Siêu tham số  ·  Confusion Matrices  ·  Learning Curves", [
  "Bảng tổng hợp chi tiết siêu tham số tối ưu và chiến lược tinh chỉnh Hyperparameter Tuning",
  "Phân tích chuyên sâu Ma trận Nhầm lẫn (Confusion Matrices) và đánh đổi sai số FN / FP",
  "Đồ thị Learning Curves: Phân tích mức độ tổng quát hóa và khoảng cách Train vs Validation",
]);

// ─── SLIDE 20: HYPERPARAMETERS ───────────────────────────────────────────────
(function slide20_hyperparams() {
  const slide = newSlide("content");
  addHeader(slide, "Backup: Siêu tham số & Chiến lược tinh chỉnh", SEC.app);

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

  note(slide, "SIÊU THAM SỐ", [
    "- XGBoost và Random Forest: RandomizedSearchCV n_iter=25, 5-fold; SVM và Naive Bayes: GridSearchCV 5-fold",
    "- Naive Bayes chọn alpha=0.01 và chỉ dùng TF-IDF vì đặc trưng phụ có giá trị âm",
    "- CV F1 (train) gần với F1 test → mô hình khái quát tốt",
    "- Q&A SVM: LinearSVC chỉ có decision_function; CalibratedClassifierCV (Platt scaling qua 5-fold) đổi khoảng cách thành xác suất [0, 1]",
  ]);
})();

// ─── SLIDE 21: CONFUSION MATRICES ────────────────────────────────────────────
(function slide21_confusion() {
  const slide = newSlide("content");
  addHeader(slide, "Backup: Confusion Matrices — Cả 4 Mô hình", SEC.app);

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

  note(slide, "CONFUSION MATRIX", [
    "- FN/FP tính từ Recall/Precision trong log trên tập test 439 mẫu (84 lừa đảo)",
    "- XGBoost và Random Forest cùng FN nhỏ nhất; Random Forest báo nhầm nhiều hơn (FP cao hơn)",
    "- Naive Bayes FN và FP cao nhất — vai trò baseline",
    "- Q&A 'test 84 mẫu có đủ tin cậy?': nhóm thừa nhận hạn chế; bù bằng 5-fold CV trên 1.754 mẫu train (CV F1 XGBoost = 0.9603)",
  ]);
})();

// ─── SLIDE 22: LEARNING CURVES ───────────────────────────────────────────────
(function slide22_learning() {
  const slide = newSlide("content");
  addHeader(slide, "Backup: Learning Curves — Train vs Validation", SEC.app);

  addFigure(slide, "learning_curves_summary.png", M, CY + 0.1, 5.7, 3.9);
  addCard(slide, 6.4, CY + 0.15, 3.1, 3.8, "Nhận định trung thực",
    ["Train F1 ≈ 0.96–1.0, Validation F1 ≈ 0.91–0.96 → còn khoảng cách 3–6 điểm (overfit nhẹ)",
     "Validation F1 của XGBoost, SVM, RF vẫn tăng theo số mẫu → thêm dữ liệu sẽ giúp",
     `CV F1 (~${MET.xgb.raw.cv_f1_randomsearch.toFixed(2)}) sát F1 test (${MET.xgb.f1.toFixed(2)}) → khái quát ổn`],
    { titleSize: 14, bodySize: 12, bullet: true, spacing: 6 });

  note(slide, "LEARNING CURVES", [
    "- Không nói 'không overfit': Train F1 gần 1.0 nhưng Validation F1 thấp hơn ~3-6 điểm (overfit nhẹ, đặc thù mô hình cây trên 5.015 chiều)",
    "- Điểm tích cực: Validation F1 vẫn đang tăng theo số mẫu và F1 test sát CV F1 nên không có dấu hiệu khái quát kém",
    "- Naive Bayes: Train F1 giảm, Validation tăng dần — hội tụ ~0.91",
  ]);
})();

// ─── FOOTER + SỐ TRANG cho mọi slide nội dung ────────────────────────────────
const TOTAL = registry.length;
registry.forEach(({ slide, kind }, i) => { if (kind === "content") addFooter(slide, i + 1, TOTAL); });
if (TOTAL !== 22) console.warn(`⚠️  Số slide = ${TOTAL} (kế hoạch: 22)`);

// ─── EXPORT ──────────────────────────────────────────────────────────────────
// PPTX_OUT (tùy chọn) cho phép dựng thử ra nơi khác mà không ghi đè file đang chỉnh tay trong PowerPoint
const outputFile = process.env.PPTX_OUT || path.join(__dirname, "phase09_presentation.pptx");
pptx.writeFile({ fileName: outputFile })
  .then(() => {
    console.log(`✅ Presentation generated (${TOTAL} slides): ${outputFile}`);
    console.log("📝 Next steps (PowerShell, Windows):");
    console.log("   1. Kiểm tra bố cục:   python <skill-root>/scripts/check_overlaps.py phase09_presentation.pptx");
    console.log("   2. Xuất PDF để xem:   python <skill-root>/scripts/soffice.py --headless --convert-to pdf --outdir qa phase09_presentation.pptx");
    console.log("   Hiệu ứng chuyển slide: bật thủ công trong PowerPoint (Transitions → Fade 0.3s → Apply To All) SAU KHI dựng xong; KHÔNG dùng inject_transitions.py.");
  })
  .catch((err) => {
    console.error("❌ Error generating presentation:", err);
    process.exit(1);
  });
