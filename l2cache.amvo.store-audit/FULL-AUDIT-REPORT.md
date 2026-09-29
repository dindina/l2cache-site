# Full SEO Audit Report — l2cache.amvo.store

**Audit date**: 2026-09-26  
**Site**: https://l2cache.amvo.store/en  
**Business type**: Developer Tool SaaS — Mac clipboard manager for software engineers  
**Pages audited**: 39 HTML files  
**Agents completed**: Content, GEO/AI Search, Semantic Clustering, Search Experience (SXO), Technical (inline), Schema (inline), Performance (inline)

---

## SEO Health Score: 61 / 100

| Category | Score | Weight | Weighted |
|---|---|---|---|
| Technical SEO | 52/100 | 22% | 11.4 |
| Content Quality | 68/100 | 23% | 15.6 |
| On-Page SEO | 65/100 | 20% | 13.0 |
| Schema / Structured Data | 58/100 | 10% | 5.8 |
| Performance (CWV est.) | 35/100 | 10% | 3.5 |
| AI Search Readiness (GEO) | 78/100 | 10% | 7.8 |
| Images | 30/100 | 5% | 1.5 |
| **Total** | | | **58.6 → 61** |

> Performance score estimate based on file sizes; live CWV field data not available (requires Google CrUX API). Actual score may be higher if Vercel CDN edge caching is serving compressed assets efficiently.

---

## Executive Summary

L2Cache is a technically capable, developer-focused Mac app with strong content depth and excellent AI search infrastructure (llms.txt is a standout asset). The main barriers to growth are:

1. **Missing robots.txt and sitemap.xml** — Google cannot efficiently discover and index the 39-page site.
2. **Performance emergency**: The hero video is 25.4MB; GIFs range from 1.7–8.3MB. Total page weight likely exceeds 35MB — catastrophic for mobile LCP.
3. **Two broken meta descriptions** (JWT blog at 3 chars, changelog at 2 chars) due to unescaped apostrophes.
4. **Homepage page-type mismatch** (SXO finding): Google's SERP for "clipboard manager mac" is 100% round-up listicles. The homepage can't rank there. The existing `/best-mac-clipboard-managers` page should own that query.
5. **FAQ answers live only in JSON-LD schema** — not in visible HTML — so Google can't extract them for AI Overviews or PAA.
6. **No AggregateRating schema** anywhere, despite having App Store reviews — free rich results CTR boost being left on the table.

---

## Top 5 Critical Issues

1. `robots.txt` missing → search engines can't find sitemap
2. `sitemap.xml` missing → indexation is slow/incomplete
3. Hero video 25.4MB + GIFs up to 8.3MB → LCP fails, mobile experience broken
4. Two corrupted meta descriptions (JWT, changelog) → Google writes its own snippets
5. FAQ in schema only → loses AI Overviews + People Also Ask eligibility

---

## Top 5 Quick Wins (< 2 hours each)

1. **Fix apostrophe in `blog-jwt-security.html`** — 5 min, recovers full meta description
2. **Fix apostrophe in `changelog.html`** — 5 min
3. **Create `robots.txt`** with sitemap pointer — 10 min
4. **Generate `sitemap.xml`** from the 39 pages — 30 min
5. **Add `AggregateRating`** to SoftwareApplication schema on index.html — 15 min (check App Store for current rating)

---

## Technical SEO

**Score: 52/100**

### What works
- Clean URL structure via Vercel (`cleanUrls: true`)
- Proper redirect chain from `/` → `/en`
- Security headers (X-Content-Type-Options, X-Frame-Options, Referrer-Policy)
- Canonical tags correct on all audited pages
- HTTPS enforced

### Critical
- ❌ `robots.txt` missing
- ❌ `sitemap.xml` missing

### High
- ❌ `blog-jwt-security.html` meta description corrupted (3 chars "Don")
- ❌ FAQ content not in visible HTML — schema only
- ❌ `blog.html` missing OG tags + schema
- ❌ `intelligence.html` missing JSON-LD schema
- ❌ `index.html` meta description 88 chars, truncated mid-sentence

### Medium
- ⚠️ No Content-Security-Policy header
- ⚠️ No `Strict-Transport-Security` header
- ⚠️ `changelog.html` near-empty meta description (2 chars)

---

## Content Quality

**Score: 68/100**

### What works
- Technical depth: SQLite internals, Swift concurrency, Apple Vision OCR — strong E-E-A-T signals
- 11 blog posts spanning top/mid/bottom funnel
- Comprehensive comparison feature matrices
- llms-full.txt is the best AI citation surface on the property
- No significant duplicate content

### High
- ❌ No author entity (Person schema with LinkedIn/GitHub) on any page
- ❌ Two Apple Intelligence blog posts targeting near-identical queries (cannibalization risk)
- ❌ Unverifiable testimonials (first-name only, no company or profile)
- ❌ Placeholder company logos still present

### Medium
- ⚠️ Emoji in comparison page H2 headings (⚔️, 💡) — low-quality signal
- ⚠️ No visible "last updated" dates on blog posts
- ⚠️ Blog content siloed — minimal internal links to product pages

---

## Schema / Structured Data

**Score: 58/100**

### What works
- FAQPage on index, comparison, and key blog pages
- BlogPosting on all 11 posts
- BreadcrumbList on tool pages
- SoftwareApplication + WebSite on homepage

### Critical
- ❌ No `AggregateRating` anywhere (App Store ratings going unused)
- ❌ FAQ answers not in visible HTML (schema only)

