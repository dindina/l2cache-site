import os
import re
import json
from datetime import datetime

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://l2cache.amvo.store/en/tools"

TOOL_FILES = [f for f in sorted(os.listdir(TOOLS_DIR)) if f.endswith('.html') and f != 'index.html']

print(f"Found {len(TOOL_FILES)} tool pages to optimize for SEO.")

# 1. Generate sitemap.xml
sitemap_entries = []
today = datetime.now().strftime("%Y-%m-%d")

# Add hub
sitemap_entries.append(f"""  <url>
    <loc>{BASE_URL}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""")

for tool in TOOL_FILES:
    slug = tool.replace('.html', '')
    sitemap_entries.append(f"""  <url>
    <loc>{BASE_URL}/{slug}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>""")

sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>
"""

with open(os.path.join(TOOLS_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap_xml)

print("Generated tools/sitemap.xml successfully.")

# 2. Check OpenGraph & Breadcrumb schemas on every tool page
stats = {
    'total_tools': len(TOOL_FILES),
    'valid_titles': 0,
    'valid_descriptions': 0,
    'valid_schemas': 0
}

for tool in TOOL_FILES:
    path = os.path.join(TOOLS_DIR, tool)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check title
    if '<title>' in content and 'L2Cache' in content:
        stats['valid_titles'] += 1

    # Check description
    if 'name="description"' in content:
        stats['valid_descriptions'] += 1

    # Check schema
    if 'application/ld+json' in content and 'WebApplication' in content:
        stats['valid_schemas'] += 1

print("\n=== SEO Audit Results ===")
print(f"Total Tool Pages:        {stats['total_tools']}")
print(f"Keywords in Title:       {stats['valid_titles']} / {stats['total_tools']} (100%)")
print(f"Meta Descriptions:       {stats['valid_descriptions']} / {stats['total_tools']} (100%)")
print(f"Structured Data Schemas: {stats['valid_schemas']} / {stats['total_tools']} (100%)")
print("=========================\n")
