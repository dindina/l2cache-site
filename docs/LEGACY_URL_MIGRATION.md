# Phase 1 — Legacy URL Preservation Plan

**Status:** Initial inventory complete  
**Date:** 15 October 2026  
**Inventory:** `LEGACY_URL_INVENTORY.csv`

## Baseline

The current generated L2Cache output contains **195 HTML artifacts**:

- 67 canonical English developer-tool pages under `/en/tools/...`.
- 67 duplicate tool outputs under `/tools/...`, already intended to redirect to `/en/tools/...`.
- 53 English homepage/product/editorial/comparison/support artifacts under `/en/...`.
- 9 non-English homepage artifacts.

The inventory assigns every artifact a proposed destination and one of these conservative actions:

| Action | Count | Meaning |
|---|---:|---|
| `REDIRECT` | 68 | 67 duplicate tool routes plus the provisional `/en` to `/` homepage move |
| `PRESERVE` | 9 | Keep maintained localized homepages |
| `PRESERVE_REWRITE` | 3 | Keep path, replace stale privacy/support/changelog presentation |
| `PRESERVE_REDESIGN` | 1 | Keep the blog hub path and rebuild its taxonomy/navigation |
| `PRESERVE_REPOSITION` | 17 | Keep core product/agent paths while aligning them to the redesigned app |
| `PRESERVE_AUDIT` | 14 | Keep comparisons/research but refresh evidence and disclosures |
| `PRESERVE_REVIEW` | 83 | Keep until traffic, backlinks, usefulness, freshness, and cannibalisation are reviewed |

No generated route is currently marked for deletion.

## Migration Rules

1. Preserve existing paths whenever the page still owns a useful and distinct search intent.
2. Use one-to-one permanent redirects; never redirect unrelated retired content to the homepage.
3. Keep query strings where they carry meaningful campaign or tool state.
4. Avoid redirect chains between `l2cache.amvo.store`, `www.l2cache.app`, `/en`, and final paths.
5. Update canonical, Open Graph, schema, sitemap, internal-link, App Store, and in-app URLs together.
6. Preserve the Vercel host rewrites for Amvo Store and Hingejoy.
7. Do not consolidate a tool and editorial page solely because their keywords overlap; compare intent and Search Console evidence first.
8. Record any later retirement in the CSV with evidence, destination, and owner approval.

## Provisional Domain Shape

```text
https://l2cache.app/                 English homepage
https://l2cache.app/fr               Maintained localized homepage
https://l2cache.app/en/tools/...     English browser utilities
https://l2cache.app/product/...      New product pages
https://l2cache.app/integrations/... New integration pages
```

Legacy `/en/<slug>` editorial and comparison URLs remain in place unless there is a strong reason to move them. A new information architecture does not require renaming every old URL.

## Search Console Snapshot

A read-only Google Search Console query for **15 September–15 October 2026** returned 35 query/page combinations and zero clicks in the script's sample.

Pages already receiving impressions and therefore requiring extra migration care include:

1. `/en/tools/certificate-decoder`
   - Largest visible cluster in the sample.
   - Queries include SSL certificate decoder, PEM decoder, CRT decoder, and certificate decode variants.
   - Preserve the exact canonical path and improve usefulness before considering consolidation.
2. `/en/best-mac-clipboard-managers`
   - Impressions for several “best clipboard manager for Mac” variants.
   - Preserve and refresh methodology, current product state, testing date, disadvantages, and disclosure.
3. `/en/codex-session-history-mac`
   - Impression for “codex cli history.”
   - Preserve and align with the redesigned coding-agent capability matrix.
4. `/en/blog-jwt-security`
   - Impression for “decode jwt without secret.”
   - Preserve; maintain a clear distinction between education and the browser tool.
5. `/en/tools/jwk-to-pem` and `/en/tools/base64-image`
   - Early impressions for related utility searches.
   - Preserve pending quality review.

The sample did not show meaningful `l2cache` branded visibility. This supports the existing brand/entity audit: the new homepage must strengthen the exact product identity, while third-party corroboration and consistent naming remain necessary.

## P0 Routes

- `/` and `/en`: canonical/redirect decision and homepage migration.
- `/en/privacy`: full policy rewrite.
- `/en/support`: update branding, domain, product version, and distribution paths.
- `/en/changelog`: preserve release history and update navigation/domain identity.
- `/sitemap.xml` and `/robots.txt`: replace old-domain URLs.

## Validation Before Cutover

1. Crawl the final Vercel preview and export all 2xx, 3xx, 4xx, canonicals, and index directives.
2. Compare the preview crawl to every CSV row.
3. Assert every legacy path has one terminal destination with no loops or chains.
4. Assert every indexable page has exactly one self-referencing canonical.
5. Validate reciprocal `hreflang` only for maintained translations.
6. Verify the sitemap contains only canonical 200-status URLs.
7. Re-run Search Console page/query exports immediately before launch.
8. Monitor 404s, canonical selection, index coverage, and rankings weekly after launch.

