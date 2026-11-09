#!/usr/bin/env python3
"""Fail the build when core SEO invariants drift."""

from __future__ import annotations

import json
import os
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
LOCALIZED_FILES = frozenset(_build.LOCALIZED_FILES)
SITE_URL = os.getenv("SITE_URL", getattr(_build, "SITE_URL", "https://l2cache.app"))
sys.path.insert(0, str(ROOT / "scripts"))
import site_i18n  # noqa: E402  (the 2.0 homepage and its locales)

PUBLIC_PAGES = [
    "support.html", "privacy.html", "intelligence.html",
    "changelog.html", "clipboard-history-mac.html", "mac-command-history.html",
    "claude-code-history.html", "codex-history.html",
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
    "blog-agent-history-analytics.html",
    "blog-screenshot-ocr-search.html",
    "claude-code-cold-cache-resume-cost.html",
    "coding-agent-session-handoff.html",
    "coding-agent-memory-mcp-hooks.html",
    "universal-search-mac-developer.html",
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
        return f"{SITE_URL}/"
    return f"{SITE_URL}/en/{filename.removesuffix('.html')}"


def count(source: str, pattern: str) -> int:
    return len(re.findall(pattern, source, flags=re.IGNORECASE))


def validate_page(path: Path, expected_canonical: str | None, expected_hreflangs: int = 0) -> None:
    """expected_canonical=None for source files, whose canonical the build rewrites."""
    source = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT)

    canonical_re = re.escape(expected_canonical or "")
    required_once = {
        "title": r"<title>.*?</title>",
        "description": r"<meta\s+name=[\"']description[\"']",
        "canonical": rf"""<link\s+rel=[\"']canonical[\"']\s+href=[\"']{canonical_re}[\"']""",
        "h1": r"<h1(?:\s|>)",
        "og:title": r"<meta\s+property=[\"']og:title[\"']",
        "og:description": r"<meta\s+property=[\"']og:description[\"']",
        "og:url": rf"""<meta\s+property=[\"']og:url[\"']\s+content=[\"']{canonical_re}[\"']""",
        "og:image": r"<meta\s+property=[\"']og:image[\"']",
        "twitter:card": r"<meta\s+name=[\"']twitter:card[\"']",
    }
    if expected_canonical is None:
        del required_once["canonical"], required_once["og:url"]
    for label, pattern in required_once.items():
        matches = count(source, pattern)
        if matches != 1:
            ERRORS.append(f"{relative}: expected one {label}, found {matches}")

    if "hreflang=" in source and not expected_hreflangs and path.name not in LOCALIZED_FILES:
        ERRORS.append(f"{relative}: hreflang must remain disabled while content is untranslated")

    # Detect duplicate hreflangs and verify count on generated localized pages
    hreflangs = re.findall(
        r'<link\s+rel=[\'"]alternate[\'"]\s+hreflang=[\'"]([^\'"]+)[\'"]',
        source,
        flags=re.IGNORECASE,
    )
    if len(hreflangs) != len(set(hreflangs)):
        ERRORS.append(f"{relative}: duplicate hreflang declarations found: {hreflangs}")

    if expected_hreflangs:
        if len(hreflangs) != expected_hreflangs:
            ERRORS.append(
                f"{relative}: expected {expected_hreflangs} hreflang declarations, found {len(hreflangs)}"
            )

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
    # Sitemap coverage follows the build's published page list, including
    # English-only landing pages and other pages not in the metadata smoke set.
    sitemap_pages = ["index.html"] + [filename for filename in _build.LEGACY_FILES if (ROOT / filename).is_file()]
    sitemap_pages += [
        path.name for path in ROOT.glob("l2cache-vs-*.html")
        if path.name not in sitemap_pages
    ]
    expected = [public_url(filename) for filename in sitemap_pages]
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


def validate_home() -> None:
    """2.0 homepage: one page per published locale, indexable, reciprocal hreflang."""
    published = site_i18n.complete_locales()
    if os.getenv("I18N_STRICT") == "1" and len(published) != len(site_i18n.LOCALES):
        ERRORS.append(f"homepage: I18N_STRICT=1 but only {published} are complete")
    for lang in published:
        page = ROOT / "out/l2cache" / ("index.html" if lang == "en" else f"{lang}/index.html")
        if not page.is_file():
            ERRORS.append(f"{page.relative_to(ROOT)}: missing")
            continue
        validate_page(page, site_i18n.page_url(lang), expected_hreflangs=len(published) + 1)
        if "noindex" in page.read_text(encoding="utf-8"):
            ERRORS.append(f"{page.relative_to(ROOT)}: still noindex")


# Claims about the whole app that PUBLISHABLE_CLAIMS_MATRIX blocks (link previews and Translate make
# network requests). Feature-level statements such as "decodes JWTs locally" stay allowed.
BLOCKED_CLAIMS = [
    r"zero network (?:requests|connectivity)",
    r"L2Cache is 100% offline",
    r"(?:full|complete) transcripts?",
    r"we have no servers, no analytics",
    r"what we collect\W+nothing",
]


def validate_claims() -> None:
    pattern = re.compile("|".join(BLOCKED_CLAIMS), re.IGNORECASE)
    for path in (ROOT / "out/l2cache").rglob("*"):
        if path.suffix not in {".html", ".txt"} or "tools" in path.relative_to(ROOT / "out/l2cache").parts[:2]:
            continue
        text = re.sub(r"<[^>]+>", " ", path.read_text(encoding="utf-8", errors="ignore"))
        for m in pattern.finditer(re.sub(r"\s+", " ", text)):
            ERRORS.append(f"{path.relative_to(ROOT)}: blocked claim \"{m.group(0)}\"")


def validate_domain() -> None:
    """Nothing in the L2Cache output may point at the old domain (it would cost a redirect hop)."""
    for path in (ROOT / "out/l2cache").rglob("*"):
        if path.suffix in {".html", ".txt", ".xml", ".json", ".js"} and "l2cache.amvo.store" in path.read_text(encoding="utf-8", errors="ignore"):
            ERRORS.append(f"{path.relative_to(ROOT)}: still references l2cache.amvo.store")


def main() -> None:
    for filename in PUBLIC_PAGES:
        validate_page(ROOT / filename, None)
        validate_page(ROOT / "out/l2cache/en" / filename, public_url(filename))
    validate_home()
    if (ROOT / "teams/index.html").is_file():
        validate_page(ROOT / "out/teams/index.html", "https://teams.amvo.store/")
    validate_domain()
    validate_claims()
    validate_sitemap()
    if ERRORS:
        print("SEO validation failed:", file=sys.stderr)
        for error in ERRORS:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"SEO validation passed for {len(PUBLIC_PAGES)} source and generated pages.")


if __name__ == "__main__":
    main()
