# Sprint W4 — New-Domain Integration (Preview Only)

**Status:** Done (2026-10-26) — verified on preview `l2cache-site-n1g8bm6ej`; production unchanged
**Goal:** A Vercel preview where the 2.0 homepage is at `/`, every page uses `l2cache.app`, and the old host redirects one hop to the same path.
**Depends on:** W1 (canonical host), W2 (pipeline). Runs before W3: the preview is English-only until translations land.
**Scope:** `build.py`, `vercel.json`, `sitemap.xml`, `robots.txt`, `llms.txt`, internal links. Production stays on the current deploy.

---

## Tasks

### T-W400 — English-only build mode ✅
- `site_i18n.py build --only-complete`: build the locales that pass `check`, and emit hreflang / language links for those only. The strict default stays for production.
- Until W3, the preview keeps the old `/{lang}` homepages, or redirects them to `/` temporarily (302), so no localized URL 404s.

### T-W401 — 2.0 homepage as the English root ✅
- Serve the 2.0 homepage at `/` and the localized versions at `/{lang}` for the L2Cache hosts only.
- Legacy `/en/<slug>` and `/en/tools/<tool>` pages keep their paths **and their content**; only the shared nav/footer links and the domain change.

### T-W402 — Switch every reference to `l2cache.app` ✅
- Build with `SITE_URL=https://l2cache.app`: canonicals, `og:url`, `og:image`, JSON-LD URLs, hreflang, sitemap, `robots.txt` `Sitemap:` line, `llms.txt` / `llms-full.txt`.
- Internal links point to final URLs (`/`, not `/en`; `/en/tools/x`, not `/tools/x`).
- Grep gate: no `amvo.store` left in L2Cache output.

### T-W403 — Old-host redirects (`l2cache.amvo.store`, `www.l2cache.amvo.store`) ✅
- `has: host` rules, permanent:
  - `/` and `/en` → `https://l2cache.app/`
  - `/tools/:tool*` → `https://l2cache.app/en/tools/:tool*`
  - `/:lang(...)/:page` (untranslated) → `https://l2cache.app/en/:page`
  - `/:path*` → `https://l2cache.app/:path*` (catch-all, last)
- `APP_LINK` rows from W1 map explicitly. Start from the tested rules on branch `fix/legacy-app-links` (`b666c2b`): lowercase `zh-hans`/`pt-br` → `/zh-Hans`, `/pt-BR`; `ta`/`ru` → English; `/download` → temporary until `[[DIRECT_DOWNLOAD_URL]]` exists. Apply them on both hosts, with destinations on `l2cache.app`.
- Every rule ends at the final URL in one hop.

### T-W404 — New-host internal redirects ✅
- `/en` → `/`, `/tools/*` → `/en/tools/*`, `/{lang}/<untranslated>` → `/en/<page>`, non-primary host → primary.

### T-W405 — Keep the other properties intact ✅
- Amvo Store and Hingejoy rewrites copied verbatim. Smoke-test `amvo.store` and `hingejoy.amvo.store` on the preview.

---

## Results (2026-10-26)
- `python3 build.py`: 2.0 homepage at `/` (English only until W3), 184 legacy pages unchanged apart from home links and domain; old localized homepages no longer built. `.py` / `__pycache__` no longer published from `tools/` (15 generator scripts were public on production).
- `validate_seo.py`: new homepage checks (canonical, hreflang count, no `noindex`) and a gate on any `l2cache.amvo.store` reference in the output.
- `node scripts/check_routes.js`: replays `vercel.json` for all 204 inventory rows on the old host plus every published page on the new host — **383 routes, 0 failures**. Protected pages are one hop to the same path. Models Vercel's case-sensitive matching and cleanUrls/trailingSlash hops.
- Old catch-all exclusion list now matches exact names (before, `de` also excluded `/developer-clipboard`).
- `www.l2cache.amvo.store` does not resolve, so only `l2cache.amvo.store` gets old-host rules. `www.l2cache.app` → apex is a Vercel domain setting (W5).
- `.vercelignore`: `.env*` (the CLI uploads `.env` by default) and `docs/baseline`.
- Legacy pages' `#features` / `#who` links mapped to the 2.0 page (`#today`, top).

## Done when
- The preview serves the 2.0 site with zero `amvo.store` references in L2Cache output.
- A spot check of 20 old URLs (including the 6 `protect` pages and `/download`) reaches the right `l2cache.app` URL in one 301.
- Amvo Store and Hingejoy pages unchanged on the preview.
