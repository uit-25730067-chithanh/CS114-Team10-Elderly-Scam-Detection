"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
SCRIPT PHÂN CHIA DỮ LIỆU TRAIN / TEST THEO TỶ LỆ PHÂN TẦNG (STRATIFIED SPLIT)
================================================================================
Mục đích:
  - Phân chia tập dữ liệu gốc `data/raw/dataset.csv` thành 2 tập riêng biệt:
    + Tập Huấn luyện (Train set): 80% dữ liệu
    + Tập Kiểm thử (Test set): 20% dữ liệu
  - Áp dụng kỹ thuật Phân tầng (Stratification) trên cả 2 tiêu chí `label` (0/1) và
    `scam_category` (5 nhóm bẫy tâm lý) để đảm bảo tập test phản ánh chính xác
    phân phối của toàn bộ thế giới thực.
  - Cố định hạt giống ngẫu nhiên (seed = 42) để kết quả phân chia có tính tái lập 100%
    (reproducibility) theo chuẩn mực khoa học của môn CS114.
  - Lưu kết quả dưới định dạng CSV bảng mã `utf-8-sig` vào thư mục `data/processed/`.

Hướng dẫn sử dụng cho thành viên trong nhóm:
  1. Chạy với cấu hình mặc định (tự động đọc dataset.csv):
     python3 split_data.py
  2. Chỉ định file dataset và tỷ lệ test tùy chỉnh:
     python3 split_data.py --input data/raw/dataset.csv --test-size 0.20 --seed 42
================================================================================
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

# Đường dẫn tương đối tìm về thư mục gốc làm việc draft/scam-detection
current_path = Path(__file__).resolve()
for parent in [current_path.parent, current_path.parent.parent, current_path.parent.parent.parent]:
    if (parent / "src" / "utils" / "helpers.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from src.utils.helpers import (
    CATEGORY_NONE,
    LABEL_NORMAL,
    LABEL_SCAM,
    RANDOM_STATE,
    TEST_SIZE,
    get_data_dir,
    set_seeds,
)


def perform_stratified_split(
    input_file: Path | str,
    output_dir: Path | str | None = None,
    test_size: float = TEST_SIZE,
    seed: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Thực hiện phân tách tập dữ liệu có phân tầng (Stratified Split).
    """
    set_seeds(seed)
    path = Path(input_file)
    if not path.exists():
        print(f"[!] Lỗi: Không tìm thấy tệp dữ liệu tại {path}")
        sys.exit(1)

    df = pd.read_csv(path, encoding="utf-8-sig")
    if df.empty or len(df) < 5:
        print("[!] Lỗi: Dataset rỗng hoặc có quá ít mẫu để phân chia (cần ít nhất 5 mẫu).")
        sys.exit(1)

    # Tạo cột stratification kết hợp: nếu lừa đảo thì stratify theo scam_category, nếu bình thường thì theo label
    stratify_col = df["scam_category"].copy()

    # Kiểm tra xem có class nào có số lượng mẫu < 2 không (sklearn yêu cầu tối thiểu 2 mẫu/class)
    counts = stratify_col.value_counts()
    rare_classes = counts[counts < 2].index.tolist()
    if rare_classes:
        print(f"[*] Cảnh báo: Các nhóm có quá ít mẫu ({rare_classes}), chuyển sang stratify theo nhãn 'label'.")
        stratify_target = df["label"]
    else:
        stratify_target = stratify_col

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=seed,
        stratify=stratify_target,
    )

    out_dir = Path(output_dir) if output_dir else get_data_dir() / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)

    train_path = out_dir / "train.csv"
    test_path = out_dir / "test.csv"

    train_df.to_csv(train_path, index=False, encoding="utf-8-sig")
    test_df.to_csv(test_path, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 65)
    print("  KẾT QUẢ PHÂN CHIA DỮ LIỆU HUẤN LUYỆN / KIỂM THỬ (STRATIFIED SPLIT)")
    print("=" * 65)
    print(f"Tệp gốc:            {path.name} ({len(df)} mẫu)")
    print(f"Tập Train (80%):    {train_path} ({len(train_df)} mẫu)")
    print(f"Tập Test (20%):     {test_path} ({len(test_df)} mẫu)")
    print("-" * 65)

    print("\nPhân phối nhãn nhị phân (Class Balance):")
    train_labels = train_df["label"].value_counts(normalize=True).to_dict()
    test_labels = test_df["label"].value_counts(normalize=True).to_dict()
    print(f"  • Train: Bình thường (0) = {train_labels.get(LABEL_NORMAL, 0):.1%} | Lừa đảo (1) = {train_labels.get(LABEL_SCAM, 0):.1%}")
    print(f"  • Test:  Bình thường (0) = {test_labels.get(LABEL_NORMAL, 0):.1%} | Lừa đảo (1) = {test_labels.get(LABEL_SCAM, 0):.1%}")

    if "scam_category" in df.columns:
        print("\nPhân phối nhóm bẫy tâm lý (Scam Categories):")
        categories = sorted(df["scam_category"].unique())
        for cat in categories:
            n_tr = (train_df["scam_category"] == cat).sum()
            n_te = (test_df["scam_category"] == cat).sum()
            pct_tr = n_tr / len(train_df)
            pct_te = n_te / len(test_df)
            print(f"  • {cat:20s}: Train = {n_tr:4d} ({pct_tr:.1%}) | Test = {n_te:3d} ({pct_te:.1%})")

    print("=" * 65)
    print("✅ ĐÃ HOÀN TẤT: Dữ liệu sạch sẵn sàng cho Phase 02 (Tiền xử lý văn bản tiếng Việt).\n")

    return train_df, test_df


def main() -> None:
    parser = argparse.ArgumentParser(description="Chia dữ liệu train/test có phân tầng cho CS114")
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Đường dẫn tới dataset CSV gốc. Mặc định: data/raw/dataset.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Thư mục xuất file train.csv và test.csv. Mặc định: data/processed/",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=TEST_SIZE,
        help=f"Tỷ lệ tập test (mặc định: {TEST_SIZE})",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=RANDOM_STATE,
        help=f"Hạt giống ngẫu nhiên (mặc định: {RANDOM_STATE})",
    )

    args = parser.parse_args()

    target_input = (
        Path(args.input)
        if args.input
        else get_data_dir() / "raw" / "dataset.csv"
    )

    if not target_input.exists():
        # Fallback to template if dataset.csv not yet exported
        template_input = get_data_dir() / "raw" / "dataset_template.csv"
        if template_input.exists():
            print(f"[*] Chưa có {target_input.name}, chạy thử nghiệm trên {template_input.name}...")
            target_input = template_input

    perform_stratified_split(
        input_file=target_input,
        output_dir=args.output_dir,
        test_size=args.test_size,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
