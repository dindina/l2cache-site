#!/usr/bin/env python3
"""Check that every internal link on the 2.0 homepage resolves (Sprint C1).

  python3 build.py && python3 scripts/check_home_links.py

Root-relative links (/en/<slug>, /en/tools/<tool>, /) must map to a built page in out/l2cache/,
#anchors must match an id on the page, and relative asset paths must exist next to the source.
External links are listed but not fetched. Exits 1 if anything is broken.
"""
import os
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "prototypes", "native-mac", "index.html")
OUT = os.path.join(ROOT, "out", "l2cache")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])


def built_page(path):
    """A root-relative path resolves if out/l2cache has it as a file, <path>.html or <path>/index.html."""
    rel = path.strip("/")
    if not rel:
        return True  # "/" is the homepage itself
    base = os.path.join(OUT, rel)
    return any(os.path.isfile(p) for p in (base, base + ".html", os.path.join(base, "index.html")))


def main():
    if not os.path.isdir(os.path.join(OUT, "en")):
        sys.exit("out/l2cache/en is missing; run `python3 build.py` first.")
    parser = Links()
    with open(SOURCE, encoding="utf-8") as f:
        parser.feed(f.read())

    broken, external, checked = [], set(), 0
    for href in parser.hrefs:
        parts = urlsplit(href)
        if parts.scheme in ("http", "https", "mailto"):
            external.add(href)
            continue
        checked += 1
        if href.startswith("#"):
            if href[1:] and href[1:] not in parser.ids:
                broken.append(f"{href}  (no element with this id)")
        elif href.startswith("/"):
            if not built_page(parts.path):
                broken.append(f"{href}  (no built page in out/l2cache)")
        elif not os.path.exists(os.path.join(os.path.dirname(SOURCE), parts.path)):
            broken.append(f"{href}  (file not found next to the source)")

    print(f"{checked} internal links checked, {len(external)} external skipped.")
    if broken:
        print(f"{len(broken)} broken:")
        for b in sorted(set(broken)):
            print(f"  {b}")
        sys.exit(1)
    print("All internal links resolve.")


if __name__ == "__main__":
    main()
