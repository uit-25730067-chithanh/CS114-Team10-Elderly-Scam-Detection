"""Vẽ sơ đồ luồng Input/Output của hệ thống (Hình 3.1 trong báo cáo).

Sơ đồ bám sát code thực tế: `src/preprocessing/pipeline.py`, `src/feature_engineering.py`
và `demo/app.py::predict_text`. Xuất ra `reports/figures/system_io_flowchart.png` (300 DPI).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

COLORS = {
    "io": ("#DBEAFE", "#1D4ED8"),
    "aux": ("#FEF3C7", "#B45309"),
    "text": ("#DCFCE7", "#15803D"),
    "merge": ("#EDE9FE", "#6D28D9"),
    "model": ("#FEE2E2", "#B91C1C"),
}


def draw_box(ax, cx, cy, w, h, text, kind, fontsize=8.5):
    face, edge = COLORS[kind]
    ax.add_patch(
        FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor=face, edgecolor=edge, linewidth=1.4,
        )
    )
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize, color="#111827", linespacing=1.35)


def arrow(ax, start, end, label=None):
    ax.add_patch(
        FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12, linewidth=1.3, color="#374151")
    )
    if label:
        ax.text((start[0] + end[0]) / 2 + 0.1, (start[1] + end[1]) / 2, label,
                fontsize=7.5, color="#374151", ha="left", va="center", style="italic")


def build_flowchart() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8.2, 10.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 13)
    ax.axis("off")

    # Input
    draw_box(ax, 5, 12.2, 5.2, 1.0, "INPUT\nTin nhắn tiếng Việt thô (văn bản gốc)", "io", 9.5)

    # Nhánh trái: đặc trưng phụ | Nhánh phải: văn bản
    arrow(ax, (4.2, 11.7), (2.4, 10.6))
    arrow(ax, (5.8, 11.7), (7.0, 10.6))
    ax.text(0.2, 11.2, "Nhánh A: tín hiệu hành vi", fontsize=7.8, ha="left", color="#B45309", weight="bold")
    ax.text(9.8, 11.2, "Nhánh B: nội dung văn bản", fontsize=7.8, ha="right", color="#15803D", weight="bold")

    draw_box(ax, 2.4, 9.85, 4.0, 1.5,
             "Trích 15 đặc trưng phụ\ntừ văn bản GỐC (regex)\nURL, SĐT, tiền, khẩn cấp,\nquyền lực, OTP, leet-speak...", "aux")
    draw_box(ax, 2.4, 7.95, 4.0, 1.0,
             "StandardScaler\n(fit chỉ trên tập train)", "aux")
    arrow(ax, (2.4, 9.1), (2.4, 8.45))

    draw_box(ax, 7.0, 9.7, 4.0, 1.8,
             "Làm sạch văn bản\nGỡ leet-speak · chuẩn hóa NFC\n& vị trí dấu · chữ thường\nthẻ ẩn danh → token ngữ nghĩa\n160 quy tắc teencode · lọc ký tự", "text", 8.2)
    draw_box(ax, 7.0, 7.95, 4.0, 1.0,
             "Tách từ PyVi\n+ lọc stopwords (giữ từ khóa miền)", "text")
    arrow(ax, (7.0, 8.8), (7.0, 8.45))
    draw_box(ax, 7.0, 6.35, 4.0, 1.1,
             "TF-IDF 5.000 chiều\nn-gram (1,2) · fit chỉ trên train", "text")
    arrow(ax, (7.0, 7.45), (7.0, 6.9))

    # Ghép
    draw_box(ax, 5, 4.45, 6.6, 1.3,
             "Ghép vector đặc trưng X ∈ ℝ⁵⁰¹⁵ = [5.000 TF-IDF | 15 đặc trưng phụ]\n"
             "(Naive Bayes chỉ dùng 5.000 chiều TF-IDF)", "merge", 8.4)
    arrow(ax, (2.4, 7.45), (3.9, 5.1))
    arrow(ax, (7.0, 5.8), (6.1, 5.1))

    # Mô hình
    draw_box(ax, 5, 2.85, 6.6, 1.2,
             "Phân loại — chọn 1 trong 4 mô hình\nXGBoost (mặc định) · Linear SVM · Random Forest · Naive Bayes\n"
             "Đầu ra: p = P(lừa đảo | tin nhắn)", "model", 8.4)
    arrow(ax, (5, 3.8), (5, 3.45))

    # Output
    draw_box(ax, 5, 0.95, 8.2, 1.4,
             "OUTPUT (ngưỡng p ≥ 0.5)\nNhãn: LỪA ĐẢO / AN TOÀN  ·  thang mức độ nguy cơ\n"
             "Đánh dấu từ khóa đáng ngờ  ·  khuyến nghị an toàn cho người cao tuổi", "io", 8.8)
    arrow(ax, (5, 2.2), (5, 1.7))

    return fig


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig = build_flowchart()
    out = FIGURES_DIR / "system_io_flowchart.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
