# Technical SEO Findings — l2cache.amvo.store

## Crawlability & Indexability

**Status**: PASS

- `robots.txt` allows all crawlers (`User-agent: *` / `Allow: /`)
- Sitemap declared: `https://l2cache.amvo.store/sitemap.xml` (101 URLs)
- Root redirect: `https://l2cache.amvo.store/` → 308 → `https://l2cache.amvo.store/en` (proper redirect, not cloaking)
- Canonical tags present and consistent on all sampled pages
- No soft 404s detected
- No JavaScript redirect traps (page is not SPA — `is_spa: false`)

## Security

**Status**: WARNING

- ✅ HTTPS enforced with HSTS (`Strict-Transport-Security: max-age=63072000` — 2 years)
- ✅ Server: Vercel (CDN with global edge network)
- ❌ Missing `X-Content-Type-Options: nosniff` header
- ❌ Missing `X-Frame-Options: DENY` or `Content-Security-Policy: frame-ancestors` header
- ❌ Missing `Referrer-Policy` header
- ⚠️ `Access-Control-Allow-Origin: *` is set broadly — acceptable for a static content site but could be tightened

**Recommendation**: Add security headers via Vercel `vercel.json` configuration:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "X-DNS-Prefetch-Control", "value": "on" }
      ]
    }
  ]
}
```

## Core Web Vitals

**Status**: UNKNOWN — PSI API rate-limited

- PageSpeed Insights API returned rate-limit error (240 QPM / 25,000 QPD limit)
- Site uses Vercel CDN with caching (`Age: 69324`, `X-Vercel-Cache: HIT`)
- 16 images on homepage including GIFs (potential LCP concern)
- Google Fonts loaded via `preconnect` but missing `crossorigin` attribute
- Recommend re-running PSI test when rate limit resets

## International Targeting

**Status**: PASS

- 10 hreflang annotations: `en`, `zh-Hans`, `fr`, `de`, `it`, `ja`, `ko`, `pt-BR`, `es`, `vi`, plus `x-default`
- hreflang present both in HTML (`<link rel="alternate">`) and sitemap (`<xhtml:link>`)
- Canonical URLs point to language-specific versions correctly
- Root `/` redirects to `/en` with `x-default` pointing to `/en`

## Structured Data Validation

**Status**: PARTIAL

- Block 1: `SoftwareApplication` + `Offer` + `Organization` — valid JSON-LD, 816 bytes
- Block 2: `FAQPage` + `Question` + `Answer` — valid JSON-LD, 1,641 bytes
- Tool pages: `WebApplication` + `FAQPage` + `Offer` + `Answer` + `Question` — valid

## Security Headers Summary

| Header | Status | Value |
|--------|--------|-------|
| Strict-Transport-Security | ✅ Present | `max-age=63072000` |
| Content-Security-Policy | ❌ Missing | — |
| X-Content-Type-Options | ❌ Missing | — |
| X-Frame-Options | ❌ Missing | — |
| Referrer-Policy | ❌ Missing | — |
| Access-Control-Allow-Origin | ⚠️ Broad | `*` |

## Render Performance Signals

| Metric | Value |
|--------|-------|
| Server | Vercel |
| Edge Cache | HIT (Age: 69,324s) |
| Content-Encoding | gzip |
| is_spa | false |
| Console Errors | 0 |
| Render Engine | Static HTML (no SSR/CSR issues) |
