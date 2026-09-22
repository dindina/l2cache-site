# Schema & Structured Data Findings — l2cache.amvo.store

## Homepage Structured Data

### Block 1: SoftwareApplication + Offer + Organization

**Status**: VALID ✅

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "L2Cache",
  "applicationCategory": "DeveloperApplication",
  "applicationSubCategory": "Clipboard Manager",
  "operatingSystem": "macOS 13.0 or later",
  "description": "Clipboard manager for Mac that saves your full clipboard history so you can search everything you've ever copied. Private, on-device AI. $4.99 one-time purchase.",
  "url": "https://l2cache.amvo.store/en/",
  "downloadUrl": "https://apps.apple.com/us/app/l2cache/id6774423992?mt=12",
  "softwareVersion": "1.4",
  "offers": {
    "@type": "Offer",
    "price": "4.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Amvo"
  }
}
```

**Notes**: 816 bytes, valid JSON-LD. All required SoftwareApplication properties present.

### Block 2: FAQPage

**Status**: VALID ✅ but DEPRECATED ⚠️

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    // 4 Question/Answer pairs
    // Q1: Is L2Cache free?
    // Q2: Does L2Cache keep my clipboard history private?
    // Q3: What Macs does L2Cache work on?
    // Q4: How is L2Cache different from the built-in macOS clipboard history?
  ]
}
```

**1,641 bytes, valid JSON-LD.** However:
> Google retired FAQ rich results for ALL sites on May 7, 2026. The FAQPage structured data no longer generates rich results in Google SERPs.

**Recommendation**: Per guidelines, **do NOT remove** the FAQPage schema. It remains valid JSON-LD, may benefit other search engines (Bing, DuckDuckGo), and serves as a content signal. Flag at Info level. Consider adding QAPage for genuine user Q&A instead.

## Tool Pages: WebApplication + FAQPage

**Status**: VALID ✅

Tool pages detected with:
- `WebApplication` (with Offer)
- `FAQPage` (with Question/Answer)

Same FAQPage deprecation note applies.

## Missing Structured Data Opportunities

| Opportunity | Severity | Recommendation |
|------------|----------|----------------|
| `Article` / `BlogPosting` on blog posts | Medium | Add structured data to all `/blog*` pages with `author`, `datePublished`, `dateModified`, `headline`, `image` |
| `WebSite` with `sitelinksSearchbox` | Low | Add site-wide `WebSite` schema with search action for in-site search |
| Breadcrumb navigation | Low | Add `BreadcrumbList` schema if breadcrumb navigation exists |
| `Review` aggregate on SoftwareApplication | Low | If customer testimonials include star ratings, add `Review` schema |
| `Pricing` structured data | Low | Consider `PriceSpecification` to clarify the free early-access vs $4.99 purchase |

## Pricing Signal Discrepancy

| Source | Price |
|--------|-------|
| Schema.org `Offer.price` | $4.99 |
| Meta description | "Free while in early access" |
| Schema comment in HTML | "price is '0' while free in early access" — **but actual price is 4.99** |

**Issue**: The HTML comment says price should be "0" during early access, but the actual JSON-LD has `"price": "4.99"`. The meta description says "Free while in early access." This creates a pricing inconsistency between structured data, HTML comment, and marketing copy.

**Recommendation**: Reconcile the pricing message:
- If free during early access: update `Offer.price` to `0` and `priceCurrency` to `USD`
- If $4.99: update the HTML comment and meta description to match

## Schema Validation Summary

| Page | JSON-LD Blocks | Valid | Types |
|------|---------------|-------|-------|
| Homepage | 2 | ✅ | SoftwareApplication, Offer, Organization, FAQPage, Question, Answer |
| Blog post | 2 | ✅ | (same as homepage — inherited) | 
| Tool page | 3 | ✅ | WebApplication, Offer, FAQPage, Question, Answer |
| Tools index | ? | — | Not checked |
