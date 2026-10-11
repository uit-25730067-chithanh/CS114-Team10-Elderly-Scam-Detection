#!/usr/bin/env python3
"""
Tạo tài liệu Huong_dan_su_dung.docx và Huong_dan_su_dung.pdf chuẩn học thuật UIT CS114.
Tham chiếu phong cách chuẩn từ CS106 (generate_academic_guide_docx.py).
"""

import os
import subprocess
from pathlib import Path
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

BLACK = RGBColor(0, 0, 0)

def set_cell_margins(cell, top=60, bottom=60, left=120, right=120):
    """Thiết lập padding ô trong bảng (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex="F2F2F2"):
    """Tô màu nền ô."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>')
    tcPr.append(shd)

def apply_booktabs_borders(table, border_color="CCCCCC", top_sz="8", bottom_sz="8", inside_sz="4"):
    """Áp dụng viền chuẩn Booktabs học thuật UIT (chỉ viền ngang)."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="{top_sz}" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="single" w:sz="{bottom_sz}" w:space="0" w:color="{border_color}"/>
            <w:insideH w:val="single" w:sz="{inside_sz}" w:space="0" w:color="{border_color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_code_block(doc, code_text):
    """Thêm đoạn mã nguồn định dạng monospace Courier New."""
    for i, line in enumerate(code_text.splitlines()):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.space_before = Pt(2) if i == 0 else Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(line)
        r.font.name = "Courier New"
        r.font.size = Pt(9.5)
        if line.strip().startswith("#"):
            r.font.color.rgb = RGBColor(100, 100, 100)
            r.italic = True
        else:
            r.font.color.rgb = BLACK
            r.bold = True

def generate_guide_docx(output_path: str):
    doc = docx.Document()

    # Cấu hình lề trang A4 chuẩn UIT (18mm trên/dưới, 22mm trái/phải)
    section = doc.sections[0]
    section.top_margin = Inches(0.70)
    section.bottom_margin = Inches(0.70)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)

    # Header & Footer
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = "Trường ĐH Công nghệ Thông tin, ĐHQG-HCM | Môn Máy học (CS114)"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if hp.runs:
        hp.runs[0].font.name = "Times New Roman"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(120, 120, 120)

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = "Nhóm 10 — Hướng dẫn cài đặt và sử dụng chương trình Elderly Scam Detection"
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if fp.runs:
        fp.runs[0].font.name = "Times New Roman"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(120, 120, 120)

    # 1. TIÊU NGỮ HỌC THUẬT UIT
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(1)
    p_inst.paragraph_format.line_spacing = 1.10
    
    r1 = p_inst.add_run("ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(10.5)
    r1.font.bold = True
    r1.font.color.rgb = BLACK

    r2 = p_inst.add_run("KHOA KHOA HỌC MÁY TÍNH — BỘ MÔN TRÍ TUỆ NHÂN TẠO\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10.5)
    r2.font.bold = True
    r2.font.color.rgb = BLACK

    r3 = p_inst.add_run("-o0o-")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = BLACK

    # 2. TIÊU ĐỀ TÀI LIỆU
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.line_spacing = 1.15

    rt1 = p_title.add_run("HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG CHƯƠNG TRÌNH\n")
    rt1.font.name = "Times New Roman"
    rt1.font.size = Pt(14.0)
    rt1.font.bold = True
    rt1.font.color.rgb = BLACK

    rt2 = p_title.add_run("MÔN HỌC: MÁY HỌC (CS114.F31.CN2.TTNT) — ĐỒ ÁN CUỐI KỲ\n")
    rt2.font.name = "Times New Roman"
    rt2.font.size = Pt(11.5)
    rt2.font.bold = True
    rt2.font.color.rgb = BLACK

    rt3 = p_title.add_run("Phát hiện Tin nhắn & Kịch bản Thao túng Tâm lý Lừa đảo nhắm vào Người cao tuổi tại Việt Nam\n")
    rt3.font.name = "Times New Roman"
    rt3.font.size = Pt(11.0)
    rt3.italic = True
    rt3.font.color.rgb = BLACK

    rt4 = p_title.add_run("Nhóm 10: Đặng Chí Thanh (Lead), Bùi Thị Mỷ Cẩm, Hoàng Cao Sơn — GVHD: ThS. Cáp Phạm Đình Thăng")
    rt4.font.name = "Times New Roman"
    rt4.font.size = Pt(10.5)
    rt4.font.color.rgb = BLACK

    # Link liên kết chính thức
    p_link = doc.add_paragraph()
    p_link.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_link.paragraph_format.space_before = Pt(2)
    p_link.paragraph_format.space_after = Pt(6)
    
    rl1 = p_link.add_run("Mã nguồn GitHub chính thức: ")
    rl1.font.name = "Times New Roman"
    rl1.font.size = Pt(9.5)
    rl1.font.bold = True
    rl1.font.color.rgb = BLACK
    
    rl2 = p_link.add_run("https://github.com/uit-25730067-chithanh/CS114-Team10-Elderly-Scam-Detection\n")
    rl2.font.name = "Times New Roman"
    rl2.font.size = Pt(9.5)
    rl2.underline = True
    rl2.font.color.rgb = BLACK

    rl3 = p_link.add_run("Video Clip Demo trực tiếp: ")
    rl3.font.name = "Times New Roman"
    rl3.font.size = Pt(9.5)
    rl3.font.bold = True
    rl3.font.color.rgb = BLACK

    rl4 = p_link.add_run("https://aceteam-uit.vercel.app/l/BhqvPH\n")
    rl4.font.name = "Times New Roman"
    rl4.font.size = Pt(9.5)
    rl4.underline = True
    rl4.font.color.rgb = BLACK

    rl5 = p_link.add_run("Ứng dụng Web Demo tương tác: ")
    rl5.font.name = "Times New Roman"
    rl5.font.size = Pt(9.5)
    rl5.font.bold = True
    rl5.font.color.rgb = BLACK

    rl6 = p_link.add_run("http://localhost:8501")
    rl6.font.name = "Times New Roman"
    rl6.font.size = Pt(9.5)
    rl6.underline = True
    rl6.font.color.rgb = BLACK

    rl7 = p_link.add_run(" (Khởi chạy cục bộ qua script Chay_Demo.bat)")
    rl7.font.name = "Times New Roman"
    rl7.font.size = Pt(9.5)
    rl7.italic = True
    rl7.font.color.rgb = BLACK

    # --- PHẦN 1: YÊU CẦU MÔI TRƯỜNG & CÀI ĐẶT ---
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(8)
    h1.paragraph_format.space_after = Pt(4)
    h1.paragraph_format.keep_with_next = True
    r = h1.add_run("1. YÊU CẦU MÔI TRƯỜNG & CÀI ĐẶT")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(4)
    p1.paragraph_format.line_spacing = 1.15
    r = p1.add_run("Chương trình được phát triển và kiểm thử ổn định trên hệ điều hành Windows 10/11, macOS và Linux với Python phiên bản từ 3.9 đến 3.11. Quá trình thiết lập môi trường thực nghiệm được thực hiện tuần tự như sau:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.color.rgb = BLACK

    p_step1 = doc.add_paragraph()
    p_step1.paragraph_format.space_before = Pt(4)
    p_step1.paragraph_format.space_after = Pt(2)
    p_step1.paragraph_format.keep_with_next = True
    r = p_step1.add_run("Bước 1: Mở Terminal tại thư mục source_code/ và kích hoạt môi trường ảo:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    add_code_block(doc, "cd source_code\npython -m venv .venv\n# Trên Windows:        .venv\\Scripts\\activate\n# Trên Linux / macOS:  source .venv/bin/activate")

    p_step2 = doc.add_paragraph()
    p_step2.paragraph_format.space_before = Pt(6)
    p_step2.paragraph_format.space_after = Pt(2)
    p_step2.paragraph_format.keep_with_next = True
    r = p_step2.add_run("Bước 2: Cài đặt danh mục thư viện phụ thuộc:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    add_code_block(doc, "pip install --upgrade pip\npip install -r requirements.txt")

    # --- PHẦN 2: CẤU TRÚC MÃ NGUỒN VÀ CHỨC NĂNG MODULE ---
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.keep_with_next = True
    r = h2.add_run("2. CẤU TRÚC MÃ NGUỒN VÀ CHỨC NĂNG MODULE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(4)
    p2.paragraph_format.line_spacing = 1.15
    r = p2.add_run("Mã nguồn dự án được tổ chức chặt chẽ theo nguyên tắc module hóa cao trong thư mục source_code/code/src/ và source_code/demo/:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.color.rgb = BLACK

    p_tb1_caption = doc.add_paragraph()
    p_tb1_caption.paragraph_format.space_before = Pt(4)
    p_tb1_caption.paragraph_format.space_after = Pt(3)
    p_tb1_caption.paragraph_format.keep_with_next = True
    r = p_tb1_caption.add_run("Bảng 1: Danh mục chức năng các module chính trong chương trình")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.italic = True
    r.font.bold = True
    r.font.color.rgb = BLACK

    modules_data = [
        ("src/preprocessing/text_cleaner.py", "Chuẩn hóa bảng mã Unicode dựng sẵn (NFC), chuyển chữ thường, loại bỏ ký tự lạ và khoảng trắng thừa."),
        ("src/preprocessing/teencode_dictionary.py", "Bản đồ tra cứu và chuẩn hóa 82 cụm từ viết tắt, tiếng lóng mạng xã hội và teencode tiếng Việt."),
        ("src/preprocessing/pipeline.py", "Quy trình khử định danh PII (SĐT, URL, OTP, tiền tệ), trích xuất 15 đặc trưng phụ (auxiliary features)."),
        ("src/preprocessing/tokenizer.py", "Tách từ ghép tiếng Việt chuyên sâu theo ngữ nghĩa văn cảnh dựa trên bộ thư viện PyVi."),
        ("src/models/random_forest_model.py", "Huấn luyện mô hình Random Forest, tối ưu siêu tham số và trích xuất độ quan trọng đặc trưng Gini."),
        ("src/evaluation/metrics_calculator.py", "Tính toán toàn diện các chỉ số F1-Score, Precision, Recall, ROC-AUC, PR-AUC và ma trận nhầm lẫn."),
        ("src/evaluation/xai_explainer.py", "Tính toán giá trị giải thích SHAP (TreeExplainer) để minh bạch hóa lý do dự đoán của mô hình."),
        ("demo/app.py", "Ứng dụng Web tương tác Streamlit: hỗ trợ phân tích thời gian thực, thang đo rủi ro và khuyến nghị an toàn."),
    ]

    t1 = doc.add_table(rows=len(modules_data) + 1, cols=2)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_booktabs_borders(t1, border_color="CCCCCC", top_sz="8", bottom_sz="8", inside_sz="4")

    col_widths_1 = [Inches(2.5), Inches(4.0)]
    headers_1 = ["Module / File", "Mô tả Hoạt động và Chức năng"]
    for j, h_txt in enumerate(headers_1):
        cell = t1.cell(0, j)
        cell.width = col_widths_1[j]
        set_cell_margins(cell, top=50, bottom=50, left=100, right=100)
        set_cell_shading(cell, "F2F2F2")
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(1)
        cp.paragraph_format.space_after = Pt(1)
        r = cp.add_run(h_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = BLACK

    for i, (mod, desc) in enumerate(modules_data):
        row = t1.rows[i + 1]
        c0 = row.cells[0]
        c0.width = col_widths_1[0]
        set_cell_margins(c0, top=35, bottom=35, left=80, right=80)
        cp0 = c0.paragraphs[0]
        cp0.paragraph_format.space_before = Pt(0)
        cp0.paragraph_format.space_after = Pt(0)
        cp0.paragraph_format.line_spacing = 1.10
        r0 = cp0.add_run(mod)
        r0.font.name = "Courier New"
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        r0.font.color.rgb = BLACK

        c1 = row.cells[1]
        c1.width = col_widths_1[1]
        set_cell_margins(c1, top=35, bottom=35, left=80, right=80)
        cp1 = c1.paragraphs[0]
        cp1.paragraph_format.space_before = Pt(0)
        cp1.paragraph_format.space_after = Pt(0)
        cp1.paragraph_format.line_spacing = 1.10
        r1 = cp1.add_run(desc)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.0)
        r1.font.color.rgb = BLACK

    # --- PHẦN 3: HƯỚNG DẪN THỰC THI CHƯƠNG TRÌNH ---
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(2)
    h3.paragraph_format.keep_with_next = True
    r = h3.add_run("3. HƯỚNG DẪN THỰC THI CHƯƠNG TRÌNH")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = BLACK

    # 3.1
    h31 = doc.add_paragraph()
    h31.paragraph_format.space_before = Pt(3)
    h31.paragraph_format.space_after = Pt(1)
    h31.paragraph_format.keep_with_next = True
    r = h31.add_run("3.1. Chạy 7 Notebooks Thực nghiệm Jupyter (Phương thức Thẩm định Kỹ thuật Chính)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p31 = doc.add_paragraph()
    p31.paragraph_format.space_before = Pt(1)
    p31.paragraph_format.space_after = Pt(3)
    p31.paragraph_format.line_spacing = 1.10
    r = p31.add_run("Quý Thầy/Cô mở Jupyter Lab hoặc Visual Studio Code và thực thi tuần tự 7 cuốn sổ tay từ ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_c = p31.add_run("01_preprocessing.ipynb")
    r_c.font.name = "Courier New"
    r_c.font.size = Pt(9.0)
    r_c.font.bold = True
    r_c.font.color.rgb = BLACK

    r = p31.add_run(" đến ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_c2 = p31.add_run("06_evaluation_xai.ipynb")
    r_c2.font.name = "Courier New"
    r_c2.font.size = Pt(9.0)
    r_c2.font.bold = True
    r_c2.font.color.rgb = BLACK

    r = p31.add_run(" trong thư mục source_code/code/notebooks/. Toàn bộ 7 notebooks đều đã được chạy sạch (Clean Run) và lưu sẵn toàn bộ đầu ra biểu đồ, ma trận nhầm lẫn và chỉ số thực nghiệm.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    # 3.2
    h32 = doc.add_paragraph()
    h32.paragraph_format.space_before = Pt(4)
    h32.paragraph_format.space_after = Pt(1)
    h32.paragraph_format.keep_with_next = True
    r = h32.add_run("3.2. Trải nghiệm Trực tuyến & Xem Video Clip Thuyết minh Demo")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p32 = doc.add_paragraph()
    p32.paragraph_format.space_before = Pt(1)
    p32.paragraph_format.space_after = Pt(3)
    p32.paragraph_format.line_spacing = 1.10
    r = p32.add_run("Quý Thầy/Cô có thể trải nghiệm trực tiếp Web Demo tại: ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_surl = p32.add_run("https://cs114-team10-elderly-scam-detection.streamlit.app/")
    r_surl.font.name = "Courier New"
    r_surl.font.size = Pt(9.0)
    r_surl.underline = True
    r_surl.font.bold = True
    r_surl.font.color.rgb = BLACK

    r = p32.add_run(", xem video clip Full HD tại: ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_vurl = p32.add_run("https://aceteam-uit.vercel.app/l/BhqvPH")
    r_vurl.font.name = "Courier New"
    r_vurl.font.size = Pt(9.0)
    r_vurl.underline = True
    r_vurl.font.bold = True
    r_vurl.font.color.rgb = BLACK

    r = p32.add_run(" (hoặc xem tại tệp source_code/demo/Link_video_demo.txt).")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    # 3.3
    h33 = doc.add_paragraph()
    h33.paragraph_format.space_before = Pt(4)
    h33.paragraph_format.space_after = Pt(1)
    h33.paragraph_format.keep_with_next = True
    r = h33.add_run("3.3. Khởi chạy Ứng dụng Web Demo Streamlit tại Máy Cục bộ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p33 = doc.add_paragraph()
    p33.paragraph_format.space_before = Pt(1)
    p33.paragraph_format.space_after = Pt(2)
    p33.paragraph_format.line_spacing = 1.10
    r = p33.add_run("Để trực tiếp trải nghiệm ứng dụng Web giao diện phát hiện tin nhắn lừa đảo bằng mô hình XGBoost tốt nhất, có hai phương thức khởi chạy:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    p_run1 = doc.add_paragraph()
    p_run1.paragraph_format.space_before = Pt(2)
    p_run1.paragraph_format.space_after = Pt(1)
    p_run1.paragraph_format.line_spacing = 1.10
    r = p_run1.add_run("• Cách 1 (Khuyên dùng trên Windows): Nhấp đúp chuột vào file ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK
    r_bat = p_run1.add_run("Chay_Demo.bat")
    r_bat.font.name = "Courier New"
    r_bat.font.size = Pt(9.0)
    r_bat.font.bold = True
    r_bat.font.color.rgb = BLACK
    r = p_run1.add_run(" trong thư mục source_code/.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    p_run2 = doc.add_paragraph()
    p_run2.paragraph_format.space_before = Pt(2)
    p_run2.paragraph_format.space_after = Pt(1)
    p_run2.paragraph_format.line_spacing = 1.10
    r = p_run2.add_run("• Cách 2 (Dòng lệnh đa nền tảng Windows / macOS / Linux):")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    add_code_block(doc, "cd source_code\ncd demo\npython -m streamlit run app.py")

    p32_note = doc.add_paragraph()
    p32_note.paragraph_format.space_before = Pt(3)
    p32_note.paragraph_format.space_after = Pt(3)
    p32_note.paragraph_format.line_spacing = 1.10
    r = p32_note.add_run("Hệ thống sẽ tự động khởi tạo dịch vụ Web cục bộ tại địa chỉ ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_url = p32_note.add_run("http://localhost:8501")
    r_url.font.name = "Courier New"
    r_url.font.size = Pt(9.0)
    r_url.font.bold = True
    r_url.font.color.rgb = BLACK

    r = p32_note.add_run(" với đầy đủ tính năng: thử nghiệm tin nhắn tùy ý, chuyển đổi 4 mô hình, hiển thị Thang đo rủi ro và các kịch bản mẫu đời thực.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    # --- PHẦN 4: BẢNG TỔNG HỢP KẾT QUẢ THỰC NGHIỆM ---
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(8)
    h4.paragraph_format.space_after = Pt(2)
    h4.paragraph_format.keep_with_next = True
    r = h4.add_run("4. BẢNG TỔNG HỢP KẾT QUẢ THỰC NGHIỆM")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p4 = doc.add_paragraph()
    p4.paragraph_format.space_before = Pt(1)
    p4.paragraph_format.space_after = Pt(2)
    p4.paragraph_format.line_spacing = 1.10
    r = p4.add_run("Kết quả đối sánh thực nghiệm của 4 mô hình học máy trên cùng tập dữ liệu kiểm tra 439 mẫu SMS (355 Normal / 84 Scam) được tổng hợp tại Bảng 2:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    p_tb2_caption = doc.add_paragraph()
    p_tb2_caption.paragraph_format.space_before = Pt(2)
    p_tb2_caption.paragraph_format.space_after = Pt(2)
    p_tb2_caption.paragraph_format.keep_with_next = True
    r = p_tb2_caption.add_run("Bảng 2: So sánh hiệu năng phát hiện tin nhắn lừa đảo giữa các mô hình thử nghiệm")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.0)
    r.italic = True
    r.font.bold = True
    r.font.color.rgb = BLACK

    models_data = [
        ("XGBoost (Được chọn)", "5.015", "0.9535", "93.18%", "97.62%", "0.9984"),
        ("Linear SVM", "5.015", "0.9474", "93.10%", "96.43%", "0.9961"),
        ("Random Forest", "5.015", "0.9458", "95.06%", "94.12%", "0.9981"),
        ("Multinomial NB (Baseline)", "5.000", "0.8864", "84.78%", "92.86%", "0.9911"),
    ]

    t2 = doc.add_table(rows=len(models_data) + 1, cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_booktabs_borders(t2, border_color="CCCCCC", top_sz="8", bottom_sz="8", inside_sz="4")

    col_widths_2 = [Inches(2.1), Inches(0.9), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.9)]
    headers_2 = ["Mô hình", "Số chiều", "F1-Score", "Precision", "Recall", "ROC-AUC"]
    for j, h_txt in enumerate(headers_2):
        cell = t2.cell(0, j)
        cell.width = col_widths_2[j]
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        set_cell_shading(cell, "F2F2F2")
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(1)
        cp.paragraph_format.space_after = Pt(1)
        r = cp.add_run(h_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = BLACK

    for i, row_data in enumerate(models_data):
        row = t2.rows[i + 1]
        for j, val in enumerate(row_data):
            c = row.cells[j]
            c.width = col_widths_2[j]
            set_cell_margins(c, top=35, bottom=35, left=60, right=60)
            cp = c.paragraphs[0]
            cp.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER
            cp.paragraph_format.space_before = Pt(0)
            cp.paragraph_format.space_after = Pt(0)
            cp.paragraph_format.line_spacing = 1.10
            r = cp.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.0)
            if i == 0 or (j == 2 and i == 0):
                r.bold = True
            r.font.color.rgb = BLACK

    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(4)
    p_note.paragraph_format.space_after = Pt(2)
    p_note.paragraph_format.line_spacing = 1.10
    r = p_note.add_run("Ghi chú: Mô hình XGBoost kết hợp không gian đặc trưng TF-IDF và 15 đặc trưng phụ được lựa chọn làm mô hình mặc định nhờ khả năng đạt F1-Score cao nhất (0.9535), độ nhạy phát hiện lừa đảo vượt trội (Recall = 97.62%, chỉ bỏ sót 2/84 mẫu lừa đảo) và độ trễ suy luận thời gian thực dưới 5ms.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.italic = True
    r.font.color.rgb = BLACK

    doc.save(output_path)
    print(f"[✓] Đã tạo thành công: {output_path}")

def convert_docx_to_pdf_word(docx_path: str, pdf_path: str):
    """Sử dụng Microsoft Word trên macOS để xuất PDF chất lượng cao."""
    apple_script = f'''
    tell application "Microsoft Word"
        set docPath to POSIX file "{docx_path}"
        set outPath to POSIX file "{pdf_path}"
        open docPath
        set theDoc to active document
        save as theDoc file format format PDF file name (outPath as text)
        close theDoc saving no
    end tell
    '''
    try:
        res = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True, check=True)
        print(f"[✓] Đã chuyển đổi sang PDF thành công qua Microsoft Word: {pdf_path}")
        return True
    except Exception as e:
        print(f"[!] Chuyển đổi PDF qua AppleScript gặp lỗi: {e}")
        return False

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent / "submit" / "25730067_25730013_25730061" / "source_code"
    out_docx = base_dir / "Huong_dan_su_dung.docx"
    out_pdf = base_dir / "Huong_dan_su_dung.pdf"
    generate_guide_docx(str(out_docx))
    convert_docx_to_pdf_word(str(out_docx), str(out_pdf))

