"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
CÔNG CỤ ẨN DANH HÓA THÔNG TIN CÁ NHÂN (PII ANONYMIZER) CHO TIN NHẮN SMS
================================================================================
Mục đích:
  - Tự động phát hiện và che giấu (mask) các thông tin nhạy cảm riêng tư (PII - Personally
    Identifiable Information) như: Số điện thoại cá nhân, Số tài khoản ngân hàng,
    Mã OTP bí mật, Số CCCD/CMND, Tên riêng... trong các tin nhắn SMS đời thực.
  - Chuẩn hóa dữ liệu tin nhắn bình thường (label=0, none) hoặc tin nhắn gia đình trước
    khi nạp vào Google Sheet nhóm và dataset huấn luyện.
  - Định dạng sẵn 8 cột kiểm toán chuẩn:
    id | text | label | scam_category | source | source_url | collector_name | notes

Hướng dẫn sử dụng cho thành viên trong nhóm:
  1. Xử lý trực tiếp từ chuỗi tin nhắn qua dòng lệnh:
     python3 anonymize_sms.py --text "Vietcombank: So du TK 0123456789 thay doi -200,000 VND. OTP: 982134"
  2. Xử lý hàng loạt từ tệp văn bản (mỗi tin nhắn 1 dòng):
     python3 anonymize_sms.py --input raw_sms.txt --output staging_normal.csv --source "bank_sms" --evidence "https://drive.google.com/..."
================================================================================
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Final

import pandas as pd

# Đường dẫn tương đối tìm về thư mục gốc làm việc draft/scam-detection
current_path = Path(__file__).resolve()
for parent in [current_path.parent, current_path.parent.parent, current_path.parent.parent.parent]:
    if (parent / "src" / "utils" / "helpers.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from src.utils.helpers import CATEGORY_NONE, LABEL_NORMAL, get_data_dir

# ─── Các biểu thức chính quy (Regex) phát hiện PII tiếng Việt ───────────────────
REGEX_OTP: Final[re.Pattern] = re.compile(
    r"(?:(?:m[aã]\s+)?otp(?:\s+(?:x[aá]c\s+th[uự]c|x[aá]c\s+nh[aậ]n)(?:\s+gd)?)?|m[aã]\s+(?:x[aá]c\s+th[uự]c|x[aá]c\s+nh[aậ]n|b[aả]o\s+m[aậ]t|giao\s+d[iị]ch))(?:\s+(?:c[uủ]a\s+b[aạ]n\s+)?(?:l[aà]|:))?[:\s]+([0-9]{4,8})\b",
    re.IGNORECASE,
)
REGEX_PHONE: Final[re.Pattern] = re.compile(
    r"(?:\+84|84|0)(?:3[2-9]|5[25689]|7[06-9]|8[1-9]|9[0-9])[0-9]{7}\b"
)
REGEX_BANK_ACCOUNT: Final[re.Pattern] = re.compile(
    r"(?:t[aà]i\s+kho[aả]n(?:\s+ngu[oồ]n|\s+[đd][ií]ch)?|s[oố]\s+tk|stk|\btk|account)[:\s#]*([0-9]{8,16})\b",
    re.IGNORECASE,
)
REGEX_CCCD: Final[re.Pattern] = re.compile(
    r"(?:cccd|cmnd|[đd][iị]nh\s+danh|c[aă]n\s+c[uư][oớ]c)[:\s]*([0-9]{9,12})\b",
    re.IGNORECASE,
)
REGEX_TRANSACTION_ID: Final[re.Pattern] = re.compile(
    r"(?:mã\s+gd|magd|mgd|ref(?:\s+no)?|số\s+gd)[:\s]*([A-Za-z0-9]{8,20})\b",
    re.IGNORECASE,
)

# ─── Che họ tên riêng (nạn nhân / người được nêu tên trong tin nhắn) ────────────
_VN_UPPER: Final[str] = "A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ"
_VN_LOWER: Final[str] = "a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
_VN_SURNAMES: Final[list[str]] = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
    "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đinh", "Tạ", "Đoàn", "Vương",
]
_VN_SURNAMES_CAPS: Final[list[str]] = [
    "NGUYEN", "TRAN", "PHAM", "HOANG", "HUYNH", "PHAN", "VU", "VO", "DANG",
    "BUI", "DO", "HO", "NGO", "DUONG", "LY", "DINH", "TA", "DOAN", "VUONG",
]

REGEX_FULL_NAME_TITLE: Final[re.Pattern] = re.compile(
    r"\b(?:" + "|".join(_VN_SURNAMES) + r")"
    r"(?!\s+Chí\s+Minh)"  # tránh nhầm địa danh "Hồ Chí Minh" thành họ tên người
    rf"(?:\s+[{_VN_UPPER}][{_VN_LOWER}]+){{1,3}}\b"
)
REGEX_FULL_NAME_CAPS: Final[re.Pattern] = re.compile(
    r"\b(?:" + "|".join(_VN_SURNAMES_CAPS) + r")"
    rf"(?:\s+[{_VN_UPPER}]{{2,}}){{2,3}}\b"
)

