# Sprint W6 — Monitoring & Second-Tier Locales

**Status:** Planned (2026-10-26)
**Goal:** Confirm rankings moved over, then expand localization to the pages with real demand in each language.
**Depends on:** W5 (cutover).
**Scope:** Search Console monitoring, `locales/l2cache/<lang>/*.json`, selected legacy pages.

---

## Tasks

### T-W601 — Weekly monitoring (4 weeks)
- Compare the new property against the W1 baseline: indexed pages, 404s, canonical Google selected, and impressions/position for `protect` pages.
- Run `check_migration.py` against production weekly.
- Stop-the-line rule: if a `protect` page has lost more than 50% of its impressions after 3 weeks, investigate before any further change.

### T-W602 — Second-tier pages (only after rankings settle)
- Template and localize: features/intelligence, pricing, privacy, support, and the generic topic pages with local search demand (`clipboard-history-mac`, `screenshot-ocr-mac`, `developer-clipboard`).
- Keyword research per market first (as in T-W302); same gates as W2.
- Coding-agent, comparison, blog and tool pages stay English-only.

### T-W603 — Retire the old pipeline
- Remove the `locales.json` find-and-replace once no page uses it; keep `validate_seo.py` gates.

---

## Done when
- 4 weekly reports written to `docs/baseline/`, with `protect` pages stable or recovering.
- Second-tier pages live in all launch locales with gates passing.
