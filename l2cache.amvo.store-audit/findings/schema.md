# Schema / Structured Data Findings — l2cache.amvo.store

**Audit date**: 2026-09-26

---

## Summary

Schema coverage is solid for blog posts and comparison pages. The main gaps are:
- Missing `AggregateRating` everywhere (despite having App Store reviews)
- FAQ answers not rendered in visible HTML (schema-only)
- Several high-value pages missing schema entirely
- No `Organization` entity anchor for brand signals
- No `VideoObject` for the hero video

---

## Critical Issues

### 1. No AggregateRating anywhere
- **Severity**: Critical
- **Evidence**: `SoftwareApplication` schema on index.html has no `aggregateRating` property. No page has AggregateRating.
- **Impact**: Star ratings in SERPs (rich results) increase CTR by ~15-30%. App Store rating and review count can legitimately populate this.
- **Fix**: Add to `index.html` SoftwareApplication schema:
  ```json
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "47",
    "bestRating": "5"
  }
  ```
  Match actual App Store rating. Add to comparison pages as well.

### 2. FAQ answers only in LD+JSON, not visible HTML
- **Severity**: Critical (shared with technical findings)
- **Evidence**: `index.html` FAQPage schema has 4 Q/A pairs; zero visible FAQ elements in the DOM.
- **Impact**: Google will not surface FAQ rich results if answers are schema-only without visible text.
- **Fix**: Add visible `<details>/<summary>` or accordion FAQ section and update schema to match.

---

## High Priority Issues

### 3. intelligence.html missing JSON-LD
- **Severity**: High
- **Type needed**: `WebPage` + `SoftwareApplication` (features feature)
- **Fix**: Add schema block with page description and `isPartOf` pointing to the main app.

### 4. blog.html missing JSON-LD
- **Severity**: High
- **Type needed**: `CollectionPage` with `hasPart` listing blog post URLs
- **Fix**: Add schema block listing top 5 blog posts with their `BlogPosting` links.

### 5. No Organization schema anywhere
- **Severity**: High
- **Evidence**: No `Organization` entity exists. All brand signals are implicit.
- **Impact**: AI search engines (Perplexity, ChatGPT, Google AI) use Organization schema to build knowledge graph entries. Without it, entity disambiguation is weaker.
- **Fix**: Add to index.html:
  ```json
  {
    "@type": "Organization",
    "@id": "https://l2cache.amvo.store/#org",
    "name": "Amvotech",
    "url": "https://l2cache.amvo.store",
    "logo": "https://l2cache.amvo.store/icon.png",
    "sameAs": ["https://apps.apple.com/us/app/l2cache/id6774423992"]
  }
  ```

### 6. No VideoObject for hero video
- **Severity**: High
- **Evidence**: `hero-demo.m4v` is embedded on index.html but has no `VideoObject` schema.
- **Impact**: Video rich results in SERPs (thumbnail + play button) are not triggered. YouTube embeds with VideoObject schema are a strong AI-citation signal.
- **Fix**: Add `VideoObject` schema referencing the video with `name`, `description`, `thumbnailUrl`, `uploadDate`, `duration`.

---

## Medium Priority Issues

### 7. BlogPosting pages missing datePublished/dateModified
- **Severity**: Medium
- **Evidence**: Several blog posts have `BlogPosting` schema but no `datePublished` or `dateModified` properties.
- **Impact**: Google News/Discover and freshness signals are weaker. E-E-A-T freshness dimension suffers.
- **Fix**: Add `"datePublished": "2026-01-15"` and `"dateModified": "2026-09-26"` to all BlogPosting schemas.

### 8. developer-clipboard.html uses Article not WebPage/Product
- **Severity**: Medium
- **Evidence**: A feature landing page uses `Article` schema — this is mismatched.
- **Fix**: Change to `WebPage` with `about` pointing to the SoftwareApplication.

### 9. comparison.html missing schema
- **Severity**: Medium
- **Fix**: Add `CollectionPage` or `ItemList` linking to all comparison pages.

### 10. changelog.html missing schema
- **Severity**: Medium
- **Fix**: Add `WebPage` schema with appropriate description.

---

## Schema Coverage Map

| Page | Schema Types | Gap |
|---|---|---|
| index.html | SoftwareApplication, FAQPage, WebSite | AggregateRating, Organization, VideoObject, FAQ not visible |
| intelligence.html | — | Needs WebPage/SoftwareApplication |
| custom-actions.html | TechArticle | Should be WebPage |
| developer-clipboard.html | Article | Should be WebPage |
| blog.html | — | Needs CollectionPage |
| blog-*.html (11) | BlogPosting (most) | Missing datePublished/Modified on some |
| l2cache-vs-*.html (7) | TechArticle, FAQPage | Add AggregateRating |
| comparison.html | — | Needs CollectionPage |
| changelog.html | — | Needs WebPage |
| best-mac-clipboard-managers.html | Article, ItemList, FAQPage | Good |
| clipboard-history-mac.html | TechArticle, FAQPage | Good |
| json-formatter-mac.html | BreadcrumbList only | Add WebApplication |
| jwt-decoder-mac.html | BreadcrumbList only | Add WebApplication |
| sql-test-data-generator.html | BreadcrumbList only | Add WebApplication |
| regex-clipboard-mac.html | BreadcrumbList only | Add WebApplication |
| screenshot-ocr-mac.html | BreadcrumbList only | Add WebApplication |

---

## What Works Well

- FAQPage schema on comparison pages, best-mac-clipboard-managers, index.
- BreadcrumbList on tool pages.
- BlogPosting schema on all 11 blog posts.
- WebSite schema with SearchAction on index.html.
- SoftwareApplication on index.html (just missing aggregateRating).
