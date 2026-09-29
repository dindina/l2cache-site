# SEO Action Plan — l2cache.amvo.store

**Generated**: 2026-09-26  
**Overall Health Score**: 61/100  
**Target**: 80/100 within 6 weeks

---

## Phase 1: Critical Fixes (Week 1 — ~4 hours total)

These are zero-risk, high-impact fixes. Do them first.

### 1.1 Fix two corrupted meta descriptions (30 min)
**Files**: `blog-jwt-security.html`, `changelog.html`  
**Problem**: Unescaped apostrophe in single-quoted HTML attribute truncates content at the `'` character.  
**Fix**: Change `content='Don't...'` → `content="Don't..."` (switch to double quotes).

```bash
# blog-jwt-security.html — change to:
<meta name="description" content="Don't paste sensitive tokens into online decoders. Discover a native Mac clipboard manager with offline JWT decoding and JSON formatting.">
# changelog.html — fix similarly
```

### 1.2 Create robots.txt (10 min)
**File**: create `/robots.txt`
```
User-agent: *
Allow: /

Sitemap: https://l2cache.amvo.store/sitemap.xml
```

### 1.3 Generate sitemap.xml (30 min)
Create `sitemap.xml` listing all 39 canonical URLs at `https://l2cache.amvo.store/en/{slug}`.

Key pages to include with priority:
- `/en` — priority 1.0
- `/en/intelligence`, `/en/custom-actions` — priority 0.9
- `/en/best-mac-clipboard-managers`, `/en/developer-clipboard` — priority 0.8
- All blog posts — priority 0.7
- All comparison pages — priority 0.6
- Tool pages (jwt-decoder-mac, etc.) — priority 0.5

Add `<lastmod>2026-09-26</lastmod>` on each URL.

### 1.4 Add AggregateRating to SoftwareApplication schema (15 min)
**File**: `index.html`  
Check App Store for current rating. Add to the existing SoftwareApplication JSON-LD block:
```json
"aggregateRating": {
  "@type": "AggregateRating",
  "ratingValue": "4.8",
  "reviewCount": "50",
  "bestRating": "5",
  "worstRating": "1"
}
```

### 1.5 Fix index.html meta description (10 min)
**File**: `index.html`  
Replace 88-char truncated description with:
> "Mac clipboard manager for developers. Search full clipboard history, decode JWTs offline, run regex grep, generate SQL mock data — all on-device with Apple Intelligence."
(156 chars — within 160 char limit)

### 1.6 Fix blog.html title and add OG + schema (30 min)
**File**: `blog.html`  
- Title: `"L2Cache Developer Blog — Clipboard, AI & macOS Tips"`
- Description: `"Deep dives into developer productivity, Mac clipboard management, on-device AI, and Swift/SQLite engineering from the L2Cache team."`
- Add OG tags (og:title, og:description, og:image using a blog hero image)
- Add `CollectionPage` JSON-LD schema

---

## Phase 2: High-Impact Improvements (Weeks 2–3 — ~12 hours)

### 2.1 Compress hero video (2 hours)
**File**: `screenshots/hero-demo.m4v` (currently 25.4MB → target <5MB)

```bash
ffmpeg -i screenshots/hero-demo.m4v \
  -vf "scale=1280:-2" \
  -c:v libx264 -crf 28 -preset slow \
  -c:a aac -b:a 96k \
  screenshots/hero-demo-web.mp4
```

Also create a poster image for LCP:
```bash
ffmpeg -i screenshots/hero-demo-web.mp4 -ss 00:00:01 -vframes 1 screenshots/hero-poster.jpg
```

Update `index.html` video tag:
```html
<video autoplay loop muted playsinline poster="screenshots/hero-poster.jpg">
  <source src="screenshots/hero-demo-web.mp4" type="video/mp4">
</video>
```

