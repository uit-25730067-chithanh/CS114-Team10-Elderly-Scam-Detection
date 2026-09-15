"""Centralized dictionary of Vietnamese SMS teencode, scam leet-speak patterns, and compound mappings."""

from __future__ import annotations

# Curated dictionary of Vietnamese SMS teencode, slang, and administrative abbreviations.
# Ambiguous unaccented single words (e.g. 'cuoc', 'goi', 'the', 'vay', 'ty') are intentionally
# excluded to prevent semantic distortion (over-normalization); they are handled as compound phrases.
TEENCODE_DICT: dict[str, str] = {
    # Pronouns, Slang & Daily Communication
    "ko": "không", "k": "không", "kh": "không", "khg": "không", "hok": "không",
    "hông": "không", "hổng": "không", "dc": "được", "đc": "được", "ng": "người",
    "ngừoi": "người", "vs": "với", "mk": "mình", "mik": "mình", "mềnh": "mình",
    "bn": "bạn", "mn": "mọi người", "r": "rồi", "ch": "chưa", "bt": "bình thường",
    "tks": "cảm ơn", "thks": "cảm ơn", "thanks": "cảm ơn", "nhug": "nhưng",
    "nha": "nha", "nhe": "nhé", "nhé": "nhé", "cx": "cũng",
    "đag": "đang", "dag": "đang", "tg": "thời gian",
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
    "qk": "quý khách", "tt": "thông tin", "yc": "yêu cầu",
    "km": "khuyến mại", "dv": "dịch vụ",
    "hd": "hợp đồng", "hđ": "hợp đồng", "nv": "nhân viên", "cs": "chăm sóc",
    "cskh": "chăm sóc khách hàng", "gprs": "mạng di động", "sim": "thẻ sim",
    "cty": "công ty", "vp": "văn phòng", "hcm": "hồ chí minh", "hn": "hà nội", "dn": "đà nẵng",
    # Financial, Transaction & Banking
    "ck": "chuyển khoản", "tk": "tài khoản", "stk": "số tài khoản", "acc": "tài khoản",
    "pass": "mật khẩu", "nh": "ngân hàng", "atm": "thẻ ngân hàng", "otp": "mã xác thực",
    "vnd": "đồng", "vnđ": "đồng", "tr": "triệu", "ngàn": "nghìn",
    "usd": "đô la", "gd": "giao dịch", "sodu": "số dư", "tinchap": "tín chấp",
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
    # Vietnamese Commercial Banks
    "vcb": "vietcombank", "tcb": "techcombank", "bidv": "bidv", "ctg": "vietinbank",
    "acb": "acb", "mb": "mbbank", "vpb": "vpbank", "tpb": "tpbank", "shb": "shb",
    "hdb": "hdbank", "vib": "vib", "msb": "msb", "ocb": "ocb", "scb": "scb",
    "agri": "agribank", "agribank": "agribank",
}

# Regex replacement patterns for deliberate scam de-obfuscation (Leet-Speak)
LEET_SPEAK_PATTERNS: list[tuple[str, str]] = [
    (r"\bth0ng\s*ba0\b", "thông báo"),
    (r"\bth0ng\b", "thông"),
    (r"\bba0\b", "báo"),
    (r"\bkh0ng\b", "không"),
    (r"\bkh0a\b", "khóa"),
    (r"\bl0ng\b", "lòng"),
    (r"\bd[!1]eu['\s]*k[!1]en\b", "điều kiện"),
    (r"\bt[!1]en\b", "tiền"),
    (r"\bh0\s*tro\b", "hỗ trợ"),
    (r"\bb[/-]?h[/-]?t[/-]?n\b", "bảo hiểm thất nghiệp"),
    (r"\bc0ng\s*an\b", "công an"),
    (r"\bqua['\s\-_]*han\b", "quá hạn"),
    (r"\bbam['\s\-_]*vao\b", "bấm vào"),
    (r"\bde['\s\-_]*lay\b", "để lấy"),
    (r"\bdu0c\b", "được"),
    (r"\bqui\s*kh\b", "quý khách"),
    (r"\bkhach\s*hang\b", "khách hàng"),
    (r"\btuyetdjnh\b", "tuyệt đỉnh"),
    (r"\bdacbjet\b", "đặc biệt"),
    (r"\btang\s*rjeng\b", "tặng riêng"),
    (r"\bkmaj\b", "khuyến mại"),
    (r"\bqualixj\b", "quà lì xì"),
]

# Important unaccented compound phrases to join for the 45% unaccented samples
UNACCENTED_COMPOUNDS: dict[str, str] = {
    # Telecommunications & Call Center
    "goi cuoc": "goi_cuoc",
    "cuoc goi": "cuoc_goi",
    "cuoc phi": "cuoc_phi",
    "gia cuoc": "gia_cuoc",
    "cuoc song": "cuoc_song",
    "tong dai": "tong_dai",
    "so dien thoai": "so_dien_thoai",
    "dien thoai": "dien_thoai",
    # Police & Legal Actions
    "vao cuoc": "vao_cuoc",
    "cong an": "cong_an",
    "canh sat": "canh_sat",
    "truy na": "truy_na",
    "bat giam": "bat_giam",
    "phong toa": "phong_toa",
    "tam khoa": "tam_khoa",
    "can cuoc": "can_cuoc",
    # Banking & Finance
    "tai khoan": "tai_khoan",
    "so tai khoan": "so_tai_khoan",
    "chuyen khoan": "chuyen_khoan",
    "chuyen tien": "chuyen_tien",
    "nhan tien": "nhan_tien",
    "so tien": "so_tien",
    "nop tien": "nop_tien",
    "ung tien": "ung_tien",
    "khoan vay": "khoan_vay",
    "vay von": "vay_von",
    "the tin dung": "the_tin_dung",
    "the atm": "the_atm",
    "the sim": "the_sim",
    "ngan hang": "ngan_hang",
    "mat khau": "mat_khau",
    "xac thuc": "xac_thuc",
    "qua han": "qua_han",
    # Emergency & Healthcare
    "cap cuu": "cap_cuu",
    "tai nan": "tai_nan",
    "benh vien": "benh_vien",
    "vien phi": "vien_phi",
    # Social Welfare & Promotion
    "bao hiem": "bao_hiem",
    "that nghiep": "that_nghiep",
    "xa hoi": "xa_hoi",
    "y te": "y_te",
    "dieu kien": "dieu_kien",
    "ho tro": "ho_tro",
    "trung thuong": "trung_thuong",
    "tri an": "tri_an",
    "mien phi": "mien_phi",
    "tang qua": "tang_qua",
    "quy khach": "quy_khach",
    "thong bao": "thong_bao",
    "lien he": "lien_he",
}

__all__ = [
    "TEENCODE_DICT",
    "LEET_SPEAK_PATTERNS",
    "UNACCENTED_COMPOUNDS",
]