# ─── Bắt lưới cuối: mọi dãy số dài còn sót (STK/mã HĐ/mã GD chưa khớp rule trên) ─
REGEX_GENERIC_LONG_DIGITS: Final[re.Pattern] = re.compile(r"\b\d{8,}\b")


def mask_pii(text: str) -> str:
    """
    Thay thế các thông tin nhạy cảm (PII) bằng các token chuẩn hóa.
    Giúp bảo vệ quyền riêng tư gia đình và bảo đảm tính khái quát của mô hình Machine Learning.
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    result = text.strip()

    # 1. Ẩn mã OTP
    result = REGEX_OTP.sub(r"Mã OTP là [MÃ_OTP]", result)

    # 2. Ẩn số tài khoản ngân hàng
    result = REGEX_BANK_ACCOUNT.sub(r"TK [SỐ_TÀI_KHOẢN]", result)

    # 3. Ẩn mã định danh cá nhân / CCCD
    result = REGEX_CCCD.sub(r"CCCD [SỐ_CCCD]", result)

    # 4. Ẩn mã giao dịch ngân hàng
    result = REGEX_TRANSACTION_ID.sub(r"Mã GD [MÃ_GIAO_DỊCH]", result)

    # 5. Ẩn số điện thoại liên lạc cá nhân
    result = REGEX_PHONE.sub(r"[SỐ_ĐIỆN_THOẠI]", result)

    # 6. Ẩn họ tên riêng (thường/hoa) xuất hiện trong tin nhắn
    result = REGEX_FULL_NAME_TITLE.sub("[HỌ_VÀ_TÊN]", result)
    result = REGEX_FULL_NAME_CAPS.sub("[HỌ_VÀ_TÊN]", result)

    # 7. Bắt lưới cuối: dãy số dài còn sót chưa khớp các rule PII cụ thể ở trên
    result = REGEX_GENERIC_LONG_DIGITS.sub("[SỐ_ĐỊNH_DANH]", result)

    # 8. Chuẩn hóa khoảng trắng dư thừa
    result = re.sub(r"\s+", " ", result).strip()

    return result


def process_raw_lines(
    lines: list[str],
    source_type: str = "telecom_bank_sms",
    source_url: str = "",
    collector_name: str = "Đặng Chí Thanh",
    notes: str = "Tin nhắn bình thường đời thực đã ẩn danh hóa PII",
) -> list[dict]:
    """Chuyển danh sách tin nhắn thô thành danh sách bản ghi chuẩn 8 cột."""
    records = []
    for line in lines:
        cleaned = mask_pii(line)
        if len(cleaned) < 15:
            continue  # Bỏ qua các chuỗi quá ngắn, rác

        records.append({
            "text": cleaned,
            "label": LABEL_NORMAL,
            "scam_category": CATEGORY_NONE,
            "source": source_type,
            "source_url": source_url,
            "collector_name": collector_name,
            "notes": notes,
        })
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Công cụ che giấu PII cho tin nhắn SMS CS114")
    parser.add_argument("--text", type=str, help="Chuỗi tin nhắn cần ẩn danh PII trực tiếp")
    parser.add_argument("--input", type=str, help="Đường dẫn file .txt chứa các tin nhắn thô (1 dòng / tin)")
    parser.add_argument("--output", type=str, default=None, help="Đường dẫn file CSV xuất ra")
    parser.add_argument("--source", type=str, default="telecom_bank_sms", help="Loại nguồn: telecom_bank_sms, family_sms, utility_sms")
    parser.add_argument("--evidence", type=str, default="", help="Link ảnh Google Drive minh chứng (source_url)")
    parser.add_argument("--collector", type=str, default="Đặng Chí Thanh", help="Tên người thu thập")

    args = parser.parse_args()

    if args.text:
        masked = mask_pii(args.text)
        print("\n" + "=" * 60)
        print("KẾT QUẢ ẨN DANH HÓA PII:")
        print("-" * 60)
        print(f"Gốc:   {args.text}")
        print(f"Đã xử lý: {masked}")
        print("=" * 60 + "\n")
        return

    if args.input:
        in_file = Path(args.input)
        if not in_file.exists():
            print(f"[!] Không tìm thấy file: {in_file}")
            sys.exit(1)

        raw_lines = [
            line.strip()
            for line in in_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]

        records = process_raw_lines(
            raw_lines,
            source_type=args.source,
            source_url=args.evidence,
            collector_name=args.collector,
        )

        df = pd.DataFrame(records)
        df.insert(0, "id", range(1, len(df) + 1))

        out_path = Path(args.output) if args.output else get_data_dir() / "raw" / "staging_normal_cleaned.csv"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False, encoding="utf-8-sig")

        print(f"[+] Đã xử lý thành công {len(df)} tin nhắn bình thường!")
        print(f"[+] Dữ liệu đã lưu tại: {out_path}")
        print("[+] Bạn có thể kiểm tra và copy các dòng này nạp vào Google Sheet nhóm.")
        return

    print("[*] Vui lòng truyền --text 'nội dung' hoặc --input <file_chua_sms.txt>.")
    print("[*] Ví dụ: python3 anonymize_sms.py --text 'Tai khoan 0123456789 bi tru 50k'")


if __name__ == "__main__":
    main()
