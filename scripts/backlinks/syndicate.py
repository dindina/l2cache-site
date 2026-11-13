"""Syndicate a pillar essay to dev.to as an unpublished draft, with the canonical URL set to l2cache.app.

    python3 scripts/backlinks/syndicate.py --dry-run [SLUG]   # write Markdown to $TMPDIR/l2cache-syndication/, no API calls
    python3 scripts/backlinks/syndicate.py SLUG               # create or update the dev.to draft
    python3 scripts/backlinks/syndicate.py SLUG --update-published   # refresh a post you already published
    python3 scripts/backlinks/syndicate.py SLUG --publish            # create or update, and publish

Creates drafts unless --publish is passed (only when the user asked to publish that essay).
Post IDs go to state.json, and existing posts are matched by canonical URL, so nothing is posted twice.
Needs DEV_TO_API_KEY (environment or l2cache-site/.env).
"""
import html, json, os, re, sys, tempfile, urllib.request
from html.parser import HTMLParser

SITE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://l2cache.app"
STATE = f"{HERE}/state.json"
API = "https://dev.to/api"


class Markdown(HTMLParser):
    """Just enough HTML → Markdown for the essay pages (no nested lists)."""

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
        if self.skip or tag == "summary" or (tag == "details"):
            self.skip += tag == "details"
            return
        if tag in ("h2", "h3"):
            self.block("#" * int(tag[1]) + " ")
        elif tag == "p":
            self.block()
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag == "pre":
            self.pre = 1
            self.block("```\n")
        elif tag == "a":
            self.links.append(absolute(a.get("href", "")))
            self.emit("[")
        elif tag == "img":
            self.block(f"![{a.get('alt', '')}]({absolute(a.get('src', ''))})")
        elif tag == "figcaption":
            self.block("*")
        elif tag in ("ul", "ol"):
            self.lists.append([tag, 0])
            self.out.append("\n")
        elif tag == "li":
            kind = self.lists[-1]
            kind[1] += 1
            self.out.append("\n" + ("- " if kind[0] == "ul" else f"{kind[1]}. "))
        elif tag == "blockquote":
            self.quotes.append(len(self.out))
        elif tag == "hr":
            self.block("---")
        elif tag == "br":
            self.emit("  \n")
        elif tag == "table":
            self.table = {"rows": [], "row": None, "cell": None, "caption": None}
        elif tag == "caption":
            self.table["cell"] = []
        elif tag == "tr":
            self.table["row"] = []
        elif tag in ("td", "th"):
            self.table["cell"] = []

    def handle_endtag(self, tag):
        if self.skip:
            self.skip -= tag == "details"
            return
        if tag == "summary":
            return
        if tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag == "pre":
            self.pre = 0
            self.out.append("\n```")
        elif tag == "a":
            self.emit(f"]({self.links.pop()})")
        elif tag == "figcaption":
            self.out.append("*")
        elif tag in ("ul", "ol"):
            self.lists.pop()
        elif tag == "blockquote":
            start = self.quotes.pop()
            quote = "".join(self.out[start:]).strip()
            self.out[start:] = ["\n\n" + "\n".join("> " + line if line else ">" for line in quote.split("\n"))]
        elif tag == "caption":
            self.table["caption"] = "".join(self.table["cell"]).strip()
            self.table["cell"] = None
        elif tag in ("td", "th"):
            self.table["row"].append("".join(self.table["cell"]).strip().replace("|", "\\|"))
            self.table["cell"] = None
        elif tag == "tr":
            self.table["rows"].append(self.table["row"])
        elif tag == "table":
            t, self.table = self.table, None
            lines = [f"**{t['caption']}**", ""] if t["caption"] else []
            for i, row in enumerate(t["rows"]):
                lines.append("| " + " | ".join(row) + " |")
                if i == 0:
                    lines.append("|" + "---|" * len(row))
            self.block("\n".join(lines))

    def handle_data(self, data):
        if self.skip or (self.table is not None and self.table["cell"] is None):
            return
        if not self.pre:
            data = re.sub(r"\s+", " ", data)
        self.emit(data)

    def markdown(self):
        md = "".join(self.out)
        md = re.sub(r"[ \t]+\n", "\n", md)
        md = re.sub(r"`\[([^\]`]+)\]\(([^)]+)\)`", r"[`\1`](\2)", md)  # <code><a>x</a></code>
        return re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"


