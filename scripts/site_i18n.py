#!/usr/bin/env python3
"""Localized builds of the 2.0 homepage (Sprint W2).

The English HTML stays the source of truth; the English text of each segment is its key
(like the app's .xcstrings). A segment is the inner HTML of the outermost text element whose
content is only text and inline tags (so `<kbd>⌘</kbd><kbd>K</kbd>` stays inside its sentence),
otherwise a single text run. Translatable attributes and JSON-LD strings are keyed the same way.

  python3 scripts/site_i18n.py extract     # rewrite locales/l2cache/en/home.json from the source page
  python3 scripts/site_i18n.py check       # every launch locale complete, tags preserved, nothing left in English
  python3 scripts/site_i18n.py build       # out/home/ (English at /, others at /<lang>)
  python3 scripts/site_i18n.py build --only-complete   # skip incomplete locales (preview, until W3)
"""
import html
import json
import os
import re
import shutil
import sys
from html.parser import HTMLParser

import pricing

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT, "prototypes", "native-mac")
SOURCE = os.path.join(SOURCE_DIR, "index.html")
LOCALES_DIR = os.path.join(ROOT, "locales", "l2cache")
OUT_DIR = os.path.join(ROOT, "out", "home")
SITE_URL = os.getenv("SITE_URL", "https://l2cache.app").rstrip("/")

# Launch locales (Sprint W1, T-W104): code → (native name, og:locale, App Store country).
LOCALES = {
    "en": ("English", "en_US", "us"),
    "de": ("Deutsch", "de_DE", "de"),
    "es": ("Español", "es_ES", "es"),
    "fr": ("Français", "fr_FR", "fr"),
    "it": ("Italiano", "it_IT", "it"),
    "ja": ("日本語", "ja_JP", "jp"),
    "ko": ("한국어", "ko_KR", "kr"),
    "pt-BR": ("Português (Brasil)", "pt_BR", "br"),
    "ru": ("Русский", "ru_RU", "ru"),
    "vi": ("Tiếng Việt", "vi_VN", "vn"),
    "zh-Hans": ("简体中文", "zh_CN", "cn"),
}

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
INLINE = {"a", "abbr", "b", "br", "code", "em", "i", "kbd", "small", "span", "strong", "sub", "sup", "time"}
SEGMENT_TAGS = {"title", "h1", "h2", "h3", "h4", "p", "li", "summary", "a", "button", "span", "strong", "em",
                "figcaption", "label", "th", "td", "dt", "dd", "small"}
NO_TEXT = {"script", "style", "svg", "code", "kbd"}  # text inside these is never translated on its own
ATTRS = {"alt", "aria-label", "title", "data-title", "data-caption", "data-label", "placeholder"}
META_KEYS = {"description", "og:title", "og:description", "og:image:alt", "twitter:title", "twitter:description"}
JSONLD_KEYS = {"name", "description", "text", "featureList"}
JSONLD_SKIP_TYPES = {"Organization", "WebSite", "SoftwareApplication"}  # their "name" is the brand
TAG_RE = re.compile(r"<[^>]+>")
WRAPPER_RE = re.compile(r"\s*<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>(.*)</\1>\s*", re.S)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


class _Node:
    __slots__ = ("tag", "inner_start", "qualifies", "has_text", "runs")

    def __init__(self, tag, inner_start):
        self.tag, self.inner_start = tag, inner_start
        self.qualifies, self.has_text, self.runs = True, False, []


