"""
Safety Advisor Component for Elderly Scam Detection App.
Author: Hoàng Cao Sơn (MSSV: 25730061)
"""

from typing import Dict, List
import streamlit as st


TRAP_DEFINITIONS = {
    "fear_authority": {
        "title": "⚖️ Bẫy Thao Túng Tâm Lý: ĐE DỌA QUYỀN LỰC",
        "description": "Kẻ gian mạo danh Công an, Viện kiểm sát, Tòa án hoặc Cảnh sát giao thông phạt nguội để đe dọa khởi tố, bắt tạm giam nhằm ép nạn nhân hoảng sợ và chuyển tiền vào 'tài khoản an toàn'.",
        "warning_tips": [
            "Công an và Viện kiểm sát KHÔNG BAO GIỜ làm việc hay tống đạt quyết định qua tin nhắn SMS/Zalo.",
            "Cơ quan chức năng không yêu cầu người dân chuyển tiền vào tài khoản cá nhân để 'phục vụ điều tra'.",
            "Nếu có giấy triệu tập, cơ quan công an sẽ gửi giấy mời trực tiếp qua Cảnh sát khu vực."
        ],
        "color": "#c0392b"
    },
    "family_emergency": {
        "title": "🚨 Bẫy Thao Túng Tâm Lý: CẤP CỨU NGƯỜI THÂN",
        "description": "Kẻ gian giả mạo con cháu hoặc bác sĩ bệnh viện (Chợ Rẫy, Bạch Mai...), thông báo người thân bị tai nạn nguy kịch đang chờ mổ, yêu cầu chuyển viện phí gấp và cấm gọi điện thoại.",
        "warning_tips": [
            "Bệnh viện luôn cấp cứu tính mạng bệnh nhân trước, không bao giờ ép người nhà chuyển khoản qua SMS thì mới mổ.",
            "Yêu cầu 'đừng gọi điện thoại' là thủ đoạn cắt đứt liên lạc để ngăn nạn nhân kiểm chứng.",
            "Hãy bình tĩnh lấy máy gọi ngay cho con cháu hoặc gọi cho người cùng nhà để kiểm tra."
        ],
        "color": "#e74c3c"
    },
    "public_service": {
        "title": "🏛️ Bẫy Thao Túng Tâm Lý: GIẢ MẠO DỊCH VỤ CÔNG / VNeID",
        "description": "Kẻ gian giả danh cán bộ Công an phường/quận hoặc nhân viên viễn thông, hướng dẫn kích hoạt định danh VNeID mức 2, cập nhật CCCD hoặc nâng cấp SIM để gửi link cài mã độc.",
        "warning_tips": [
            "Cán bộ Công an không hướng dẫn cài đặt phần mềm qua đường link gửi qua tin nhắn.",
            "Tất cả ứng dụng chính thức (VNeID, VssID) chỉ tải trực tiếp từ kho ứng dụng CH Play hoặc App Store.",
            "Tuyệt đối không cấp quyền Trợ năng (Accessibility) cho bất kỳ tệp tin .apk lạ nào."
        ],
        "color": "#d35400"
    },
    "health_gift": {
        "title": "🎁 Bẫy Thao Túng Tâm Lý: DỤ DỖ QUÀ TẶNG & THUỐC SỨC KHỎE",
        "description": "Kẻ gian đánh vào tâm lý người già muốn giữ gìn sức khỏe hoặc thích tri ân quà tặng, mời chào bài thuốc đông y trị dứt điểm bách bệnh hoặc thông báo trúng thưởng lớn.",
        "warning_tips": [
            "Không có giải thưởng hay quà tặng miễn phí nào lại bắt người nhận phải đóng tiền thuế/phí vận chuyển trước.",
            "Không mua các loại thuốc đông y, thực phẩm chức năng không rõ nguồn gốc quảng cáo thổi phồng trên mạng.",
            "Khi có bệnh, hãy đi khám tại các bệnh viện uy tín hoặc trạm y tế địa phương."
        ],
        "color": "#8e44ad"
    },
    "none": {
        "title": "✅ TIN NHẮN BÌNH THƯỜNG / AN TOÀN",
        "description": "Tin nhắn mang đặc trưng giao dịch ngân hàng, viễn thông hoặc trao đổi sinh hoạt gia đình thông thường.",
        "warning_tips": [
            "Vẫn luôn giữ thói quen không cung cấp mã OTP cho người khác trong mọi tình huống.",
            "Chỉ mở các liên kết chính thức từ ngân hàng có tên miền đã đăng ký bảo mật."
        ],
        "color": "#27ae60"
    }
}


