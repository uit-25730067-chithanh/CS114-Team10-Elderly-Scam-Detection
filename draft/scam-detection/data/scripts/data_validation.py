"""
CS114 Final Project — Scam Detection
Dataset Validation Script.

Validates raw or processed dataset CSV files against the schema,
data types, category integrity, class balance, and provenance requirements.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Final

import pandas as pd

# Path resolution: find draft/scam-detection root
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
    SCAM_CATEGORIES,
    get_data_dir,
)

REQUIRED_COLUMNS: Final[list[str]] = [
    "id",
    "text",
    "label",
    "scam_category",
    "source",
]

PROVENANCE_COLUMNS: Final[list[str]] = [
    "source_url",
    "source_title",
    "evidence_type",
    "collector_name",
    "notes",
]

ALLOWED_EVIDENCE_TYPES: Final[set[str]] = {
    "gov_portal",
    "news_press",
    "real_sms_screenshot",
    "telecom_bank_sms",
    "other",
}


def validate_dataset(file_path: Path | str, verbose: bool = True) -> tuple[bool, list[str]]:
    """
    Validate a dataset CSV file against project quality gates.

    Checks:
    1. File exists and is non-empty.
    2. All required columns exist ('id', 'text', 'label', 'scam_category', 'source').
    3. No null/empty text values.
    4. Labels belong to {0, 1}.
    5. Scam categories belong to defined set of categories.
    6. No duplicate message texts.
    7. Consistent label-category alignment:
       - label=0 must have scam_category='none'
       - label=1 must have scam_category in SCAM_CATEGORIES and != 'none'
    8. Validates provenance fields when present (evidence_type, source_url).

    Returns:
        (is_valid, list_of_errors)
    """
    path = Path(file_path)
    errors: list[str] = []

    if not path.exists():
        errors.append(f"File not found: {path}")
        return False, errors

    try:
        # Read with utf-8-sig to safely handle BOM from Windows/Excel exports
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception as e:
        errors.append(f"Failed to read CSV: {e}")
        return False, errors

    if df.empty:
        errors.append("Dataset is completely empty.")
        return False, errors

    # Check required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        return False, errors

    # Check empty texts
    empty_text_mask = df["text"].isna() | (df["text"].astype(str).str.strip() == "")
    if empty_text_mask.any():
        empty_count = int(empty_text_mask.sum())
        errors.append(f"Found {empty_count} rows with empty or whitespace-only 'text'.")

    # Check label validity
    invalid_labels = df[~df["label"].isin([LABEL_NORMAL, LABEL_SCAM])]
    if not invalid_labels.empty:
        errors.append(
            f"Found {len(invalid_labels)} rows with invalid label values: "
            f"{invalid_labels['label'].unique().tolist()} (must be 0 or 1)."
        )

    # Check category validity
    invalid_categories = df[~df["scam_category"].isin(SCAM_CATEGORIES)]
    if not invalid_categories.empty:
        errors.append(
            f"Found {len(invalid_categories)} rows with invalid scam_category values: "
            f"{invalid_categories['scam_category'].unique().tolist()} "
            f"(must be one of {SCAM_CATEGORIES})."
        )

    # Check label-category alignment
    normal_wrong_cat = df[(df["label"] == LABEL_NORMAL) & (df["scam_category"] != CATEGORY_NONE)]
    if not normal_wrong_cat.empty:
        errors.append(
            f"Found {len(normal_wrong_cat)} normal samples (label=0) with non-'none' category."
        )

    scam_wrong_cat = df[(df["label"] == LABEL_SCAM) & (df["scam_category"] == CATEGORY_NONE)]
    if not scam_wrong_cat.empty:
        errors.append(
            f"Found {len(scam_wrong_cat)} scam samples (label=1) with scam_category='none'."
        )

    # Check duplicate texts
    duplicate_mask = df.duplicated(subset=["text"], keep=False)
    if duplicate_mask.any():
        dup_count = int(duplicate_mask.sum())
        errors.append(f"Found {dup_count} rows with duplicate message text.")

    # Check provenance fields if present
    if "evidence_type" in df.columns:
        invalid_evidence = df[
            df["evidence_type"].notna() & ~df["evidence_type"].isin(ALLOWED_EVIDENCE_TYPES)
        ]
        if not invalid_evidence.empty:
            errors.append(
                f"Found {len(invalid_evidence)} rows with unknown evidence_type: "
                f"{invalid_evidence['evidence_type'].unique().tolist()}."
            )

    is_valid = len(errors) == 0

    if verbose:
        print("\n" + "=" * 60)
        print(f"  DATASET VALIDATION REPORT: {path.name}")
        print("=" * 60)
        print(f"Total Rows:       {len(df)}")
        print(f"Columns:          {list(df.columns)}")

        if "label" in df.columns:
            label_counts = df["label"].value_counts().to_dict()
            print(f"Class Balance:    Normal (0): {label_counts.get(LABEL_NORMAL, 0)} | "
                  f"Scam (1): {label_counts.get(LABEL_SCAM, 0)}")

        if "scam_category" in df.columns:
            print("\nScam Category Distribution:")
            for cat, count in df["scam_category"].value_counts().items():
                print(f"  - {cat:20s}: {count:4d}")

        if "collector_name" in df.columns:
            print("\nCollector Contributions:")
            for collector, count in df["collector_name"].value_counts().items():
                print(f"  - {str(collector):20s}: {count:4d} samples")

        if "source_url" in df.columns:
            urls_present = df["source_url"].notna() & (df["source_url"].astype(str).str.strip() != "")
            print(f"\nProvenance URLs:  {urls_present.sum()} / {len(df)} samples ({urls_present.mean():.1%})")

        print("-" * 60)
        if is_valid:
            print("✅ STATUS: PASSED — Dataset conforms to all validation rules.")
        else:
            print("❌ STATUS: FAILED — Issues found:")
            for err in errors:
                print(f"   • {err}")
        print("=" * 60 + "\n")

    return is_valid, errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate CS114 Scam Detection Dataset CSV")
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to dataset CSV file. Defaults to data/raw/dataset.csv or template.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed console report.",
    )

    args = parser.parse_args()

    if args.file:
        target_path = Path(args.file)
    else:
        raw_dataset = get_data_dir() / "raw" / "dataset.csv"
        template_csv = get_data_dir() / "raw" / "dataset_template.csv"
        target_path = raw_dataset if raw_dataset.exists() else template_csv

    is_valid, _ = validate_dataset(target_path, verbose=not args.quiet)
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
