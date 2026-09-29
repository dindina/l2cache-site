# Technical SEO Findings — l2cache.amvo.store

**Audit date**: 2026-09-26  
**Site**: https://l2cache.amvo.store/en  
**Method**: Local HTML analysis + vercel.json routing review

---

## Critical Issues

### 1. robots.txt is missing
- **Severity**: Critical
- **Evidence**: No `robots.txt` file exists in the project root or `/out/` directory.
- **Impact**: Search engines cannot discover sitemap, and crawlers may infer there are no crawl directives. Most crawlers will still crawl everything, but it's a professional signal gap and llm-crawlers look for this file.
- **Fix**: Create `robots.txt` at site root with `Sitemap:` directive pointing to sitemap.xml.

### 2. sitemap.xml is missing
- **Severity**: Critical
- **Evidence**: No `sitemap.xml` exists. There is a `sitemap.html` page but no machine-readable XML sitemap.
- **Impact**: Google and other engines cannot efficiently discover all 39 pages. New content may take weeks longer to index.
- **Fix**: Generate `sitemap.xml` listing all canonical URLs with `<lastmod>` dates. Reference it from robots.txt.

---

## High Priority Issues

### 3. blog-jwt-security.html meta description is corrupted
- **Severity**: High
- **Evidence**: Meta description reads "Don" (3 chars). The HTML source has `content='Don't paste sensitive tokens...'` using a single-quoted attribute value containing an unescaped apostrophe, which truncates the attribute.
- **Impact**: Google will generate its own snippet; CTR likely reduced.
- **Fix**: Change to double-quoted attribute or escape the apostrophe as `&#39;`.

### 4. FAQ answers exist only in JSON-LD schema, not in visible HTML
- **Severity**: High
- **Evidence**: `index.html` has FAQPage schema with 4 Q/A pairs but zero visible FAQ HTML elements. Google cannot extract answers for AI Overviews if they're not in the page body.
- **Impact**: Loses Google AI Overviews citations, People Also Ask rankings, and Bing Copilot citations.
- **Fix**: Render FAQ visibly on the page, then keep the JSON-LD in sync.

### 5. blog.html missing OG tags and schema
- **Severity**: High
- **Evidence**: Blog index page has no `og:title`, `og:description`, `og:image` or any JSON-LD schema.
- **Impact**: Social previews will be blank; no structured signals for the blog hub page.
- **Fix**: Add standard OG meta tags and an `ItemList` or `CollectionPage` schema.

### 6. intelligence.html missing JSON-LD schema
- **Severity**: High
- **Evidence**: intelligence.html has OG tags but no `application/ld+json`.
- **Impact**: Feature page misses `WebPage` / `Product` / `SoftwareApplication` signals.
- **Fix**: Add `WebPage` + `SoftwareApplication` with feature-specific description.

### 7. index.html meta description too short
- **Severity**: High
- **Evidence**: 88 chars — "Clipboard manager for Mac that saves your full clipboard history — search everything you". Cuts off mid-sentence.
- **Impact**: Truncated snippet in SERPs reduces CTR.
- **Fix**: Rewrite to 140–155 chars with a complete sentence and primary CTA.

---

## Medium Priority Issues

### 8. Multiple comparison pages and feature pages missing H1
- **Severity**: Medium
- **Evidence**: Python audit with `re.findall(r'<h1[^>]*>(.*?)</h1>')` returns empty for:  
  `benchmark.html`, `best-mac-clipboard-managers.html`, `clipboard-history-mac.html`, `clipboard-privacy-report.html`, `developer-clipboard.html`, all `l2cache-vs-*.html` (7 pages), `mac-command-history.html`
- **Note**: The regex misses H1s containing nested HTML (`<br>`, `<span>`) — verified that `index.html` and `intelligence.html` have H1s with inline tags. Comparison pages likely also have H1s with emoji/span wrappers. **Manually verify these before fixing.**
- **Fix**: If H1 is genuinely absent, add it. If it's nested HTML, no action needed.

### 9. changelog.html has thin title and description
- **Severity**: Medium
- **Evidence**: Title = "Changelog — L2Cache" (20 chars), description = "Wh" (truncated, likely same apostrophe bug as JWT page).
- **Fix**: Fix apostrophe escaping; expand title to include keyword.

### 10. Security headers missing Content-Security-Policy
- **Severity**: Medium
- **Evidence**: `vercel.json` sets `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `X-DNS-Prefetch-Control` but no `Content-Security-Policy` or `Strict-Transport-Security`.
- **Fix**: Add CSP header; add `Strict-Transport-Security: max-age=31536000; includeSubDomains`.

### 11. No `<html lang>` hreflang on comparison/blog pages
- **Severity**: Medium
- **Evidence**: Many standalone comparison pages set `lang="en"` on `<html>` but have no `hreflang` alternate links.
- **Impact**: No alternate-language signals for the English canonical; minor international signal gap.

---

## Low Priority Issues

### 12. comparison.html (hub page) missing schema
- **Severity**: Low
- **Evidence**: `/comparison.html` has OG but no JSON-LD. It's a hub linking to all comparison pages.
- **Fix**: Add `CollectionPage` or `WebPage` schema.

### 13. privacy.html and support.html missing schema
- **Severity**: Low
- **Fix**: Add minimal `WebPage` schema to round out coverage.

---

## What Works Well

- Vercel routing is clean: proper `cleanUrls`, redirect chain from `/` → `/en`, all locale aliases redirect to `/en`.
- OG tags present on 35/39 pages.
- Security headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy all set at CDN level.
- HTTPS enforced via Vercel (no mixed content risks in static site).
- llms.txt and llms-full.txt present and well-structured.
- Canonical tags correct on all audited pages.