def diagnose_scam_category(text: str) -> str:
    """Xác định nhóm bẫy tâm lý dựa trên nội dung tin nhắn (hỗ trợ cả có dấu và không dấu)."""
    t = text.lower()

    # 1. Bẫy Dịch vụ công / VNeID / Căn cước (ưu tiên kiểm tra trước vì thường kèm mạo danh Công an)
    if any(k in t for k in [
        "vneid", "định danh", "mức 2", "bảo hiểm xã hội", "nâng cấp sim", "thuế", "đồng bộ",
        "căn cước", "cccd", "dịch vụ công", "dich vu cong", "dinh danh", "muc 2", "bao hiem xa hoi", "nang cap sim", "thue", "dong bo"
    ]):
        return "public_service"

    # 2. Bẫy Cấp cứu / Tai nạn người thân
    if any(k in t for k in [
        "tai nạn", "cấp cứu", "bệnh viện", "viện phí", "chuyển tiền gấp", "đừng gọi con",
        "đang họp không tiện", "mổ gấp", "nguy kịch",
        "tai nan", "cap cuu", "benh vien", "vien phi", "chuyen tien gap", "dung goi con",
        "dang hop khong tien", "mo gap", "nguy kich"
    ]):
        return "family_emergency"

    # 3. Bẫy Quà tặng / Sức khỏe / Trúng thưởng
    if any(k in t for k in [
        "trúng thưởng", "quà tri ân", "miễn phí", "thuốc đặc trị", "bài thuốc", "tặng xe", "tri ân",
        "trung thuong", "qua tri an", "mien phi", "thuoc dac tri", "bai thuoc", "tang xe", "tri an"
    ]):
        return "health_gift"

    # 4. Bẫy Đe dọa quyền lực (Công an, Tòa án, Viện kiểm sát, CSGT)
    if any(k in t for k in [
        "công an", "viện kiểm sát", "tòa án", "bắt tạm giam", "lệnh bắt", "phạt nguội",
        "khởi tố", "phong tỏa", "csgt", "truy nã", "hồ sơ vụ án",
        "cong an", "vien kiem sat", "toa an", "bat tam giam", "lenh bat", "phat nguoi",
        "khoi to", "phong toa", "truy na", "ho so vu an"
    ]):
        return "fear_authority"

    return "none"



