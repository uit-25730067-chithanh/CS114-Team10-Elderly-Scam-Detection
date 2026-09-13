"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
PIPELINE THU THẬP & CHỨNG THỰC DỮ LIỆU LỪA ĐẢO BÙI THỊ MỶ CẨM (PHASE 01)
================================================================================
Mục đích:
  - Thu thập tập dữ liệu lừa đảo thực tế (label=1) nhắm vào 2 nhóm bẫy tâm lý:
    + Nhóm 1: Sức khỏe & Quà tặng tri ân (`health_gift`)
    + Nhóm 2: Dịch vụ công, VNeID, SIM, EVN, Ngân hàng, Phạt nguội (`public_service`)
  - TUYỆT ĐỐI TUÂN THỦ QUY TẮC ZERO SYNTHETIC TEXT (100% REAL DATA, 0% AI SINH):
    + 100% mẫu tin nhắn là dữ liệu đời thực, có nguồn gốc kiểm chứng 1-1.
    + Nguồn 1: UIT IE403 Ground Truth Smishing Dataset (duynguyenhoang22).
      Theo dõi chính xác dòng vật lý (physical line #L...) trên GitHub.
    + Nguồn 2: Vietnamese Quality-Assured SMS Dataset (IEEE Access 2026).
      Theo dõi chính xác dòng vật lý (physical line #L...) trên GitHub.
    + Nguồn 3: Trích dẫn nguyên văn (verbatim) từ các bản tin cảnh báo báo chí chính thống.
  - Phân định ranh giới rõ ràng với Hoàng Cao Sơn:
    + Loại bỏ hoàn toàn các tin nhắn Quyền lực (fear_authority) và Cấp cứu (family_emergency).
  - Ẩn danh hóa 100% PII (SĐT, STK, CCCD, OTP) qua anonymize_sms.py.
  - Chuẩn hóa 8 cột kiểm toán, loại bỏ trùng lặp (0 duplicates), kiểm tra độ dài hợp lệ.
  - Đảm bảo độc lập tuyệt đối với tập Normal của Đặng Chí Thanh (0% overlap).
  - Tự động chạy data_validation.py để xác thực chất lượng.
================================================================================
"""

from __future__ import annotations

import csv
import io
import re
import sys
import time
import urllib.error
import urllib.request
import unicodedata
from pathlib import Path
from typing import Final

import pandas as pd

# Đường dẫn tương đối
current_path = Path(__file__).resolve()
draft_dir = current_path.parent.parent.parent
sys.path.insert(0, str(draft_dir))

from data.scripts.anonymize_sms import mask_pii
from data.scripts.data_validation import validate_dataset
from src.utils.helpers import (
    CATEGORY_HEALTH_GIFT,
    CATEGORY_PUBLIC_SERVICE,
    LABEL_SCAM,
    get_data_dir,
)

COLLECTOR_NAME: Final[str] = "Bùi Thị Mỷ Cẩm"

# Biểu thức chính quy phát hiện cờ bạc / cá cược / nổ hũ / khiêu dâm / game bài
GAMBLING_ADULT_PATTERNS: Final[list[str]] = [
    r"kubet", r"casino", r"danh\s*ba[`i]?", r"lo\s*de", r"so\s*xo", r"xo\s*so", r"x0s0",
    r"no\s*hu", r"n[/\s]*o[/\s]*h[/\s]*u", r"quay\s*hu",
    r"ban\s*ca", r"ba?n'\s*ca", r"b[/\s]*a[/\s]*n[/\s]*c[/\s]*a",
    r"tai\s*xiu", r"da\s*ga", r"ca\s*cuoc", r"\bcuoc\b", r"game\s*bai", r"nohu",
    r"slot", r"nha\s*cai", r"baccarat", r"bcr", r"dat\s*cuoc", r"jili", r"8day",
    r"giaitri\d*q", r"nap\s*dau", r"na?p\s*dau", r"nap\s*lan\s*dau", r"tan\s*thu", r"hoan\s*tra", r"ho?an\s*tra",
    r"cuuthua", r"rut\s*sieu\s*toc", r"vong\s*cuoc", r"x\d\s*vong\s*cuoc",
    r"tang\s*\d+k", r"thuong\s*\d+k", r"nap\s*\d+k", r"\bli\s*xi\b",
    r"gai\s*goi", r"tinh\s*mot\s*dem", r"\bsex\b", r"show\s*hang", r"may\s*bay\s*ba\s*gia",
    r"gai\s*lam", r"lam\s*tjnh", r"lam\s*tinh"
]

# Biểu thức chính quy Quyền lực / Cấp cứu thuộc trách nhiệm của Hoàng Cao Sơn (phải loại trừ)
SON_PATTERNS: Final[list[str]] = [
    r"truy\s*na", r"canh\s*sat\s*dieu\s*tra", r"bat\s*tam\s*giam", r"lenh\s*bat",
    r"khoi\s*to", r"khoi\s*kien", r"trieu\s*tap", r"to\s*giac",
    r"vien\s*kiem\s*sat", r"toa\s*an", r"dieu\s*tra\s*hinh\s*su",
    r"tai\s*nan", r"cap\s*cuu", r"mo\s*gap", r"vien\s*phi",
    r"chiem\s*doat\s*tai\s*san", r"canh\s*bao\s*lan\s*cuoi", r"trung\s*tam\s*tin\s*dung"
]

# Biểu thức chính quy nội dung ngoài phạm vi lừa đảo tài chính (tuyên truyền, chính trị...) — phải loại trừ
OFF_TOPIC_PATTERNS: Final[list[str]] = [
    r"phap\s*luan\s*cong"
]

# Biểu thức chính quy lừa đảo Việc làm/CTV online & Đầu tư/Crypto — KHÁC bản chất với
# "quà tặng/sức khỏe" nên phải loại trừ khỏi health_gift (re-audit 13/09/2026 phát hiện
# ~34/93 mẫu health_gift cũ thực chất là 2 nhóm lừa đảo này, không phải quà tặng tri ân)
JOB_AND_INVESTMENT_PATTERNS: Final[list[str]] = [
    r"tuyen\s*dung", r"tuyen\s*ctv", r"tuyen\s*nhan\s*vien", r"cong\s*tac\s*vien", r"\bctv\b",
    r"viec\s*lam", r"viec\s*nhe", r"ban\s*thoi\s*gian", r"lam\s*viec\s*tai\s*nha",
    r"kiem\s*tien", r"kiem\s*them", r"luong\s*cung", r"hoa\s*hong", r"nhiem\s*vu",
    r"dau\s*tu", r"sinh\s*loi", r"lai\s*suat", r"\btrade\b", r"robot\s*tu\s*dong",
    r"gop\s*von", r"\bcrypto\b", r"\busdt\b", r"\bcoin\b", r"nhan\s*doi\s*tai\s*san", r"bao\s*loi"
]

# Biểu thức chính quy phân loại Sức khỏe & Quà tặng (health_gift)
# LƯU Ý: KHÔNG dùng \bqua\b / \btrung\b đơn lẻ — sau khi bỏ dấu, "quà" và "qua"
# (giới từ rất phổ biến) trùng nhau, gây fallback sai nhãn hàng loạt.
HEALTH_GIFT_PATTERNS: Final[list[str]] = [
    r"covid", r"thuoc", r"chua\s*benh", r"suc\s*khoe", r"kham\s*benh", r"benh\s*vien",
    r"trung\s*thuong", r"trung\s*tuyen", r"qua\s*tang", r"tri\s*an", r"voucher",
    r"nhan\s*qua", r"uu\s*dai", r"chuc\s*mung"
]

# Biểu thức chính quy phân loại Dịch vụ công & Viễn thông / Ngân hàng / Điện lực (public_service)
PUBLIC_SERVICE_PATTERNS: Final[list[str]] = [
    r"dich\s*vu\s*cong", r"\bdvc\b", r"vneid", r"vne-id", r"dinh\s*danh", r"can\s*cuoc", r"cccd",
    r"bao\s*hiem", r"bhxh", r"bhyt", r"b[\s/\.\-]*h[\s/\.\-]*t[\s/\.\-]*n", r"so\s*ho\s*khau", r"ho\s*khau",
    r"thue", r"cuc\s*thue", r"quyet\s*toan", r"hoan\s*thue", r"tong\s*cuc",
    r"dien\s*luc", r"\bevn\b", r"tien\s*dien", r"cat\s*dien",
    r"khoa\s*sim", r"chuan\s*hoa", r"thue\s*bao", r"nha\s*mang", r"viettel", r"vinaphone", r"mobifone",
    r"ngan\s*hang", r"vietcombank", r"bidv", r"vietinbank", r"techcombank", r"mbbank", r"mb\s*bank", r"acb",
    r"sacombank", r"vpbank", r"agribank", r"tpbank", r"shb", r"hdbank", r"msb", r"\bvcb\b",
    r"the\s*tin\s*dung", r"bien\s*dong\s*so\s*du", r"tam\s*khoa", r"khoa\s*the",
    r"smart\s*banking", r"digibank", r"\botp\b", r"ma\s*xac\s*thuc", r"phat\s*nguoi", r"giao\s*thong",
    r"giay\s*to", r"bang\s*lai", r"dang\s*ky", r"ho\s*so", r"bo\s*sung", r"loi\s*he\s*thong",
    r"dong\s*bo", r"tai\s*chinh\s*toan\s*cau", r"tieu\s*dung\s*o\s*nuoc\s*ngoai", r"phong\s*toa",
    r"gian\s*lan", r"buu\s*dien", r"luong\s*huu", r"an\s*sinh\s*xa\s*hoi", r"sinh\s*trac\s*hoc"
]
# LƯU Ý: đã bỏ pattern chung chung `tai\s*khoan` (16/09/2026) — quá rộng, nuốt nhầm
# các mẫu quà tặng thương hiệu (vd "tài khoản Shopee/Messenger của bạn được tặng...")
# vào public_service dù không hề mạo danh cơ quan/ngân hàng cụ thể nào. Các mẫu
# public_service hợp lệ vẫn được bắt qua tên ngân hàng cụ thể hoặc các pattern
# hành động/đe dọa cụ thể hơn ở trên (khóa, phong tỏa, gian lận, xác thực...).


def remove_vietnamese_accents(text: str) -> str:
    """Loại bỏ dấu tiếng Việt để đối sánh từ khóa chống lách luật spam."""
    norm = unicodedata.normalize("NFD", text)
    result = re.sub(r"[\u0300-\u036f]", "", norm)
    return result.replace("đ", "d").replace("Đ", "D").lower()


# Danh sách loại trừ CHÍNH XÁC (không dùng heuristic) cho các dòng text lỗi/không đọc
# được đã xác nhận thủ công trong nguồn IEEE Access 2026. LƯU Ý: đã thử 3 phiên bản
# heuristic tự động (độ dài token sau khi bỏ URL, đếm camelCase, đếm camelCase sau khi
# bỏ URL) — cả 3 đều gây false positive loại nhầm dữ liệu health_gift/public_service
# hợp lệ, thật (mẫu BHTN leetspeak, mẫu VPBANK nhắc "iPhone"/"512GB"/"4K" — các cụm
# hoàn toàn bình thường trong tin nhắn quà tặng/khuyến mãi thật). Vì health_gift đang
# rất khan hiếm dữ liệu, chấp nhận đánh đổi: dùng danh sách chính xác (an toàn tuyệt
# đối, không rủi ro loại nhầm) thay vì heuristic tổng quát (rủi ro cao hơn giá trị).
GARBLED_TEXT_DENYLIST: Final[set[str]] = {
    "JaKDiemDanh(phsqqgk.oerapple.com(TriAnx2NapYgroupsgooglecomul",
    "CgDOiXoiOi<mmmQqM.uszalo.me(TriAnMootTRaamNghjnYggroupsgooglecom?O",
}


def is_garbled_text(raw_text: str) -> bool:
    """Kiểm tra dòng text có nằm trong danh sách text lỗi/không đọc được đã xác nhận."""
    return raw_text.strip() in GARBLED_TEXT_DENYLIST


def classify_cam_sample(raw_text: str) -> str | None:
    """
    Phân loại nghiêm ngặt mẫu lừa đảo cho phần việc của Bùi Thị Mỷ Cẩm.
    - Loại bỏ 100% cờ bạc / cá cược / game bài / khiêu dâm.
    - Loại bỏ 100% quyền lực / cấp cứu (phần việc của Hoàng Cao Sơn).
    - Chỉ gán nhãn khi khớp đúng tín hiệu ngữ nghĩa của public_service hoặc health_gift.
    - TUYỆT ĐỐI KHÔNG FALLBACK tự tiện.
    """
    if is_garbled_text(raw_text):
        return None

    norm = remove_vietnamese_accents(raw_text)

    # 1. Loại bỏ cờ bạc & nhạy cảm
    for pattern in GAMBLING_ADULT_PATTERNS:
        if re.search(pattern, norm, re.IGNORECASE):
            return None

    # 2. Loại bỏ quyền lực & cấp cứu của Sơn
    for pattern in SON_PATTERNS:
        if re.search(pattern, norm, re.IGNORECASE):
            return None

    # 2b. Loại bỏ nội dung ngoài phạm vi lừa đảo tài chính (tuyên truyền, chính trị...)
    for pattern in OFF_TOPIC_PATTERNS:
        if re.search(pattern, norm, re.IGNORECASE):
            return None

    # 2c. Loại bỏ lừa đảo Việc làm/CTV online & Đầu tư/Crypto — khác bản chất
    # "quà tặng/sức khỏe", dù có thể vô tình chứa chữ "chúc mừng"/"ưu đãi"/"quà"
    for pattern in JOB_AND_INVESTMENT_PATTERNS:
        if re.search(pattern, norm, re.IGNORECASE):
            return None

    # 3. Phân loại chuẩn xác theo bẫy tâm lý
    is_ps = any(re.search(pattern, norm, re.IGNORECASE) for pattern in PUBLIC_SERVICE_PATTERNS)
    is_hg = any(re.search(pattern, norm, re.IGNORECASE) for pattern in HEALTH_GIFT_PATTERNS)

    if is_ps:
        return CATEGORY_PUBLIC_SERVICE
    if is_hg:
        return CATEGORY_HEALTH_GIFT

    return None


def normalize_text_for_dedup(text: str) -> str:
    """Chuẩn hóa văn bản để loại bỏ trùng lặp ngữ nghĩa."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", text.lower())).strip()


