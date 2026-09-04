#!/usr/bin/env python3
"""
Verification script for CS114 Final Project (Elderly Scam Detection).
Executes checks on directory layout, technical documents, code modules, and phase plans.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


def log_success(msg: str) -> None:
    print(f"[\033[92mSUCCESS\033[0m] {msg}")


def log_warning(msg: str) -> None:
    print(f"[\033[93mWARNING\033[0m] {msg}")


def log_error(msg: str) -> None:
    print(f"[\033[91mERROR\033[0m] {msg}")


def log_info(msg: str) -> None:
    print(f"[*] {msg}")


def main() -> int:
    print("=== Running Verification for CS114 Final Project ===")
    final_dir = Path(__file__).resolve().parent
    draft_dir = final_dir / "draft" / "scam-detection"
    plans_dir = final_dir / "plans" / "scam-detection-full-submit"

    all_passed = True

    # 1. Verify Core Directories
    required_dirs = [
        final_dir / "docs",
        draft_dir,
        draft_dir / "src",
        draft_dir / "src" / "utils",
        draft_dir / "src" / "preprocessing",
        draft_dir / "src" / "models",
        draft_dir / "src" / "evaluation",
        draft_dir / "data" / "raw",
        draft_dir / "data" / "processed",
        draft_dir / "notebooks",
        draft_dir / "reports" / "figures",
        draft_dir / "demo",
        plans_dir,
        final_dir / "submit",
    ]

    log_info("Checking essential directory structure...")
    for directory in required_dirs:
        if directory.is_dir():
            log_success(f"Directory exists: {directory.relative_to(final_dir)}")
        else:
            log_error(f"Missing directory: {directory}")
            all_passed = False

    # 2. Verify Key Files
    required_files = [
        final_dir / "README.md",
        final_dir / "AGENTS.md",
        final_dir / "BRAINSTORM.md",
        final_dir / ".gitignore",
        draft_dir / "README.md",
        draft_dir / "requirements.txt",
        draft_dir / "data" / "raw" / "dataset_template.csv",
        draft_dir / "src" / "utils" / "helpers.py",
        draft_dir / "src" / "utils" / "__init__.py",
        plans_dir / "plan.md",
    ]

    log_info("Checking required files...")
    for file_path in required_files:
        if file_path.is_file():
            size = file_path.stat().st_size
            log_success(f"File exists: {file_path.relative_to(final_dir)} ({size} bytes)")
        else:
            log_error(f"Missing required file: {file_path}")
            all_passed = False

    # 3. Verify Phase Plans (phase-00 to phase-10)
    log_info("Checking 11 phase plan specifications...")
    for phase_num in range(11):
        phase_files = list(plans_dir.glob(f"phase-{phase_num:02d}-*.md"))
        if phase_files:
            log_success(f"Phase {phase_num:02d} plan found: {phase_files[0].name}")
        else:
            log_error(f"Missing plan file for phase-{phase_num:02d}")
            all_passed = False

    # 4. Verify Dataset Template Schema
    template_csv = draft_dir / "data" / "raw" / "dataset_template.csv"
    if template_csv.is_file():
        log_info("Verifying dataset_template.csv schema...")
        with open(template_csv, "r", encoding="utf-8") as f:
            header = f.readline().strip()
            expected_header = "id,text,label,scam_category,source"
            if header == expected_header:
                log_success(f"Template header matches: '{header}'")
            else:
                log_error(f"Header mismatch: expected '{expected_header}', got '{header}'")
                all_passed = False
            
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) >= 5:
                log_success(f"Template contains {len(lines)} sample rows")
            else:
                log_warning(f"Template has only {len(lines)} samples (expected >= 5)")

    # 5. Verify Python Package Import & Helpers Constants
    log_info("Testing Python utils module import...")
    sys.path.insert(0, str(draft_dir))
    try:
        from src.utils.helpers import (
            RANDOM_STATE,
            SCAM_CATEGORIES,
            TARGET_F1_SCORE,
            TARGET_RECALL_SCAM,
            get_project_root,
            set_seeds,
        )
        set_seeds(RANDOM_STATE)
        resolved_root = get_project_root()
        if resolved_root.resolve() == draft_dir.resolve():
            log_success(f"helpers.py imported successfully. RANDOM_STATE={RANDOM_STATE}, Categories={len(SCAM_CATEGORIES)}")
            log_success(f"Target metrics: F1 >= {TARGET_F1_SCORE}, Recall >= {TARGET_RECALL_SCAM}")
        else:
            log_error(f"Project root mismatch: {resolved_root} vs {draft_dir}")
            all_passed = False
    except Exception as e:
        log_error(f"Failed to import from src.utils.helpers: {e}")
        all_passed = False

    # 6. Verify Markdown Integrity (Broken file:// links)
    log_info("Checking Markdown files for broken local file:// links...")
    for md_file in final_dir.rglob("*.md"):
        if ".git" in md_file.parts:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            file_links = re.findall(r"\[.*?\]\((file:///.*?)\)", content)
            for link in file_links:
                clean_path = link.replace("file://", "")
                if not os.path.exists(clean_path):
                    log_error(f"Broken file link in {md_file.relative_to(final_dir)}: {link}")
                    all_passed = False
        except Exception as err:
            log_warning(f"Could not read {md_file.name}: {err}")

    # 7. Verify Team Student IDs & Submission Package Naming
    log_info("Checking Team Roster (3 members) & Student IDs...")
    agents_md = final_dir / "AGENTS.md"
    readme_md = final_dir / "README.md"
    expected_mssvs = ["25730067", "25730013", "25730061"]
    
    for mssv in expected_mssvs:
        if mssv in agents_md.read_text(encoding="utf-8"):
            log_success(f"MSSV {mssv} verified in AGENTS.md")
        else:
            log_error(f"MSSV {mssv} missing in AGENTS.md")
            all_passed = False
            
        if mssv in readme_md.read_text(encoding="utf-8"):
            log_success(f"MSSV {mssv} verified in README.md")
        else:
            log_error(f"MSSV {mssv} missing in README.md")
            all_passed = False

    # Final Summary
    print("-" * 50)
    if all_passed:
        log_success("All Final project checks PASSED! Ready for Sprint execution.")
        return 0
    else:
        log_error("Final project verification FAILED with errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
