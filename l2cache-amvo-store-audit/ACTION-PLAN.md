# Prioritized Action Plan — l2cache.amvo.store

**Total Recommendations**: 18
**Critical**: 0 | **High**: 1 | **Medium**: 5 | **Low**: 12

---

## Phase 1: Critical Fixes (Week 1)

### 1. Add Security Headers via Vercel

**Severity**: High
**Effort**: 5 minutes
**Dependency**: None

**Action**: Create `vercel.json` in site root with security headers:

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

**Verification**: `curl -sI https://l2cache.amvo.store/en | grep -i x-content-type-options`

### 2. Fix Pricing Signal Discrepancy

**Severity**: Medium
**Effort**: 15 minutes
**Dependency**: Product decision required

**Action**: Decide on one messaging:
- **Option A** (if free in early access): Update JSON-LD `Offer.price` to `"0"`
- **Option B** (if paid): Update HTML comment + meta description to say "$4.99"

**Verification**: Check homepage HTML comment → matches JSON-LD price value

### 3. Add llms.txt for AI Crawler Guidance

**Severity**: Medium
**Effort**: 15 minutes
**Dependency**: None

**Action**: Create `/llms.txt` at site root with site purpose and key page links.

**Verification**: `curl -s https://l2cache.amvo.store/llms.txt`

### 4. Add BlogPosting Schema to Blog Posts

**Severity**: Medium
**Effort**: 2 hours (template for all posts)
**Dependency**: Schema fix #2 completed first

**Action**: Add `BlogPosting` JSON-LD to blog post template with `author`, `datePublished`, `dateModified`, `headline`, `image`.

**Verification**: Each blog post returns `schema.org/BlogPosting` in structured data

### 5. Convert Animated GIFs to Video/WebP

**Severity**: Medium
**Effort**: 1 hour
**Dependency**: None

**Action**: Replace 6 `<img>` GIF tags with `<video autoplay muted loop playsinline>` or animated WebP.

**Verification**: 0 `<img>` tags with `.gif` extension on homepage

---

## Phase 2: High-Impact Improvements (Week 2–3)

### 6. Expand Thin Tool Pages

**Severity**: Medium
**Effort**: 20 hours (47 pages × ~25 minutes each)
**Dependency**: None

**Action**: Add substantive content to each tool page:
- 2-3 code examples showing real usage
- "L2Cache Integration" section (how this tool works with clipboard history)
- FAQ with 3-4 developer-specific questions

**Verification**: Each tool page exceeds 350 words with code examples

### 7. Fix Meta Descriptions Length

**Severity**: Low
**Effort**: 1 minute
**Dependency**: None

**Action**: Trim 2 meta descriptions to ≤155 characters:
- Blog post (220 chars → ≤155)
- Tools index (198 chars → ≤155)

**Verification**: All meta descriptions ≤155 characters

### 8. Optimize Image Loading

**Severity**: Low
**Effort**: 30 minutes
**Dependency**: None

**Action**: Add `loading="lazy"` and `width`/`height` to all non-critical images.

**Verification**: `grep -c 'loading="lazy"' index.html` > 10

### 9. Fix Font Preloading

**Severity**: Low
**Effort**: 5 minutes
**Dependency**: None

**Action**: Add `crossorigin` to Google Fonts `<link>` and preconnect to `fonts.gstatic.com`.

**Verification**: Both `fonts.googleapis.com` and `fonts.gstatic.com` have preconnect tags with `crossorigin`

### 10. Add On-Page Meta Tags

**Severity**: Low
**Effort**: 5 minutes
**Dependency**: None

**Action**: Add `<meta name="author">`, `<meta name="theme-color">` to HTML.

**Verification**: Both meta tags present in homepage HTML

---

## Phase 3: Content & Authority (Month 2)

### 11. Add WebSite Schema with SitelinksSearchbox

**Severity**: Low
**Effort**: 30 minutes
**Dependency**: Phase 1 schema work

**Action**: Add `WebSite` JSON-LD with `PotentialAction` for site search.

**Verification**: Structured data includes `WebSite` type with `potentialAction`

### 12. Add BreadcrumbList Schema

**Severity**: Low
**Effort**: 30 minutes
**Dependency**: None

**Action**: Add `BreadcrumbList` structured data (even if no visual breadcrumbs yet).

**Verification**: Structured data includes `BreadcrumbList` on tool/blog pages

### 13. Upgrade Twitter Card

**Severity**: Low
**Effort**: 5 minutes
**Dependency**: None

**Action**: Change `twitter:card` from `summary` to `summary_large_image`.

**Verification**: `grep 'twitter:card' index.html` shows `summary_large_image`

### 14. Create Branded OG Image

**Severity**: Low
**Effort**: 2 hours (design) + implementation
**Dependency**: None

**Action**: Design 1200×630 OG image with product name, tagline, and screenshot.

**Verification**: `og:image` URL returns a properly sized image

### 15. Add Outbound Citations to Blog

**Severity**: Low
**Effort**: 1 hour
**Dependency**: None

**Action**: Add 2-3 outbound links to relevant external docs (Apple Developer, JSON spec, etc.) in blog posts.

**Verification**: Blog posts contain ≥2 outbound links to authoritative sources

### 16. Add Image Sitemap

**Severity**: Low
**Effort**: 30 minutes
**Dependency**: None

**Action**: Add `<image:image>` entries to sitemap for homepage screenshots and OG images.

**Verification**: Sitemap XML includes `<image:image>` tags

### 17. Add changefreq/Priority to Sitemap

**Severity**: Low
**Effort**: 30 minutes
**Dependency**: None

**Action**: Add `changefreq` and `priority` attributes to sitemap entries.

**Verification**: Sitemap URLs have `changefreq` and `priority` attributes

### 18. Create llms-full.txt

**Severity**: Low
**Effort**: 1 hour
**Dependency**: llms.txt (#3) completed

**Action**: Create comprehensive `llms-full.txt` with detailed descriptions of all 47 tools.

**Verification**: `curl -s https://l2cache.amvo.store/llms-full.txt` returns detailed content

---

## Dependency Graph

```
Phase 1 (Week 1):
  1. Security Headers ──────────────┐
  2. Pricing Fix ───────────────────┤
  3. llms.txt ──────────────────────┼── 7. BlogPosting Schema (needs pricing fix)
  4. BlogPosting Schema ────────────┤
  5. GIF Optimization ──────────────┘

Phase 2 (Week 2-3):
  6. Expand Tool Pages
  7. Meta Description Fix
  8. Image Loading
  9. Font Preloading
  10. Meta Tags

Phase 3 (Month 2):
  11-18: All independent of each other
```

## Effort Summary

| Phase | Hours |
|-------|-------|
| Phase 1 (Critical/High) | 3.5 hr |
| Phase 2 (High-Impact) | 21 hr |
| Phase 3 (Content & Authority) | 6 hr |
| **Total** | **~30.5 hr** |