def fetch_github_raw_csv_text(url: str, timeout: int = 20, max_retries: int = 2) -> str:
    """Tải nội dung CSV từ GitHub Raw an toàn với timeout và cơ chế retry."""
    req = urllib.request.Request(url, headers={"User-Agent": "CS114-DataCollector/1.0"})
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8-sig", errors="replace")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt == max_retries:
                raise RuntimeError(f"Lỗi tải dữ liệu sau {max_retries} lần thử từ {url}: {e}")
            time.sleep(1)
    return ""


def fetch_uit_ie403_samples() -> list[dict]:
    """
    Thu thập các mẫu tin nhắn smishing đời thực từ bộ dữ liệu UIT IE403.
    Repo: duynguyenhoang22/SMS_Phishing_Detection
    Định vị chính xác dòng vật lý trên GitHub (#L...).
    """
    print("[1/3] Đang nạp dữ liệu từ UIT IE403 Ground Truth Smishing Dataset...")
    url = "https://raw.githubusercontent.com/duynguyenhoang22/SMS_Phishing_Detection/main/data/dataset_label_1.csv"
    raw_content = fetch_github_raw_csv_text(url, timeout=20)

    f = io.StringIO(raw_content)
    reader = csv.reader(f)
    next(reader)  # Header
    start_line = 2

    samples = []
    for row in reader:
        end_line = reader.line_num
        raw_text = row[0].strip() if len(row) > 0 else ""

        if len(raw_text) >= 25:
            cat = classify_cam_sample(raw_text)
            if cat is not None:
                permalink = f"https://github.com/duynguyenhoang22/SMS_Phishing_Detection/blob/main/data/dataset_label_1.csv#L{start_line}"
                samples.append({
                    "raw_text": raw_text,
                    "scam_category": cat,
                    "source": "github_uit_ie403",
                    "source_url": permalink,
                    "notes": f"UIT IE403 Ground Truth Smishing Dataset line {start_line}"
                })

        start_line = end_line + 1

    print(f"      -> Thu thập được {len(samples)} mẫu hợp lệ từ UIT IE403.")
    return samples


