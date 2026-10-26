# Sprint W5 — Validation & Cutover

**Status:** Planned (2026-10-26)
**Goal:** Prove every legacy URL lands correctly, then switch production and tell Google, Bing and every link you control.
**Depends on:** W4 (preview).
**Scope:** `tools/check_migration.py` (new), production deploy, Search Console, Bing, App Store Connect, the L2Cache app repo, external profiles.

---

## Tasks

### T-W501 — Migration checker `tools/check_migration.py`
- For every inventory row and `APP_LINK` row, request the old-host URL and assert: exactly one 301/308, the expected destination, a 200 at the end, a self-referencing canonical, and no `noindex`.
- Also assert: sitemap contains only 200 canonical URLs, hreflang is reciprocal, and `/en`, `www`, `/tools` produce no chains.
- Runs against a preview URL (`--host`) and against production after cutover. Exit code ≠ 0 on any failure.

### T-W502 — Pre-launch checks
- Checker passes on the preview with 0 failures.
- Lighthouse on `/` and two locales: performance and SEO in line with `ce18fab`.
- Fresh Search Console export (W1 script) the day before cutover.

### T-W503 — Cutover
- Deploy to production; run the checker against production immediately.
- Search Console: submit the new sitemap on `l2cache.app`; run **Change of Address** from the old property. Keep the old sitemap submitted for about 4 weeks.
- Bing Webmaster: Site Move; run `submit_indexnow.py` with the new URLs.

### T-W504 — Links you control
- App Store Connect: marketing, support and privacy URLs in all 12 locales (`update_asc_metadata.py`).
- L2Cache app: replace the 9 `l2cache.amvo.store` URLs (`AppDelegate`, `SettingsLicencePane`, `CustomActionsSettingsView`, `PDFExportManager`) and `release_pipeline.py`. Ship in the 2.0 build. Also remove the force unwraps on the two `CustomActionsSettingsView` links (project rule).
- GitHub, dev.to and Medium articles, the outreach templates.

---

## Done when
- Checker passes with 0 failures on production.
- Change of Address accepted; Bing Site Move submitted.
- No `l2cache.amvo.store` URL left in the app, App Store metadata or owned profiles.
