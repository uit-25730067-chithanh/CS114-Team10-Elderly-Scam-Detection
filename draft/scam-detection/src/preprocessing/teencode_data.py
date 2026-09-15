"""Curated dictionary of Vietnamese SMS teencode, slang, and abbreviations."""

from __future__ import annotations

# Over 170+ curated Vietnamese mappings based on the 2,193 raw corpus samples
TEENCODE_DICT: dict[str, str] = {
    # Pronouns, Slang & Daily Communication
    "ko": "không", "k": "không", "kh": "không", "khg": "không", "hok": "không",
    "hông": "không", "hổng": "không", "dc": "được", "đc": "được", "ng": "người",
    "ngừoi": "người", "vs": "với", "mk": "mình", "mik": "mình", "mềnh": "mình",
    "bn": "bạn", "mn": "mọi người", "r": "rồi", "ch": "chưa", "bt": "bình thường",
    "tks": "cảm ơn", "ty": "cảm ơn", "thks": "cảm ơn", "thanks": "cảm ơn",
    "nhug": "nhưng", "nha": "nha", "nhe": "nhé", "nhé": "nhé", "cx": "cũng",
    "đag": "đang", "dag": "đang", "tg": "thời gian", "h": "giờ", "p": "phút",
    "đk": "đăng ký", "dk": "đăng ký", "uk": "ừ", "uh": "ừ", "uhm": "ừ", "um": "ừ",
    "ok": "đồng ý", "oke": "đồng ý", "okie": "đồng ý", "oki": "đồng ý",
    "bít": "biết", "bik": "biết", "lun": "luôn", "luon": "luôn", "thui": "thôi",
    "wa": "quá", "z": "vậy", "thía": "thế", "ntn": "như thế nào", "j": "gì",
    "ae": "anh em", "vk": "vợ", "ox": "ông xã", "bx": "bà xã", "gđ": "gia đình", "cv": "công việc",
    # Interaction & Social Media
    "ib": "nhắn tin", "inbox": "nhắn tin", "rep": "trả lời", "tl": "trả lời",
    "nt": "nhắn tin", "kb": "kết bạn", "dt": "điện thoại", "đt": "điện thoại",
    "sdt": "số điện thoại", "sđt": "số điện thoại", "fb": "facebook", "zalo": "zalo",
    "mess": "nhắn tin", "call": "gọi điện", "sn": "sinh năm", "ns": "nói",
    "nsx": "ngày sản xuất", "hsd": "hạn sử dụng", "bl": "bình luận", "share": "chia sẻ",
    "link": "đường dẫn", "web": "trang mạng",
    # Telecom, Service & SMS Spam Patterns
    "tb": "thông báo", "qc": "quảng cáo", "lh": "liên hệ", "soan": "soạn",
    "qk": "quý khách", "kh": "khách hàng", "tt": "thông tin", "yc": "yêu cầu",
    "km": "khuyến mại", "cuoc": "cước", "goi": "gói", "dv": "dịch vụ",
    "hd": "hợp đồng", "hđ": "hợp đồng", "nv": "nhân viên", "cs": "chăm sóc",
    "cskh": "chăm sóc khách hàng", "gprs": "mạng di động", "sim": "thẻ sim",
    "cty": "công ty", "vp": "văn phòng", "hcm": "hồ chí minh", "hn": "hà nội", "dn": "đà nẵng",
    # Financial, Transaction & Banking
    "ck": "chuyển khoản", "tk": "tài khoản", "stk": "số tài khoản", "acc": "tài khoản",
    "pass": "mật khẩu", "nh": "ngân hàng", "atm": "thẻ ngân hàng", "otp": "mã xác thực",
    "vnd": "đồng", "vnđ": "đồng", "tr": "triệu", "ngàn": "nghìn", "k": "nghìn",
    "usd": "đô la", "gd": "giao dịch", "sodu": "số dư", "tien": "tiền", "khoan": "khoản",
    "vay": "khoản vay", "tinchap": "tín chấp", "the": "thẻ",
    # Authority, Police, Public Administration & Healthcare
    "ca": "công an", "cand": "công an nhân dân", "csgt": "cảnh sát giao thông",
    "cstt": "cảnh sát trật tự", "vks": "viện kiểm sát", "vksnd": "viện kiểm sát nhân dân",
    "ta": "tòa án", "tand": "tòa án nhân dân", "ubnd": "ủy ban nhân dân",
    "bca": "bộ công an", "byt": "bộ y tế", "bkhcn": "bộ khoa học và công nghệ",
    "bhtn": "bảo hiểm thất nghiệp", "bhxh": "bảo hiểm xã hội", "bhyt": "bảo hiểm y tế",
    "bhnt": "bảo hiểm nhân thọ", "bv": "bệnh viện", "bsy": "bác sĩ", "bs": "bác sĩ",
    "bnt": "bệnh nhân", "cc": "cấp cứu", "hstc": "hồi sức tích cực", "vneid": "vneid",
    "cmnd": "chứng minh nhân dân", "cccd": "căn cước công dân", "gplx": "giấy phép lái xe",
    "nq": "nghị quyết", "pl": "pháp luật",
    # Vietnamese Banks
    "vcb": "vietcombank", "tcb": "techcombank", "bidv": "bidv", "ctg": "vietinbank",
    "acb": "acb", "mb": "mbbank", "vpb": "vpbank", "tpb": "tpbank", "shb": "shb",
    "hdb": "hdbank", "vib": "vib", "msb": "msb", "ocb": "ocb", "scb": "scb",
    "agri": "agribank", "agribank": "agribank",
}
