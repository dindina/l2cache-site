"""Turn docs/medium/<src>/article.html into l2cache-site article pages (site-first, Medium imports them)."""
import html, json, os, re, shutil

MEDIUM = "/Users/dinesh/tech/L2Cache/docs/medium"
SITE = "/Users/dinesh/tech/l2cache-site"
TEMPLATE = open(f"{SITE}/claude-code-cold-cache-resume-cost.html").read()
DATE, DATE_TEXT = "2026-11-11", "November 11, 2026"
MODIFIED, MODIFIED_TEXT = "2026-11-13", "November 13, 2026"
APP = "https://apps.apple.com/us/app/l2cache/id6774423992?mt=12"

ARTICLES = [
    dict(src="one-search-developer-memory", slug="search-developer-history-mac", date=("2026-11-13", "November 13, 2026"),
         seo_title="Search Claude Code History, Terminal and Clipboard at Once",
         section="clipboard",
         tag="Search · Measured", short="One Search Box for Everything",
         desc="Seven real questions asked of one search box over agent chats, terminal, clipboard, screenshots and git: what it found, what it missed, what I fixed.",
         related=[("universal-search-mac-developer", "Search", "One ⌘K search for everything you did as a developer"),
                  ("screenshot-ocr-mac", "Screenshots", "Search the text inside your screenshots")],
         cta=("Ask one place", "L2Cache searches your agent sessions, terminal history, clipboard and screenshots together, on your Mac.")),
    dict(src="screenshot-to-agent", slug="copy-screenshots-errors-to-coding-agents", date=("2026-11-13", "November 13, 2026"),
         seo_title="How to Paste Screenshots and Errors Into Claude Code and Codex",
         section="coding-agents",
         tag="Coding agents · Measured", short="Copy Screenshots and Errors to Agents",
         desc="Ctrl+V pastes one screenshot into Claude Code. Hand coding agents several copies at once instead: screenshots go as text plus a file path, 10× cheaper.",
         related=[("coding-agent-memory-mcp-hooks", "Coding agents", "Coding agent memory with MCP and hooks"),
                  ("screenshot-ocr-mac", "Screenshots", "Search the text inside your screenshots")],
         cta=("Copy it, then ask", "L2Cache hands Claude Code and Codex what you just copied: errors, commands and screenshots as text.")),
    dict(src="claude-code-cold-session-cost", slug="claude-code-cold-session-tax", seo_title="Claude Code Prompt Cache: Why a Cold Session Costs 12–80× More",
         section="context-cost",
         tag="Claude Code · Measured", short="Stretch Your Weekly Limit",
         desc="When Claude Code's prompt cache expires, the first message back costs 12–80× a warm turn. Measured over 10,000 requests, with three rules and a script.",
         related=[("claude-code-cold-cache-resume-cost", "Claude Code", "Why resuming a cold Claude Code session costs more"),
                  ("coding-agent-session-handoff", "Coding agents", "Start a fresh coding-agent session without losing context")],
         cta=("Know before a session goes cold", "L2Cache warns you before a heavy session's cache expires and offers a fresh start with a handoff.")),
    dict(src="claude-code-plan-limit-burn", slug="why-claude-resume-burns-plan", seo_title="Why claude --resume Burns Your $30 Plan by Wednesday",
         date=("2026-11-14", "November 14, 2026"),
         section="context-cost",
         tag="Claude Code · Limits", short="Why Resume Burns Your Plan",
         desc="Why sending one prompt after a break in Claude Code costs up to 40× a normal turn, how prompt cache TTLs actually work, and how to stop mid-week lockouts.",
         related=[("claude-code-cold-session-tax", "Claude Code", "Why a cold session costs 12–80× more"),
                  ("coding-agent-session-handoff", "Coding agents", "Start a fresh coding-agent session without losing context")],
         cta=("Stop cold resumes from burning your limits", "L2Cache warns you before a cold resume reloads your context and offers a fresh start with a handoff.")),
    dict(src="coding-agent-memory-what-to-inject", slug="coding-agent-memory-what-to-inject", seo_title="Coding Agent Memory: What to Inject, What to Pull (MCP)",
         section="coding-agents",
         tag="Coding agents · Memory", short="Memory for Claude Code and Codex",
         desc="Coding agent memory works best on a diet: push only what the agent can't find itself (hooks, CLAUDE.md) and let it pull the rest over MCP. Measured.",
         related=[("coding-agent-memory-mcp-hooks", "Coding agents", "Coding agent memory with MCP and hooks"),
                  ("coding-agent-session-handoff", "Coding agents", "Start a fresh coding-agent session without losing context")],
         cta=("Give your agent the few facts it can't find", "L2Cache hands coding agents a small handoff and lets them ask your local history for the rest.")),
    dict(src="error-already-fixed", slug="coding-agent-errors-already-fixed", seo_title="Coding Agents Miss Failed Tests (Exit 0) and Repeat Old Errors",
         section="coding-agents",
         tag="Coding agents · Errors", short="Every Error You've Already Fixed Is in Your History",
         desc="120 of 127 test and build failures my coding agent hit reported exit 0 because of pipes, and 1 in 6 errors came back. The pipefail fix and how to find old fixes.",
         related=[("coding-agent-memory-mcp-hooks", "Coding agents", "Coding agent memory with MCP and hooks"),
                  ("claude-code-session-history-mac", "Claude Code", "Claude Code session history on Mac")],
         cta=("Find the fix from last time", "L2Cache remembers what fixed what, and shows verified fixes when the error comes back.")),
    dict(src="your-mac-knows-yesterday", slug="your-mac-knows-what-you-did-yesterday", seo_title="What Did I Do Yesterday? Rebuild It From Git and Agent History",
         section="projects-worklog",
         tag="Today · Local history", short="Your Mac Already Knows What You Did Yesterday",
         desc="What did I do yesterday? Rebuild it from git reflogs, Claude Code transcripts and zsh history on your Mac. One-liners, a script, no time tracking.",
         related=[("developer-morning-context-today", "Today", "Where you left off, every morning"),
                  ("project-story-git-timeline-mac", "Projects", "Project Story: a git timeline for your Mac")],
         cta=("Start the day where you left off", "L2Cache's Today page shows where each project was left, built from history already on your Mac.")),
    dict(src="timesheet-from-coding-activity", slug="billable-hours-from-coding-activity", seo_title="Billable Hours From Git: A Timesheet From Coding Activity",
         section="projects-worklog",
         tag="Worklog · Measured", short="Fill Your Timesheet From Agent History",
         desc="Estimate billable hours from git and coding-agent activity: 61 h over two weeks vs 120.5 h of first-to-last span. Four rules, a script, the standup.",
         related=[("developer-timesheet-standup-from-activity", "Worklog", "Timesheet and standup from your activity"),
                  ("developer-morning-context-today", "Today", "Where you left off, every morning")],
         cta=("A timesheet you only have to correct", "L2Cache estimates your week from local activity, and you fix what it got wrong."))]


