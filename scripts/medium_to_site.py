"""Turn docs/medium/<src>/article.html into l2cache-site article pages (site-first, Medium imports them)."""
import html, os, re, shutil

MEDIUM = "/Users/dinesh/tech/L2Cache/docs/medium"
SITE = "/Users/dinesh/tech/l2cache-site"
TEMPLATE = open(f"{SITE}/claude-code-cold-cache-resume-cost.html").read()
DATE, DATE_TEXT = "2026-11-11", "November 11, 2026"
APP = "https://apps.apple.com/us/app/l2cache/id6774423992?mt=12"

ARTICLES = [
    dict(src="claude-code-cold-session-cost", slug="claude-code-cold-session-tax", section="context-cost",
         tag="Claude Code · Measured", short="The Hidden Cost of a Cold Session",
         desc="I measured 10,000 requests from my own Claude Code sessions. Big contexts weren't the expensive part; the breaks were. With a script to measure your own.",
         related=[("claude-code-cold-cache-resume-cost", "Claude Code", "Why resuming a cold Claude Code session costs more"),
                  ("coding-agent-session-handoff", "Coding agents", "Start a fresh coding-agent session without losing context")],
         cta=("Know before a session goes cold", "L2Cache warns you before a heavy session's cache expires and offers a fresh start with a handoff.")),
    dict(src="coding-agent-memory-what-to-inject", slug="coding-agent-memory-what-to-inject", section="coding-agents",
         tag="Coding agents · Memory", short="Your Coding Agent Has Amnesia",
         desc="Agent memory works best on a diet: inject only what the agent can't find out for itself, and let it ask for the rest. With real numbers on what agents pull.",
         related=[("coding-agent-memory-mcp-hooks", "Coding agents", "Coding agent memory with MCP and hooks"),
                  ("coding-agent-session-handoff", "Coding agents", "Start a fresh coding-agent session without losing context")],
         cta=("Give your agent the few facts it can't find", "L2Cache hands coding agents a small handoff and lets them ask your local history for the rest.")),
    dict(src="error-already-fixed", slug="coding-agent-errors-already-fixed", section="coding-agents",
         tag="Coding agents · Errors", short="Every Error You've Already Fixed Is in Your History",
         desc="I counted the failures my coding agent hit over a month. One in six came back, and most failures were reported as successes. How to capture and find old fixes.",
         related=[("coding-agent-memory-mcp-hooks", "Coding agents", "Coding agent memory with MCP and hooks"),
                  ("claude-code-session-history-mac", "Claude Code", "Claude Code session history on Mac")],
         cta=("Find the fix from last time", "L2Cache remembers what fixed what, and shows verified fixes when the error comes back.")),
    dict(src="your-mac-knows-yesterday", slug="your-mac-knows-what-you-did-yesterday", section="projects-worklog",
         tag="Today · Local history", short="Your Mac Already Knows What You Did Yesterday",
         desc="Rebuild your morning context from data already on disk: agent transcripts, shell history and git, with no time tracking. With a script to try it.",
         related=[("developer-morning-context-today", "Today", "Where you left off, every morning"),
                  ("project-story-git-timeline-mac", "Projects", "Project Story: a git timeline for your Mac")],
         cta=("Start the day where you left off", "L2Cache's Today page shows where each project was left, built from history already on your Mac.")),
    dict(src="timesheet-from-coding-activity", slug="billable-hours-from-coding-activity", section="projects-worklog",
         tag="Worklog · Measured", short="The Standup That Writes Itself",
         desc="I estimated two weeks of my working time from coding activity: 61 hours, against 120.5 hours of first-to-last span. The rules, the script, and the standup.",
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
    body = body.replace("<blockquote>", '<blockquote class="highlight-box"><p>').replace("</blockquote>", "</p></blockquote>")
    words = len(re.sub(r"<pre>.*?</pre>|<[^>]+>", " ", body, flags=re.S).split())
    minutes = max(1, round(words / 230))

    url = f"https://l2cache.amvo.store/en/{a['slug']}"
    head, rest = TEMPLATE.split("<body>", 1)
    t = html.escape(title, quote=True)
    d = html.escape(a["desc"], quote=True)
    head = re.sub(r"<title>.*?</title>", f"<title>{t} | L2Cache</title>", head, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{d}"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', rf'\g<1>{t}"', head)
    head = re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*"', rf'\g<1>{d}"', head)
    head = head.replace("https://l2cache.amvo.store/en/claude-code-cold-cache-resume-cost", url)
    head = re.sub(r'"headline": "[^"]*"', f'"headline": {json_str(title)}', head)
    head = re.sub(r'"description": "[^"]*"', f'"description": {json_str(a["desc"])}', head)
    head = re.sub(r'"datePublished": "[^"]*"', f'"datePublished": "{DATE}"', head)
    head = re.sub(r'"dateModified": "[^"]*"', f'"dateModified": "{DATE}"', head)
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
  <p class="meta">{DATE_TEXT} · {minutes} min read</p>
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
    import json
    return json.dumps(s, ensure_ascii=False)


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
