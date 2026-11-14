#!/usr/bin/env python3
"""Export all site blog posts and pillars into Hashnode-ready Markdown files with YAML frontmatter.

Each file has:
- YAML frontmatter with title, subtitle, slug, tags, cover image, and canonical URL pointing to l2cache.app
- Clean Markdown body with live HTTPS assets
- Absolute links
"""
import os, sys, re, json, html
from html.parser import HTMLParser

SITE = "/Users/dinesh/tech/l2cache-site"
OUT_DIR = "/Users/dinesh/tech/L2Cache/docs/hashnode"
BASE = "https://l2cache.app"

os.makedirs(OUT_DIR, exist_ok=True)

class Markdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.links, self.lists, self.quotes = [], [], [], []
        self.pre = self.skip = 0
        self.table = None

    def emit(self, s):
        if self.table is not None and self.table["cell"] is not None:
            self.table["cell"].append(s)
        else:
            self.out.append(s)

    def block(self, s=""):
        self.out.append("\n\n" + s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip or tag in ("summary", "details", "nav", "footer", "script", "style"):
            self.skip += 1
            return
        if tag in ("h2", "h3", "h4"):
            self.block("#" * int(tag[1]) + " ")
        elif tag == "p":
            prefix = "> " if self.quotes else ""
            self.block(prefix)
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag == "pre":
            self.pre = 1
            self.block("```text\n")
        elif tag == "blockquote":
            self.quotes.append(1)
            self.block("> ")
        elif tag == "a":
            href = a.get("href", "")
            if href.startswith("/"):
                href = f"{BASE}{href}"
            elif not href.startswith("http") and not href.startswith("#"):
                href = f"{BASE}/en/{href.replace('.html', '')}"
            self.links.append(href)
            self.emit("[")
        elif tag == "img":
            src = a.get("src", "")
            if src.startswith("/"):
                src = f"{BASE}{src}"
            elif not src.startswith("http"):
                src = f"{BASE}/{src.lstrip('./')}"
            alt = a.get("alt", "")
            self.block(f"![{alt}]({src})\n")
        elif tag == "li":
            self.block("- ")

    def handle_endtag(self, tag):
        if self.skip:
            self.skip -= 1
            return
        if tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag == "pre":
            self.pre = 0
            self.emit("\n```\n")
        elif tag == "blockquote" and self.quotes:
            self.quotes.pop()
        elif tag == "a" and self.links:
            href = self.links.pop()
            self.emit(f"]({href})")

    def handle_data(self, data):
        if self.skip:
            return
        self.emit(data)

    def markdown(self):
        txt = "".join(self.out).strip()
        txt = re.sub(r'\n{3,}', '\n\n', txt)
        return txt

def parse_html_page(filepath, slug, default_tags):
    raw = open(filepath, "r", encoding="utf-8").read()
    
    title_match = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = html.unescape(title_match.group(1)).strip() if title_match else slug.replace("-", " ").title()
    title = re.sub(r'<[^>]+>', '', title)
    
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', raw)
    desc = html.unescape(desc_match.group(1)).strip() if desc_match else ""
    
    cover_match = re.search(r'<meta (?:property|name)="(?:og:image|twitter:image)" content="([^"]*)"', raw)
    cover = cover_match.group(1).replace("l2cache.amvo.store", "l2cache.app") if cover_match else ""
    if not cover or "icon.png" in cover:
        # Check first image inside body
        img_match = re.search(r'<img [^>]*src="([^"]+)"', raw)
        if img_match and "icon.png" not in img_match.group(1):
            src = img_match.group(1)
            cover = f"{BASE}/{src.lstrip('./')}" if not src.startswith("http") else src

    # Extract body content between h1 and cta/footer
    body_part = raw.split("</h1>", 1)[1] if "</h1>" in raw else raw
    for split_tag in ['<div class="cta-box">', '<div class="related">', '<footer', '<div class="howto">']:
        if split_tag in body_part:
            body_part = body_part.split(split_tag, 1)[0]
            
    body_part = re.sub(r'<p class="meta">.*?</p>', '', body_part, flags=re.S)
    body_part = re.sub(r'<a href="blog.html"[^>]*>.*?</a>', '', body_part, flags=re.S)

    parser = Markdown()
    parser.feed(body_part)
    body_md = parser.markdown()
    
    canonical = f"{BASE}/en/{slug}"
    
    frontmatter = f"""---
title: "{title}"
subtitle: "{desc}"
slug: "{slug}"
tags: {json.dumps(default_tags)}
cover: "{cover}"
canonical: "{canonical}"
---

"""
    footer = f"\n\n---\n\n*Originally published at [l2cache.app]({canonical}).*\n"
    return frontmatter + body_md + footer

def main():
    pillars_file = os.path.join(SITE, "scripts/backlinks/pillars.json")
    pillars = json.load(open(pillars_file)) if os.path.exists(pillars_file) else []
    
    exported = []
    
    # 1. Export Pillars
    for idx, p in enumerate(pillars, start=1):
        slug = p["slug"]
        html_file = os.path.join(SITE, f"{slug}.html")
        if not os.path.exists(html_file):
            continue
        md = parse_html_page(html_file, slug, p.get("devto_tags", ["ai", "productivity", "macos"]))
        out_name = f"{idx:02d}-{slug}.md"
        out_path = os.path.join(OUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
        exported.append((idx, slug, out_name, out_path))
        print(f"Exported [{idx:02d}]: {slug} -> {out_name}")

    # 2. Export Technical Blog Posts
    curr_idx = len(exported) + 1
    blog_files = [f for f in os.listdir(SITE) if f.startswith("blog-") and f.endswith(".html")]
    blog_files.sort()
    
    default_blog_tags = {
        "blog-swift-sqlite-concurrency": ["swift", "macos", "sqlite", "ios"],
        "blog-sqlite-fts5-hangs": ["sqlite", "performance", "database", "macos"],
        "blog-apple-intelligence-clipboard": ["apple", "ai", "macos", "swift"],
        "blog-developer-workflow-apple-intelligence": ["apple", "ai", "productivity", "developer-tools"],
        "blog-zero-cloud-mac-desktop-ai": ["privacy", "ai", "macos", "local-ai"],
        "blog-screenshot-ocr-search": ["ocr", "macos", "productivity", "search"],
        "blog-agent-history-analytics": ["ai", "claude", "analytics", "developer-tools"],
        "blog-jwt-security": ["security", "jwt", "auth", "developer-tools"],
        "blog-regex-clipboard": ["regex", "productivity", "developer-tools", "macos"],
        "blog-sql-test-data": ["sql", "testing", "database", "productivity"],
        "blog-clipboard-automation-developer-workflows": ["automation", "productivity", "macos", "developer-tools"]
    }
    
    for f in blog_files:
        slug = f.replace(".html", "")
        html_path = os.path.join(SITE, f)
        tags = default_blog_tags.get(slug, ["macos", "developer-tools", "productivity"])
        md = parse_html_page(html_path, slug, tags)
        out_name = f"{curr_idx:02d}-{slug}.md"
        out_path = os.path.join(OUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write(md)
        exported.append((curr_idx, slug, out_name, out_path))
        print(f"Exported [{curr_idx:02d}]: {slug} -> {out_name}")
        curr_idx += 1

    # Generate INDEX.md in OUT_DIR
    index_path = os.path.join(OUT_DIR, "README.md")
    with open(index_path, "w", encoding="utf-8") as idx_file:
        idx_file.write("# Hashnode Articles Library (Pre-formatted Markdown)\n\n")
        idx_file.write("All articles below include pre-configured YAML frontmatter, canonical tags, absolute image links, and code highlighting.\n\n")
        idx_file.write("| # | Slug | Markdown File | Canonical Link |\n")
        idx_file.write("|---|---|---|---|\n")
        for num, slug, fname, fpath in exported:
            idx_file.write(f"| {num:02d} | `{slug}` | [`{fname}`]({fname}) | [{slug}]({BASE}/en/{slug}) |\n")
        idx_file.write("\n### Quick Clipboard Command:\n")
        idx_file.write("To copy any article directly to your clipboard, run:\n")
        idx_file.write("```bash\n")
        idx_file.write("pbcopy < docs/hashnode/01-why-claude-resume-burns-plan.md\n")
        idx_file.write("```\n")
        
    print(f"\nDone! Successfully generated {len(exported)} Hashnode articles in {OUT_DIR}")

if __name__ == "__main__":
    main()