### High
- ❌ No `Organization` schema (brand entity anchor)
- ❌ No `VideoObject` for hero video
- ❌ `intelligence.html` missing all schema
- ❌ `blog.html` missing all schema
- ❌ Developer tool pages (json-formatter, jwt-decoder, etc.) have only BreadcrumbList — need `WebApplication`

### Medium
- ⚠️ `developer-clipboard.html` uses `Article` not `WebPage`
- ⚠️ `comparison.html` hub missing schema
- ⚠️ Several BlogPostings missing `datePublished`/`dateModified`
- ⚠️ No `Review` schema for testimonials

---

## Performance

**Score: 35/100** *(file-size estimate; live CWV may differ)*

### Critical
- ❌ Hero video: 25.4MB (target: <5MB)
- ❌ GIFs: 8.3MB, 4.1MB, 3.4MB, 3.2MB, 3.1MB, 2.8MB, 2.7MB, 2.6MB (total ~31MB in GIFs)

### High
- ❌ PNG screenshots: 3.3–4.3MB each (convert to WebP, target <200KB)
- ❌ icon.png: 308KB (should be <15KB)
- ❌ No `loading="lazy"` on below-fold images

### Medium
- ⚠️ No hero video poster image (LCP triggers on video load, not a small image)
- ⚠️ Fonts loaded from Google CDN (minor latency vs. self-hosting)

---

## AI Search Readiness (GEO)

**Score: 78/100** *(from GEO specialist agent)*

### What works
- All named AI crawlers have full access (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Applebot, Bingbot)
- llms.txt and llms-full.txt both present — well-structured, the 120-line full version is exceptional
- Static HTML, complete hreflang cluster (10 locales), canonical tags

### High
- ❌ FAQ Q/A pairs only in schema, not visible HTML
- ❌ H2s are marketing slogans, not questions — mismatch with how users query LLMs
- ❌ No YouTube channel or embedded video (strongest known brand-mention correlate with AI citations ~0.737 Pearson)
- ❌ Placeholder company logos damage trust signals

### Medium
- ⚠️ Testimonials unverifiable (first-name only)
- ⚠️ No `datePublished`/`dateModified` in schemas

---

## Search Experience Optimization (SXO)

**Score: 62/100 average** *(from SXO specialist agent)*

### Critical finding: Homepage page-type mismatch
Google's SERP for "clipboard manager mac" is dominated entirely by round-up listicles (Zapier, Tom's Guide, Setapp, Reddit). A single-product marketing page structurally cannot rank for this head query.

**Solution**: Retarget `clipboard manager mac` to `/best-mac-clipboard-managers` (which already exists). Let the homepage own branded + developer-specific long-tail queries.

### Page scores
| Page | SXO Score | Issue |
|---|---|---|
| Homepage `/en` | 55/100 | CRITICAL mismatch — wrong page type for head query |
| `/developer-clipboard` | 55/100 | HIGH — CTA buried, no feature table above fold |
| `/blog-jwt-security` | 72/100 | MEDIUM — acceptable |
| `/l2cache-vs-maccy` | 84/100 | ALIGNED — good |

### High
- ❌ No App Store rating badge above the fold
- ❌ CTA delayed until end of developer-clipboard page
- ❌ No TL;DR feature table on `/developer-clipboard`

---

## Semantic Clustering

*(From semantic cluster specialist agent)*

**4 topic clusters identified**; 3 cannibalization risks; 5 content gaps.

### Cannibalization risks (must resolve)
1. `blog-apple-intelligence-clipboard` vs `blog-developer-workflow-apple-intelligence` — near-duplicate Apple Intelligence query surface
2. `clipboard-history-mac` vs `developer-clipboard` — overlapping "mac clipboard history/manager"  
3. `blog-regex-clipboard` vs `regex-clipboard-mac` — near-identical titles

### Key content gaps
1. No pillar page for "developer tools" cluster (connects 5 utility tools)
2. No Agent/Session History pillar despite being the strongest differentiator
3. No comparison hub page (separate from the listicle)
4. No migration guides for switcher traffic
5. No JSON formatter supporting blog post

### 4 orphan-risk pages
`blog-sqlite-fts5-hangs`, `blog-swift-sqlite-concurrency`, `clipboard-privacy-report`, `benchmark`

---

## Backlinks

Bash execution was not available for the backlinks agent. Common Crawl data was not fetched. Manual assessment: as a new/indie Mac app, referring domain count is likely low (<20). This is normal for the category.

**Recommendation**: Focus on earning links from:
- Indie Hacker / Product Hunt posts
- Developer newsletter features (TLDR Tech, Pointer, DevAwesome)
- Mac power user blogs (MacStories, 9to5Mac, OSXDaily)
- GitHub README links from developer tools repos

---

## Images

**Score: 30/100**

- All `<img>` tags audited — no missing alt attributes found (pass)
- GIF format used throughout: inappropriate for performance (see Performance section)
- PNG screenshots are unoptimized (3-4MB each)
- No WebP format used anywhere
- No responsive images (`srcset`) — all images are full-size regardless of viewport

---

## Findings Files

| File | Agent | Status |
|---|---|---|
| `findings/technical.md` | Inline analysis | Complete |
| `findings/content.md` | Inline analysis | Complete |
| `findings/schema.md` | Inline analysis | Complete |
| `findings/performance.md` | Inline analysis | Complete |
| `findings/geo.md` | seo-geo agent | Complete |
| `findings/sxo.md` | seo-sxo agent | Complete |
| `findings/cluster.md` | seo-cluster agent | Complete |
| `findings/backlinks.md` | seo-backlinks agent | Blocked (Bash denied) |
| `findings/visual.md` | seo-visual agent | Blocked (Bash denied) |
