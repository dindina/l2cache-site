# Phase 3 — Foundation and Migration Boundary

**Status:** Initial parity audit complete; implementation boundary established  
**Date:** 15 October 2026  
**Selected visual direction:** Original Living Project Timeline prototype (`prototypes/living-project-timeline/`); the Jack-layout hybrid is not the lead.

## Current Build Contract

The existing Vercel project is a multi-property deployment. Any redesign must preserve all three outputs:

| Property | Current output | Routing owner |
|---|---|---|
| L2Cache | `out/l2cache/` | Final catch-all rewrite in `vercel.json` |
| Amvo Store | `out/amvo-store/` | Host-specific rewrites for `amvo.store` |
| Hingejoy | `out/hingejoy/` | Host-specific rewrites for `hingejoy.amvo.store` |

The current Python build pipeline also owns:

- 10 locale homepages and translation replacement.
- English product, editorial, comparison, support, privacy, and utility pages.
- Clean URL generation and internal-link rewriting.
- Canonical and `hreflang` output.
- XML sitemap and robots file generation.
- Asset copying and Vercel Analytics injection.

The `validate_seo.py` validator imports `build.py` and checks generated canonicals, metadata, localized alternates, and sitemap coverage. A new implementation must either preserve these checks or replace them with equivalent automated checks before cutover.

## Migration Boundary

1. Keep the new homepage source and styles in `prototypes/living-project-timeline/` until production metadata and presentation-safe product captures are ready.
2. Do not replace the root source or modify routing while the existing worktree contains unrelated uncommitted edits to `index.html`, `build.py`, and `validate_seo.py`.
3. When integration begins, route only the L2Cache host to the new English root. Preserve Amvo Store and Hingejoy rewrites verbatim.
4. Keep `/en` as a one-hop permanent redirect to `/` after the new root is served and validated. Preserve all other legacy paths according to `LEGACY_URL_INVENTORY.csv`.
5. Maintain localized homepages only for languages approved in `[[LAUNCH_LOCALES]]`; untranslated locales must not receive `hreflang` alternates.
6. Update canonical, Open Graph, schema, sitemap, robots, App Store website references, and in-app URLs in the same migration window.
7. Keep the old English homepage available in preview until redirect and parity validation pass.

## Architecture Recommendation

Use a staged static migration. Preserve the current Python build for legacy content and the other two properties while the redesigned L2Cache homepage is developed as a small, dependency-free static page. This reuses the current deployment contract and avoids adding a framework dependency before multi-property, locale, and route parity have been proven.

If a component framework is still desired for the later product/content pages, evaluate it after the homepage route and legacy redirects are working in a Vercel preview. Any framework build must write only to `out/l2cache/` and must not own or erase `out/amvo-store/` or `out/hingejoy/`.

This is a sequencing recommendation, not a final long-term framework lock.

## Production Metadata Contract for the New Homepage

The selected homepage cannot inherit prototype metadata. Before it becomes indexable, it needs:

- One title, meta description, H1, and self-canonical at `https://l2cache.app/`.
- Open Graph and Twitter metadata using the same canonical URL and a production-ready social image.
- Stable `Organization`, `WebSite`, `SoftwareApplication`, and `WebPage` entity IDs connected to the selected public publisher identity.
- Visible claims consistent with `PUBLISHABLE_CLAIMS_MATRIX.md`.
- No unresolved `[[PLACEHOLDER]]` tokens in rendered output.
- Inclusion in the canonical sitemap exactly once.
- Crawlable page copy in initial HTML; demonstrations must remain progressive enhancement.
- Prototype paths marked `noindex,nofollow` and excluded from the production sitemap.

## Next Foundation Work

1. Create presentation-safe captures for Today, Project Story, Command-K, Coding Agents, and terminal recovery, following the original prototype's composition.
2. Build an isolated production-shaped homepage source from the approved prototype, with final metadata helpers and placeholder validation.
3. Add an output check that confirms legacy routes and all three host outputs survive the build.
4. Preview the generated result on Vercel and validate redirects, canonicals, sitemap, accessibility, and performance before any production cutover.

