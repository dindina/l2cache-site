#!/usr/bin/env python3
"""Fail the build when core SEO invariants drift."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://l2cache.amvo.store"
PUBLIC_PAGES = [
    "index.html", "support.html", "privacy.html", "intelligence.html",
    "changelog.html", "clipboard-history-mac.html", "mac-command-history.html",
    "comparison.html", "developer-clipboard.html", "custom-actions.html",
    "jwt-decoder-mac.html", "json-formatter-mac.html", "regex-clipboard-mac.html",
    "screenshot-ocr-mac.html", "sql-test-data-generator.html", "sitemap.html",
    "blog.html", "blog-regex-clipboard.html", "blog-sql-test-data.html",
    "blog-jwt-security.html", "blog-sqlite-fts5-hangs.html",
    "blog-swift-sqlite-concurrency.html", "l2cache-vs-maccy.html",
    "l2cache-vs-clipy.html", "l2cache-vs-paste.html",
]
ERRORS: list[str] = []


def public_url(filename: str) -> str:
    if filename == "index.html":
        return f"{SITE_URL}/en/"
    return f"{SITE_URL}/en/{filename.removesuffix('.html')}"


def count(source: str, pattern: str) -> int:
    return len(re.findall(pattern, source, flags=re.IGNORECASE))


def validate_page(path: Path, expected_canonical: str) -> None:
    source = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT)

    required_once = {
        "title": r"<title>.*?</title>",
        "description": r"<meta\s+name=[\"']description[\"']",
        "canonical": rf"""<link\s+rel=[\"']canonical[\"']\s+href=[\"']{re.escape(expected_canonical)}[\"']""",
        "h1": r"<h1(?:\s|>)",
        "og:title": r"<meta\s+property=[\"']og:title[\"']",
        "og:description": r"<meta\s+property=[\"']og:description[\"']",
        "og:url": rf"""<meta\s+property=[\"']og:url[\"']\s+content=[\"']{re.escape(expected_canonical)}[\"']""",
        "og:image": r"<meta\s+property=[\"']og:image[\"']",
        "twitter:card": r"<meta\s+name=[\"']twitter:card[\"']",
    }
    for label, pattern in required_once.items():
        matches = count(source, pattern)
        if matches != 1:
            ERRORS.append(f"{relative}: expected one {label}, found {matches}")

    if "hreflang=" in source:
        ERRORS.append(f"{relative}: hreflang must remain disabled while content is untranslated")

    for block in re.findall(
        r"""<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>""",
        source,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        try:
            json.loads(block)
        except json.JSONDecodeError as error:
            ERRORS.append(f"{relative}: invalid JSON-LD: {error}")


def validate_sitemap() -> None:
    path = ROOT / "out/l2cache/sitemap.xml"
    tree = ET.parse(path)
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text for node in tree.findall("s:url/s:loc", namespace)]
    expected = [public_url(filename) for filename in PUBLIC_PAGES]
    if urls != expected:
        ERRORS.append("out/l2cache/sitemap.xml: URLs do not match canonical English pages")
    if any(url and url.endswith(".html") for url in urls):
        ERRORS.append("out/l2cache/sitemap.xml: contains non-canonical .html URLs")


def main() -> None:
    for filename in PUBLIC_PAGES:
        validate_page(ROOT / filename, public_url(filename))
        validate_page(ROOT / "out/l2cache/en" / filename, public_url(filename))
    validate_sitemap()
    if ERRORS:
        print("SEO validation failed:", file=sys.stderr)
        for error in ERRORS:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"SEO validation passed for {len(PUBLIC_PAGES)} source and generated pages.")


if __name__ == "__main__":
    main()
