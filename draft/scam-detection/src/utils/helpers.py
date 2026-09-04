"""
CS114 Final Project — Scam Detection
Shared Constants and Utility Functions for Vietnamese Elderly Scam Detection.
"""

from __future__ import annotations

import os
import random
from pathlib import Path
from typing import Final

import numpy as np

# ─── Reproducibility Constants ──────────────────────────────────────────────
RANDOM_STATE: Final[int] = 42
TEST_SIZE: Final[float] = 0.20
VALIDATION_SIZE: Final[float] = 0.15

# ─── Data Schema & Class Labels ─────────────────────────────────────────────
LABEL_NORMAL: Final[int] = 0
LABEL_SCAM: Final[int] = 1

LABEL_NAMES: Final[dict[int, str]] = {
    LABEL_NORMAL: "Bình thường",
    LABEL_SCAM: "Lừa đảo",
}

# 4 Core Psychological Manipulation Bait Categories + None
CATEGORY_FEAR_AUTHORITY: Final[str] = "fear_authority"       # Đe dọa / Giả danh Công an, Viện Kiểm Sát
CATEGORY_FAMILY_EMERGENCY: Final[str] = "family_emergency"   # Cấp cứu người thân, tai nạn gấp
CATEGORY_HEALTH_GIFT: Final[str] = "health_gift"             # Tặng thuốc, quà tri ân hưu trí
CATEGORY_PUBLIC_SERVICE: Final[str] = "public_service"       # Giả mạo VNeID, SIM, dịch vụ công
CATEGORY_NONE: Final[str] = "none"                           # Bình thường

SCAM_CATEGORIES: Final[list[str]] = [
    CATEGORY_FEAR_AUTHORITY,
    CATEGORY_FAMILY_EMERGENCY,
    CATEGORY_HEALTH_GIFT,
    CATEGORY_PUBLIC_SERVICE,
    CATEGORY_NONE,
]

CATEGORY_DESCRIPTIONS: Final[dict[str, str]] = {
    CATEGORY_FEAR_AUTHORITY: "Đe dọa / Giả danh cơ quan công quyền (Công an, Tòa án, Viện kiểm sát)",
    CATEGORY_FAMILY_EMERGENCY: "Thúc ép khẩn cấp gia đình (Con cháu tai nạn, viện phí mổ gấp)",
    CATEGORY_HEALTH_GIFT: "Dụ dỗ sức khỏe & tri ân (Tặng thuốc đông y miễn phí, quà hưu trí trúng vàng)",
    CATEGORY_PUBLIC_SERVICE: "Giả mạo dịch vụ công (Cập nhật VNeID mức 2, đổi SIM 4G/5G, trợ cấp)",
    CATEGORY_NONE: "Tin nhắn thông thường hoặc dịch vụ chính thống",
}

# ─── Target Metrics (Brainstorm Contract) ───────────────────────────────────
TARGET_F1_SCORE: Final[float] = 0.88
TARGET_RECALL_SCAM: Final[float] = 0.92


# ─── Reproducibility Helpers ────────────────────────────────────────────────
def set_seeds(seed: int = RANDOM_STATE) -> None:
    """Set random seeds across Python and NumPy for strict reproducibility."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


# ─── Directory & Path Resolution ────────────────────────────────────────────
def get_project_root() -> Path:
    """
    Return the root directory of the working project (draft/scam-detection).
    """
    return Path(__file__).resolve().parent.parent.parent


def get_data_dir() -> Path:
    """Return the path to data directory."""
    return get_project_root() / "data"


def get_models_dir() -> Path:
    """Return the path to models directory."""
    return get_project_root() / "models"


def get_reports_dir() -> Path:
    """Return the path to reports directory."""
    return get_project_root() / "reports"
