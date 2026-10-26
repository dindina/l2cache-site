# Sprint W1 — Baseline & Decisions

**Status:** Done (2026-10-26) — live link fixes deferred to W4
**Goal:** Capture what currently ranks, settle the decisions that shape every URL, and clear the blockers named in Phase 1/3.
**Depends on:** —
**Scope:** Search Console / Bing access, Vercel domain settings, `docs/LEGACY_URL_INVENTORY.csv`, worktree hygiene. No production routing changes.

---

## Tasks

### T-W101 — Restore Search Console access
- ✅ 2026-10-26: `amvo.store` verified as a Domain property (root TXT; `l2cache.amvo.store` is a CNAME so it can't hold one) and the service account added as Full user. `sc-domain:l2cache.amvo.store` now reports `siteFullUser`.
- Keep both `google-site-verification` TXT records at the `amvo.store` root permanently.
- ✅ `sc-domain:l2cache.app` verified (TXT at `@`) with the service account as Full user; `l2cache.app` also verified in Bing. Keep the TXT record permanently.

### T-W102 — Ranking baseline
- ✅ `tools/export_gsc_baseline.py` → `docs/baseline/gsc-l2cache.amvo.store-2026-10-26-{pages,queries}.csv` (2025-06-24 → 2026-10-23).
- Result: 1,856 impressions, 3 clicks, 33 pages. `/en/clipboard-history-mac` (923, pos 56) and `/en/mac-command-history` (680, pos 49) hold 86%. Localized homepages: 0 impressions. Top countries: US, India, Philippines, Vietnam, Turkey.
- ✅ Inventory now has `baseline_impressions`, `baseline_position` and `protect` (≥ 20 impressions, plus the homepage): clipboard-history-mac, mac-command-history, certificate-decoder, codex-session-history-mac, rtf-to-markdown, best-mac-clipboard-managers, `/`, `/en`. Added `/es/privacy` (seen by Google, not in the inventory).
- ✅ Bing: `l2cache.amvo.store` re-verified (existing `BingSiteAuth.xml`); `tools/export_bing_baseline.py` → `docs/baseline/bing-l2cache.amvo.store-2026-10-26-{pages,queries,traffic}.csv` (2026-10-01 → 2026-10-24 only; older data unavailable). `/en/mac-command-history` is **position 4.6 on Bing** (279 of 314 impressions, all 4 clicks) — the most valuable URL on the site. Inventory has `bing_impressions` / `bing_position`.
- ✅ Backlinks: Google knows one external link — the owned Medium article *How to find and resume OpenAI Codex CLI sessions* (`docs/baseline/links-google-l2cache.amvo.store-2026-10-26.csv`); Bing `GetLinkCounts` reports none. Ranking equity is on-page/content, not links. Update the Medium link to `l2cache.app` at cutover (T-W504).

### T-W103 — Canonical host decision
- Today `l2cache.app` 308s to `www.l2cache.app`. Pick one host (recommended: apex `l2cache.app`, as in the plan) and set it as the primary domain in Vercel, so the other host 301s to it.
- Record the decision in `NEXT_GEN_WEBSITE_PLAN.md`.

### T-W104 — Launch locales (`[[LAUNCH_LOCALES]]`)
- Recommended: en, de, es, fr, it, ja, ko, pt-BR, ru, vi, zh-Hans (current 9 + ru). Tamil deferred (no App Store listing).
- Record in the plan; W2/W3 build exactly this list.

### T-W105 — App-referenced URLs
- ✅ 8 `APP_LINK` rows added to the inventory (2026-10-26).
- **Bug today (Direct build only):** *Check for Updates* opens `l2cache.amvo.store/download` → `/en/download` → **404**. Needs `[[DIRECT_DOWNLOAD_URL]]`.
- **Bug today (all builds):** Settings › Website / Changelog / Intelligence / Support build `/{lang}/<page>.html` with lowercase `zh-hans`, `pt-br`, and with `ta`. The site's paths are case-sensitive, so Chinese, Portuguese and Tamil users get 404s.
- Site fix: redirect lowercase codes to `/zh-Hans`, `/pt-BR`, and `ta`/`ru` to English. **Decision 2026-10-26: not deployed to the current site; ships with the W4 rules.** Tested rules on branch `fix/legacy-app-links` (`b666c2b`, based on production commit `236f2a2`); verified on a preview deploy.
- Fix in the app (2.0 build): use the site's exact codes and the new domain (also T-W504).

### T-W106 — Clear the Phase 3 blockers
- Uncommitted `index.html`, `build.py`, `validate_seo.py` and docs edits on `l2cache2.0`: left untouched. Any production-only change is built from a separate worktree of the live commit (`236f2a2` = production, verified page-by-page on 2026-10-26).
- ✅ 2026-10-26: Bing API key regenerated (the leaked key from `030262c` now returns `InvalidApiKey`); `seo_health_check.py` reads `BING_API_KEY` from `.env`. The old value stays in git history but is dead.

---

## Done when
- Baseline CSVs are committed, and the inventory has impression and `protect` columns plus the `APP_LINK` rows.
- Canonical host and launch locales are written into the plan, and Vercel primary domain matches.
- `/download` no longer 404s on the current site.
- Clean worktree; no credential in source.
