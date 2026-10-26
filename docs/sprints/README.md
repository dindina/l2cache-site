# L2Cache 2.0 Website — Domain Move & Localization Sprints

**Status:** Planned (2026-10-26)
**Goal:** Launch the 2.0 site on `l2cache.app` without losing the rankings earned on `l2cache.amvo.store`, with properly localized pages.
**Builds on:** [LEGACY_URL_MIGRATION.md](../LEGACY_URL_MIGRATION.md), [LEGACY_URL_INVENTORY.csv](../LEGACY_URL_INVENTORY.csv), [PHASE_3_FOUNDATION_NOTES.md](../PHASE_3_FOUNDATION_NOTES.md), [NEXT_GEN_WEBSITE_PLAN.md](../NEXT_GEN_WEBSITE_PLAN.md).
**2.0 homepage source:** `prototypes/native-mac/` (commit `ce18fab`).

## Principles

1. **Change the domain, not the paths.** Every `/en/<slug>` and `/en/tools/<tool>` keeps its path on `l2cache.app`. Only the English homepage moves (`/en` → `/`).
2. **One hop.** Every old URL reaches its final URL in a single 301. No chains through `/en`, `www` or `/tools`.
3. **One big change at a time.** Launch day = new domain + 2.0 homepage (English and localized). Other pages move with their content unchanged; refreshes come after rankings settle.
4. **A page is fully localized or not published in that locale.** Only fully translated pages get `hreflang`. The build fails on leftover English.
5. **Old domain redirects are permanent.** Installed copies of the app link to `l2cache.amvo.store`, so the redirects never get removed.
6. **Amvo Store and Hingejoy routing stays untouched.** All new rules are scoped to the L2Cache hosts.

## Sprints

**Order (changed 2026-10-26):** W1 → W2 → W4 → **W3** → W5 → W6. Translations come last, just before cutover, because the English page is still changing; every English edit after W3 would cost 10 re-translations.

| Sprint | Title | Outcome |
|---|---|---|
| [W1](Sprint-W1-Baseline-and-Decisions.md) ✅ | Baseline & decisions | Search Console baseline exported, canonical host and launch locales settled, worktree clean |
| [W2](Sprint-W2-Localization-Pipeline.md) | Localization pipeline | Keyed-string build for the 2.0 homepage with a leftover-English gate |
| [W3](Sprint-W3-Translations.md) | Translations & localized assets | 2.0 homepage in 11 languages, native keywords, localized images |
| [W4](Sprint-W4-New-Domain-Integration.md) | New-domain integration (preview) | 2.0 at `/`, every URL on `l2cache.app`, redirect map in `vercel.json` |
| [W5](Sprint-W5-Validation-and-Cutover.md) | Validation & cutover | 195-row redirect check passes, production switched, Google/Bing told |
| [W6](Sprint-W6-Monitoring-and-Tier-2-Locales.md) | Monitoring & second-tier locales | 4 weeks of monitoring, then localized features/pricing/topic pages |

## Current facts (checked 2026-10-26)

- `l2cache.app` is already on the same Vercel project and serves the **old** site. Its pages canonicalize to `l2cache.amvo.store`, so there is no duplicate-content problem yet.
- `l2cache.app` 308-redirects to `www.l2cache.app`, then to `/en`. The plan says the canonical host is the apex, so this must be resolved in W1.
- `fetch_gsc_stats.py` fails with `HTTP 403` — no current Search Console access from scripts.
- Localized homepages today are about 25% English (title, description and FAQ schema all English). Only `index.html` is localized; other `/{lang}/*` URLs 301 to English.
- The app links to `l2cache.amvo.store` in 9 places (`AppDelegate`, `SettingsLicencePane`, `CustomActionsSettingsView`, `PDFExportManager`), including `/download`.
