"""Sample real-world scam and normal messages for 1-click testing in elderly demo UI."""

SAMPLE_MESSAGES = {
    "scam_authority": {
        "title": "🔴 Kịch bản 1: Mạo danh Công an / Viện Kiểm Sát (Dọa bắt giữ)",
        "tag": "Thao túng Sợ hãi Quyền lực (Fear / Authority)",
        "content": (
            "THÔNG BÁO KHẨN TỪ BỘ CÔNG AN: Hiện tại cơ quan Cảnh sát Điều tra đang thụ lý vụ án rửa tiền "
            "xuyên quốc gia có liên quan đến số CMND/CCCD của ông/bà. Tòa án đã phê chuẩn Lệnh bắt tạm giam số 412/QĐ-VKS. "
            "Yêu cầu ông/bà giữ bí mật tuyệt đối, không được nói cho người nhà và chuyển ngay toàn bộ số tiền tiết kiệm "
            "vào tài khoản bảo chứng của Viện Kiểm sát Nhân dân số: 03948291028 tại MB Bank để giám định trong 2 giờ. "
            "Nếu không chấp hành sẽ bị bắt giữ áp giải khẩn cấp!"
        ),
        "explanation": "Chiêu trò đánh vào tâm lý sợ hãi pháp luật của người già, yêu cầu giữ bí mật với con cháu và hối thúc chuyển tiền ngay."
    },
    "scam_emergency": {
        "title": "🔴 Kịch bản 2: Con cháu gặp nạn cấp cứu (Thao túng tình cảm)",
        "tag": "Khẩn cấp Gia đình (Family Emergency)",
        "content": (
            "Bác ơi! Cháu là Hùng bạn của Tuấn con bác đây ạ! Thằng Tuấn trên đường đi làm về vừa bị xe tải tông "
            "chấn thương sọ não nguy kịch, đang cấp cứu ở Bệnh viện Chợ Rẫy mất máu nhiều lắm! Bác sĩ bảo phải đóng 35 triệu "
            "tiền viện phí mổ gấp trong 30 phút nữa mới giữ được tính mạng. Điện thoại Tuấn bị vỡ nát rồi, bác chuyển khoản gấp "
            "vào số tài khoản bác sĩ cấp cứu: 190382910382 Techcombank (chủ TK Nguyen Van An) để họ đưa vào phòng mổ ngay bác ơi!"
        ),
        "explanation": "Đánh vào tình yêu thương con cháu tột cùng, tạo tình huống sinh tử khẩn cấp khiến người già hoảng loạn chuyển tiền không kịp suy xét."
    },
    "scam_gift": {
        "title": "🔴 Kịch bản 3: Tri ân quà tặng sức khỏe / Thuốc tiên miễn phí",
        "tag": "Bẫy Lòng tham & Quà tặng Sức khỏe (Health / Gift Trap)",
        "content": (
            "Chúc mừng cụ Nguyễn Văn A! Cụ là 1 trong 5 hội viên người cao tuổi may mắn nhất được Hội Người Cao Tuổi Việt Nam "
            "tặng miễn phí Bộ quà Tết Tri Ân gồm 3 hộp Sữa canxi nano và Thuốc thảo dược trị dứt điểm đau nhức xương khớp trị giá 6.500.000đ. "
            "Vui lòng nhấn vào đường dẫn http://nhanqua-tri-an-nguoigia.vn/xac-nhan để điền địa chỉ và chuyển 180.000đ phí giao hàng đảm bảo."
        ),
        "explanation": "Đánh vào nỗi lo bệnh tật của người già và tâm lý thích được tri ân/tặng quà, lừa nhấp vào liên kết lạ hoặc gửi phí ảo."
    },
    "normal_family": {
        "title": "🟢 Kịch bản 4: Tin nhắn con cái hỏi thăm bình thường",
        "tag": "Tin nhắn An toàn (Normal Family Message)",
        "content": (
            "Bố ơi, chiều nay con đi làm về sớm con ghé qua nhà biếu bố mẹ ít hoa quả với sữa nhé ạ. Bố uống thuốc huyết áp buổi sáng chưa? "
            "Hôm nay trời trở lạnh bố nhớ mặc ấm và quàng khăn cổ kẻo ho nhé bố."
        ),
        "explanation": "Tin nhắn sinh hoạt đời thường, lời lẽ tự nhiên, không chứa yếu tố dọa nạt, không giục chuyển tiền gấp hay đòi mã OTP."
    }
}
