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
        draft_dir / "models",
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
    ignored_md_dirs = {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build"}
    for md_file in final_dir.rglob("*.md"):
        if any(part in ignored_md_dirs for part in md_file.parts):
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

    # 8. Verify Documentation Semantic Parity & 11-File Matrix
    log_info("Checking Documentation Semantic Parity & 11-File Matrix...")
    matrix_files = [
        ("Kế hoạch chi tiết (phase files)", list(plans_dir.glob("phase-*.md"))),
        ("Kế hoạch tổng thể (plan.md)", [plans_dir / "plan.md"]),
        ("Lộ trình & Phân công (project-roadmap.md)", [draft_dir / "docs" / "project-roadmap.md"]),
        ("Bối cảnh điều phối AI (AGENTS.md)", [final_dir / "AGENTS.md"]),
        ("Kiến trúc hệ thống (system-architecture.md)", [draft_dir / "docs" / "system-architecture.md"]),
        ("Data Dictionary Registry", [draft_dir / "data" / "processed" / "README.md"]),
        ("Model Registry", [draft_dir / "models" / "README.md"]),
        ("Notebook Registry", [draft_dir / "notebooks" / "README.md"]),
        ("Figure Catalog Registry", [draft_dir / "reports" / "figures" / "README.md"]),
        ("Cổng thông tin nhóm (README files)", [final_dir / "README.md", draft_dir / "README.md"]),
        ("Đề cương báo cáo (phase-09-report-ppt.md)", [plans_dir / "phase-09-report-ppt.md"]),
        ("Đóng gói nộp bài (submit/README.md)", [final_dir / "submit" / "README.md"]),
    ]

    for label, files in matrix_files:
        for f in files:
            if f.is_file() and f.stat().st_size > 100:
                log_success(f"[Parity] {label}: {f.name} verified ({f.stat().st_size} bytes)")
            else:
                log_error(f"[Parity] Missing or empty matrix file: {label} ({f})")
                all_passed = False

    plan_file = plans_dir / "plan.md"
    agents_file = final_dir / "AGENTS.md"
    roadmap_file = draft_dir / "docs" / "project-roadmap.md"

    if plan_file.is_file() and agents_file.is_file() and roadmap_file.is_file():
        plan_content = plan_file.read_text(encoding="utf-8")
        agents_content = agents_file.read_text(encoding="utf-8")
        roadmap_content = roadmap_file.read_text(encoding="utf-8")

        phase_matches = re.findall(r"\|\s*(\d{2})\s*\|.*?\|\s*`?([a-z-]+)`?\s*[✅🚀]*\s*\|", plan_content)
        for phase_id_str, status in phase_matches:
            phase_tag = f"Phase {phase_id_str}"
            if status == "passed":
                phase_mds = list(plans_dir.glob(f"phase-{phase_id_str}-*.md"))
                if phase_mds:
                    phase_text = phase_mds[0].read_text(encoding="utf-8")
                    if "## Evidence" in phase_text or "### Evidence" in phase_text:
                        evidence_part = re.split(r"#{2,3}\s*Evidence", phase_text)[-1][:300]
                        if len(evidence_part.strip()) > 30:
                            log_success(f"[Parity] {phase_tag} ({status}): Evidence verified in {phase_mds[0].name}")
                        else:
                            log_warning(f"[Parity] {phase_tag} marked passed but Evidence section is brief/empty")
                    else:
                        log_error(f"[Parity] {phase_tag} marked passed but missing '## Evidence' section")
                        all_passed = False

                sync_pattern = rf"(?:done|passed|hoàn thành).*?phase\s*{phase_id_str}|phase\s*{phase_id_str}.*?(?:done|passed|hoàn thành)"

                if re.search(sync_pattern, agents_content, re.IGNORECASE):
                    log_success(f"[Parity] {phase_tag} status synchronized in AGENTS.md")
                else:
                    log_error(f"[Parity] {phase_tag} marked passed in plan.md but NOT synchronized in AGENTS.md")
                    all_passed = False

                if re.search(sync_pattern, roadmap_content, re.IGNORECASE):
                    log_success(f"[Parity] {phase_tag} status synchronized in project-roadmap.md")
                else:
                    log_error(f"[Parity] {phase_tag} marked passed in plan.md but NOT synchronized in project-roadmap.md")
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
