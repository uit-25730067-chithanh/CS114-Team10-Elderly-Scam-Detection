"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
SCRIPT THU THẬP & ĐỒNG BỘ DỮ LIỆU BÌNH THƯỜNG CỦA ĐẶNG CHÍ THANH (PHASE 01)
================================================================================
Mục đích:
  - Khai thác toàn bộ kho dữ liệu tin nhắn Bình thường đời thực (label=0, scam_category='none')
    từ Vietnamese Quality-Assured SMS Dataset (công bố khoa học IEEE Access 2026).
  - TUYỆT ĐỐI KHÔNG SỬ DỤNG AI HOẶC TEMPLATE TỰ SINH DỮ LIỆU.
  - Ẩn danh hóa 100% PII (SĐT, STK, OTP, CCCD, Mã GD) qua module `anonymize_sms.py`.
  - Lọc bỏ trùng lặp tuyệt đối sau khi ẩn danh hóa để đảm bảo tính độc bản 100%.
  - Gán chính xác source_url 1-1 trỏ trực tiếp đến dòng dữ liệu gốc (permalink #L...)
    trong repository chính thức trên GitHub của bộ dữ liệu IEEE Access.
  - Xuất file `staging_thanh_normal.csv` và `dataset.csv` (chuẩn utf-8-sig).
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
from src.utils.helpers import CATEGORY_NONE, LABEL_NORMAL, get_data_dir

import io
import urllib.request

IEEE_DATASET_URL: Final[str] = (
    "https://raw.githubusercontent.com/trannguyenthaituan251209/vietnamese_sms_dataset/main/full_dataset.csv"
)
IEEE_GITHUB_REPO_URL: Final[str] = (
    "https://github.com/trannguyenthaituan251209/vietnamese_sms_dataset/blob/main/full_dataset.csv"
)
MIN_MESSAGE_LENGTH: Final[int] = 25


def extract_all_authentic_normal_samples(holdout_texts: set[str] | None = None) -> list[dict]:
    """
    Trích xuất toàn bộ mẫu tin nhắn bình thường đời thực độc bản từ bộ dữ liệu IEEE Access 2026.
    Mỗi mẫu được kiểm tra độ dài, che giấu PII và tạo liên kết truy xuất nguồn gốc 1-1.
    Tự động loại bỏ bất kỳ mẫu nào đã xuất hiện trong tập Holdout Test cá nhân để chống rò rỉ dữ liệu (Anti-Leakage).
    """
    print("[*] Đang tải toàn bộ Vietnamese Quality-Assured SMS Dataset (IEEE Access 2026)...")
    try:
        req = urllib.request.Request(IEEE_DATASET_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            csv_bytes = resp.read()
        df = pd.read_csv(io.BytesIO(csv_bytes))
    except Exception as exc:
        print(f"[!] Lỗi khi tải dữ liệu từ {IEEE_DATASET_URL}: {exc}")
        sys.exit(1)

    norm = df[df["label"] == 0].copy()

    samples: list[dict] = []
    seen_texts: set[str] = set()
    excluded_holdout_count = 0

    for idx, row in norm.iterrows():
        raw_msg = str(row["message"]).strip()
        if len(raw_msg) < MIN_MESSAGE_LENGTH:
            continue

        masked_text = mask_pii(raw_msg)
        if len(masked_text) < MIN_MESSAGE_LENGTH or masked_text in seen_texts:
            continue

        # Chống rò rỉ dữ liệu (Anti-Data Leakage) đối với tập Holdout Test
        if holdout_texts and masked_text in holdout_texts:
            excluded_holdout_count += 1
            continue

        seen_texts.add(masked_text)
        line_number = idx + 2  # Dòng 1 là tiêu đề CSV
        source_url = f"{IEEE_GITHUB_REPO_URL}#L{line_number}"

        samples.append({
            "text": masked_text,
            "source_url": source_url,
            "original_line": line_number,
        })

    if excluded_holdout_count > 0:
        print(f"[*] Đã loại trừ {excluded_holdout_count} mẫu trùng khớp với Holdout Test set để chống rò rỉ dữ liệu (Anti-Data Leakage).")

    print(f"[+] Đã trích xuất thành công {len(samples)} mẫu tin nhắn bình thường đời thực độc bản (100% PII masked, 0 duplicate, 0 leakage).")
    return samples


def build_and_export_dataset(samples: list[dict], data_dir: Path) -> pd.DataFrame:
    """Tạo DataFrame chuẩn kiểm toán 8 cột và xuất ra file CSV."""
    raw_dir = data_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for idx, s in enumerate(samples, start=1):
        rows.append({
            "id": idx,
            "text": s["text"],
            "label": LABEL_NORMAL,
            "scam_category": CATEGORY_NONE,
            "source": "Vietnamese Quality-Assured SMS Dataset (IEEE Access 2026)",
            "source_url": s["source_url"],
            "collector_name": "Đặng Chí Thanh",
            "notes": f"Tin nhắn SMS thực tế dòng #{s['original_line']} (IEEE Access 2026); đã ẩn danh hóa PII",
        })

    dataset_df = pd.DataFrame(rows)

    # 1. Xuất file staging riêng của Đặng Chí Thanh
    staging_path = raw_dir / "staging_thanh_normal.csv"
    dataset_df.to_csv(staging_path, index=False, encoding="utf-8-sig")
    print(f"[+] Đã xuất file staging: {staging_path} ({len(dataset_df)} dòng)")

    # 2. Xuất file dataset.csv chính thức của nhóm
    dataset_path = raw_dir / "dataset.csv"
    dataset_df.to_csv(dataset_path, index=False, encoding="utf-8-sig")
    print(f"[+] Đã xuất file dataset chính: {dataset_path} ({len(dataset_df)} dòng)")

    return dataset_df


def main():
    print("=" * 75)
    print(" CS114 - KHAI THÁC TOÀN BỘ KHO DỮ LIỆU BÌNH THƯỜNG ĐỜI THỰC IEEE ACCESS 2026")
    print(" Người thực hiện: Đặng Chí Thanh (MSSV: 25730067) — PM & Data Lead")
    print(" Tiêu chuẩn: 100% Đời thực | Zero AI Generated | 100% PII Masked | 1-1 Link")
    print("=" * 75)

    data_dir = get_data_dir()
    real_test_path = data_dir / "processed" / "real_world_test_thanh.csv"
    holdout_texts: set[str] = set()
    if real_test_path.exists():
        try:
            real_df = pd.read_csv(real_test_path, encoding="utf-8-sig")
            holdout_texts = set(real_df["text"].dropna().str.strip())
            print(f"[*] Đã nạp {len(holdout_texts)} mẫu Holdout Test thực tế để loại trừ rò rỉ dữ liệu (Anti-Leakage).")
        except Exception as e:
            print(f"[*] Cảnh báo khi đọc real_world_test_thanh.csv: {e}")

    samples = extract_all_authentic_normal_samples(holdout_texts=holdout_texts)
    if not samples:
        print("[!] Lỗi: Không trích xuất được dữ liệu!")
        sys.exit(1)

    df = build_and_export_dataset(samples, data_dir)
    print("=" * 75)
    print(f"✅ HOÀN TẤT THU THẬP: {len(df)} mẫu đời thực độc bản, 100% PII masked, 100% source_url 1-1!")
    print("=" * 75)


if __name__ == "__main__":
    main()