def fetch_verified_news_quotes() -> list[dict]:
    """
    Các mẫu trích dẫn nguyên văn (verbatim) tin nhắn lừa đảo từ báo chí chính thống.
    Được kiểm chứng 100% tồn tại nguyên văn trên trang tin bài báo.
    """
    print("[2/3] Đang nạp các mẫu trích dẫn nguyên văn từ báo chí chính thống...")
    quotes = [
        {
            "raw_text": "Chúng tôi thông báo bạn đã vi phạm luật giao thông và bị phạt số tiền 50.000 VND do đỗ xe gây cản trở. Vui lòng thanh toán khoản phạt này sớm để tránh phát sinh thêm chi phí. Để thanh toán, vui lòng làm theo hướng dẫn...",
            "scam_category": CATEGORY_PUBLIC_SERVICE,
            "source": "tuoitre.vn",
            "source_url": "https://tuoitre.vn/canh-bao-chieu-lua-phat-nguoi-50-000-vnd-qua-website-gia-dich-vu-cong-de-chiem-the-ngan-hang-20260427145237114.htm",
            "notes": "Báo Tuổi Trẻ trích dẫn nguyên văn tin nhắn phạt nguội giả mạo dịch vụ công"
        },
        {
            "raw_text": "HUIT - Chúc mừng bạn đã trúng tuyển chính thức! Mời bạn đến HUIT nhập học từ ngày 18-8 đến 17h ngày 27-8-2024. Đồng thời, HUIT tặng ngay ưu đãi 3 triệu đồng dành cho 2.000 thí sinh nhập học sớm nhất. Tra cứu kết quả tại: huit.edu.vn/kqtt.",
            "scam_category": CATEGORY_HEALTH_GIFT,
            "source": "tuoitre.vn",
            "source_url": "https://tuoitre.vn/truong-dai-hoc-kinh-te-tai-chinh-tphcm-de-nghi-cong-an-xu-ly-tin-nhan-lua-dao-nhap-hoc-2024082508243626.htm",
            "notes": "Báo Tuổi Trẻ trích dẫn tin nhắn mạo danh trường đại học tặng ưu đãi nhập học"
        }
    ]
    print(f"      -> Nạp được {len(quotes)} mẫu kiểm chứng từ báo chí.")
    return quotes


