#!/usr/bin/env python3
"""Fail the build when core SEO invariants drift."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import importlib.util

ROOT = Path(__file__).parent

# Pages the build actually localizes (see build.py HTML_FILES). For these the
# build now emits reciprocal hreflang + a self-referencing per-locale canonical,
# so the "no hreflang" guard below must NOT apply to them. Pages outside this
# set are English-only and must stay without hreflang.
_build_spec = importlib.util.spec_from_file_location("l2cache_build", ROOT / "build.py")
_build = importlib.util.module_from_spec(_build_spec)
_build_spec.loader.exec_module(_build)  # type: ignore[arg-type]
LOCALIZED_FILES = frozenset(_build.HTML_FILES) | frozenset(p.name for p in (ROOT / "l2cache-vs-*.html").parent.glob("l2cache-vs-*.html"))
SITE_URL = "https://l2cache.amvo.store"
PUBLIC_PAGES = [
    "index.html", "support.html", "privacy.html", "intelligence.html",
    "changelog.html", "clipboard-history-mac.html", "mac-command-history.html",
    "comparison.html", "benchmark.html", "best-mac-clipboard-managers.html",
    "clipboard-privacy-report.html", "developer-clipboard.html", "custom-actions.html",
    "jwt-decoder-mac.html", "json-formatter-mac.html", "regex-clipboard-mac.html",
    "screenshot-ocr-mac.html", "sql-test-data-generator.html", "sitemap.html",
    "blog.html", "blog-clipboard-automation-developer-workflows.html",
    "blog-regex-clipboard.html", "blog-sql-test-data.html",
    "blog-jwt-security.html", "blog-sqlite-fts5-hangs.html",
    "blog-swift-sqlite-concurrency.html", "blog-apple-intelligence-clipboard.html",
    "blog-developer-workflow-apple-intelligence.html",
    "blog-zero-cloud-mac-desktop-ai.html",
]

# Comparison pages are generated (generate_comparisons.py) and can grow over
# time; discover them from disk rather than hardcoding each slug.
import glob as _glob
PUBLIC_PAGES += sorted(_glob.glob(str(ROOT / "l2cache-vs-*.html")))
PUBLIC_PAGES = [p.split("/")[-1] for p in PUBLIC_PAGES]
PUBLIC_PAGES = [p for p in PUBLIC_PAGES if p.endswith(".html")]

ERRORS: list[str] = []


def public_url(filename: str) -> str:
    if filename == "index.html":
        return f"{SITE_URL}/en"
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

    if "hreflang=" in source and path.name not in LOCALIZED_FILES:
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
    # Tool pages are also built into /en/tools and included in the sitemap.
    # (tools/index.html maps to /en/tools itself, so no extra bare entry needed.)
    if (ROOT / "tools").is_dir():
        for tf in sorted(ROOT.glob("tools/*.html")):
            clean = "" if tf.name == "index.html" else f"/{tf.stem}"
            expected.append(f"{SITE_URL}/en/tools{clean}")
    if sorted(urls) != sorted(expected):
        ERRORS.append("out/l2cache/sitemap.xml: URLs do not match canonical English pages")
        missing = set(expected) - set(urls)
        extra = set(urls) - set(expected)
        if missing:
            ERRORS.append(f"  missing {len(missing)}: {sorted(missing)[:3]}...")
        if extra:
            ERRORS.append(f"  extra {len(extra)}: {sorted(extra)[:3]}...")
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
