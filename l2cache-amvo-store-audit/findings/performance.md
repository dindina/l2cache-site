# Performance & Core Web Vitals — l2cache.amvo.store

## Measurement Status

**Unable to measure precisely**: PageSpeed Insights API returned rate-limit error (240 QPM / 25,000 QPD quota exceeded). Recommend re-running when quota resets.

## Observable Performance Signals

| Signal | Value | Assessment |
|--------|-------|-----------|
| Server | Vercel | ✅ CDN with global edge network |
| Cache | `Age: 69324`, `X-Vercel-Cache: HIT` | ✅ Strong caching, 19+ hour age |
| Content-Encoding | gzip | ✅ Present, but missing Brotli (`br`) |
| Transfer-Encoding | chunked | ✅ |
| is_spa | false | ✅ Static HTML, no JS rendering issues |
| Console Errors | 0 | ✅ Clean |

## Homepage Asset Analysis

- **16 images** on homepage: 10 PNG/JPG screenshots + 6 GIF animations
- GIF files: `terminal-history.gif`, `l2cache-ocr.gif`, `l2cache-sql-smart.gif`, `custom-smart-actions.gif`, `l2cache-jwt.gif`
- **Google Fonts**: `DM Mono`, `Fraunces`, `DM Sans` loaded via `https://fonts.googleapis.com`
- **Preconnect**: `https://fonts.googleapis.com` ✓ (but missing `crossorigin` attribute)
- **Missing font preconnect**: `https://fonts.gstatic.com` not preconnected

## Potential Issues

| Issue | Severity | Impact | Recommendation |
|-------|----------|--------|----------------|
| GIF animations | Medium | LCP, bandwidth | Convert to `<video>` or WebP/APNG with `loading="lazy"` |
| Missing `crossorigin` on font preconnect | Low | FOIT/FOUT | Add `crossorigin` to Google Fonts `<link>` |
| Missing `preconnect` to `fonts.gstatic.com` | Low | Font load time | Add `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` |
| Missing Brotli compression | Low | Transfer size | Vercel enables `br` by default — verify configuration |
| No image `loading="lazy"` attribute | Low | LCP for below-fold images | Add lazy loading to screenshot images |
| No image `width`/`height` attributes | Low | CLS | Add explicit dimensions to prevent layout shift |
| No preload for critical hero image | Low | LCP | Add `<link rel="preload">` for primary screenshot |

## Estimated CWV Status (Precautionary)

| Metric | Estimated Status | Confidence |
|--------|-----------------|------------|
| LCP | ⚠️ At risk | Low — large screenshots near viewport |
| INP | ✅ Likely good | Low — static HTML, no heavy JS |
| CLS | ✅ Likely good | Low — CSS fonts with `display=swap` |