def fetch_ieee_access_samples(limit: int = 450) -> list[dict]:
    """
    Thu thập các mẫu tin nhắn lừa đảo từ Vietnamese Quality-Assured SMS Dataset (IEEE Access 2026).
    Repo: trannguyenthaituan251209/vietnamese_sms_dataset
    Định vị chính xác dòng vật lý trên GitHub (#L...).
    """
    print(f"[3/3] Đang nạp dữ liệu từ IEEE Access 2026 (giới hạn ngạch ~{limit} mẫu)...")
    url = "https://raw.githubusercontent.com/trannguyenthaituan251209/vietnamese_sms_dataset/main/full_dataset.csv"
    raw_content = fetch_github_raw_csv_text(url, timeout=20)

    f = io.StringIO(raw_content)
    reader = csv.reader(f)
    next(reader)  # Header
    start_line = 2

    samples = []
    for row in reader:
        end_line = reader.line_num
        if len(row) > 3 and row[3].strip() == "1":
            raw_text = row[2].strip()
            if len(raw_text) >= 25:
                cat = classify_cam_sample(raw_text)
                if cat is not None:
                    permalink = f"https://github.com/trannguyenthaituan251209/vietnamese_sms_dataset/blob/main/full_dataset.csv#L{start_line}"
                    samples.append({
                        "raw_text": raw_text,
                        "scam_category": cat,
                        "source": "github_ieee_access_2026",
                        "source_url": permalink,
                        "notes": f"IEEE Access 2026 Vietnamese SMS Dataset line {start_line}"
                    })

                    if len(samples) >= limit:
                        break

        start_line = end_line + 1

    print(f"      -> Thu thập được {len(samples)} mẫu hợp lệ từ IEEE Access 2026.")
    return samples


