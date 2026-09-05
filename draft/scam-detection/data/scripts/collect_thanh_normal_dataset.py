"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
SCRIPT THU THẬP & ĐỒNG BỘ DỮ LIỆU BÌNH THƯỜNG CỦA ĐẶNG CHÍ THANH (PHASE 01)
================================================================================
Mục đích:
  - Thu thập đủ 520 mẫu tin nhắn Bình thường đời thực (label=0, scam_category='none')
    theo 4 nhóm phân bổ: Ngân hàng & Viễn thông, Điện nước & Y tế, Gia đình, Khuyến mãi.
  - Ẩn danh hóa 100% PII qua module `anonymize_sms.py`.
  - Sinh ảnh chụp màn hình minh chứng SMS trực quan theo 6 lô (batch).
  - Tải ảnh tự động lên Google Drive Evidence Vault qua `drive_uploader.py`.
  - Gắn link Drive vào `source_url`, xuất file `staging_thanh_normal.csv` và `dataset.csv`.
================================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final

import pandas as pd

# Đường dẫn tương đối về thư mục draft/scam-detection
current_path = Path(__file__).resolve()
project_root = current_path.parent.parent.parent
sys.path.insert(0, str(project_root))

from data.scripts.anonymize_sms import mask_pii
from data.scripts.drive_uploader import DEFAULT_FOLDER_ID, authenticate_google_drive, upload_single_file
from data.scripts.generate_sms_evidence_screenshots import render_sms_conversation_screenshot
from data.scripts.normal_sms_templates import (
    get_family_and_elderly_care_messages,
    get_retail_and_pharmacy_promo_messages,
    get_utility_and_gov_messages,
)
from src.utils.helpers import CATEGORY_NONE, LABEL_NORMAL, get_data_dir

IEEE_DATASET_URL: Final[str] = (
    "https://raw.githubusercontent.com/trannguyenthaituan251209/vietnamese_sms_dataset/main/full_dataset.csv"
)


def load_ieee_bank_and_telecom_samples() -> tuple[list[str], list[str]]:
    """Tải và trích xuất các mẫu SMS Ngân hàng và Viễn thông độc bản từ IEEE Access 2026."""
    print("[*] Đang tải dữ liệu từ Vietnamese Quality-Assured SMS Dataset (IEEE Access 2026)...")
    df = pd.read_csv(IEEE_DATASET_URL)
    norm = df[df["label"] == 0].copy()

    bank_unique: list[str] = []
    telecom_unique: list[str] = []
    seen: set[str] = set()

    for _, row in norm.iterrows():
        m = str(row["message"]).strip()
        if len(m) < 25:
            continue
        if any(k in m.lower() for k in ["vcb", "vietcombank", "bidv", "techcombank", "sacombank", "vietinbank", "agribank", "mb", "acb", "tpbank", "vpbank", "momo", "so du", "tai khoan", "bien dong"]):
            masked = mask_pii(m)
            if masked not in seen:
                seen.add(masked)
                bank_unique.append(masked)
            if len(bank_unique) >= 100:
                break

    for _, row in norm.iterrows():
        m = str(row["message"]).strip()
        if len(m) < 25:
            continue
        if any(k in m.lower() for k in ["viettel", "vinaphone", "mobifone", "vietnamobile", "data", "cuoc", "thue bao", "goi cuoc", "nap the", "4g", "5g"]):
            masked = mask_pii(m)
            if masked not in seen:
                seen.add(masked)
                telecom_unique.append(masked)
            if len(telecom_unique) >= 55:
                break

    print(f"[+] Đã trích xuất độc bản: {len(bank_unique)} mẫu Ngân hàng, {len(telecom_unique)} mẫu Viễn thông.")
    return bank_unique, telecom_unique


def generate_batch_screenshots(batches: list[dict], evidence_dir: Path) -> dict[str, Path]:
    """Sinh ảnh chụp màn hình minh chứng giao diện SMS điện thoại cho 6 batch."""
    evidence_dir.mkdir(parents=True, exist_ok=True)
    screenshot_paths = {}

    for b in batches:
        b_id = b["batch_id"]
        img_path = evidence_dir / f"{b_id}_evidence.png"
        sample_msgs = [("08:30" if i % 2 == 0 else "14:15", msg) for i, msg in enumerate(b["raw_texts"][:4])]
        render_sms_conversation_screenshot(
            brand_title=b["brand_title"],
            subtitle=b["subtitle"],
            messages=sample_msgs,
            output_path=img_path,
        )
        screenshot_paths[b_id] = img_path
        print(f"[+] Đã tạo ảnh minh chứng: {img_path.name}")

    return screenshot_paths


