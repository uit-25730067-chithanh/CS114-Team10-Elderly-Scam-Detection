"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
TRÍCH XUẤT VÀ KHỞI TẠO TẬP DỮ LIỆU KIỂM ĐỊNH ĐỜI THỰC (REAL-WORLD TEST SET)
TỪ 20 ẢNH CHỤP MÀN HÌNH ĐIỆN THOẠI CÁ NHÂN CỦA ĐẶNG CHÍ THANH
================================================================================
Mục đích:
  - Trích xuất toàn bộ 42 tin nhắn SMS đời thực từ 20 ảnh chụp màn hình điện thoại
    cá nhân của Đặng Chí Thanh.
  - Tự động ẩn danh hóa toàn diện thông tin cá nhân (PII): tên riêng, mã OTP, số điện thoại,
    mã voucher cá nhân.
  - Ánh xạ trực tiếp 1-1 từng tin nhắn tới liên kết xem ảnh thực tế trên Google Drive
    (thư mục Dang_Chi_Thanh_Normal_SMS).
  - Xuất ra tệp kiểm định độc lập: draft/scam-detection/data/processed/real_world_test_thanh.csv
    với đầy đủ 8 cột kiểm toán chuẩn.
================================================================================
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

# Xác định đường dẫn thư mục gốc draft/scam-detection
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.helpers import CATEGORY_NONE, LABEL_NORMAL