### 2.2 Convert GIFs to videos (3 hours)
Convert top 8 largest GIFs. For each:
```bash
ffmpeg -i input.gif \
  -c:v libx264 -pix_fmt yuv420p -crf 28 -an \
  output.mp4
```
Replace `<img src="*.gif">` with `<video autoplay loop muted playsinline>` tags. Estimated saving: ~28MB → ~2MB.

### 2.3 Add visible FAQ section to index.html (1.5 hours)
Move the 4 FAQ items from JSON-LD into visible HTML above the footer. Keep JSON-LD in sync.

```html
<section class="faq-section">
  <h2>Frequently Asked Questions</h2>
  <details><summary>Is L2Cache clipboard data stored in the cloud?</summary>
    <p>No. All clipboard data stays on your Mac...</p>
  </details>
  ...
</section>
```

### 2.4 Add Organization schema (30 min)
Add to `index.html` JSON-LD alongside existing SoftwareApplication:
```json
{
  "@type": "Organization",
  "@id": "https://l2cache.amvo.store/#org",
  "name": "Amvotech",
  "url": "https://l2cache.amvo.store",
  "logo": "https://l2cache.amvo.store/icon.png",
  "sameAs": [
    "https://apps.apple.com/us/app/l2cache/id6774423992"
  ]
}
```

### 2.5 Add VideoObject schema for hero video (20 min)
```json
{
  "@type": "VideoObject",
  "name": "L2Cache — Smart Clipboard Manager for Mac Developers",
  "description": "See L2Cache in action: clipboard history, JWT decoding, regex search, SQL mock data, and AI-powered content detection.",
  "thumbnailUrl": "https://l2cache.amvo.store/screenshots/hero-poster.jpg",
  "uploadDate": "2026-09-26",
  "duration": "PT30S",
  "contentUrl": "https://l2cache.amvo.store/screenshots/hero-demo-web.mp4"
}
```

### 2.6 Add WebApplication schema to tool pages (30 min)
**Files**: `json-formatter-mac.html`, `jwt-decoder-mac.html`, `sql-test-data-generator.html`, `regex-clipboard-mac.html`, `screenshot-ocr-mac.html`

Each needs a `WebApplication` schema block with `name`, `description`, `featureList`, `operatingSystem: "macOS"`.

### 2.7 Add intelligence.html schema (15 min)
**File**: `intelligence.html`  
Add `WebPage` + `SoftwareApplication` JSON-LD block.

### 2.8 Retarget homepage keyword strategy (SXO fix) (1 hour)
Based on SXO agent finding: Google's SERP for "clipboard manager mac" is all round-up listicles.

**Actions**:
- Ensure `/best-mac-clipboard-managers` targets "clipboard manager mac" and "best clipboard managers for mac"
- Ensure `/en` (homepage) targets "l2cache mac" + developer-specific long-tail: "developer clipboard manager mac", "clipboard history mac developer"
- Update index.html title: `"L2Cache — Developer Clipboard Manager for Mac"` (already ~right — no change needed)
- Add internal link from `/best-mac-clipboard-managers` → homepage CTA

### 2.9 Add datePublished/dateModified to all BlogPosting schemas (1 hour)
All 11 blog posts need:
```json
"datePublished": "2026-MM-DD",
"dateModified": "2026-09-26"
```

### 2.10 Add `loading="lazy"` to below-fold images (30 min)
Sitewide: add `loading="lazy"` to all `<img>` tags that are not in the hero/first viewport.

---

## Phase 3: Content & Authority (Month 2 — ~20 hours)

### 3.1 Create Agent Session History pillar page
The cluster agent identified agent/session history as the strongest differentiator but with only one blog post. Create a dedicated feature page `/en/agent-session-history` as a pillar with:
- Feature overview with GIF/video demo
- How it works (technical depth)
- Claude Code + Codex CLI sections
- Token analytics breakdown
- Internal links to `blog-agent-history-analytics`

