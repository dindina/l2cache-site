# Sprint W4 — New-Domain Integration (Preview Only)

**Status:** Planned (2026-10-26)
**Goal:** A Vercel preview where the 2.0 homepage is at `/`, every page uses `l2cache.app`, and the old host redirects one hop to the same path.
**Depends on:** W1 (canonical host), W3 (localized homepage).
**Scope:** `build.py`, `vercel.json`, `sitemap.xml`, `robots.txt`, `llms.txt`, internal links. Production stays on the current deploy.

---

## Tasks

### T-W401 — 2.0 homepage as the English root
- Serve the 2.0 homepage at `/` and the localized versions at `/{lang}` for the L2Cache hosts only.
- Legacy `/en/<slug>` and `/en/tools/<tool>` pages keep their paths **and their content**; only the shared nav/footer links and the domain change.

### T-W402 — Switch every reference to `l2cache.app`
- Build with `SITE_URL=https://l2cache.app`: canonicals, `og:url`, `og:image`, JSON-LD URLs, hreflang, sitemap, `robots.txt` `Sitemap:` line, `llms.txt` / `llms-full.txt`.
- Internal links point to final URLs (`/`, not `/en`; `/en/tools/x`, not `/tools/x`).
- Grep gate: no `amvo.store` left in L2Cache output.

### T-W403 — Old-host redirects (`l2cache.amvo.store`, `www.l2cache.amvo.store`)
- `has: host` rules, permanent:
  - `/` and `/en` → `https://l2cache.app/`
  - `/tools/:tool*` → `https://l2cache.app/en/tools/:tool*`
  - `/:lang(...)/:page` (untranslated) → `https://l2cache.app/en/:page`
  - `/:path*` → `https://l2cache.app/:path*` (catch-all, last)
- `APP_LINK` rows from W1 map explicitly. Start from the tested rules on branch `fix/legacy-app-links` (`b666c2b`): lowercase `zh-hans`/`pt-br` → `/zh-Hans`, `/pt-BR`; `ta`/`ru` → English; `/download` → temporary until `[[DIRECT_DOWNLOAD_URL]]` exists. Apply them on both hosts, with destinations on `l2cache.app`.
- Every rule ends at the final URL in one hop.

### T-W404 — New-host internal redirects
- `/en` → `/`, `/tools/*` → `/en/tools/*`, `/{lang}/<untranslated>` → `/en/<page>`, non-primary host → primary.

### T-W405 — Keep the other properties intact
- Amvo Store and Hingejoy rewrites copied verbatim. Smoke-test `amvo.store` and `hingejoy.amvo.store` on the preview.

---

## Done when
- The preview serves the 2.0 site with zero `amvo.store` references in L2Cache output.
- A spot check of 20 old URLs (including the 6 `protect` pages and `/download`) reaches the right `l2cache.app` URL in one 301.
- Amvo Store and Hingejoy pages unchanged on the preview.