def page(a):
    src = open(f"{MEDIUM}/{a['src']}/article.html").read()
    body = src.split("<hr>", 1)[1].split("</body>", 1)[0]
    title = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<h1>(.*?)</h1>", body, re.S).group(1))).strip()
    subtitle = re.search(r'<h3 class="subtitle">(.*?)</h3>', body, re.S).group(1).strip()
    body = re.sub(r"<h1>.*?</h1>\s*", "", body, count=1, flags=re.S)
    body = re.sub(r'<h3 class="subtitle">.*?</h3>\s*', "", body, count=1, flags=re.S)
    body = re.sub(r"<p>\[IMAGE[^<]*\]</p>\s*", "", body)

    def img(m):
        name = m.group(1)
        if not os.path.exists(f"{MEDIUM}/{a['src']}/{name}"):
            return "<!--missing-image-->"
        dest = f"medium-{a['slug']}-{name}"
        shutil.copy(f"{MEDIUM}/{a['src']}/{name}", f"{SITE}/screenshots/{dest}")
        return f'<img src="screenshots/{dest}" loading="lazy"'
    body = re.sub(r'<img src="([^"/]+\.png)"', img, body)
    # Missing screenshots: drop the image and its caption.
    body = re.sub(r'<!--missing-image-->[^>]*>\s*(<figcaption>.*?</figcaption>\s*)?', "", body, flags=re.S)
    # Medium-only CTA paragraph -> site CTA box below.
    body = re.sub(r"<p><em>L2Cache is a native Mac app.*?</p>\s*", "", body, flags=re.S)
    # Absolute, tracked site links -> the site's relative links.
    body = re.sub(r'href="https://l2cache\.app/en/([a-z0-9-]+)\?[^"]*"', r'href="\1.html"', body)
    body = re.sub(r'href="https://l2cache\.app/\?[^"]*"', 'href="index.html"', body)
    # Scripts: offer each as a download under its code block.
    for script in sorted(f for f in os.listdir(f"{MEDIUM}/{a['src']}") if f.endswith(".py")):
        code = open(f"{MEDIUM}/{a['src']}/{script}").read().rstrip()
        os.makedirs(f"{SITE}/downloads", exist_ok=True)
        shutil.copy(f"{MEDIUM}/{a['src']}/{script}", f"{SITE}/downloads/{script}")
        for m in re.finditer(r"<pre><code>(.*?)</code></pre>", body, re.S):
            if html.unescape(m.group(1)).strip() == code.strip():
                link = f'\n<p class="note"><a href="/downloads/{script}" download>Download {script}</a></p>'
                body = body[:m.end()] + link + body[m.end():]
                break
    body = body.replace("<img ", '<img style="max-width:100%;height:auto;display:block;margin:32px auto 8px;border-radius:8px" ')
    body = body.replace("<figcaption>", '<figcaption class="note" style="text-align:center;margin-bottom:32px">')
    # Key findings box and data tables: site styling (Medium imports them as a list and plain text).
    body = body.replace('<div class="key-findings">', '<div class="highlight-box key-findings">')
    body = body.replace('<table class="data">', '<div class="table-wrap"><table class="data">').replace("</table>", "</table></div>")
    # A table that repeats the chart right above it: collapsed for readers, still in the HTML for crawlers.
    body = re.sub(r'(<img [^>]*>\s*(?:<figcaption>.*?</figcaption>\s*)?)<div class="table-wrap">(.*?)</div>',
                  r'\1<details class="table-wrap"><summary>Show the data as a table</summary>\2</details>', body, flags=re.S)
    faqs = faq_pairs(body)
    body = body.replace("<blockquote>", '<blockquote class="highlight-box"><p>').replace("</blockquote>", "</p></blockquote>")
    words = len(re.sub(r"<pre>.*?</pre>|<[^>]+>", " ", body, flags=re.S).split())
    minutes = max(1, round(words / 230))

    url = f"https://l2cache.amvo.store/en/{a['slug']}"
    chart = re.search(r'<img [^>]*src="screenshots/([^"]+)"[^>]*alt="([^"]*)"', body)
    image = f"https://l2cache.amvo.store/screenshots/{chart.group(1)}" if chart else "https://l2cache.amvo.store/icon.png"
    image_alt = html.escape(html.unescape(chart.group(2)), quote=True) if chart else "L2Cache app icon"
    head, rest = TEMPLATE.split("<body>", 1)
    t = html.escape(title, quote=True)
    d = html.escape(a["desc"], quote=True)
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(a.get('seo_title', title), quote=True)}</title>", head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{d}"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', rf'\g<1>{t}"', head)
    head = re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*"', rf'\g<1>{d}"', head)
    head = head.replace("https://l2cache.amvo.store/en/claude-code-cold-cache-resume-cost", url)
    head = re.sub(r'"headline": "[^"]*"', f'"headline": {json_str(title)}', head)
    head = re.sub(r'"description": "[^"]*"', f'"description": {json_str(a["desc"])}', head)
    (date, date_text), modified = a.get("date", (DATE, DATE_TEXT)), max(MODIFIED, a.get("date", (DATE,))[0])
    head = re.sub(r'"datePublished": "[^"]*"', f'"datePublished": "{date}"', head)
    head = re.sub(r'"dateModified": "[^"]*"', f'"dateModified": "{modified}"', head)
    head = head.replace('content="https://l2cache.amvo.store/icon.png"', f'content="{image}"')
    head = head.replace('"image": "https://l2cache.amvo.store/icon.png"', f'"image": "{image}"')
    head = re.sub(r'(<meta (?:property="og:image:alt"|name="twitter:image:alt") content=")[^"]*"', rf'\g<1>{image_alt}"', head)
    head = re.sub(r'\s*<meta property="og:image:(?:width|height)" content="\d+">', "", head)
    if faqs:
        faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faqs]}
        head = head.replace("</head>", f'  <script type="application/ld+json">\n{json.dumps(faq_ld, ensure_ascii=False, indent=2)}\n  </script>\n</head>', 1)
    head = head.replace("  </style>", STYLE + "  </style>", 1)
    head = re.sub(r'("position": 3, "name": )"[^"]*"', rf'\g<1>{json_str(a["short"])}', head)
    head = head.replace("    .prerelease-box", "    .unused-prerelease")  # template is already clean; harmless

    related = "\n".join(
        f'      <a href="{s}.html"><div><div class="r-tag">{html.escape(tag)}</div><div class="r-title">{html.escape(rt)}</div></div><div class="r-more">Read article →</div></a>'
        for s, tag, rt in a["related"])
    nav = rest.split('<div class="container">', 1)[0]
    footer = "<footer>" + rest.split("<footer>", 1)[1]
    return a, title, head + "<body>" + nav + f'''<div class="container">
  <a href="blog.html" class="label" style="text-decoration: none;">← Back to Blog</a>
  <h1>{html.escape(title)}</h1>
  <p class="meta">{date_text}{f" · Updated {MODIFIED_TEXT}" if modified != date else ""} · {minutes} min read</p>
  <p><strong>{subtitle}</strong></p>
{body.strip()}

  <div class="related">
    <h3>Related reading</h3>
    <div class="related-grid">
{related}
    </div>
  </div>

  <div class="cta-box">
    <div class="cta-title">{html.escape(a["cta"][0])}</div>
    <p>{html.escape(a["cta"][1])}</p>
    <a href="{APP}" class="cta-btn">Download L2Cache for Mac</a>
  </div>
</div>

''' + footer