def build_and_validate_cam_dataset() -> pd.DataFrame:
    """Tổng hợp toàn bộ dữ liệu thực tế, lọc trùng, che PII và xuất file staging."""
    print("=" * 60)
    print("BẮT ĐẦU QUY TRÌNH TỔNG HỢP DỮ LIỆU BÙI THỊ MỶ CẨM (100% REAL)")
    print("=" * 60)
    
    # 1. Thu thập từ các nguồn
    uit_samples = fetch_uit_ie403_samples()
    news_samples = fetch_verified_news_quotes()
    ieee_samples = fetch_ieee_access_samples(limit=450)
    
    all_candidates = uit_samples + news_samples + ieee_samples
    
    # 2. Đọc tập Normal của Thanh để kiểm tra chống rò rỉ / va chạm nhãn
    thanh_normal_file = draft_dir / "data" / "raw" / "dataset.csv"
    thanh_normal_texts = set()
    if thanh_normal_file.exists():
        df_normal = pd.read_csv(thanh_normal_file)
        thanh_normal_texts = set(df_normal["text"].dropna().apply(normalize_text_for_dedup))
        print(f"[*] Đã tải {len(thanh_normal_texts)} văn bản bình thường của Đặng Chí Thanh để đối chiếu.")
    
    # 3. Ẩn danh hóa PII, loại trùng lặp và xác thực độ dài
    final_records = []
    seen_texts = set()
    collision_count = 0
    
    for item in all_candidates:
        masked = mask_pii(item["raw_text"])
        if len(masked) < 25 or len(masked) > 600:
            continue
            
        norm = normalize_text_for_dedup(masked)
        
        # Kiểm tra không trùng với chính nó
        if norm in seen_texts:
            continue
            
        # Kiểm tra không va chạm với tập Normal của Thanh
        if norm in thanh_normal_texts:
            collision_count += 1
            continue
            
        seen_texts.add(norm)
        final_records.append({
            "text": masked,
            "label": LABEL_SCAM,
            "scam_category": item["scam_category"],
            "source": item["source"],
            "source_url": item["source_url"],
            "collector_name": COLLECTOR_NAME,
            "notes": item["notes"]
        })
        
        # Đạt ngưỡng an toàn ~530 mẫu
        if len(final_records) >= 530:
            break
            
    print(f"[*] Tổng số mẫu sau lọc trùng và PII: {len(final_records)} mẫu (loại {collision_count} mẫu va chạm normal).")
    
    # 4. Gán id từ 1..N
    df_result = pd.DataFrame(final_records)
    df_result.insert(0, "id", range(1, len(df_result) + 1))
    
    # Sắp xếp đúng 8 cột kiểm toán chuẩn
    columns = ["id", "text", "label", "scam_category", "source", "source_url", "collector_name", "notes"]
    df_result = df_result[columns]
    
    # 5. Xuất file staging_cam_scam.csv
    out_dir = draft_dir / "data" / "raw"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "staging_cam_scam.csv"
    
    df_result.to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"[+] Đã xuất file: {out_file}")
    
    # 6. Kiểm định chất lượng qua data_validation.py
    print("\n" + "=" * 60)
    print("CHẠY KIỂM ĐỊNH TỰ ĐỘNG (data_validation.py)")
    print("=" * 60)
    is_valid, errors = validate_dataset(out_file, verbose=True)
    
    if is_valid:
        print("\n✅ KIỂM ĐỊNH HOÀN TOÀN THÀNH CÔNG (PASSED 100%)!")
    else:
        print(f"\n❌ KIỂM ĐỊNH THẤT BẠI VỚI {len(errors)} LỖI:")
        for err in errors:
            print(f"  - {err}")
            
    return df_result


if __name__ == "__main__":
    build_and_validate_cam_dataset()
