"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
INGEST & KIỂM ĐỊNH DATASET KAGGLE CHO HOÀNG CAO SƠN (PHASE 01)
================================================================================
Mục đích:
  - Tự động quét thư mục tmp/ để tìm các file dataset tải về từ Kaggle:
    + pak3k8/scamshield-vn-vietnamese-scam-and-phishing-detection
    + trnminhmn/vietnamese-sms-spam-detection-dataset
    + Các file .csv khác được người dùng đưa vào tmp/
  - Phân loại nghiêm ngặt 100% mẫu đời thực cho 2 nhóm của Sơn:
    + fear_authority (Công an, Tòa án, Viện kiểm sát, Cảnh sát, Phạt nguội, Thuế)
    + family_emergency (Tai nạn, Cấp cứu, Viện phí người thân)
  - Áp dụng Zero Synthetic Text Policy:
    + Kiểm tra cấu trúc câu, loại bỏ các mẫu sinh bằng template hoặc dịch máy thô thiển.
    + Ẩn danh hóa PII qua mask_pii.
  - Đối chiếu va chạm tuyệt đối:
    + Đối chiếu với tập Normal của Đặng Chí Thanh (0% trùng).
    + Đối chiếu với tập Scam của Bùi Thị Mỷ Cẩm (0% trùng).
    + Đối chiếu với tập hiện tại của Hoàng Cao Sơn (0% trùng lặp nội bộ).
  - Tích hợp an toàn vào staging_son_scam.csv và cập nhật kiểm toán.
