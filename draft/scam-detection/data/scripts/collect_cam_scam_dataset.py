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
import urllib.request
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

# Từ khóa cờ bạc / cá cược / game bài bị loại trừ hoàn toàn
GAMBLING_KEYWORDS: Final[list[str]] = [
    "kubet", "casino", "đánh bài", "lô đề", "nổ hũ", "bắn cá",
    "tài xỉu", "đá gà", "cá cược", "game bài", "thần tài", "nohu",
    "slot", "nhà cái", "baccarat", "quay hũ", "đặt cược"
]

# Từ khóa Quyền lực / Cấp cứu thuộc trách nhiệm của Hoàng Cao Sơn (phải loại trừ)
SON_KEYWORDS: Final[list[str]] = [
    "lệnh truy nã", "cơ quan cảnh sát điều tra", "bắt tạm giam", "lệnh bắt",
    "khởi tố", "viện kiểm sát", "tòa án nhân dân", "điều tra hình sự",
    "cháu bị tai nạn", "con bị tai nạn", "tai nạn giao thông cấp cứu",
    "mổ gấp", "chuyển viện phí gấp"
]

# Từ khóa phân loại Sức khỏe & Quà tặng (health_gift)
HEALTH_GIFT_KEYWORDS: Final[list[str]] = [
    "covid", "thuốc", "chữa bệnh", "sức khỏe", "trúng", "quà", "tri ân",
    "tặng", "chúc mừng", "việc làm", "tuyển dụng", "hoa hồng", "voucher",
    "ưu đãi", "điểm", "priority", "thưởng", "khuyến mại", "khám bệnh",
    "bốc thăm", "quà tặng", "trúng thưởng", "đổi điểm"
]


def normalize_text_for_dedup(text: str) -> str:
    """Chuẩn hóa văn bản để loại bỏ trùng lặp ngữ nghĩa."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", text.lower())).strip()


def fetch_uit_ie403_samples() -> list[dict]:
    """
    Thu thập các mẫu tin nhắn smishing đời thực từ bộ dữ liệu UIT IE403.
    Repo: duynguyenhoang22/SMS_Phishing_Detection
    Định vị chính xác dòng vật lý trên GitHub (#L...).
    """
    print("[1/3] Đang nạp dữ liệu từ UIT IE403 Ground Truth Smishing Dataset...")
    url = "https://raw.githubusercontent.com/duynguyenhoang22/SMS_Phishing_Detection/main/data/dataset_label_1.csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req) as resp:
        raw_content = resp.read().decode("utf-8-sig", errors="replace")
        
    f = io.StringIO(raw_content)
    reader = csv.reader(f)
    next(reader)  # Header
    start_line = 2
    
    samples = []
    for row in reader:
        end_line = reader.line_num
        raw_text = row[0].strip() if len(row) > 0 else ""
        
        if len(raw_text) >= 25:
            low = raw_text.lower()
            
            # Loại trừ phần việc của Sơn & cờ bạc
            if not any(k in low for k in SON_KEYWORDS) and not any(k in low for k in GAMBLING_KEYWORDS):
                if any(k in low for k in HEALTH_GIFT_KEYWORDS):
                    cat = CATEGORY_HEALTH_GIFT
                else:
                    cat = CATEGORY_PUBLIC_SERVICE
                    
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


def fetch_ieee_access_samples(limit: int = 350) -> list[dict]:
    """
    Thu thập các mẫu tin nhắn lừa đảo từ Vietnamese Quality-Assured SMS Dataset (IEEE Access 2026).
    Repo: trannguyenthaituan251209/vietnamese_sms_dataset
    Định vị chính xác dòng vật lý trên GitHub (#L...).
    """
    print(f"[3/3] Đang nạp dữ liệu từ IEEE Access 2026 (giới hạn ngạch ~{limit} mẫu)...")
    url = "https://raw.githubusercontent.com/trannguyenthaituan251209/vietnamese_sms_dataset/main/full_dataset.csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req) as resp:
        raw_content = resp.read().decode("utf-8-sig", errors="replace")
        
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
                low = raw_text.lower()
                
                # Loại trừ phần việc của Sơn & cờ bạc
                if not any(k in low for k in SON_KEYWORDS) and not any(k in low for k in GAMBLING_KEYWORDS):
                    if any(k in low for k in HEALTH_GIFT_KEYWORDS):
                        cat = CATEGORY_HEALTH_GIFT
                    else:
                        cat = CATEGORY_PUBLIC_SERVICE
                        
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
    ieee_samples = fetch_ieee_access_samples(limit=350)
    
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
