# L2Cache 2.0 Website — Content & Internal Linking Sprints

**Status:** Planned (2026-11-08)
**Goal:** Every feature on the 2.0 homepage links to an article that explains it, and every existing article is reachable from the homepage.
**Homepage source:** `prototypes/native-mac/` (commit `e324f73`).
**Runs alongside:** the W-series ([README.md](README.md)). These sprints touch the homepage HTML, so finish each before W3 translations start; every English change after W3 costs 10 re-translations.

## Why

- The 2.0 footer links 18 of about 50 English pages. 13 of 14 blog posts, the agent lifesaver guides, 6 of 9 comparisons and the single-tool pages have no homepage link.
- Six homepage features have no article behind them at all (checked 2026-11-08 by searching every English page):

| Homepage feature | Existing article | Gap |
|---|---|---|
| Context & cost (cold cache, token savings) | none | **C2** |
| Session handoff | none | **C2** |
| MCP & Hooks | none (two passing mentions) | **C3** |
| ⌘K universal search | none (screenshot OCR only) | **C3** |
| Smart bubble / programmable clipboard | `custom-actions` (custom actions only) | **C4** |
| Projects (Project Story) | none | **C5** |
| Worklog (timesheet & standup) | none | **C5** |
| Today | `day-in-the-life-mac-developer` (partial) | **C6** |
| Coding agents, Clipboard history, Terminal history, Screenshot search | covered | link only (C1) |

## Principles

1. **Ship complete.** Each article sprint also wires its pages in: `build.py` `HTML_FILES`, `sitemap.xml`, `llms.txt`, `blog.html`, the homepage footer and the matching popup's "Read more" link. No sprint leaves an orphan page.
2. **Facts come from the app.** Every claim is checked against the app repo (PRDs in `~/tech/L2Cache/docs/`, then code). Nothing deferred or parked is described as shipped. Each sprint's review lists the source for each claim.
3. **Final URLs.** Links use `/en/<slug>` (Sprint W4 rule). Articles stay English-only (Sprint W6).
4. **Match the existing article template** (`blog-agent-history-analytics.html`): same head, nav, schema (`Article` + `BreadcrumbList`), footer.
5. **Done means checked.** `scripts/check_home_links.py` (built in C1) passes, `python3 build.py` and `python3 scripts/site_i18n.py extract` run, `python3 validate_seo.py` passes, and each new page is checked at 1440px and 390px.

## Sprints

| Sprint | Title | Outcome | When |
|---|---|---|---|
| [C1](Sprint-C1-Homepage-Link-Hub.md) ✅ | Homepage link hub | Five-column footer, "From the blog" band, "Read more" in popups, link checker | 2026-11-08 |
| [C2](Sprint-C2-Context-and-Handoff-Articles.md) | Context & handoff articles | Cold-cache cost article, session handoff article | 2026-11-09 |
| [C3](Sprint-C3-MCP-Hooks-and-Search-Articles.md) | MCP, hooks & search articles | Agent memory via MCP + hooks, ⌘K universal search | 2026-11-09 |
| [C4](Sprint-C4-Programmable-Clipboard-Article.md) | Programmable clipboard article | Smart bubble + custom actions article; `custom-actions` page refreshed | 2026-11-09 |
| [C5](Sprint-C5-Projects-and-Worklog-Articles.md) | Projects & Worklog articles | Project Story article, timesheet & standup article | 2026-11-09 |
| [C6](Sprint-C6-Today-Article-and-Final-Pass.md) | Today article & final pass | Today article, blog index refresh, featured picks updated, IndexNow | 2026-11-09 |