def render_safety_advisor(
    category: str,
    is_scam: bool,
    font_multiplier: float = 1.0,
    user_text: str = "",
    aux_dict: dict = None,
) -> None:
    """Hiển thị bảng khuyến cáo an toàn thiết kế sát sao với từng nội dung tin nhắn của người cao tuổi."""
    info = TRAP_DEFINITIONS.get(category, TRAP_DEFINITIONS["none"])
    if is_scam and category == "none":
        info = {
            "title": "⚠️ Bẫy Thao Túng Tâm Lý: THỦ ĐOẠN LỪA ĐẢO MỚI",
            "description": "Mô hình AI phát hiện tin nhắn có các đặc trưng thao túng tâm lý, hối thúc hoặc câu dụ tương đồng với các thủ đoạn lừa đảo tinh vi.",
            "color": "#c0392b"
        }
    base_font = int(18 * font_multiplier)
    title_font = int(22 * font_multiplier)
    user_lower = user_text.lower() if user_text else ""
    aux = aux_dict or {}

    # Thẻ neo phục vụ Mobile Auto-scroll
    st.markdown('<div id="verdict-anchor" style="scroll-margin-top: 80px;"></div>', unsafe_allow_html=True)

    if is_scam:
        # Bảng phân tích bản chất bẫy tâm lý
        st.markdown(f"""
        <div style="
            background-color: #fff9f9;
            border: 1.5px solid {info['color']}55;
            border-left: 6px solid {info['color']};
            border-radius: 12px;
            padding: clamp(14px, 3.5vw, 20px);
            margin: 16px 0 12px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        ">
            <div style="font-size: clamp(18px, 4.2vw, {title_font}px); font-weight: 800; color: {info['color']}; margin-bottom: 8px; line-height: 1.35;">
                {info['title']}
            </div>
            <p style="font-size: clamp(14px, 3.5vw, {base_font}px); line-height: 1.6; color: #333333; margin-bottom: 12px;">
                <b>Dấu hiệu nhận biết:</b> {info['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Xây dựng danh sách khuyến nghị hành động THỰC TẾ, SÁT SAO với đúng nội dung tin nhắn
        action_cards = []

        # 1. Khuyến nghị theo nhóm bẫy cụ thể (Domain-specific Action)
        if category == "fear_authority":
            action_cards.append({
                "icon": "🏛️",
                "title": "Cơ quan Công quyền KHÔNG BAO GIỜ đòi tiền qua mạng:",
                "detail": "Công an, Tòa án và CSGT không gửi thông báo phạt nguội hay dọa bắt qua SMS/Zalo. Giấy phạt nguội chỉ gửi bằng văn bản giấy qua bưu điện về tận nhà. Tra cứu chuẩn xác chỉ qua website chính thức: csgt.vn.",
                "color": "#e53935"
            })
        elif category == "family_emergency":
            action_cards.append({
                "icon": "📱",
                "title": "Bác hãy gọi điện thoại xác thực trực tiếp ngay:",
                "detail": "Bác hãy lấy máy gọi ngay số điện thoại riêng của con/cháu (hoặc gọi qua Zalo/gọi video nhìn mặt). Bệnh viện luôn cấp cứu bảo toàn tính mạng bệnh nhân trước, KHÔNG BAO GIỜ bắt người nhà chuyển tiền qua SMS mới tiến hành mổ!",
                "color": "#e53935"
            })
        elif category == "public_service":
            action_cards.append({
                "icon": "🏢",
                "title": "Cập nhật VNeID / Dịch vụ công chỉ làm tại Công an xã/phường:",
                "detail": "Cán bộ không gọi điện hay nhắn tin hướng dẫn kích hoạt định danh qua link ngoài. Bác tuyệt đối không tải tệp lạ đuôi .apk ngoài kho CH Play / App Store để tránh bị kẻ gian chiếm quyền điều khiển điện thoại.",
                "color": "#e53935"
            })
        elif category == "health_gift":
            action_cards.append({
                "icon": "🎁",
                "title": "Cảnh giác bẫy trúng thưởng xe máy & tặng thuốc miễn phí:",
                "detail": "Không có chương trình tri ân thật nào bắt người nhận phải đóng trước tiền thuế hay phí giao hàng. Bác tuyệt đối không chuyển tiền và không mua các loại thuốc đông y không có nguồn gốc được quảng cáo qua tin nhắn.",
                "color": "#e53935"
            })

        # 2. Khuyến nghị nếu phát hiện có đường link lạ (URL / Link detected)
        has_url = aux.get("num_urls", 0) > 0 or any(k in user_lower for k in ["http", "bit.ly", ".apk", "www.", ".com", ".vn"])
        if has_url:
            action_cards.append({
                "icon": "🔗",
                "title": "Tin nhắn có chứa đường liên kết (link) nghi vấn:",
                "detail": "Kẻ xấu thường dùng link lạ để dẫn dụ người cao tuổi cài mã độc đánh cắp tài khoản ngân hàng. Bác tuyệt đối KHÔNG ĐƯỢC BẤM vào bất kỳ đường link nào trong tin nhắn này!",
                "color": "#d97706"
            })

        # 3. Khuyến nghị nếu phát hiện có yêu cầu tiền bạc / số tài khoản
        has_money = aux.get("num_money_mentions", 0) > 0 or any(k in user_lower for k in ["chuyển", "stk", "tài khoản", "ngân hàng", "triệu", "vnd", "tiền"])
        if has_money:
            action_cards.append({
                "icon": "🛑",
                "title": "Phát hiện yêu cầu chuyển tiền / giao dịch tài chính:",
                "detail": "Bác hãy bình tĩnh dừng lại ít nhất 15 phút, KHÔNG chuyển bất kỳ khoản tiền nào cho đến khi được con cháu hoặc người thân trong gia đình kiểm tra tận mắt.",
                "color": "#b91c1c"
            })

        # Fallback an toàn nếu chưa match thẻ nào
        if not action_cards:
            action_cards.append({
                "icon": "🛡️",
                "title": "Cảnh giác trước yêu cầu lạ:",
                "detail": "Bác tuyệt đối không cung cấp mật khẩu, mã OTP hoặc làm theo chỉ dẫn trong tin nhắn này. Hãy hỏi ý kiến người thân trước khi thực hiện.",
                "color": "#e53935"
            })

        # Render khối hướng dẫn xử lý khẩn cấp sát sao (không dùng khoảng thụt đầu dòng 4+ spaces tránh lỗi Markdown code block)
        cards_html = "".join([
            f'<div style="background: #ffffff; padding: 12px 16px; border-radius: 10px; border-left: 5px solid {card["color"]}; line-height: 1.55; margin-bottom: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.03);">'
            f'<div style="font-size: clamp(14px, 3.5vw, {base_font}px); font-weight: 800; color: #0f172a; margin-bottom: 4px;">'
            f'{card["icon"]} {card["title"]}</div>'
            f'<div style="font-size: clamp(13px, 3.2vw, {base_font - 1}px); color: #334155;">'
            f'{card["detail"]}</div></div>'
            for card in action_cards
        ])

        hotlines_html = (
            f'<div style="background: #e8f5e9; padding: 14px 16px; border-radius: 12px; border-left: 5px solid #2e7d32; font-weight: 700; color: #1b5e20; margin-top: 6px;">'
            f'📞 BÁC HÃY GỌI TRỢ GIÚP KHẨN CẤP HOẶC GỌI CHO CON CHÁU:'
            f'<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 10px;">'
            f'<a href="tel:156" class="action-hotline-btn" style="width: 100%; box-sizing: border-box; background: linear-gradient(135deg, #d32f2f 0%, #b71c1c 100%); color: #ffffff !important; text-decoration: none !important; padding: 12px 16px; border-radius: 10px; font-size: clamp(15px, 3.8vw, 18px); font-weight: 900; text-align: center; box-shadow: 0 3px 8px rgba(183, 28, 28, 0.4); display: block;"><span style="color: #ffffff !important; font-weight: 900;">☎️ BẤM GỌI TỔNG ĐÀI 156</span></a>'
            f'<a href="tel:113" class="action-hotline-btn" style="width: 100%; box-sizing: border-box; background: linear-gradient(135deg, #e65100 0%, #bf360c 100%); color: #ffffff !important; text-decoration: none !important; padding: 12px 16px; border-radius: 10px; font-size: clamp(15px, 3.8vw, 18px); font-weight: 900; text-align: center; box-shadow: 0 3px 8px rgba(191, 54, 12, 0.4); display: block;"><span style="color: #ffffff !important; font-weight: 900;">🚨 BẤM GỌI CÔNG AN 113</span></a>'
            f'</div></div>'
        )

        full_action_box_html = (
            f'<div style="background: linear-gradient(135deg, #fce4ec 0%, #fff3e0 100%); border: 2.5px solid #ff7043; border-radius: 16px; padding: clamp(14px, 3.5vw, 20px); margin-top: 14px; margin-bottom: 24px;">'
            f'<div style="font-size: clamp(17px, 4vw, {title_font}px); font-weight: 900; color: #d84315; text-align: center; margin-bottom: 14px; line-height: 1.35;">🛡️ HÀNH ĐỘNG CẦN LÀM NGAY DÀNH CHO ÔNG/BÀ</div>'
            f'<div style="display: flex; flex-direction: column; gap: 4px;">'
            f'{cards_html}'
            f'{hotlines_html}'
            f'</div></div>'
        )

        st.markdown(full_action_box_html, unsafe_allow_html=True)

    else:
        # Trường hợp tin nhắn an toàn (ngân hàng, sinh hoạt)
        is_bank = any(k in user_lower for k in ["vcb", "vietcombank", "bidv", "techcombank", "mbbank", "agribank", "số dư", "so du", "giao dịch", "vnd", "tài khoản"])
        if is_bank:
            safe_desc = "Hệ thống nhận diện đây là thông báo biến động số dư hoặc giao dịch ngân hàng thông thường. Không chứa từ ngữ đe dọa, hối thúc hay đường link giả mạo."
        else:
            safe_desc = "Hệ thống xác nhận đây là tin nhắn bình thường hoặc trao đổi sinh hoạt gia đình, không phát hiện bẫy tâm lý nguy hiểm."

        st.markdown(f"""
        <div style="
            background-color: #f1f8e9;
            border-left: 6px solid #558b2f;
            border-radius: 12px;
            padding: clamp(14px, 3.5vw, 20px);
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        ">
            <div style="font-size: clamp(18px, 4.2vw, {title_font}px); font-weight: 800; color: #33691e; margin-bottom: 8px; line-height: 1.35;">
                ✅ TIN NHẮN BÌNH THƯỜNG / AN TOÀN
            </div>
            <p style="font-size: clamp(14px, 3.5vw, {base_font}px); line-height: 1.6; color: #2e7d32; margin-bottom: 10px;">
                {safe_desc}
            </p>
            <div style="background: #ffffff; padding: 10px 14px; border-radius: 8px; border-left: 4px solid #558b2f; font-size: clamp(13px, 3vw, {base_font - 2}px); color: #1e293b; line-height: 1.5;">
                💡 <b>Lưu ý bảo mật thường nhật:</b> Ngân hàng không bao giờ yêu cầu khách hàng cung cấp mật khẩu đăng nhập hay mã xác thực OTP qua điện thoại hoặc tin nhắn.
            </div>
        </div>
        """, unsafe_allow_html=True)

