import os
import re

tools_dir = "/Users/dinesh/tech/L2Cache/tools"
site_dir = "/Users/dinesh/tech/l2cache-site"

# 1. Update all tool files in tools/
tool_files = [f for f in sorted(os.listdir(tools_dir)) if f.endswith('.html')]
print(f"Updating internal linking mesh across {len(tool_files)} tool pages...")

footer_links_markup = """      <ul class="footer-links">
        <li><a href="/en/">Home</a></li>
        <li><a href="/en/benchmark">Benchmark 2026</a></li>
        <li><a href="/en/best-mac-clipboard-managers">Best Mac Clipboard Managers</a></li>
        <li><a href="/en/clipboard-privacy-report">Privacy Report</a></li>
        <li><a href="/en/tools">Free Tools (63)</a></li>
        <li><a href="/en/privacy">Privacy Policy</a></li>
        <li><a href="/en/support">Support</a></li>
      </ul>"""

nav_links_markup = """    <ul class="nav-links">
      <li><a href="/en/developer-clipboard">Developers</a></li>
      <li><a href="/en/tools" class="active">Free Tools (63)</a></li>
      <li><a href="/en/benchmark">Benchmark</a></li>
      <li><a href="/en/best-mac-clipboard-managers">Buyer's Guide</a></li>
      <li><a href="/en/blog">Blog</a></li>
      <li><a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="nav-cta">Download for Mac</a></li>
    </ul>"""

tool_hub_callout = """
      <!-- Contextual SEO Research & Guides Hub -->
      <div style="background: #ffffff; border: 1.5px solid var(--border); border-radius: 18px; padding: 26px 28px; margin: 48px 0 24px; box-shadow: 0 4px 16px rgba(0,0,0,0.03);">
        <h3 style="font-size: 17px; font-weight: 800; color: #0a0a0a; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
          <span>📚</span> Recommended Research & Mac Clipboard Guides
        </h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; font-size: 13.5px;">
          <a href="/en/benchmark" style="color: #007a5a; text-decoration: none; font-weight: 700; background: #f0fdf9; border: 1px solid #c7f0e3; padding: 10px 14px; border-radius: 10px; display: flex; align-items: center; gap: 6px;">
            <span>📊</span> Mac Clipboard Benchmark (2026)
          </a>
          <a href="/en/best-mac-clipboard-managers" style="color: #007a5a; text-decoration: none; font-weight: 700; background: #f0fdf9; border: 1px solid #c7f0e3; padding: 10px 14px; border-radius: 10px; display: flex; align-items: center; gap: 6px;">
            <span>🏆</span> 7 Best Mac Clipboard Managers
          </a>
          <a href="/en/clipboard-privacy-report" style="color: #007a5a; text-decoration: none; font-weight: 700; background: #f0fdf9; border: 1px solid #c7f0e3; padding: 10px 14px; border-radius: 10px; display: flex; align-items: center; gap: 6px;">
            <span>🔒</span> State of Clipboard Privacy
          </a>
          <a href="/en/developer-clipboard" style="color: #007a5a; text-decoration: none; font-weight: 700; background: #f0fdf9; border: 1px solid #c7f0e3; padding: 10px 14px; border-radius: 10px; display: flex; align-items: center; gap: 6px;">
            <span>⚡</span> Developer Clipboard Guide
          </a>
        </div>
      </div>
"""

updated_tools = 0
for fname in tool_files:
    fpath = os.path.join(tools_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update footer links
    content = re.sub(r'<ul class=[\"\x27]footer-links[\"\x27]>[\s\S]*?<\/ul>', footer_links_markup, content)

    # 2. Update nav links
    content = re.sub(r'<ul class=[\"\x27]nav-links[\"\x27]>[\s\S]*?<\/ul>', nav_links_markup, content)

    # 3. Add contextual research hub callout before FAQ or before </div></div> closing article
    if "Recommended Research & Mac Clipboard Guides" not in content and fname != "index.html":
        if '<div class="faq-section">' in content:
            content = content.replace('<div class="faq-section">', tool_hub_callout + '\n      <div class="faq-section">')
        elif '<!-- FAQ' in content:
            content = re.sub(r'(<!-- FAQ[^\n]*\n)', tool_hub_callout + r'\n\1', content)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    updated_tools += 1

print(f"Updated internal links on {updated_tools} tool pages!")

# 2. Update index.html homepage footer and nav in l2cache-site
index_path = os.path.join(site_dir, "index.html")
if os.path.exists(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        home_content = f.read()

    home_footer_links = """    <ul class="footer-links">
      <li><a href="/en/developer-clipboard">Developers</a></li>
      <li><a href="/en/tools">Free Tools (63)</a></li>
      <li><a href="/en/benchmark">Benchmark 2026</a></li>
      <li><a href="/en/best-mac-clipboard-managers">Best Mac Clipboard Managers</a></li>
      <li><a href="/en/clipboard-privacy-report">Privacy Report</a></li>
      <li><a href="/en/comparison">Compare All</a></li>
      <li><a href="/en/privacy">Privacy Policy</a></li>
      <li><a href="/en/support">Support</a></li>
    </ul>"""

    home_content = re.sub(r'<ul class=[\"\x27]footer-links[\"\x27]>[\s\S]*?<\/ul>', home_footer_links, home_content)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(home_content)
    print("Updated homepage footer internal linking mesh!")

print("Internal linking mesh successfully built across the entire site!")
