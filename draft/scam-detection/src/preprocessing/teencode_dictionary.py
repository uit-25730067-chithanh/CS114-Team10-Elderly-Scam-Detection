"""Re-export teencode dictionary, leet-speak patterns, and unaccented compound mappings."""

from __future__ import annotations

from .leetspeak_data import LEET_SPEAK_PATTERNS, UNACCENTED_COMPOUNDS
from .teencode_data import TEENCODE_DICT

__all__ = [
    "TEENCODE_DICT",
    "LEET_SPEAK_PATTERNS",
    "UNACCENTED_COMPOUNDS",
]
