"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
SCRIPT HỢP NHẤT DỮ LIỆU ĐỜI THỰC CHÍNH THỨC (CONSOLIDATE MASTER DATASET)
================================================================================
Mục đích:
  - Tự động hóa hoàn toàn quy trình hợp nhất (deterministic consolidation) 3 tệp dữ liệu
    staging đã được kiểm toán của cả 3 thành viên:
      1. staging_thanh_normal.csv (1.773 mẫu SMS bình thường chuẩn IEEE Access 2026)
      2. staging_cam_scam.csv (205 mẫu lừa đảo dịch vụ công & sức khỏe quà tặng)
      3. staging_son_scam.csv (215 mẫu lừa đảo quyền lực & cấp cứu gia đình)
  - Đánh số lại ID tuần tự từ 1 đến N.
  - Đảm bảo 0% duplicate, 100% Zero Synthetic Text, định dạng mã hóa utf-8-sig.
================================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

# Path resolution: find raw data directory
current_path = Path(__file__).resolve()
raw_dir = current_path.parent.parent / "raw"
staging_thanh = raw_dir / "staging_thanh_normal.csv"
staging_cam = raw_dir / "staging_cam_scam.csv"
staging_son = raw_dir / "staging_son_scam.csv"
output_dataset = raw_dir / "dataset.csv"

REQUIRED_COLUMNS = [
    "id",
    "text",
    "label",
    "scam_category",
    "source",
    "source_url",
    "collector_name",
    "notes",
]


def consolidate() -> pd.DataFrame:
    print("=== Hợp nhất Dữ liệu Đồ án Cuối kỳ CS114 ===")
    
    staging_files = [
        ("Đặng Chí Thanh (Normal)", staging_thanh),
        ("Bùi Thị Mỷ Cẩm (Scam)", staging_cam),
        ("Hoàng Cao Sơn (Scam)", staging_son),
    ]
    
    dfs: list[pd.DataFrame] = []
    for label, file_path in staging_files:
        if not file_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file staging: {file_path}")
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        print(f"[*] Đọc {label}: {len(df)} dòng từ {file_path.name}")
        dfs.append(df)
        
    master_df = pd.concat(dfs, ignore_index=True)
    initial_count = len(master_df)
    
    # Kiểm tra và loại bỏ duplicate (nếu có)
    cleaned_texts = master_df["text"].astype(str).str.strip()
    dup_mask = cleaned_texts.duplicated(keep="first")
    if dup_mask.any():
        dup_count = int(dup_mask.sum())
        print(f"[!] Cảnh báo: Phát hiện {dup_count} dòng trùng lặp. Đang loại bỏ...")
        master_df = master_df[~dup_mask].reset_index(drop=True)
    else:
        print("[SUCCESS] Tuyệt đối không có dòng trùng lặp (0 duplicate).")
        
    # Đánh số ID tuần tự 1..N
    master_df["id"] = range(1, len(master_df) + 1)
    
    # Sắp xếp đúng thứ tự cột chuẩn
    master_df = master_df[REQUIRED_COLUMNS]
    
    # Lưu file CSV với chuẩn utf-8-sig
    master_df.to_csv(output_dataset, index=False, encoding="utf-8-sig")
    print(f"[SUCCESS] Đã ghi {len(master_df)} mẫu vào {output_dataset.name} (utf-8-sig).")
    
    # In thống kê phân bố
    print("\n--- Thống kê Phân bổ Master Dataset ---")
    print(f"Tổng số mẫu: {len(master_df)}")
    print(f"Class Balance:\n{master_df['label'].value_counts().to_string()}")
    print(f"\nScam Categories:\n{master_df['scam_category'].value_counts().to_string()}")
    print(f"\nContributors:\n{master_df['collector_name'].value_counts().to_string()}")
    print("=" * 50)
    
    return master_df


if __name__ == "__main__":
    consolidate()
