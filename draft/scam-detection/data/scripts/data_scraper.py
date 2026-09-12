"""
================================================================================
DỰ ÁN CUỐI KỲ CS114 - MÁY HỌC (NHÓM 10 - UIT)
CÔNG CỤ CÀO DỮ LIỆU BÁN TỰ ĐỘNG & BÓC TÁCH NGUỒN GỐC (DATA SCRAPER & PROVENANCE)
================================================================================
Mục đích:
  - Hỗ trợ các thành viên trong nhóm (đặc biệt là Sơn & Cẩm) cào nhanh các bài viết cảnh báo
    lừa đảo từ các cổng thông tin chính thống và báo chí uy tín của Việt Nam:
    (Dân Trí, VnExpress, Tuổi Trẻ, chongthurac.vn, canhsat.vn, Cục ATTT).
  - Tự động trích xuất các câu trích dẫn tin nhắn SMS / hội thoại lừa đảo đặt trong ngoặc kép
    hoặc gắn mác [CẢNH BÁO], [THÔNG BÁO].
  - Gợi ý phân loại sơ bộ 4 nhóm bẫy tâm lý (scam_category) dựa trên từ khóa nhận diện.
  - Tự động ghi nhận đầy đủ 8 cột kiểm toán nguồn gốc (source_url, source_title, SHA256 hash).
  - Xuất ra file CSV tạm thời (staging) để thành viên kiểm duyệt trước khi đưa lên Google Sheet.

Hướng dẫn sử dụng cho thành viên trong nhóm:
  1. Cào từ 1 đường link bài báo đơn lẻ:
     python3 data_scraper.py --url "https://dantri.com.vn/phap-luat/canh-bao-chieu-tro-lua-dao..."
  2. Cào hàng loạt từ 1 file chứa danh sách link (mỗi dòng 1 link):
     python3 data_scraper.py --file danh_sach_link.txt --collector "Hoàng Cao Sơn"
================================================================================
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
from urllib.parse import urlparse

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
    CATEGORY_PUBLIC_SERVICE: [
        "vneid", "định danh", "mức 2", "dịch vụ công", "bộ công an", "cccd", "căn cước",
        "đồng bộ dữ liệu", "sai lệch thông tin", "bảo hiểm xã hội", "bhxh", "vssid",
        "lương hưu", "trợ cấp", "bảo hiểm y tế", "bhyt", "sim 4g", "sim 5g", "khoá sim",
        "khoa sim", "khóa sim", "chuẩn hóa", "thuê bao", "cục viễn thông", "evn",
        "tiền điện", "cắt điện", "tổng cục thuế", "hoàn thuế", "quyết toán thuế",
        "thuế điện tử", "cập nhật thông tin",
    ],
    CATEGORY_HEALTH_GIFT: [
        "tặng thuốc", "chữa dứt điểm", "cao xương khớp", "tiểu đường", "sữa non",
        "viện 108", "bệnh viện quân y", "thảo dược", "đông y gia truyền", "tri ân",
        "quà tặng", "quà tri ân", "miễn phí", "trúng thưởng", "hưu trí", "sâm",
        "mã quay thưởng", "nhận quà", "hội thảo sức khỏe", "khám bệnh miễn phí",
        "tiền ship", "phí vận chuyển", "voucher", "trúng vàng", "thực phẩm chức năng",
    ],
    CATEGORY_FEAR_AUTHORITY: [
        "công an", "viện kiểm sát", "toà án", "tòa án", "bắt tạm giam",
        "rửa tiền", "lệnh triệu tập", "phong tỏa tài khoản", "tạm giữ",
        "thi hành án", "lệnh bắt",
    ],
    CATEGORY_FAMILY_EMERGENCY: [
        "cấp cứu", "tai nạn", "bệnh viện", "viện phí", "mổ gấp", "con bị ngã",
        "cháu bị tai nạn", "chuyển tiền gấp",
    ],
}

# Regex patterns to strip journalist narrative framing from extracted quotes
JOURNALIST_PREFIX_PATTERNS: Final[list[re.Pattern]] = [
    re.compile(r"^(?:(?:Chị|Anh|Bà|Ông|Nạn nhân)\s+[A-ZĐ]\.?\s+(?:cho biết|kể lại|chia sẻ|nhận được|phản ánh)(?::|,)?\s*)", re.IGNORECASE),
    re.compile(r"^(?:(?:Theo|Cụ thể|Điển hình là|Theo thông tin từ|Theo phản ánh|Theo cơ quan công an)(?::|,)?\s*)", re.IGNORECASE),
    re.compile(r"^(?:(?:Nội dung tin nhắn|Tin nhắn có nội dung|Kẻ gian nhắn tin|Đối tượng gửi tin nhắn)(?:\s+như sau)?(?::|,)?\s*)", re.IGNORECASE),
]


def clean_scam_quote(text: str) -> str:
    """Strip leading/trailing quotes and journalistic narrative framing."""
    cleaned = text.strip()
    cleaned = re.sub(r"^[\"“'«]+|[\"”'»]+$", "", cleaned).strip()
    for pat in JOURNALIST_PREFIX_PATTERNS:
        cleaned = pat.sub("", cleaned).strip()
    cleaned = re.sub(r"^[\"“'«]+|[\"”'»]+$", "", cleaned).strip()
    return cleaned


def infer_scam_category(text: str) -> str:
    """
    Deterministic rule to categorize scam messages into standard categories.
    Evaluates specific institutional/trap patterns before general fallbacks.
    """
    lower = text.lower()

    # 1. Public service / identity / utilities / taxes
    if any(kw in lower for kw in CATEGORY_KEYWORDS[CATEGORY_PUBLIC_SERVICE]):
        return CATEGORY_PUBLIC_SERVICE

    # 2. Health / gifts / medical miracles
    if any(kw in lower for kw in CATEGORY_KEYWORDS[CATEGORY_HEALTH_GIFT]):
        return CATEGORY_HEALTH_GIFT

    # 3. Fear authority (police, prosecutors, arrest warrants)
    if any(kw in lower for kw in CATEGORY_KEYWORDS[CATEGORY_FEAR_AUTHORITY]):
        return CATEGORY_FEAR_AUTHORITY

    # 4. Family emergency (hospital fee, urgent surgery)
    if any(kw in lower for kw in CATEGORY_KEYWORDS[CATEGORY_FAMILY_EMERGENCY]):
        return CATEGORY_FAMILY_EMERGENCY

    return CATEGORY_PUBLIC_SERVICE  # Default fallback for administrative/SMS scams


def fetch_article_text(url: str, timeout: int = 10) -> tuple[str, str, str, list[str]]:
    """
    Fetch an article page and extract (title, text_content, raw_html_hash, blockquotes).

    Args:
        url: The web URL to scrape.
        timeout: Network request timeout in seconds (default: 10).

    Returns:
        tuple containing:
            - title (str): Title of the article.
            - full_text (str): Clean text content of the article paragraphs (deduplicated).
            - raw_hash (str): SHA256 hex digest of the raw HTML content.
            - extracted_blockquotes (list[str]): Explicit blockquote/q elements.
    """
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"

    raw_hash = hashlib.sha256(resp.content).hexdigest()
    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.find("h1") or soup.find("title")
    title = title_tag.get_text().strip() if title_tag else "No Title"

    # Capture explicit quote tags before decomposing
    quote_elements = soup.find_all(["blockquote", "q"])
    extracted_blockquotes = [q.get_text().strip() for q in quote_elements if len(q.get_text().strip()) >= 25]

    for s in soup(["script", "style", "nav", "footer", "header", "aside"]):
        s.decompose()

    # Chỉ trích xuất từ container nội dung bài báo để tránh trùng lặp giữa thẻ div cha và p con
    content_container = soup.find(["article", "main"]) or soup.body or soup
    paragraphs = []
    seen_texts = set()

    # Ưu tiên lấy các thẻ p văn bản chính
    for p in content_container.find_all("p"):
        txt = p.get_text(strip=True)
        if txt and len(txt) >= 15 and txt not in seen_texts:
            seen_texts.add(txt)
            paragraphs.append(txt)

    # Nếu trang không dùng thẻ p mà dùng thẻ div lẻ lá (leaf divs), bổ sung fallback an toàn
    if not paragraphs:
        for d in content_container.find_all("div"):
            if not d.find(["p", "div"]):
                txt = d.get_text(strip=True)
                if txt and len(txt) >= 15 and txt not in seen_texts:
                    seen_texts.add(txt)
                    paragraphs.append(txt)

    full_text = "\n".join(paragraphs)

    return title, full_text, raw_hash, extracted_blockquotes


def extract_candidate_quotes(full_text: str, extra_quotes: list[str] | None = None) -> list[str]:
    """
    Extract candidate SMS/dialogue quotes embedded in article text.
    Looks for text in double quotation marks, HTML quotes, or SMS tags.
    Strips journalistic framing to keep clean victim-facing message text.
    """
    candidates: list[str] = []

    # 1. Quoted segments
    quote_matches = re.findall(r'["“«]([^"”»]{25,500})["”»]', full_text)
    for q in quote_matches:
        cleaned = clean_scam_quote(q)
        has_keywords = any(
            kw in cleaned.lower()
            for kw_list in CATEGORY_KEYWORDS.values()
            for kw in kw_list
        )
        has_alert_clues = any(clue in cleaned.lower() for clue in ["http", "0", "vnd", "chuyển", "gửi", "bấm", "cập nhật", "liên hệ", "hotline"])
        if (has_keywords or has_alert_clues) and len(cleaned) >= 25:
            candidates.append(cleaned)

    # 2. SMS lines starting with headers like [VNeID], [BHXH], [CẢNH BÁO], [TB], [DVC]
    sms_lines = re.findall(
        r"(?:\[(?:VNeID|BHXH|EVN|DVC|TTCS|156|CẢNH BÁO|TB|THÔNG BÁO)\]|[0-9]{3,4}:)[^\n]{25,500}",
        full_text,
        re.IGNORECASE,
    )
    for line in sms_lines:
        cleaned = clean_scam_quote(line)
        if len(cleaned) >= 25:
            candidates.append(cleaned)

    # 3. Add explicit HTML blockquotes/elements
    if extra_quotes:
        for eq in extra_quotes:
            cleaned = clean_scam_quote(eq)
            if len(cleaned) >= 25:
                candidates.append(cleaned)

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
        title, text_content, raw_hash, extra_quotes = fetch_article_text(url)
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")
        return []

    quotes = extract_candidate_quotes(text_content, extra_quotes=extra_quotes)
    print(f"    Found {len(quotes)} candidate quotes in '{title[:50]}...'")

    records = []
    evidence_type = "gov_portal" if any(g in url for g in [".gov.vn", "canhsat.vn", "chongthurac.vn", "tinnhiemmang.vn"]) else "news_press"

    parsed_url = urlparse(url)
    source_domain = parsed_url.netloc if parsed_url.netloc else (parsed_url.path.split("/")[0] if parsed_url.path else "unknown")

    for quote in quotes:
        records.append({
            "text": quote,
            "label": LABEL_SCAM,
            "scam_category": infer_scam_category(quote),
            "source": source_domain,
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
            urls_to_scrape = [
                line.strip()
                for line in file_path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.startswith("#")
            ]
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
