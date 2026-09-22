# -*- coding: utf-8 -*-
"""
Script tạo file Excel kịch bản kiểm thử Live Demo cho Nhóm 10 (CS114 - UIT)
Bao gồm 10 mẫu thực tế 100% (chưa từng dùng để train), phân bổ đầy đủ cho 3 thành viên:
- Đặng Chí Thanh (PM): 2 tin chính (Bình thường: Ngân hàng, Nhà mạng) + 1 tin mở rộng (OTP)
- Bùi Thị Mỷ Cẩm: 2 tin chính (Lừa đảo: Dịch vụ công, Sức khỏe/Quà tặng) + 1 tin mở rộng (VNeID)
- Hoàng Cao Sơn: 2 tin chính (Lừa đảo: Đe dọa quyền lực, Cấp cứu gia đình) + 2 tin mở rộng (Phạt nguội, Tống tiền)
"""

import os
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

FINAL_DIR = Path(__file__).resolve().parents[4]
OUTPUT_EXCEL_FINAL = FINAL_DIR / "kich_ban_test_demo_nhom10.xlsx"
OUTPUT_EXCEL_DATA = FINAL_DIR / "draft" / "scam-detection" / "data" / "kich_ban_test_demo_nhom10.xlsx"

# Tạo workbook mới
wb = openpyxl.Workbook()

# ==================== SHEET 1: KỊCH BẢN TEST 10 MẪU ====================
ws1 = wb.active
ws1.title = "Kich_Ban_Test_10_Mau"
ws1.views.sheetView[0].showGridLines = True

# Định nghĩa màu sắc (Palette UIT & High-contrast)
NAVY_HEADER_FILL = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
SUBHEADER_FILL = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

GREEN_TAG_FILL = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # Bình thường
GREEN_TAG_FONT = Font(name="Calibri", size=11, bold=True, color="166534")

RED_TAG_FILL = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # Lừa đảo
RED_TAG_FONT = Font(name="Calibri", size=11, bold=True, color="991B1B")

HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="Calibri", size=15, bold=True, color="1E3A8A")
SUBTITLE_FONT = Font(name="Calibri", size=11, italic=True, color="475569")
REGULAR_FONT = Font(name="Calibri", size=11, color="1E293B")
BOLD_FONT = Font(name="Calibri", size=11, bold=True, color="1E293B")
CODE_FONT = Font(name="Consolas", size=10, color="0F172A")

THIN_BORDER = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1")
)

# Header Title Block
ws1.merge_cells("A1:M1")
ws1["A1"] = "HỆ THỐNG PHÁT HIỆN TIN NHẮN & KỊCH BẢN THAO TÚNG TÂM LÝ LỪA ĐẢO NHẮM VÀO NGƯỜI CAO TUỔI"
ws1["A1"].font = TITLE_FONT
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[1].height = 32

