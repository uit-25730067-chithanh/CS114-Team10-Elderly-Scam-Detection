"""
CS114 Final Project — Scam Detection
Semi-Automated Data Scraper & Provenance Extractor.

Crawls scam alert articles from legitimate Vietnamese news sites and official portals
(Dan Tri, VnExpress, Tuoi Tre, Chong Thu Rac, Canh Sat), extracts candidate scam
messages/dialogues quoted in the text, and generates a staging CSV with full provenance
(source_url, source_title, evidence_type, timestamp, content hash).
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Final

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Path resolution: find draft/scam-detection root
current_path = Path(__file__).resolve()
for parent in [current_path.parent, current_path.parent.parent, current_path.parent.parent.parent]:
    if (parent / "src" / "utils" / "helpers.py").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from src.utils.helpers import (
    CATEGORY_FAMILY_EMERGENCY,
    CATEGORY_FEAR_AUTHORITY,
    CATEGORY_HEALTH_GIFT,
    CATEGORY_PUBLIC_SERVICE,
    LABEL_SCAM,
    get_data_dir,
)

USER_AGENT: Final[str] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

# Heuristic patterns for inferring psychological trap category from quoted text
CATEGORY_KEYWORDS: Final[dict[str, list[str]]] = {
    CATEGORY_FEAR_AUTHORITY: [
        "công an", "viện kiểm sát", "toà án", "tòa án", "bắt tạm giam",
        "rửa tiền", "lệnh triệu tập", "phong tỏa tài khoản", "tạm giữ",
    ],
    CATEGORY_FAMILY_EMERGENCY: [
        "cấp cứu", "tai nạn", "bệnh viện", "viện phí", "mổ gấp", "con bị ngã",
    ],
    CATEGORY_HEALTH_GIFT: [
        "tặng thuốc", "tri ân", "miễn phí", "trúng thưởng", "hưu trí",
        "cao xương khớp", "sâm", "thảo dược",
    ],
    CATEGORY_PUBLIC_SERVICE: [
        "vneid", "định danh", "dịch vụ công", "sim 4g", "sim 5g",
        "khoá sim", "cập nhật thông tin", "trợ cấp",
    ],
}


def infer_scam_category(text: str) -> str:
    """Heuristic rule to suggest a preliminary scam category based on keywords."""
    lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return category
    return CATEGORY_FEAR_AUTHORITY  # Default fallback for manual review


def fetch_article_text(url: str, timeout: int = 10) -> tuple[str, str, str]:
    """
    Fetch an article page and extract (title, text_content, raw_html_hash).
    """
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()

    raw_hash = hashlib.sha256(resp.content).hexdigest()
    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.find("h1") or soup.find("title")
    title = title_tag.get_text().strip() if title_tag else "No Title"

    for s in soup(["script", "style", "nav", "footer", "header"]):
        s.decompose()

    paragraphs = [p.get_text().strip() for p in soup.find_all("p") if p.get_text().strip()]
    full_text = "\n".join(paragraphs)

    return title, full_text, raw_hash


def extract_candidate_quotes(full_text: str) -> list[str]:
    """
    Extract candidate SMS/dialogue quotes embedded in article text.
    Looks for text in double quotation marks or starting with SMS tags.
    """
    candidates: list[str] = []

    quote_matches = re.findall(r'["“]([^"”]{25,500})["”]', full_text)
    for q in quote_matches:
        cleaned = q.strip()
        has_keywords = any(
            kw in cleaned.lower()
            for kw_list in CATEGORY_KEYWORDS.values()
            for kw in kw_list
        )
        has_alert_clues = any(clue in cleaned.lower() for clue in ["http", "0", "vnd", "chuyển", "gửi", "bấm"])
        if has_keywords or has_alert_clues:
            candidates.append(cleaned)

    sms_lines = re.findall(r"(?:\[CẢNH BÁO\]|\[TB\]|\[THÔNG BÁO\])[^\n]{30,500}", full_text, re.IGNORECASE)
    for line in sms_lines:
        candidates.append(line.strip())

    unique_candidates: list[str] = []
    seen = set()
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    return unique_candidates


def process_url(url: str, collector_name: str = "Crawler") -> list[dict]:
    """
    Scrape a single URL, extract candidate quotes, and format provenance records.
    """
    print(f"[*] Fetching: {url}")
    try:
        title, text_content, raw_hash = fetch_article_text(url)
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return []

    quotes = extract_candidate_quotes(text_content)
    print(f"    Found {len(quotes)} candidate quotes in '{title[:50]}...'")

    records = []
    evidence_type = "gov_portal" if any(g in url for g in [".gov.vn", "canhsat.vn", "chongthurac.vn"]) else "news_press"

    for quote in quotes:
        records.append({
            "text": quote,
            "label": LABEL_SCAM,
            "scam_category": infer_scam_category(quote),
            "source": Path(url).netloc if hasattr(Path(url), "netloc") else url.split("/")[2],
            "source_url": url,
            "source_title": title,
            "evidence_type": evidence_type,
            "collector_name": collector_name,
            "notes": f"Scraped via semi-auto crawler at {datetime.now().strftime('%Y-%m-%d %H:%M')}; SHA256={raw_hash[:8]}",
        })

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape and extract candidate scam messages with provenance")
    parser.add_argument("--url", type=str, help="Single article URL to crawl")
    parser.add_argument("--file", type=str, help="Path to text file containing list of URLs (one per line)")
    parser.add_argument("--output", type=str, default=None, help="Output staging CSV path")
    parser.add_argument("--collector", type=str, default="Thanh_Lead", help="Collector name to log")

    args = parser.parse_args()

    urls_to_scrape: list[str] = []
    if args.url:
        urls_to_scrape.append(args.url)
    elif args.file:
        file_path = Path(args.file)
        if file_path.exists():
            urls_to_scrape = [line.strip() for line in file_path.read_text().splitlines() if line.strip() and not line.startswith("#")]
        else:
            print(f"[!] File not found: {args.file}")
            sys.exit(1)
    else:
        print("[*] No URL provided. Specify --url <URL> or --file <urls.txt>.")
        print("[*] Usage example: python3 data/scripts/data_scraper.py --url 'https://dantri.com.vn/...'")
        sys.exit(0)

    all_records = []
    for url in urls_to_scrape:
        recs = process_url(url, collector_name=args.collector)
        all_records.extend(recs)
        time.sleep(1)

    if not all_records:
        print("[*] No candidate records extracted.")
        sys.exit(0)

    df_candidates = pd.DataFrame(all_records)
    df_candidates.insert(0, "id", range(1, len(df_candidates) + 1))

    output_path = Path(args.output) if args.output else get_data_dir() / "raw" / "staging_scraped_candidates.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_candidates.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\n[+] SUCCESS: Extracted {len(df_candidates)} candidate messages to {output_path}")
    print(f"[+] The team can now review, verify, and copy approved rows to the Google Sheet!")


if __name__ == "__main__":
    main()