def json_str(s):
    return json.dumps(s, ensure_ascii=False)


def faq_pairs(body):
    """(question, answer) pairs from the visible FAQ section, so the schema matches the page exactly."""
    section = re.search(r"<h2>Frequently asked questions</h2>(.*?)(?=<h2>|<hr>|$)", body, re.S)
    text = lambda x: html.unescape(re.sub(r"<[^>]+>", "", x)).strip()
    return [(text(q), text(ans)) for q, ans in re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", section.group(1), re.S)] if section else []


STYLE = """    .key-findings ul { margin: 8px 0 0 20px; }
    .key-findings li { margin-bottom: 6px; }
    .table-wrap { overflow-x: auto; margin: 24px 0 32px; }
    details.table-wrap summary { cursor: pointer; font-family: var(--mono); font-size: 13px; color: var(--purple); margin-bottom: 12px; }
    table.data { width: 100%; border-collapse: collapse; font-size: 15px; }
    table.data caption { text-align: left; font-size: 13px; color: var(--text-dim); margin-bottom: 8px; }
    table.data th, table.data td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: top; }
    table.data code { overflow-wrap: anywhere; }
    table.data th { font-family: var(--mono); font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); }
"""


def card(a, title):
    return f'''  <a href="{a["slug"]}.html" class="blog-card">
    <div class="blog-card-body">
      <div class="blog-tag">{html.escape(a["tag"])}</div>
      <div class="blog-title">{html.escape(title)}</div>
      <div class="blog-desc">{html.escape(a["desc"])}</div>
      <div class="blog-readmore">Read Article →</div>
    </div>
  </a>

'''


if __name__ == "__main__":
    blog = open(f"{SITE}/blog.html").read()
    build = open(f"{SITE}/build.py").read()
    for a in ARTICLES:
        a, title, out = page(a)
        open(f"{SITE}/{a['slug']}.html", "w").write(out)
        if f'href="{a["slug"]}.html" class="blog-card"' not in blog:
            i = blog.index(f'id="{a["section"]}"')
            g = blog.index('<div class="blog-grid">\n', i) + len('<div class="blog-grid">\n')
            blog = blog[:g] + card(a, title) + blog[g:]
        if f'"{a["slug"]}.html"' not in build:
            build = build.replace('HTML_FILES = ["', f'HTML_FILES = ["{a["slug"]}.html", "', 1)
        print("wrote", a["slug"])
    if '"downloads"' not in build:
        build = build.replace('for asset in ["icon.png", "screenshots",', 'for asset in ["icon.png", "screenshots", "downloads",', 1)
    open(f"{SITE}/blog.html", "w").write(blog)
    open(f"{SITE}/build.py", "w").write(build)
