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



def render_safety_advisor(category: str, is_scam: bool, font_multiplier: float = 1.0) -> None:
    """Hiển thị bảng khuyến cáo an toàn thiết kế dành riêng cho người cao tuổi."""
    info = TRAP_DEFINITIONS.get(category, TRAP_DEFINITIONS["none"])
    base_font = int(18 * font_multiplier)
    title_font = int(22 * font_multiplier)

    if is_scam:
        st.markdown(f"""
        <div style="
            background-color: #fff9f9;
            border-left: 6px solid {info['color']};
            border-radius: 12px;
            padding: 20px;
            margin: 16px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        ">
            <div style="font-size: {title_font}px; font-weight: 800; color: {info['color']}; margin-bottom: 10px;">
                {info['title']}
            </div>
            <p style="font-size: {base_font}px; line-height: 1.6; color: #333333; margin-bottom: 16px;">
                <b>Dấu hiệu nhận biết:</b> {info['description']}
            </p>
            <div style="font-size: {base_font}px; font-weight: 700; color: #c0392b; margin-bottom: 8px;">
                ⚠️ Lời khuyên quan trọng dành cho Ông/Bà:
            </div>
            <ul style="font-size: {base_font}px; line-height: 1.7; color: #2c3e50; margin: 0; padding-left: 24px;">
                {"".join(f'<li style="margin-bottom: 8px;">{tip}</li>' for tip in info['warning_tips'])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Hộp nguyên tắc "3 KHÔNG & 1 GỌI"
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fce4ec 0%, #fff3e0 100%);
            border: 3px solid #ff7043;
            border-radius: 16px;
            padding: 22px;
            margin-top: 18px;
        ">
            <div style="font-size: {title_font}px; font-weight: 900; color: #d84315; text-align: center; margin-bottom: 14px;">
                🛡️ QUY TẮC AN TOÀN "3 KHÔNG & 1 GỌI" CHO NGƯỜI CAO TUỔI
            </div>
            <div style="display: grid; grid-template-columns: 1fr; gap: 10px; font-size: {base_font}px;">
                <div style="background: #ffffff; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #e53935;">
                    ❌ <b>1. KHÔNG bấm vào đường link lạ:</b> Kẻ xấu có thể cài mã độc để trộm sạch tiền ngân hàng.
                </div>
                <div style="background: #ffffff; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #e53935;">
                    ❌ <b>2. KHÔNG cung cấp mật khẩu, mã OTP:</b> Nhân viên ngân hàng và Công an không bao giờ hỏi mật khẩu.
                </div>
                <div style="background: #ffffff; padding: 12px 16px; border-radius: 10px; border-left: 4px solid #e53935;">
                    ❌ <b>3. KHÔNG chuyển tiền trong lúc hoảng sợ:</b> Càng bị hối thúc dọa dẫm thì càng phải bình tĩnh dừng lại.
                </div>
                <div style="background: #e8f5e9; padding: 14px 18px; border-radius: 10px; border-left: 6px solid #2e7d32; font-weight: 700; color: #1b5e20;">
                    📞 <b>BƯỚC DUY NHẤT CẦN LÀM:</b> GỌI NGAY CHO CON CHÁU hoặc gọi đường dây nóng miễn phí:
                    <div style="font-size: {int(26*font_multiplier)}px; color: #c62828; margin-top: 6px; font-weight: 900;">
                        ☎️ TỔNG ĐÀI CỤC AN TOÀN THÔNG TIN: 156 (Miễn phí)
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div style="
            background-color: #f1f8e9;
            border-left: 6px solid #558b2f;
            border-radius: 12px;
            padding: 20px;
            margin: 16px 0;
        ">
            <div style="font-size: {title_font}px; font-weight: 800; color: #33691e; margin-bottom: 10px;">
                {info['title']}
            </div>
            <p style="font-size: {base_font}px; line-height: 1.6; color: #2e7d32;">
                Hệ thống xác nhận đây là tin nhắn bình thường. Tuy vậy, Ông/Bà vẫn luôn nhớ <b>không bao giờ gửi mã OTP ngân hàng</b> cho bất kỳ ai nhé!
            </p>
        </div>
        """, unsafe_allow_html=True)