### 3.2 Create Developer Tools hub page
Connect the 5 utility tools (JWT decoder, JSON formatter, SQL generator, regex matcher, OCR) under a single hub `/en/developer-tools` with:
- Brief descriptions of each tool
- Links to individual tool pages
- Schema `CollectionPage` with `hasPart`

### 3.3 Resolve Apple Intelligence content cannibalization
Consolidate or clearly differentiate:
- `blog-apple-intelligence-clipboard.html` → privacy/security angle (keep as-is, strengthen)
- `blog-developer-workflow-apple-intelligence.html` → rewrite as practical workflow guide with real code/command examples

### 3.4 Add author entities to all blog posts
Add Person schema with LinkedIn/GitHub URL to all BlogPosting schemas. Add visible author bio section at bottom of each post.

### 3.5 Replace placeholder logos with real social proof
Either:
- **Option A**: Get 3-5 real companies or identifiable users. Screenshot their names from App Store reviews.
- **Option B**: Replace the logos section with a stats strip: "X downloads · Y App Store reviews · Z average rating"

### 3.6 Publish YouTube channel + embed demo video
The GEO agent found that YouTube presence has the highest correlation with AI citation rates (~0.737). A 60-90 second demo video:
- Published to YouTube
- Embedded on `/en` and `/en/intelligence`
- With `VideoObject` schema including `@id` pointing to the YouTube URL

### 3.7 Optimize PNGs to WebP
```bash
for f in screenshots/*.png; do
  cwebp -q 82 "$f" -o "${f%.png}.webp"
done
```
Update HTML references. Estimated: 3-4MB → 200-400KB per image.

### 3.8 Reduce icon.png from 308KB to <15KB
Export a 128×128 PNG as favicon. Use a small WebP for nav logo.

---

## Phase 4: Monitoring & Iteration (Ongoing)

### 4.1 Submit sitemap.xml to Google Search Console
Once sitemap.xml is created, submit via GSC. Monitor index coverage report.

### 4.2 Set up drift baseline
After all Phase 1-2 changes are live, run a new audit to establish the new baseline. Track changes in title tags, meta descriptions, schema, and page structure using the seo-drift agent.

### 4.3 Monitor AI Overviews
Search for key queries in Google and Bing:
- "best clipboard manager mac"
- "how to decode JWT on mac"
- "clipboard history mac developer"

Check if L2Cache appears in AI Overviews. If not after Phase 2-3 work, the FAQ expansion in Phase 2.3 needs more Q/A pairs.

### 4.4 Internal linking pass
Run a quarterly internal linking audit. Every blog post should link to at least 2 product pages. Every product page should link to at least 1 blog post.

---

## Priority Matrix

| Priority | Item | Effort | Impact |
|---|---|---|---|
| P0 | Fix 2 broken meta descriptions | 30 min | High |
| P0 | Create robots.txt | 10 min | High |
| P0 | Generate sitemap.xml | 30 min | High |
| P0 | Add AggregateRating schema | 15 min | High (CTR) |
| P0 | Fix index.html meta description | 10 min | Medium |
| P1 | Compress hero video 25MB→5MB | 2 hrs | High (LCP) |
| P1 | Convert GIFs to videos | 3 hrs | High (performance) |
| P1 | Add visible FAQ section | 1.5 hrs | High (AI citations) |
| P1 | Add Organization schema | 30 min | Medium |
| P1 | Add VideoObject schema | 20 min | Medium |
| P2 | Agent history pillar page | 4 hrs | High (differentiation) |
| P2 | Developer tools hub page | 3 hrs | Medium |
| P2 | Fix content cannibalization | 2 hrs | Medium |
| P2 | Author entities on blog posts | 1 hr | Medium (E-E-A-T) |
| P2 | Replace placeholder logos | 2 hrs | Medium (trust) |
| P2 | Optimize PNG → WebP | 1 hr | High (performance) |
| P3 | YouTube channel + embed | 1 day | High (GEO/AI) |
| P3 | Submit to GSC | 15 min | Medium |