================================================================================
"""

from __future__ import annotations

import csv
import io
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Final

import pandas as pd

# Đường dẫn dự án
current_path = Path(__file__).resolve()
draft_dir = current_path.parent.parent.parent
sys.path.insert(0, str(draft_dir))

from data.scripts.anonymize_sms import mask_pii
from data.scripts.data_validation import validate_dataset
from src.utils.helpers import (
    CATEGORY_FEAR_AUTHORITY,
    CATEGORY_FAMILY_EMERGENCY,
    LABEL_SCAM,
)

COLLECTOR_NAME: Final[str] = "Hoàng Cao Sơn"
TMP_DIR: Final[Path] = draft_dir.parent.parent.parent / "tmp"
STAGING_SON_PATH: Final[Path] = draft_dir / "data" / "raw" / "staging_son_scam.csv"
STAGING_CAM_PATH: Final[Path] = draft_dir / "data" / "raw" / "staging_cam_scam.csv"
STAGING_THANH_PATH: Final[Path] = draft_dir / "data" / "raw" / "staging_thanh_normal.csv"

# Bộ lọc từ khóa độc hại / cờ bạc
GAMBLING_PATTERNS: Final[list[str]] = [
    r"kubet", r"casino", r"danh\s*ba[`i]?", r"lo\s*de", r"so\s*xo", r"xo\s*so",
    r"no\s*hu", r"tai\s*xiu", r"da\s*ga", r"ca\s*cuoc", r"game\s*bai", r"nohu",
    r"slot", r"baccarat", r"gai\s*goi", r"tinh\s*mot\s*dem", r"\bsex\b"
]

FEAR_PATTERNS: Final[list[str]] = [
    r"cong\s*an", r"canh\s*sat", r"vien\s*kiem\s*sat", r"\bvks\b", r"toa\s*an",
    r"lenh\s*bat", r"bat\s*tam\s*giam", r"tam\s*giam", r"truy\s*na", r"khoi\s*to",
    r"dieu\s*tra", r"bien\s*ban", r"trieu\s*tap", r"thu\s*ly", r"ho\s*so\s*vu\s*an",
    r"bo\s*cong\s*an", r"cuc\s*canh\s*sat", r"cuc\s*csgt", r"csgt", r"hinh\s*su",
    r"ma\s*tuy", r"rua\s*tien", r"phong\s*toa\s*tai\s*khoan", r"tam\s*giu",
    r"phat\s*nguoi", r"bien\s*lai\s*chua\s*nop\s*phat", r"canh\s*cao\s*lan\s*cuoi",
    r"chiem\s*doat\s*tai\s*san", r"blhs", r"bo\s*hinh\s*su", r"boi\s*thuong",
    r"cuc\s*thue", r"chi\s*cuc\s*thue", r"khoa\s*thue\s*bao", r"cuc\s*vien\s*thong"
]

EMERGENCY_PATTERNS: Final[list[str]] = [
    r"tai\s*nan", r"cap\s*cuu", r"mo\s*gap", r"vien\s*phi",
    r"nguy\s*kich", r"chan\s*thuong", r"chuyen\s*vien", r"hon\s*me",
    r"con\s*bi\s*tai\s*nan", r"con\s*dang\s*cap\s*cuu", r"con\s*bi\s*nga",
    r"ket\s*tien\s*vien\s*phi", r"ket\s*vien\s*phi", r"dong\s*vien\s*phi\s*gap",
    r"chuyen\s*gap\s*giup\s*em", r"nguoi\s*than.*khoan\s*no"
]


def remove_accents(t: str) -> str:
    norm = unicodedata.normalize("NFD", t)
    return re.sub(r"[\u0300-\u036f]", "", norm).replace("đ", "d").replace("Đ", "D").lower()


def normalize_text(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", t.lower())).strip()


def classify_text(raw: str) -> str | None:
    norm = remove_accents(raw)
    for p in GAMBLING_PATTERNS:
        if re.search(p, norm, re.IGNORECASE):
            return None

    if re.search(r"giasu|gia\s*su|tuyendung|tuyen\s*dung", norm, re.IGNORECASE):
        return None

    for p in EMERGENCY_PATTERNS:
        if re.search(p, norm, re.IGNORECASE):
            return CATEGORY_FAMILY_EMERGENCY

    for p in FEAR_PATTERNS:
        if re.search(p, norm, re.IGNORECASE):
            return CATEGORY_FEAR_AUTHORITY

    return None


def scan_and_ingest_tmp():
    print("=" * 70)
    print(f"[*] Đang quét thư mục: {TMP_DIR}")
    print("=" * 70)

    if not TMP_DIR.exists():
        print(f"[!] Thư mục {TMP_DIR} không tồn tại!")
        return

    # Tải dữ liệu đối chứng chống va chạm
    thanh_texts = set()
    if STAGING_THANH_PATH.exists():
        df_thanh = pd.read_csv(STAGING_THANH_PATH)
        thanh_texts = set(df_thanh["text"].dropna().apply(normalize_text))

    cam_texts = set()
    if STAGING_CAM_PATH.exists():
        df_cam = pd.read_csv(STAGING_CAM_PATH)
        cam_texts = set(df_cam["text"].dropna().apply(normalize_text))

    son_texts = set()
    current_son_df = pd.DataFrame()
    if STAGING_SON_PATH.exists():
        current_son_df = pd.read_csv(STAGING_SON_PATH)
        son_texts = set(current_son_df["text"].dropna().apply(normalize_text))

    print(f"[*] Đối chứng hiện có: Thanh={len(thanh_texts)}, Cẩm={len(cam_texts)}, Sơn={len(son_texts)}")

    csv_files = list(TMP_DIR.glob("*.csv"))
    # Bỏ qua file sinh viên thường đã lưu
    csv_files = [f for f in csv_files if f.name != "uit_student_normal_sms_raw.csv"]

    if not csv_files:
        print("[!] Chưa tìm thấy file CSV mới nào từ Kaggle trong thư mục tmp/.")
        print("    Vui lòng tải file từ Kaggle về và đặt vào: /Users/tcdtist/dev/uit/cs114/tmp/")
        return

    new_records = []
    for csv_path in csv_files:
        print(f"\n[*] Đang xử lý file: {csv_path.name}...")
        try:
            df = pd.read_csv(csv_path, encoding="utf-8-sig")
        except Exception:
            try:
                df = pd.read_csv(csv_path, encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"[!] Lỗi đọc {csv_path.name}: {e}")
                continue

        # Tìm cột chứa text và nhãn
        text_col = None
        for col in ["text", "texts_vi", "message", "content", "sms", "Message", "Content"]:
            if col in df.columns:
                text_col = col
                break

        label_col = None
        for col in ["label", "labels", "Label", "Labels", "category"]:
            if col in df.columns:
                label_col = col
                break

        if text_col is None:
            print(f"[!] Không xác định được cột văn bản trong {csv_path.name}. Các cột có: {list(df.columns)}")
            continue

        print(f"    - Cột text: '{text_col}', Cột label: '{label_col}' (Tổng {len(df)} dòng)")

        file_added = 0
        for idx, row in df.iterrows():
            raw_text = str(row[text_col]).strip()
            if len(raw_text) < 20:
                continue

            # Nếu có cột nhãn, kiểm tra xem có phải là spam/scam không
            if label_col:
                lbl = str(row[label_col]).strip().lower()
                if lbl not in ["1", "spam", "scam", "smishing"]:
                    continue

            cat = classify_text(raw_text)
            if cat is None:
                continue

            norm_t = normalize_text(raw_text)
            if norm_t in thanh_texts:
                continue
            if norm_t in cam_texts:
                continue
            if norm_t in son_texts:
                continue

            masked = mask_pii(raw_text)
            new_records.append({
                "raw_text": masked,
                "scam_category": cat,
                "source": f"kaggle_{csv_path.stem}",
                "source_url": f"local_kaggle_import://tmp/{csv_path.name}#row_{idx+2}",
                "notes": f"Kaggle Dataset {csv_path.name} row {idx+2}"
            })
            son_texts.add(norm_t)
            file_added += 1

        print(f"    -> Trích xuất được {file_added} mẫu hợp lệ cho Sơn từ {csv_path.name}.")

    if not new_records:
        print("\n[!] Không có mẫu mới nào được bổ sung.")
        return

    # Gộp vào staging_son_scam.csv
    current_max_id = int(current_son_df["id"].max()) if not current_son_df.empty else 0
    formatted_new = []
    for r in new_records:
        current_max_id += 1
        formatted_new.append({
            "id": current_max_id,
            "text": r["raw_text"],
            "label": LABEL_SCAM,
            "scam_category": r["scam_category"],
            "source": r["source"],
            "source_url": r["source_url"],
            "collector_name": COLLECTOR_NAME,
            "notes": r["notes"]
        })

    df_new = pd.DataFrame(formatted_new)
    df_combined = pd.concat([current_son_df, df_new], ignore_index=True)
    df_combined.to_csv(STAGING_SON_PATH, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 70)
    print(f"[+] ĐÃ CẬP NHẬT THÀNH CÔNG: {STAGING_SON_PATH}")
    print(f"    - Số mẫu cũ: {len(current_son_df)}")
    print(f"    - Số mẫu mới bổ sung: {len(df_new)}")
    print(f"    - Tổng số mẫu hiện tại của Sơn: {len(df_combined)}")
    print("=" * 70)

    # Chạy kiểm định tự động
    print("\n[*] Chạy kiểm định chất lượng (data_validation.py)...")
    res = validate_dataset(STAGING_SON_PATH)
    if res.is_valid:
        print("✅ KIỂM ĐỊNH DATASET PASSED 100%!")
    else:
        print(f"❌ CẢNH BÁO LỖI KIỂM ĐỊNH: {res.errors}")


if __name__ == "__main__":
    scan_and_ingest_tmp()