class Segmenter(HTMLParser):
    """Finds translatable ranges in the source without changing anything else."""

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.src = source
        self.line_starts = [0] + [m.end() for m in re.finditer("\n", source)]
        self.stack = [_Node("#root", 0)]
        self.segments = []   # (start, end) of inner HTML or text run
        self.attrs = []      # (start, end) of an attribute value
        self.jsonld = []     # (start, end) of a JSON-LD script body
        self._json_start = None

    def _offset(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def _in(self, tags):
        return any(n.tag in tags for n in self.stack)

    def handle_starttag(self, tag, attrs):
        start = self._offset()
        raw = self.get_starttag_text()
        self._collect_attrs(tag, dict(attrs), raw, start)
        parent = self.stack[-1]
        if tag not in INLINE:
            parent.qualifies = False
        if tag == "script" and dict(attrs).get("type") == "application/ld+json":
            self._json_start = start + len(raw)
        if tag not in VOID:
            self.stack.append(_Node(tag, start + len(raw)))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        end = self._offset()
        if tag == "script" and self._json_start is not None:
            self.jsonld.append((self._json_start, end))
            self._json_start = None
        while len(self.stack) > 1:
            node = self.stack.pop()
            parent = self.stack[-1]
            if node.tag == tag:
                break
        else:
            return
        if not node.qualifies:
            parent.qualifies = False
        if node.has_text:
            parent.has_text = True
        if node.tag in SEGMENT_TAGS and node.qualifies and node.has_text and not self._in(NO_TEXT):
            # Outermost wins: drop segments already recorded inside this element.
            self.segments = [s for s in self.segments if not (node.inner_start <= s[0] and s[1] <= end)]
            self.segments.append((node.inner_start, end))
        elif not node.qualifies and node.tag not in NO_TEXT:
            self.segments += [r for r in node.runs if norm(self.src[r[0]:r[1]])]

    def _text(self, length):
        start = self._offset()
        node = self.stack[-1]
        if self._in(NO_TEXT):
            return
        if self.src[start:start + length].strip():
            node.has_text = True
        if node.runs and node.runs[-1][1] == start:   # entities split text; merge adjacent pieces
            node.runs[-1] = (node.runs[-1][0], start + length)
        else:
            node.runs.append((start, start + length))

    def handle_data(self, data):
        self._text(len(data))

    def handle_entityref(self, name):
        self._text(len(name) + 2)

    def handle_charref(self, name):
        self._text(len(name) + 3)

    def _collect_attrs(self, tag, attrs, raw, start):
        wanted = set(ATTRS)
        if tag == "meta" and (attrs.get("name") in META_KEYS or attrs.get("property") in META_KEYS):
            wanted.add("content")
        for name in wanted:
            m = re.search(r'\s%s="([^"]*)"' % re.escape(name), raw)
            if m and m.group(1).strip():
                self.attrs.append((start + m.start(1), start + m.end(1)))


def narrow(source, start, end):
    """A segment that is one element wrapping all its text (a menu link) keys on the text inside."""
    while True:
        m = WRAPPER_RE.fullmatch(source, start, end)
        if not m or "<" + m.group(1) in m.group(2):
            return start, end
        start, end = m.start(2), m.end(2)


def parse(source):
    s = Segmenter(source)
    s.feed(source)
    s.close()
    s.segments = [narrow(source, a, b) for a, b in s.segments]
    return s


def jsonld_strings(obj, out, parent_type=None):
    """Collect (and later replace) translatable JSON-LD strings."""
    if isinstance(obj, dict):
        kind = obj.get("@type", parent_type)
        for k, v in obj.items():
            if k in JSONLD_KEYS and not (k == "name" and kind in JSONLD_SKIP_TYPES):
                if isinstance(v, str):
                    out.append(v)
                elif isinstance(v, list):
                    out += [x for x in v if isinstance(x, str)]
            elif isinstance(v, (dict, list)):
                jsonld_strings(v, out, kind)
    elif isinstance(obj, list):
        for v in obj:
            jsonld_strings(v, out, parent_type)


def translate_jsonld(obj, cat, lang, parent_type=None):
    if isinstance(obj, dict):
        kind = obj.get("@type", parent_type)
        for k, v in list(obj.items()):
            if k == "inLanguage":
                obj[k] = lang
            elif k in JSONLD_KEYS and not (k == "name" and kind in JSONLD_SKIP_TYPES):
                obj[k] = cat.get(v, v) if isinstance(v, str) else [cat.get(x, x) for x in v]
            elif isinstance(v, (dict, list)):
                translate_jsonld(v, cat, lang, kind)
    elif isinstance(obj, list):
        for v in obj:
            translate_jsonld(v, cat, lang, parent_type)


def language_nav(lang, label, published):
    """Plain crawlable links to the same page in every locale (T-W204). Added after translation,
    so only its label goes through the catalog; the names are each language's own."""
    items = []
    for code in published:
        name = LOCALES[code][0]
        href = "/" if code == "en" else f"/{code}"
        current = ' aria-current="page"' if code == lang else ""
        items.append(f'<li><a href="{href}" hreflang="{code}" lang="{code}"{current}>{name}</a></li>')
    return (f'    <nav class="wrap footer-langs" aria-label="{label}">\n      <ul>\n        '
            + "\n        ".join(items) + "\n      </ul>\n    </nav>\n")


def head_block(lang, published):
    tags = [f'<link rel="alternate" hreflang="{c}" href="{page_url(c)}">' for c in published]
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{page_url("en")}">')
    tags.append(f'<meta property="og:locale" content="{LOCALES[lang][1]}">')
    tags += [f'<meta property="og:locale:alternate" content="{LOCALES[c][1]}">' for c in published if c != lang]
    return "".join(f"  {t}\n" for t in tags)


def page_url(lang):
    return f"{SITE_URL}/" if lang == "en" else f"{SITE_URL}/{lang}"


FOOTER_MARKER = '    <div class="wrap footer-legal">'
LANGUAGE_LABEL = "Language"


def with_language_nav(page, lang, cat, published):
    if FOOTER_MARKER not in page:
        raise SystemExit("footer-legal marker not found in the source page")
    if len(published) < 2:
        return page
    nav = language_nav(lang, cat.get(LANGUAGE_LABEL, LANGUAGE_LABEL), published)
    return page.replace(FOOTER_MARKER, nav + FOOTER_MARKER, 1)


def extract(source):
    """English catalog in page order: every segment, attribute value and JSON-LD string."""
    page = source
    p = parse(page)
    keys = [norm(page[a:b]) for a, b in sorted(p.segments + p.attrs)] + [LANGUAGE_LABEL]
    for a, b in p.jsonld:
        jsonld_strings(json.loads(page[a:b]), keys)
    seen, ordered = set(), []
    for k in keys:
        if k and k not in seen:
            seen.add(k)
            ordered.append(k)
    return ordered


def load(lang):
    path = os.path.join(LOCALES_DIR, lang, "home.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def keep_list():
    with open(os.path.join(LOCALES_DIR, "keep.json"), encoding="utf-8") as f:
        return set(json.load(f))


def tags_of(s):
    """Every tag, attributes included: a translation must keep markup and links exactly."""
    return sorted(TAG_RE.findall(s))


def check(langs=None):
    """Errors that block a locale: missing keys, changed inline tags, untranslated English."""
    source_keys = extract(open(SOURCE, encoding="utf-8").read())
    keep = keep_list()
    errors = []
    for lang in langs or [c for c in LOCALES if c != "en"]:
        try:
            cat = load(lang)
        except FileNotFoundError:
            errors.append(f"{lang}: locales/l2cache/{lang}/home.json missing")
            continue
        for key in source_keys:
            value = cat.get(key)
            if value is None or not value.strip():
                errors.append(f"{lang}: missing — {key[:80]}")
            elif tags_of(value) != tags_of(key):
                errors.append(f"{lang}: inline tags differ — {key[:80]}")
            elif value == key and key not in keep and len(re.findall(r"[A-Za-z]{2,}", html.unescape(key))) >= 2:
                errors.append(f"{lang}: still English — {key[:80]}")
        stale = set(cat) - set(source_keys)
        if stale:
            errors.append(f"{lang}: {len(stale)} stale key(s) no longer on the page (run extract, then remove them)")
    return errors


def render(source, lang, cat, published=tuple(LOCALES)):
    page = source
    p = parse(page)
    edits = []
    for a, b in p.segments + p.attrs:
        raw = page[a:b]
        key = norm(raw)
        if lang != "en" and key in cat:
            lead, trail = raw[: len(raw) - len(raw.lstrip())], raw[len(raw.rstrip()):]
            edits.append((a, b, lead + cat[key] + trail))
    for a, b in p.jsonld:
        if lang != "en":
            data = json.loads(page[a:b])
            translate_jsonld(data, cat, lang)
            body = json.dumps(data, ensure_ascii=False, indent=2)
            edits.append((a, b, "\n  " + body.replace("\n", "\n  ") + "\n  "))
    edits.sort()
    for (a1, b1, _), (a2, _, _) in zip(edits, edits[1:]):
        if a2 < b1:
            raise SystemExit(f"overlapping edits at {a1}-{b1} and {a2}")
    out, pos = [], 0
    for a, b, text in edits:
        out += [page[pos:a], text]
        pos = b
    out.append(page[pos:])
    page = with_language_nav("".join(out), lang, cat, published)

    # Per-locale head and links.
    url = page_url(lang)
    page = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', page, count=1)
    page = re.sub(r'(<link rel="canonical" href=")[^"]*(")', rf"\g<1>{url}\2", page, count=1)
    page = re.sub(r'(<meta property="og:url" content=")[^"]*(")', rf"\g<1>{url}\2", page, count=1)
    page = page.replace('  <meta name="theme-color"', head_block(lang, published) + '  <meta name="theme-color"', 1)
    page = page.replace("apps.apple.com/us/", f"apps.apple.com/{LOCALES[lang][2]}/")
    if lang != "en":
        page = re.sub(r'(class="brand" href=")/(")', rf"\1/{lang}\2", page)
        # Locale pages live in a sub-folder; keep shared assets at the site root.
        page = re.sub(r'(src|href|srcset|imagesrcset|data-full)="(img/|styles\.css|script\.js)',
                      r'\1="/\2', page)
        page = re.sub(r'(srcset=")([^"]*)"',
                      lambda m: m.group(1) + re.sub(r"(^|, )img/", r"\1/img/", m.group(2)) + '"', page)
    return page


NOINDEX_RE = re.compile(r'  <!-- Prototype:[^\n]*-->\n  <meta name="robots" content="noindex,nofollow">\n')
INDEX_META = '<meta name="robots" content="index,follow">'


def complete_locales():
    """English plus every locale that passes check()."""
    return ["en"] + [c for c in LOCALES if c != "en" and not check([c])]


def build(out_dir=OUT_DIR, only_complete=False, clean=True):
    """Write the homepage for each published locale into out_dir; returns the published codes."""
    if only_complete:
        published = complete_locales()
    else:
        errors = check()
        if errors:
            print("\n".join(errors[:40]))
            raise SystemExit(f"\n{len(errors)} localization error(s); nothing built.")
        published = list(LOCALES)
    source = open(SOURCE, encoding="utf-8").read()
    # Older sources carry a prototype noindex block; the published page must always be indexable.
    source = NOINDEX_RE.sub("", source, count=1)
    if "noindex" in source or INDEX_META not in source:
        raise SystemExit(f"homepage source must have {INDEX_META} and no noindex")
    if clean:
        shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(os.path.join(out_dir, "img"), exist_ok=True)
    for name in ("styles.css", "script.js"):
        shutil.copy(os.path.join(SOURCE_DIR, name), out_dir)
    for name in os.listdir(os.path.join(SOURCE_DIR, "img")):
        if name.endswith(".webp") or name in ("icon-64.png", "icon-180.png", "og-home.jpg"):
            shutil.copy(os.path.join(SOURCE_DIR, "img", name), os.path.join(out_dir, "img", name))
    for lang in published:
        cat = {} if lang == "en" else load(lang)
        target = os.path.join(out_dir, "index.html") if lang == "en" else os.path.join(out_dir, lang, "index.html")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(pricing.apply(render(source, lang, cat, published)))
    skipped = [c for c in LOCALES if c not in published]
    print(f"Homepage: {', '.join(published)}" + (f" (skipped incomplete: {', '.join(skipped)})" if skipped else ""))
    return published


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "extract":
        keys = extract(open(SOURCE, encoding="utf-8").read())
        os.makedirs(os.path.join(LOCALES_DIR, "en"), exist_ok=True)
        with open(os.path.join(LOCALES_DIR, "en", "home.json"), "w", encoding="utf-8") as f:
            json.dump({k: k for k in keys}, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"{len(keys)} strings → locales/l2cache/en/home.json")
    elif cmd == "check":
        errors = check(sys.argv[2:] or None)
        print("\n".join(errors) if errors else "All locales complete.")
        sys.exit(1 if errors else 0)
    elif cmd == "build":
        build(only_complete="--only-complete" in sys.argv)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