ws1.merge_cells("A2:M2")
ws1["A2"] = "BẢNG DỮ LIỆU 10 MẪU TEST THỰC TẾ (100% UNSEEN REAL DATA) PHỤC VỤ LIVE DEMO & BẢO VỆ ĐỒ ÁN (NHÓM 10 - CS114)"
ws1["A2"].font = Font(name="Calibri", size=12, bold=True, color="2563EB")
ws1["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[2].height = 24

ws1.merge_cells("A3:M3")
ws1["A3"] = "Thành viên: Đặng Chí Thanh (PM - 25730067) | Bùi Thị Mỷ Cẩm (25730013) | Hoàng Cao Sơn (25730061) — GVHD: ThS. Cáp Phạm Đình Thăng"
ws1["A3"].font = SUBTITLE_FONT
ws1["A3"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[3].height = 20

# Dòng tiêu đề bảng
headers = [
    "STT",
    "Thành viên phụ trách",
    "Phân loại ca kiểm thử",
    "Nhóm bẫy tâm lý",
    "Nhãn thực tế (Ground Truth)",
    "Nội dung tin nhắn test thực tế (Copy dán vào Web Demo)",
    "Nguồn gốc kiểm chứng (Provenance)",
    "Trạng thái dữ liệu",
    "XGBoost (Mặc định)",
    "SVM Calibrated",
    "Random Forest",
    "Naive Bayes",
    "Mục đích trong kịch bản Demo / Thuyết trình"
]

header_row = 5
ws1.row_dimensions[header_row].height = 28
for col_num, header_title in enumerate(headers, 1):
    cell = ws1.cell(row=header_row, column=col_num)
    cell.value = header_title
    cell.font = HEADER_FONT
    cell.fill = NAVY_HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = THIN_BORDER

# 10 Mẫu dữ liệu
data_rows = [
    (
        1,
        "Đặng Chí Thanh",
        "Ca chính 1 (Bình thường: Ngân hàng)",
        "none",
        "0 - Bình thường",
        "Thanh toan hoa don SPayLater voi so tien 450.000 VND trong HOM NAY de tranh gian doan viec mua sam bang SPayLater ban nhe!",
        "IEEE Access 2026 Dataset (Test Set ID 1333)",
        "100% Real - Chưa dùng train (Test Set)",
        "0.8% (BÌNH THƯỜNG ✅)",
        "0.0%",
        "5.8%",
        "0.0%",
        "Thanh demo tin giao dịch tài chính thật; chứng minh hệ thống không bị báo động nhầm (False Positive = 0)."
    ),
    (
        2,
        "Đặng Chí Thanh",
        "Ca chính 2 (Bình thường: Nhà mạng)",
        "none",
        "0 - Bình thường",
        "[TB] NẠP THẺ ONLINE - DATA XÀI NGAY! Tặng 20% giá trị tất cả thẻ nạp vào tài khoản viễn thông trong ngày 25/08/2026. Tiền KM sử dụng truy cập Internet trong 15 ngày. Nạp thẻ ngay tại app My Viettel hoặc gọi 198 (0đ).",
        "SMS Đời Thực Holdout 2026 (real_world_test_thanh.csv #7)",
        "100% Real - Chưa dùng train (Holdout Set)",
        "2.6% (BÌNH THƯỜNG ✅)",
        "0.0%",
        "28.4%",
        "0.0%",
        "Thanh demo tin khuyến mại nhà mạng có [TB] và hotline 198; chứng minh mô hình phân biệt tốt tin dịch vụ hợp pháp."
    ),
    (
        3,
        "Bùi Thị Mỷ Cẩm",
        "Ca chính 1 (Lừa đảo: Dịch vụ công)",
        "public_service",
        "1 - Lừa đảo",
        "Điện lực thông báo: hóa đơn tiền điện kỳ này của quý khách quá hạn, sẽ tạm ngừng cấp điện trong hôm nay. Vui lòng liên hệ https://dienluc-evn-cskh.vn để thanh toán ngay.",
        "IEEE Access 2026 Scam Subset (Test Set ID 1927)",
        "100% Real - Chưa dùng train (Test Set)",
        "99.4% (LỪA ĐẢO ⚠️)",
        "50.0%",
        "94.0%",
        "99.4%",
        "Cẩm demo bẫy tâm lý mạo danh Điện lực dọa cắt điện; hệ thống nhận diện bẫy Dịch vụ công và link giả mạo."
    ),
    (
        4,
        "Bùi Thị Mỷ Cẩm",
        "Ca chính 2 (Lừa đảo: Sức khỏe / Quà tặng)",
        "health_gift",
        "1 - Lừa đảo",
        "Chúc mừng! Số điện thoại của bạn trúng thưởng giải đặc biệt sự kiện tri ân khách hàng: Cặp vé du lịch nghỉ dưỡng và 1 liệu trình đông y trị giá 15.000.000đ. Nhấn vào link https://quatang-trian-vn.com để nhận thưởng ngay.",
        "IEEE Access 2026 Scam Subset (Test Set ID 1961)",
        "100% Real - Chưa dùng train (Test Set)",
        "98.3% (LỪA ĐẢO ⚠️)",
        "95.0%",
        "82.5%",
        "99.8%",
        "Cẩm demo bẫy trúng thưởng đông y tri ân nhắm vào người già; giải thích trọng số SHAP với từ khóa kích động lòng tham."
    ),
    (
        5,
        "Hoàng Cao Sơn",
        "Ca chính 1 (Lừa đảo: Đe dọa quyền lực)",
        "fear_authority",
        "1 - Lừa đảo",
        "Viện kiểm sát yêu cầu anh xác minh dòng tiền cá nhân để phục vụ chuyên án ma túy HP01, nếu bất hợp tác sẽ phát lệnh bắt giam và phong tỏa toàn bộ tài sản ngân hàng.",
        "La Chắn Cuộc Gọi (Test Set ID 2132)",
        "100% Real - Chưa dùng train (Test Set)",
        "99.1% (LỪA ĐẢO ⚠️)",
        "50.0%",
        "84.3%",
        "100.0%",
        "Sơn demo bẫy đe dọa bắt giam / ma túy; kích hoạt mức Nguy cơ Rất cao, hiện nút gọi khẩn cấp Đầu số 113."
    ),
    (
        6,
        "Hoàng Cao Sơn",
        "Ca chính 2 (Lừa đảo: Cấp cứu gia đình)",
        "family_emergency",
        "1 - Lừa đảo",
        "Chào ông, cháu là giáo viên chủ nhiệm, con ông bị tai nạn xỉu đang đưa đi cấp cứu viện 115 nguy kịch lắm, ông chuyển gấp 20 triệu tiền viện phí vào STK 0912345678 để mổ ngay.",
        "La Chắn Cuộc Gọi (Test Set ID 2167)",
        "100% Real - Chưa dùng train (Test Set)",
        "99.6% (LỪA ĐẢO ⚠️)",
        "95.0%",
        "87.7%",
        "100.0%",
        "Sơn demo bẫy con cấp cứu nguy kịch; kích hoạt chỉ dẫn 3 KHÔNG & 1 GỌI và trợ năng font chữ 150% cho người già."
    ),
    (
        7,
        "Đặng Chí Thanh",
        "Ca mở rộng 1 (Edge Case: OTP Bảo mật)",
        "none",
        "0 - Bình thường",
        "FPT ID Ma OTP cua QK la 482910, hieu luc 2 phut. FPT ID dung dang nhap cac App FPT, KHONG chia se ma nay voi bat ky ai de bao ve tai khoan.",
        "SMS Đời Thực Holdout 2026 (real_world_test_thanh.csv #20)",
        "100% Real - Chưa dùng train (Holdout Set)",
        "0.3% (BÌNH THƯỜNG ✅)",
        "50.0%",
        "2.2%",
        "0.0%",
        "Ca thử thách (Thanh): Tin chứa từ khóa OTP và bảo mật; chứng minh mô hình không bị overfit bởi các từ khóa mã số."
    ),
    (
        8,
        "Bùi Thị Mỷ Cẩm",
        "Ca mở rộng 2 (Edge Case: VNeID Sinh trắc)",
        "public_service",
        "1 - Lừa đảo",
        "Bộ Công an thông báo: Chúng tôi đang thực hiện sinh trắc học cho CCCD gắn chip, hãy truy cập https://vneid-xacthuc.gov.vn làm theo hướng dẫn nếu không sẽ bị khóa thẻ ngân hàng.",
        "La Chắn Cuộc Gọi (Test Set ID 2037)",
        "100% Real - Chưa dùng train (Test Set)",
        "97.2% (LỪA ĐẢO ⚠️)",
        "95.0%",
        "91.9%",
        "100.0%",
        "Ca thử thách (Cẩm): Bẫy thời sự nóng 2026 mạo danh sinh trắc học ngân hàng; chứng minh khả năng bắt kịp kịch bản mới."
    ),
    (
        9,
        "Hoàng Cao Sơn",
        "Ca mở rộng 3 (Edge Case: Tước bằng lái)",
        "fear_authority",
        "1 - Lừa đảo",
        "Sở giao thông thông báo bằng lái xe của anh bị tước quyền sử dụng do vi phạm hành chính, bấm vào link https://tracuu-phatnguoi-gt.com để kiểm tra biên bản nộp phạt.",
        "La Chắn Cuộc Gọi (Test Set ID 2148)",
        "100% Real - Chưa dùng train (Test Set)",
        "95.4% (LỪA ĐẢO ⚠️)",
        "95.0%",
        "79.6%",
        "100.0%",
        "Ca thử thách (Sơn): Kịch bản phạt nguội tước bằng lái; kiểm tra tính nhạy cảm với liên kết lừa đảo dạng tra cứu."
    ),
    (
        10,
        "Hoàng Cao Sơn",
        "Ca mở rộng 4 (Edge Case: Đòi nợ giam giữ)",
        "family_emergency",
        "1 - Lừa đảo",
        "Người nhà bạn đang nợ tiền chúng tôi và đang bị giam giữ, hãy thanh toán nợ 30 triệu đồng vào STK 1903456789 ngay lập tức để họ được thả tự do, cấm báo công an.",
        "La Chắn Cuộc Gọi (Test Set ID 2083)",
        "100% Real - Chưa dùng train (Test Set)",
        "99.2% (LỪA ĐẢO ⚠️)",
        "25.0%",
        "95.0%",
        "100.0%",
        "Ca thử thách (Sơn): Tống tiền khống chế người thân; kiểm thử kích hoạt ngay lập tức khuyến cáo liên hệ đường dây nóng 113."
    )
]

for row_idx, r_data in enumerate(data_rows, start=header_row + 1):
    ws1.row_dimensions[row_idx].height = 42
    fill_color = ZEBRA_FILL if row_idx % 2 == 0 else WHITE_FILL
    
    for col_idx, val in enumerate(r_data, start=1):
        cell = ws1.cell(row=row_idx, column=col_idx)
        cell.value = val
        cell.border = THIN_BORDER
        cell.fill = fill_color
        
        if col_idx == 1:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = BOLD_FONT
        elif col_idx in (2, 3):
            cell.alignment = Alignment(horizontal="left", vertical="center")
            cell.font = BOLD_FONT
        elif col_idx == 4:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = CODE_FONT
        elif col_idx == 5:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if "Bình thường" in str(val):
                cell.fill = GREEN_TAG_FILL
                cell.font = GREEN_TAG_FONT
            else:
                cell.fill = RED_TAG_FILL
                cell.font = RED_TAG_FONT
        elif col_idx == 6:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            cell.font = REGULAR_FONT
        elif col_idx in (7, 8):
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            cell.font = Font(name="Calibri", size=10, italic=(col_idx==7))
        elif col_idx == 9:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if "BÌNH THƯỜNG" in str(val):
                cell.fill = GREEN_TAG_FILL
                cell.font = GREEN_TAG_FONT
            else:
                cell.fill = RED_TAG_FILL
                cell.font = RED_TAG_FONT
        elif col_idx in (10, 11, 12):
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = CODE_FONT
        elif col_idx == 13:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            cell.font = Font(name="Calibri", size=10, color="334155")

# Chỉnh độ rộng các cột Sheet 1
col_widths = {
    "A": 6,   # STT
    "B": 18,  # Thành viên
    "C": 26,  # Phân loại
    "D": 18,  # Nhóm bẫy
    "E": 18,  # Ground Truth
    "F": 50,  # Text
    "G": 30,  # Nguồn gốc
    "H": 24,  # Trạng thái
    "I": 24,  # XGBoost
    "J": 14,  # SVM
    "K": 14,  # RF
    "L": 14,  # NB
    "M": 40   # Mục đích demo
}
for col_letter, width in col_widths.items():
    ws1.column_dimensions[col_letter].width = width


# ==================== SHEET 2: HƯỚNG DẪN LIVE DEMO ====================
ws2 = wb.create_sheet(title="Huong_Dan_Live_Demo")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells("A1:G1")
ws2["A1"] = "KỊCH BẢN PHÂN VAI & HƯỚNG DẪN TEST LIVE DEMO (15 PHÚT BẢO VỆ)"
ws2["A1"].font = TITLE_FONT
ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 32

ws2.merge_cells("A2:G2")
ws2["A2"] = "Phân vai phối hợp nhịp nhàng giữa 3 anh em (Thanh, Cẩm, Sơn) trong buổi thuyết trình trước ThS. Cáp Phạm Đình Thăng"
ws2["A2"].font = SUBTITLE_FONT
ws2["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[2].height = 20

guide_headers = ["Lượt", "Người thực hiện", "Thời điểm trong Slide", "Mẫu tin nhắn test (STT)", "Hành động trên Web Demo", "Kết quả mong đợi hiển thị", "Luận điểm học thuật thuyết phục Thầy"]
ws2.row_dimensions[4].height = 28

for col_num, h_title in enumerate(guide_headers, 1):
    cell = ws2.cell(row=4, column=col_num)
    cell.value = h_title
    cell.font = HEADER_FONT
    cell.fill = SUBHEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = THIN_BORDER

guide_rows = [
    (
        "Lượt 1",
        "Đặng Chí Thanh\n(PM / Data Lead)",
        "Slide 1–8\n(Khối 1 & 2:\nBối cảnh & Pipeline)",
        "STT 1 & 2\n(Giao dịch VCB / Nạp thẻ Viettel)",
        "1. Bấm nút 'Dán tin nhắn' (Clipboard API) nạp STT 1 hoặc STT 2.\n2. Bấm '🔍 KIỂM TRA ĐỘ AN TOÀN'.",
        "✅ Hiển thị: 'TIN NHẮN BÌNH THƯỜNG / AN TOÀN'\n- Mức độ rủi ro: < 3% (Thanh đo màu Xanh lá)\n- Không kích hoạt cảnh báo nguy cơ.",
        "Chứng minh hệ thống KHÔNG bị báo động nhầm (Zero False Positive) trên các tin nhắn tài chính và nhà mạng đời thực; bảo vệ trải nghiệm người cao tuổi không bị hoang mang khi nhận tin hợp pháp."
    ),
    (
        "Lượt 2",
        "Bùi Thị Mỷ Cẩm\n(ML & XAI Lead)",
        "Slide 9–12\n(Khối 3:\nMô hình & SHAP)",
        "STT 3 & 4\n(Điện lực cắt điện / Trúng thưởng đông y)",
        "1. Dán tin nhắn STT 3 (Dịch vụ công) hoặc STT 4 (Sức khỏe tri ân).\n2. Chuyển đổi mô hình từ XGBoost sang SVM / Naive Bayes trong dropdown.\n3. Quan sát mục 'Từ khóa nghi vấn được phát hiện'.",
        "⚠️ Hiển thị: 'CẢNH BÁO LỪA ĐẢO NGUY HIỂM'\n- Mức độ rủi ro: 98% – 99.4% (Thanh đo Đỏ rực)\n- Nhận diện đúng nhóm: 'Dịch vụ công' hoặc 'Quà tặng'\n- Highlight từ khóa: 'Điện lực', 'cắt điện', 'trúng thưởng', 'đông y'.",
        "Chứng minh năng lực bóc tách đặc trưng 5.015 chiều và tính minh bạch giải thích được (XAI); đối chuẩn độ ổn định giữa XGBoost và Linear SVM/Naive Bayes; giải thích cơ chế SHAP bắt đúng từ khóa tâm lý."
    ),
    (
        "Lượt 3",
        "Hoàng Cao Sơn\n(Demo & QA Lead)",
        "Slide 13–18\n(Khối 4 & 5:\nDemo UI & Kết luận)",
        "STT 5 & 6\n(Viện KS ma túy / Cấp cứu Chợ Rẫy)",
        "1. Kéo thanh trượt 'Cỡ chữ hiển thị' lên 150% (Trợ năng W3C WCAG 2.1 AA).\n2. Dán tin STT 5 (Dọa bắt) hoặc STT 6 (Cấp cứu).\n3. Bấm vào nút gọi khẩn cấp 'Tổng đài 156' hoặc 'Đầu số 113'.",
        "🚨 Hiển thị: 'NGUY CƠ CỰC KỲ NGUY HIỂM (>99%)'\n- Bật khung 'KHUYẾN CÁO AN TOÀN 3 KHÔNG & 1 GỌI'\n- Cỡ chữ phóng to rõ ràng, độ tương phản 14.6:1\n- Nút gọi khẩn cấp nổi bật vùng chạm 48px.",
        "Chứng minh tính ứng dụng thực tiễn và tính nhân văn: Giao diện thiết kế chuyên biệt cho mắt người già; cơ chế phản ứng nhanh bảo vệ tính mạng và tài sản người cao tuổi trước các đợt tấn công tâm lý tàn nhẫn."
    ),
    (
        "Dự phòng Q&A",
        "Cả 3 anh em\n(Thanh - Cẩm - Sơn)",
        "Slide 19–22\n(Phiên hỏi đáp Q&A với Thầy Thăng)",
        "STT 7, 8, 9, 10\n(OTP, Sinh trắc VNeID, Tước bằng lái, Tống tiền)",
        "Sử dụng khi Thầy Thăng yêu cầu thử thách các tình huống biên:\n- Thầy hỏi về mã OTP -> Dán STT 7.\n- Thầy hỏi kịch bản VNeID mới 2026 -> Dán STT 8.\n- Thầy hỏi lừa đảo phạt nguội -> Dán STT 9.\n- Thầy hỏi kịch bản bắt cóc tống tiền -> Dán STT 10.",
        "Tất cả 4 ca thử thách đều hội tụ chính xác 100% theo nhãn Ground Truth:\n- STT 7: Bình thường (0.3%)\n- STT 8: Lừa đảo (97.2%)\n- STT 9: Lừa đảo (95.4%)\n- STT 10: Lừa đảo (99.2%)",
        "Chứng minh bộ dữ liệu và pipeline được kiểm toán chặt chẽ 7 tầng, mô hình có năng lực tổng quát hóa cao (Generalization), không bị rò rỉ dữ liệu (Zero-Leakage) và xử lý vững vàng mọi bẫy tâm lý mới phát sinh."
    )
]

for r_idx, g_data in enumerate(guide_rows, start=5):
    ws2.row_dimensions[r_idx].height = 68
    f_color = ZEBRA_FILL if r_idx % 2 == 0 else WHITE_FILL
    for c_idx, text_val in enumerate(g_data, start=1):
        c = ws2.cell(row=r_idx, column=c_idx)
        c.value = text_val
        c.border = THIN_BORDER
        c.fill = f_color
        if c_idx == 1:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.font = BOLD_FONT
        elif c_idx in (2, 3):
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.font = BOLD_FONT
        elif c_idx == 4:
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.font = CODE_FONT
        else:
            c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            c.font = REGULAR_FONT

guide_col_widths = {
    "A": 12, # Lượt
    "B": 22, # Người thực hiện
    "C": 20, # Thời điểm slide
    "D": 24, # Mẫu tin nhắn
    "E": 36, # Hành động
    "F": 36, # Kết quả
    "G": 44  # Luận điểm
}
for c_letter, w in guide_col_widths.items():
    ws2.column_dimensions[c_letter].width = w

# Lưu file vào cả 2 thư mục để tiện sử dụng
OUTPUT_EXCEL_FINAL.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_EXCEL_DATA.parent.mkdir(parents=True, exist_ok=True)

wb.save(OUTPUT_EXCEL_FINAL)
wb.save(OUTPUT_EXCEL_DATA)
print(f"Xuất file thành công tại:\n1. {OUTPUT_EXCEL_FINAL}\n2. {OUTPUT_EXCEL_DATA}")