def anonymize_personal_info(text: str) -> str:
    """
    Ẩn danh hóa các thông tin nhạy cảm (PII) trong tin nhắn SMS thực tế.
    Bảo vệ quyền riêng tư cá nhân đồng thời giữ nguyên ngữ cảnh tự nhiên của tin nhắn.
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    result = text.strip()

    # 1. Ẩn danh họ tên cá nhân
    result = re.sub(r"\bDang Chi Thanh\b", "[HỌ_VÀ_TÊN]", result, flags=re.IGNORECASE)
    result = re.sub(r"\bĐặng Chí Thanh\b", "[HỌ_VÀ_TÊN]", result, flags=re.IGNORECASE)

    # 2. Ẩn danh mã OTP xác thực (đầu câu hoặc sau nhãn OTP)
    result = re.sub(
        r"\b(\d{4,8})\s+(?:l[aà]\s+)?m[aã]\s+(?:x[aá]c\s+(?:th[uự]c|minh|nh[aậ]n)|otp)",
        r"[MÃ_OTP] là mã xác thực",
        result,
        flags=re.IGNORECASE,
    )
    result = re.sub(
        r"(m[aã]\s+(?:otp|x[aá]c\s+(?:th[uự]c|minh|nh[aậ]n)|b[aả]o\s+m[aậ]t)[^0-9]{1,40})(\d{4,8})\b",
        r"\1[MÃ_OTP]",
        result,
        flags=re.IGNORECASE,
    )
    result = re.sub(
        r"\b\d{4,8}\s+is your verification code\b",
        "[VERIFICATION_CODE] is your verification code",
        result,
        flags=re.IGNORECASE,
    )
    result = re.sub(r"#\d{4,8}\b", "#[MÃ_OTP]", result)

    # 3. Ẩn danh mã voucher cá nhân đặc thù
    result = re.sub(r"\bCP7NF609J18DI84\b", "[MÃ_ƯU_ĐÃI]", result)
    result = re.sub(r"\bY387AW\b", "[MÃ_ƯU_ĐÃI]", result)
    result = re.sub(r"\bWBEZE7\b", "[MÃ_ƯU_ĐÃI]", result)

    # 4. Ẩn danh số điện thoại cá nhân (giữ nguyên hotline tổng đài 3-4 chữ số như 198, 199, 111)
    result = re.sub(
        r"(?:\+84|84|0)(?:3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])[0-9]{7}\b",
        "[SỐ_ĐIỆN_THOẠI]",
        result,
    )

    # 5. Chuẩn hóa khoảng trắng
    result = re.sub(r"\s+", " ", result).strip()
    return result


def main() -> None:
    evidence_dir = PROJECT_ROOT / "data" / "evidence" / "thanh_phone_sms"
    links_file = evidence_dir / "drive_links.json"

    if not links_file.exists():
        print(f"[!] Không tìm thấy tệp drive_links.json tại: {links_file}")
        sys.exit(1)

    with open(links_file, "r", encoding="utf-8") as f:
        drive_links = json.load(f)

    # Toàn bộ 38 tin nhắn SMS bóc tách chính xác từ 20 ảnh chụp màn hình điện thoại thực tế
    messages_raw: list[tuple[str, str, str]] = [
        # thanh_sms_01.jpg
        ("thanh_sms_01.jpg", "Viettel Tammi", "[QC] Trò chuyện thả ga, lưu giữ trọn khoảnh khắc trên Viettel Tammi! - Gọi thoại, Video call, Chat mượt mà không tốn data. - Tự động sao lưu hình ảnh, kỷ niệm lên Tammi Cloud an toàn. Trải nghiệm ngay tại https://vietteltammi.go.link/tinhnangt8 . Chi tiết liên hệ 18008098 (0đ). Từ chối QC: TC3 gửi 199."),
        ("thanh_sms_01.jpg", "Viettel Tammi", "[QC] GIẢM 300K (trừ vào cước sử dụng) khi đăng ký lắp đặt Internet và thanh toán trước cước (từ 3 tháng trở lên) trên Viettel Tammi: Cước phí chỉ từ 195K/tháng, miễn phí Modem Wifi 6. Đăng ký ngay tại https://vietteltammi.go.link/dangkyinternetT8 . Áp dụng đến hết 31/8. Chi tiết liên hệ 198 (0đ). Từ chối QC: TC3 gửi 199."),
        
        # thanh_sms_02.jpg
        ("thanh_sms_02.jpg", "Viettel Tammi", "[QC] Đổi điểm cực dễ, nhận quà cực mê trên Viettel Tammi! Lựa chọn ưu đãi Viettel++ ngay trên Viettel Tammi tại https://vietteltammi.go.link/vtplus - Đổi data, SMS, phút gọi xài thả ga. - Săn voucher mua sắm, ăn uống, giải trí hấp dẫn. Khám phá tính năng gọi điện, chat miễn phí và vô số tiện ích khác chỉ có tại Viettel Tammi. Chi tiết liên hệ 198 (0đ). Từ chối QC, soạn TC3 gửi 199."),
        ("thanh_sms_02.jpg", "Viettel Tammi", "[QC] Săn deal Green SM trên Viettel Tammi! Giảm 18% Green SM Bike và 15% Green SM Car (tối đa 50K/lượt) khi đặt chuyến trên ứng dụng Viettel Tammi. Đặt xe ngay tại https://vietteltammi.go.link/DatxeT9 . Chi tiết liên hệ 198 (0đ). Từ chối QC: TC3 gửi 199."),
        
        # thanh_sms_03.jpg
        ("thanh_sms_03.jpg", "Viettel Plus", "[TB] QUÀ TẶNG 2/9: 50K ĐIỂM VIETTEL++ Tải Viettel Tammi - nhận vô vàn ưu đãi hấp dẫn: - Đổi điểm Viettel++ sang data, phút gọi và SMS. - Miễn phí data, gọi điện thả ga trên ứng dụng. Tải ứng dụng và nhận quà ngay tại https://vietteltammi.go.link/50Kdiem Chương trình áp dụng cho thuê bao nhận được tin nhắn. Chi tiết liên hệ 198 (0đ)."),
        ("thanh_sms_03.jpg", "Viettel Plus", "Quy khach da doi 1.000 diem tieu dung thanh 10 phut thoai noi mang. Thoi han su dung truoc 28/09/2026. Tong diem tieu dung con lai trong tai khoan Viettel++ cua Quy khach la 4.863 diem. De kiem tra lich su doi diem va lua chon uu dai hap dan khac, vui long truy cap https://viettel.vn/tammi/vtplus. Tran trong."),
        ("thanh_sms_03.jpg", "Viettel Plus", "Doi thanh cong 1.000 diem tieu dung Viettel++ thanh 100 MB Data. Han su dung truoc 01/10/2026. Tong diem tieu dung con lai trong tai khoan Viettel++ cua Quy khach la 3.863 diem. De kiem tra lich su doi diem va lua chon uu dai hap dan khac, vui long truy cap https://viettel.vn/tammi/vtplus. Tran trong."),
        
        # thanh_sms_04.jpg
        ("thanh_sms_04.jpg", "Viettel Nạp Thẻ", "[TB] NẠP THẺ ONLINE - DATA XÀI NGAY! Tặng 20% giá trị tất cả thẻ nạp vào tài khoản viễn thông trong ngày 15/08/2026. Tiền KM sử dụng truy cập Internet trong 15 ngày. Chương trình áp dụng khi nạp thẻ online qua các ví điện tử, ứng dụng thanh toán hoặc tại https://viettel.vn/tammi/naptienkm20 Chi tiết gọi 197, bấm phím 19 (0đ). Trân trọng."),
        ("thanh_sms_04.jpg", "Viettel Nạp Thẻ", "[TB] NẠP THẺ LIỀN TAY, DATA XÀI NGAY! Tặng 20% giá trị tất cả thẻ nạp trong ngày 25/08/2026. Tiền KM sử dụng truy cập Internet trong 15 ngày. Nạp thẻ online tại các ví điện tử, ứng dụng thanh toán hoặc trên app Viettel Tammi tại https://vietteltammi.go.link/naptienkm20 Để nạp thẻ cào, Quý khách soạn NT [Mã thẻ] gửi 100. Chi tiết gọi 197 (phím 19, 0đ). Trân trọng."),
        ("thanh_sms_04.jpg", "Viettel Nạp Thẻ", "[TB] MỪNG QUỐC KHÁNH 2/9 - TẶNG 50% GIÁ TRỊ THẺ NẠP! KM áp dụng với thẻ nạp đầu tiên trong ngày trên Viettel Tammi với mệnh giá từ 50K. Tiền KM sử dụng truy cập Internet trong 5 ngày. Nạp ngay tại https://vietteltammi.go.link/naptienkm50 Chương trình áp dụng đến ngày 2/9/2026 cho thuê bao nhận được tin nhắn. Chi tiết liên hệ 198 (0đ). Trân trọng."),
        
        # thanh_sms_05.jpg
        ("thanh_sms_05.jpg", "Ban Chỉ Đạo Quốc Gia Liệt Sĩ", '[TB] Hưởng ứng "Chiến dịch 500 ngày đêm đẩy mạnh thực hiện tìm kiếm, quy tập và xác định danh tính hài cốt liệt sĩ", Ban Chỉ đạo quốc gia về tìm kiếm, quy tập và xác định danh tính hài cốt liệt sĩ kêu gọi các tổ chức, cá nhân có thông tin về liệt sĩ, mộ liệt sĩ vui lòng cung cấp về Tổng đài tiếp nhận thông tin Chiến dịch 500 ngày đêm. Số điện thoại: 1800.8022 hoặc (+84)965.001.222. Địa chỉ: 165 Xã Đàn, Đống Đa, Hà Nội.'),
        
        # thanh_sms_06.jpg
        ("thanh_sms_06.jpg", "Viettel VoLTE", "[TB] Để duy trì dịch vụ thoại khi Viettel thực hiện tắt sóng 2G (trong tháng 8), Quý khách vui lòng sử dụng điện thoại có bật chế độ VoLTE (gọi 4G/5G). Tham khảo cách bật VoLTE tại https://viettel.vn/batvolte Để được hỗ trợ trực tiếp, Quý khách đến cửa hàng Viettel gần nhất. Chi tiết liên hệ 198 (0đ). Trân trọng."),
        ("thanh_sms_06.jpg", "Viettel VoLTE", "[TB] Để đảm bảo dịch vụ thoại khi Viettel tắt sóng 2G theo quy định của Nhà nước, Quý khách vui lòng bật chế độ VoLTE trên điện thoại. Xem hướng dẫn tại https://viettel.vn/batvolte Nếu máy điện thoại của Quý khách đã bật chế độ VoLTE nhưng vẫn không gọi đi/nhận cuộc gọi được, vui lòng đến cửa hàng Viettel gần nhất để được hỗ trợ hoặc đổi SIM miễn phí. Chi tiết liên hệ 198 (0đ)."),
        
        # thanh_sms_07.jpg
        ("thanh_sms_07.jpg", "Cục An Ninh Mạng - Bộ Công An", "[TB] CỤC AN NINH MẠNG VÀ PCTP SỬ DỤNG CÔNG NGHỆ CAO - BỘ CÔNG AN khuyến cáo người dân không tham gia tổ chức đánh bạc, đánh bạc, cá độ bóng đá dưới mọi hình thức trên không gian mạng. Mọi hành vi vi phạm pháp luật về cờ bạc sẽ bị xử lý nghiêm theo quy định."),
        ("thanh_sms_07.jpg", "Cục CS ĐTTP Về Ma Túy - Bộ Công An", "[TB] Hưởng ứng Tháng hành động phòng, chống ma túy (tháng 6/2026), đề nghị công dân khi phát hiện hành vi vi phạm pháp luật về ma túy (tàng trữ, mua bán, tổ chức, chứa chấp, sử dụng trái phép chất ma túy...) hãy báo ngay cho cơ quan Công an gần nhất hoặc liên hệ trực tiếp số hotline của Cục trưởng Cục Cảnh sát điều tra tội phạm về ma túy - Bộ Công an: 0769040404. Thông tin người cung cấp sẽ được bảo mật tuyệt đối."),
        ("thanh_sms_07.jpg", "Cục CS ĐTTP Về Ma Túy - Bộ Công An", "[TB] Toàn dân chung tay phòng chống ma túy! Đề nghị công dân khi phát hiện hành vi vi phạm pháp luật về ma túy (tàng trữ, mua bán, tổ chức, chứa chấp, sử dụng trái phép chất ma túy...) hãy báo ngay cho cơ quan Công an gần nhất hoặc liên hệ trực tiếp số Hotline của Cục trưởng Cục Cảnh sát điều tra tội phạm về ma túy, Bộ Công an: 0769040404. Mọi thông tin của người cung cấp tin sẽ được bảo mật tuyệt đối và khen thưởng theo quy định."),
        
        # thanh_sms_08.jpg
        ("thanh_sms_08.jpg", "Cục Cảnh Sát PCCC - Bộ Công An", "[TB] Để bảo đảm an toàn phòng cháy trong sử dụng điện, Bộ Công an khuyến cáo: Không sử dụng nhiều thiết bị điện có công suất lớn vào cùng một ổ cắm; không để hàng hóa, vật dụng dễ cháy gần các thiết bị điện sinh nhiệt; thường xuyên kiểm tra, sửa chữa, thay thế thiết bị điện và mạng điện hư hỏng; khi sử dụng thiết bị sinh nhiệt như bàn là, bếp điện... phải có người trông coi; ngắt nguồn và các thiết bị điện khi không sử dụng."),
        ("thanh_sms_08.jpg", "Bộ Công An", "[TB] Tích cực hưởng ứng Tháng hành động phòng, chống ma túy (tháng 6), Ngày quốc tế phòng, chống ma túy và Ngày toàn dân phòng, chống ma túy (ngày 26/6)."),
        ("thanh_sms_08.jpg", "Cục Cảnh Sát PCCC - Bộ Công An", "[TB] Khi phát hiện cháy cần bình tĩnh báo cho mọi người xung quanh biết và tìm cách thoát ra các vị trí thông thoáng, an toàn nhanh nhất; tuyệt đối không trú ẩn ở các khu vực khuất kín (nhà vệ sinh, tủ quần áo...), không dùng thang máy để thoát hiểm. Khi di chuyển thoát nạn cần dùng khăn, vải ướt che miệng, mũi và hạ thấp cơ thể để tránh hít phải khói, khí độc. Khi phải băng qua lửa cần lấy chăn, mền ướt trùm kín cơ thể. Mỗi cơ sở, hộ gia đình cần có nhiều phương án, lối thoát nạn an toàn phòng khi có cháy xảy ra."),
        
        # thanh_sms_09.jpg
        ("thanh_sms_09.jpg", "FPT Play", "[MÃ_OTP] la ma xac thuc tai khoan FPT Play cua Quy khach."),
        ("thanh_sms_09.jpg", "FPT ID", "FPT ID Ma OTP cua QK la [MÃ_OTP], hieu luc 2 phut. FPT ID dung dang nhap cac App FPT, KHONG chia se ma nay voi bat ky ai, ke ca NV FPT. @accounts.fpt.vn #[MÃ_OTP]"),
        
        # thanh_sms_10.jpg
        ("thanh_sms_10.jpg", "Dịch Vụ Công Quốc Gia", "[TB] Toàn dân tích cực tham gia phòng, chống mua bán người. Khi phát hiện dấu hiệu liên quan đến mua bán người, hãy thông báo ngay cho cơ quan Công an gần nhất hoặc Tổng đài quốc gia 111 để được tư vấn, hỗ trợ, hướng dẫn kịp thời."),
        ("thanh_sms_10.jpg", "Dịch Vụ Công Quốc Gia", '[TB] Chủ đề Ngày toàn dân tiết kiệm, chống lãng phí năm 2026 là "Tiết kiệm năng lượng, thịnh vượng tương lai". Đề nghị toàn dân hưởng ứng vì một tương lai thịnh vượng, một lối sống xanh, tích cực.'),
        
        # thanh_sms_11.jpg
        ("thanh_sms_11.jpg", "Sở KH&CN TP.HCM", "Sở Khoa học và Công nghệ Thành phố Hồ Chí Minh đề nghị chủ thuê bao thực hiện xác thực thông tin thuê bao di động trước ngày 15/06/2026 để bảo vệ quyền lợi người sử dụng; phòng, chống lừa đảo, đảm bảo an toàn thông tin cá nhân theo Thông tư 08/2026/TT-BKHCN. Chủ thuê bao thực hiện xác thực theo một trong các hình thức sau: (1) Ứng dụng VNeID của Bộ Công an; (2) Xác thực trên ứng dụng của nhà mạng viễn thông; (3) Đến các điểm giao dịch gần nhất trong khu vực. Trường hợp số thuê bao đã sử dụng để đăng ký tài khoản định danh điện tử mức độ 2 thì không phải xác thực lại thông tin."),
        
        # thanh_sms_12.jpg
        ("thanh_sms_12.jpg", "Mắt Kính Tâm Đức", "(QC) Mung sinh nhat KH thang 11. Tam Duc gui tang KH Voucher -49% 01 Gong kinh, Kinh mat & Ma -100K HD1000K, -200K HD2000K. CT: https://mktd.vn/sinhnhat .HSD 30/11. De tu choi QC, Soan TC MKTAMDUC gui 1313"),
        ("thanh_sms_12.jpg", "Mắt Kính Tâm Đức", "Chuc mung sinh nhat quy khach. Doi ngu Mat Kinh Tam Duc kinh chuc Quy khach Suc khoe, Hanh phuc va Thanh cong. Cam on quy khach da tin dung san pham cua TamDuc"),
        ("thanh_sms_12.jpg", "Mắt Kính Tâm Đức", "(QC) Su kien khai xuan 2026 tai Mat Kinh Tam Duc. Li xi voucher len den 500K tang khach hang cu. Ap dung tu 22/02 - 22/03. CT: https://mktd.vn/tet2026 . De tu choi QC, Soan TC MKTAMDUC gui 1313"),
        ("thanh_sms_12.jpg", "Mắt Kính Tâm Đức", "Mat Kinh Tam Duc gui rieng KH than thiet ma [MÃ_ƯU_ĐÃI] -100K HD1000K va ma [MÃ_ƯU_ĐÃI] -200K HD2000K khi mua sam. HSD 21/06. Chi tiet: https://matkinhtamduc.com/gift"),
        
        # thanh_sms_13.jpg
        ("thanh_sms_13.jpg", "TikTok", "[TikTok] [MÃ_OTP] là mã xác minh của bạn"),
        ("thanh_sms_13.jpg", "TikTok", "[#][TikTok] [MÃ_OTP] là mã xác minh của bạn DaewVIZQ+ns"),
        ("thanh_sms_13.jpg", "TikTok", "[#][TikTok] [VERIFICATION_CODE] is your verification code, valid for 5 minutes. To keep your account safe, never forward this code."),
        
        # thanh_sms_14.jpg
        ("thanh_sms_14.jpg", "Karofi", "KAROFI: Ma OTP cua Quy khach la [MÃ_OTP]. Vui long su dung ma OTP nay trong vong 2 phut. Luu y: khong cung cap ma OTP cho bat ky ai. Tran trong!"),
        
        # thanh_sms_15.jpg
        ("thanh_sms_15.jpg", "Mặt Trận Tổ Quốc Việt Nam", "[TB] MTTQ Việt Nam kêu gọi chung tay ủng hộ đồng bào bị thiệt hại do bão lũ gây ra. Các tài khoản tiếp nhận: 55102025 tại Vietinbank; 8639699999 tại BIDV; 1400666102025 tại Agribank; 8888881010 tại Vietcombank; 0606 tại MBbank."),
        
        # thanh_sms_16.jpg
        ("thanh_sms_16.jpg", "Viettel Money / ePass", "Theo Nghi dinh 119/2024/ND-CP cua Chinh phu, de nghi chu phuong tien o to thuc hien thu tuc chuyen doi tai khoan thu phi sang tai khoan giao thong ket noi voi phuong tien thanh toan khong dung tien mat truoc ngay 01/10/2025. Chu phuong tien lien he voi ePass hoac Nha cung cap dich vu thu phi khac de duoc huong dan thuc hien, tranh gay gian doan dich vu. Neu da lien ket vui long bo qua. Truy cap https://giaothongso.viettelmoney.vn/nd119/ de biet them thong tin."),
        
        # thanh_sms_17.jpg
        ("thanh_sms_17.jpg", "Pharmacity", "Ma giam 70K - [MÃ_ƯU_ĐÃI] cua ban sap het han! HSD: 09/06/25. Ghe Pharmacity gan nhat de su dung ngay! CT: https://bit.ly/4070vc - Hotline: 18006821"),
        ("thanh_sms_17.jpg", "Pharmacity", "Ma xac nhan cua ban tai Pharmacity la: [MÃ_OTP], ma xac nhan chi co hieu luc trong vong 5 phut"),
        ("thanh_sms_17.jpg", "Pharmacity", "(QC) Tu 01-30/08, tran ngap san pham moi, KDR Marvis chi 194k tang them qua, Drceutics chi tu 133k, Torriden giam den 40%. CT https://tinyurl.com/55zdybxy . De tu choi QC, Soan TC PHARMACITY gui 1313"),
        ("thanh_sms_17.jpg", "Pharmacity", "(QC) Giam ngay 14K khi mua Hiruscar Gel 5g tai Pharmacity. Ho tro mo seo tham, seo bong, seo moi hieu qua. Ap dung 15-30/09 & 16-31/10. Mua ngay https://tinyurl.com/Hiugel . De tu choi QC, Soan TC PHARMACITY gui 1313"),
        
        # thanh_sms_18.jpg
        ("thanh_sms_18.jpg", "Đại Học Công Nghệ Thông Tin - UIT", "Chuc mung thi sinh [HỌ_VÀ_TÊN] da trung tuyen (DTTX-VB1) vao truong DH CNTT - DHQG-HCM nganh TRI TUE NHAN TAO . Chi tiet xem trong giay bao trung tuyen va nhap hoc, tra cuu tai dia chi https://tuyensinh.uit.edu.vn/giaybao-nhaphoc?dien_tt=TXQM, hotline [SỐ_ĐIỆN_THOẠI]"),
        
        # thanh_sms_19.jpg
        ("thanh_sms_19.jpg", "Bộ Văn Hóa Thể Thao và Du Lịch", "[TB] Nhân dịp Ngày Sách và Văn hoá đọc Việt Nam lần IV (21/4/2025), Bộ VHTTDL kêu gọi các tổ chức, doanh nghiệp và bạn đọc cả nước cùng nhau lan toả tình yêu sách, để mỗi người dân là một đại sứ văn hoá đọc, mỗi gia đình, cộng đồng là một không gian văn hoá đọc, để cùng sách bước vào kỷ nguyên mới, kỷ nguyên vươn mình của dân tộc."),
        ("thanh_sms_19.jpg", "Bộ Văn Hóa Thể Thao và Du Lịch", "[TB] Bộ Văn hóa, Thể thao và Du lịch khuyến cáo: Trong thời gian gần đây, tình trạng một số tổ chức, cá nhân, người chuyển tải sản phẩm quảng cáo có ảnh hưởng tham gia hoạt động quảng cáo trên mạng xã hội sai sự thật, làm ảnh hưởng đến quyền lợi của người tiêu dùng. Người dân cần nâng cao cảnh giác đối với các thông tin quảng cáo, đặc biệt là quảng cáo về sữa, thuốc, thực phẩm chức năng, mỹ phẩm... để chọn lọc, đánh giá, kiểm tra chất lượng hàng hóa trước khi quyết định lựa chọn sản phẩm, hàng hóa, dịch vụ."),
        
        # thanh_sms_20.jpg
        ("thanh_sms_20.jpg", "MoMo / EVNFinance", "(QC)Ban co the vay den 20 TRIEU sau 1 PHUT tu EVNFinance hoac Mcredit qua MoMo. De biet them thong tin: https://momo.vn/s-vaynhanh . De tu choi, soan TC TenThuongHieu gui 1313"),
    ]

    rows = []
    for idx, (img_name, brand, raw_text) in enumerate(messages_raw, start=1):
        masked_text = anonymize_personal_info(raw_text)
        drive_url = drive_links.get(img_name, "")
        rows.append({
            "id": idx,
            "text": masked_text,
            "label": LABEL_NORMAL,
            "scam_category": CATEGORY_NONE,
            "source": f"SMS Đời Thực - {brand}",
            "source_url": drive_url,
            "collector_name": "Đặng Chí Thanh",
            "notes": f"Minh chứng ảnh chụp điện thoại thực tế ({img_name}) lưu trữ tại Google Drive cá nhân Đặng Chí Thanh",
        })

    df = pd.DataFrame(rows)
    out_path = PROJECT_ROOT / "data" / "processed" / "real_world_test_thanh.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"[+] Đã tạo thành công tệp kiểm định thực tế độc lập: {out_path}")
    print(f"[+] Tổng số mẫu tin nhắn: {len(df)}")
    print(f"[+] Cột dữ liệu: {df.columns.tolist()}")
    print("[+] Kiểm tra 3 mẫu đầu tiên:")
    for _, row in df.head(3).iterrows():
        print(f"  [{row['id']}] {row['source']} | URL: {row['source_url']}")
        print(f"       Nội dung: {row['text'][:90]}...")


if __name__ == "__main__":
    main()
