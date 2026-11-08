# Sprint C1 — Homepage link hub

**Status:** ✅ Done · **Date:** 2026-11-08
**Scope:** `prototypes/native-mac/index.html`, `styles.css`, `locales/l2cache/en/home.json`, new `scripts/check_home_links.py`.
**Out of scope:** new articles (C2–C6), legacy page templates.

## Tasks

### T-C101 — Link checker
`scripts/check_home_links.py`: parse the homepage source, collect every internal `href`, and fail if one doesn't map to a page in `out/l2cache/` (`/en/<slug>` → `out/l2cache/en/<slug>.html`, `/en/tools/<x>` → `out/l2cache/en/tools/<x>…`, `/` and `#anchors` resolve on the page). Prints the broken links and exits non-zero.

### T-C102 — Five-column footer
Replace the four columns with five. Every link is checked by T-C101.

| Product | Coding agents | Guides & blog | Free tools | Compare |
|---|---|---|---|---|
| Clipboard history | Claude Code history | Blog (all articles) | JSON formatter | Best Mac clipboard managers |
| Terminal history | Codex history | SQLite FTS5 hangs | JWT decoder | Compare all |
| Screenshot search | GitHub Copilot history | Swift & SQLite concurrency | Regex tester | L2Cache vs Maccy |
| Custom actions | Grok Build history | Zero-cloud desktop AI | SQL test data | L2Cache vs Paste |
| AI features | Claude Code lifesaver | Clipboard privacy report | Screenshot OCR | L2Cache vs Raycast |
| Changelog | Codex lifesaver | Clipboard benchmark | All 66 tools | L2Cache vs Alfred |
| | Copilot lifesaver | REST API developer tools | | L2Cache vs Atuin, CleanClip, Clipy, CopyClip, PastePal |
| | Session resume guide | | | |

Bottom row: Support · Privacy policy · Sitemap · language switcher (unchanged) · © line.
Phones: columns stack two-up; Compare's last row wraps.

### T-C103 — "From the blog" band
A section between the FAQ/pricing area and the footer: eyebrow "From the blog", heading, six cards (3×2 desktop, swipe row on phones like the tiles), "Read all articles →" to `/en/blog`.
Each card: tag chip (feature colour), title, one-line summary, reading time.

| Card | Tag |
|---|---|
| Claude Code session history lifesaver | Coding agents |
| Codex session history lifesaver | Coding agents |
| AI agent JSONL & session resume guide | Coding agents |
| Agent history analytics | Coding agents |
| Clipboard automation for developer workflows | Clipboard |
| A day in the life of a Mac developer | Workflow |

C6 swaps in the new articles once they exist.

### T-C104 — "Read more" in feature popups
A row at the end of each carousel slide's copy, linking to existing pages now; C2–C6 add the new ones.

| Slide | Links (now) |
|---|---|
| Context & cost | Session resume guide |
| Today | A day in the life of a Mac developer |
| Coding agents | Claude Code history · Codex history |
| MCP & Hooks | Session resume guide |
| Projects | — (C5) |
| Search | Screenshot search |
| Clipboard | Custom actions · Clipboard history |
| Terminal | Terminal history |

### T-C105 — Verify
- `python3 build.py`, `python3 scripts/site_i18n.py extract`, `python3 scripts/site_i18n.py build --only-complete`.
- `python3 scripts/check_home_links.py` passes.
- `python3 validate_seo.py` passes, or only shows failures that were already there before this sprint.
- Screenshots at 1440px, 900px and 390px: footer, blog band, one popup with "Read more"; no horizontal scroll.

## Definition of done
All five tasks pass, one commit in `l2cache-site`, review section below filled in.

## Review
- **T-C101:** `scripts/check_home_links.py` maps `/en/<slug>`, `/en/tools/<x>` and `/` to `out/l2cache/`, checks `#anchors` and relative assets. Resolver tested with good and bad paths (`/en/nope` fails).
- **T-C102:** footer now Product (6) · Coding agents (7) · Guides & blog (7) · Free tools (6) · Compare (7 + "Also vs" 4); Support · Privacy policy · Sitemap moved to the legal row. Change from plan: "Screenshot OCR" in Free tools became "JSON to TypeScript" (`/en/tools/json-to-typescript`) because Screenshot search already links `screenshot-ocr-mac` in Product.
- **T-C103:** "From the blog" band above the footer, six cards with summaries from each article's meta description and reading times from word counts; swipe row on phones.
- **T-C104:** "Read more" row on 7 of 8 slides; Projects waits for C5.
- **T-C105:** `build.py` OK, `site_i18n.py extract` → 577 strings, `check_home_links.py` → 69 internal links resolve, `validate_seo.py` passed (41 pages). Checked at 1440px, 900px and 390px: no horizontal scroll, all 8 slides still fit without scrolling, blog cards equal height.
- Internal homepage links went from 31 to 69.