def absolute(url):
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return url
    if url.endswith(".html"):
        return f"{BASE}/en/{url[:-5]}" if url != "index.html" else f"{BASE}/"
    return f"{BASE}/{url.lstrip('/')}"


def essay(p):
    """Title, description, Markdown body and cover image for one pillar, from the site page."""
    page = open(f"{SITE}/{p['slug']}.html").read()
    title = html.unescape(re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S).group(1)).strip()
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', page).group(1))
    body = page.split("</h1>", 1)[1].split('<div class="related">', 1)[0]
    body = re.sub(r'<p class="meta">.*?</p>', "", body, count=1, flags=re.S)
    parser = Markdown()
    parser.feed(body)
    url = f"{BASE}/en/{p['slug']}"
    md = parser.markdown() + f"\n---\n\n*Originally published at [l2cache.app]({url}).*\n"
    cover = re.search(r'<img [^>]*src="([^"]+)"', body)
    return dict(title=title, description=desc, body_markdown=md, canonical_url=url,
                main_image=absolute(cover.group(1)) if cover else None, tags=p["devto_tags"][:4])


def api_key():
    key = os.environ.get("DEV_TO_API_KEY") or os.environ.get("DEVTO_API_KEY")
    if not key and os.path.exists(f"{SITE}/.env"):
        for line in open(f"{SITE}/.env"):
            m = re.match(r"\s*DEV_?TO_API_KEY\s*=\s*(\S+)", line)
            if m:
                key = m.group(1).strip("\"'")
    if not key:
        sys.exit("DEV_TO_API_KEY is not set")
    return key


def call(method, path, body=None):
    req = urllib.request.Request(f"{API}{path}", method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"api-key": api_key(), "Content-Type": "application/json",
                                          "Accept": "application/vnd.forem.api-v1+json", "User-Agent": "l2cache-syndicate"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def my_articles():
    found, page = [], 1
    while True:
        batch = call("GET", f"/articles/me/all?per_page=100&page={page}")
        found += batch
        if len(batch) < 100:
            return found
        page += 1


def syndicate(p, article):
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    posts = state.setdefault("devto", {})
    existing = next((a for a in my_articles() if a["id"] == posts.get(p["slug"])
                     or (a.get("canonical_url") or "").rstrip("/") == article["canonical_url"]), None)
    if existing and existing["published"] and "--update-published" in sys.argv:
        fields = {k: v for k, v in article.items() if v}
        post = call("PUT", f"/articles/{existing['id']}", {"article": fields})
        print(f"{p['slug']}: updated published post {post['url']}")
        posts[p["slug"]] = post["id"]
    elif existing and existing["published"]:
        print(f"{p['slug']}: already published on dev.to ({existing['url']}), left unchanged (--update-published to refresh it)")
        posts[p["slug"]] = existing["id"]
    else:
        fields = {k: v for k, v in article.items() if v} | {"published": "--publish" in sys.argv}
        if existing:
            post = call("PUT", f"/articles/{existing['id']}", {"article": fields})
            print(f"{p['slug']}: updated {'and published' if post.get('published') or post.get('published_at') else 'draft'} {post['id']} {post.get('url', '')}")
        else:
            post = call("POST", "/articles", {"article": fields})
            print(f"{p['slug']}: created {'and published' if post.get('published') or post.get('published_at') else 'draft'} {post['id']} {post.get('url', '')}")
        posts[p["slug"]] = post["id"]
    json.dump(state, open(STATE, "w"), indent=2)
    open(STATE, "a").write("\n")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    pillars = json.load(open(f"{HERE}/pillars.json"))
    chosen = [p for p in pillars if not args or p["slug"] in args]
    if not chosen or (not dry and len(chosen) != 1):
        sys.exit("usage: syndicate.py [--dry-run] [SLUG]  (one slug per real run; slugs: "
                 + ", ".join(p["slug"] for p in pillars) + ")")
    for p in chosen:
        article = essay(p)
        if dry:
            folder = f"{tempfile.gettempdir()}/l2cache-syndication"  # not out/: Vercel deploys it
            os.makedirs(folder, exist_ok=True)
            path = f"{folder}/{p['slug']}.md"
            meta = {k: v for k, v in article.items() if k != "body_markdown"}
            open(path, "w").write(f"<!-- {json.dumps(meta, ensure_ascii=False)} -->\n\n# {article['title']}\n\n{article['body_markdown']}")
            print("wrote", path)
        else:
            syndicate(p, article)


if __name__ == "__main__":
    main()