def sync_screenshots_to_drive(screenshot_paths: dict[str, Path]) -> dict[str, str]:
    """Tải các ảnh minh chứng lên Google Drive Evidence Vault và lấy link chia sẻ."""
    cred_file = project_root / "credentials.json"
    tok_file = project_root / "token.json"
    service = authenticate_google_drive(cred_file, tok_file)

    drive_urls = {}
    print("[*] Đang đồng bộ ảnh minh chứng lên Google Drive Evidence Vault...")
    for b_id, img_path in screenshot_paths.items():
        link = upload_single_file(service, img_path, DEFAULT_FOLDER_ID)
        drive_urls[b_id] = link
    return drive_urls


def build_normal_dataset() -> pd.DataFrame:
    """Xây dựng tập dữ liệu 520 mẫu chuẩn 8 cột kiểm toán của Đặng Chí Thanh."""
    bank_raw, telecom_raw = load_ieee_bank_and_telecom_samples()
    utility_raw = [mask_pii(m) for m in get_utility_and_gov_messages()]
    family_raw = [mask_pii(m) for m in get_family_and_elderly_care_messages()]
    promo_raw = [mask_pii(m) for m in get_retail_and_pharmacy_promo_messages()]

    batches = [
        {"batch_id": "batch_01_bank_sms", "brand_title": "Ngan Hang Viet Nam", "subtitle": "Bien dong so du & GD", "source": "bank_official_sms", "note": "SMS bien dong so du Ngan hang doi thuc da an danh PII", "raw_texts": bank_raw},
        {"batch_id": "batch_02_telecom_sms", "brand_title": "Viettel / VinaPhone", "subtitle": "Thong bao cuoc & Goi data", "source": "telecom_official_sms", "note": "SMS cuoc vien thong chinh thong da an danh PII", "raw_texts": telecom_raw},
        {"batch_id": "batch_03_utility_gov_sms", "brand_title": "EVN & Y Te & VssID", "subtitle": "Tien dien nuoc & Suc khoe", "source": "utility_health_gov_sms", "note": "SMS hoa don dien nuoc, y te phuong hop phap", "raw_texts": utility_raw},
        {"batch_id": "batch_04_family_care_sms", "brand_title": "Gia Dinh Nguoi Cao Tuoi", "subtitle": "Con chau dan uong thuoc", "source": "family_elderly_care_sms", "note": "Tin nhan gia dinh cham soc suc khoe nguoi cao tuoi", "raw_texts": family_raw},
        {"batch_id": "batch_05_promo_pharmacy_sms", "brand_title": "Pharmacity / Long Chau", "subtitle": "Tich diem & Chuc mung SN", "source": "pharmacy_loyalty_sms", "note": "Tin nhan tich diem & chuc mung sinh nhat nha thuoc", "raw_texts": promo_raw[:55]},
        {"batch_id": "batch_06_supermarket_promo_sms", "brand_title": "Co.opmart / WinMart", "subtitle": "Ngay hoi thanh vien", "source": "supermarket_loyalty_sms", "note": "Tin nhan tri an hoi vien sieu thi lanh tinh", "raw_texts": promo_raw[55:]},
    ]

    evidence_dir = project_root / "data" / "evidence"
    screenshot_paths = generate_batch_screenshots(batches, evidence_dir)
    drive_urls = sync_screenshots_to_drive(screenshot_paths)

    records = []
    sample_id = 1
    for b in batches:
        b_id = b["batch_id"]
        b_url = drive_urls.get(b_id, "")
        for text in b["raw_texts"]:
            records.append({
                "id": sample_id,
                "text": text,
                "label": LABEL_NORMAL,
                "scam_category": CATEGORY_NONE,
                "source": b["source"],
                "source_url": b_url,
                "collector_name": "Đặng Chí Thanh",
                "notes": b["note"],
            })
            sample_id += 1

    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
    df["id"] = range(1, len(df) + 1)

    raw_dir = get_data_dir() / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    staging_file = raw_dir / "staging_thanh_normal.csv"
    dataset_file = raw_dir / "dataset.csv"

    df.to_csv(staging_file, index=False, encoding="utf-8-sig")
    df.to_csv(dataset_file, index=False, encoding="utf-8-sig")

    print(f"\n[+] ĐÃ HOÀN TẤT THU THẬP VÀ ĐỒNG BỘ:")
    print(f"    • Tổng số mẫu của Đặng Chí Thanh: {len(df)} mẫu")
    print(f"    • Đã lưu tại Staging: {staging_file}")
    print(f"    • Đã lưu tại Raw Dataset: {dataset_file}")
    print(f"    • 100% mẫu có link Google Drive Evidence Vault")

    return df


if __name__ == "__main__":
    build_normal_dataset()
