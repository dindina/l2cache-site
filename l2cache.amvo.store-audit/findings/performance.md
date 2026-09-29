# Performance Findings — l2cache.amvo.store

**Audit date**: 2026-09-26  
**Method**: Local file size analysis (no live CWV data available)

---

## Critical Issues

### 1. Hero video is 25.4MB
- **Severity**: Critical
- **Evidence**: `screenshots/hero-demo.m4v` is 25.4MB.
- **Impact**: On a 10 Mbps connection the video data starts loading for ~20 seconds before it can loop. This directly impacts LCP (Largest Contentful Paint) if the video is above the fold.
- **Fix**: 
  - Re-encode to H.264 with CRF 28-32, two-pass, 720p max: `ffmpeg -i hero-demo.m4v -vf scale=1280:-2 -crf 28 -preset slow hero-demo-web.mp4`
  - Target: <5MB for a 30-second hero clip.
  - Add `poster="screenshots/hero-poster.jpg"` attribute to the `<video>` tag so LCP triggers on the image (much smaller) not the video.

### 2. Multiple GIFs over 3MB
- **Severity**: Critical
- **Evidence**:
  - `l2cache-smart-connections.gif`: 8.3MB
  - `l2cache-sql.gif`: 4.1MB
  - `json-smart-actions.gif`: 3.4MB
  - `l2cache-ocr.gif`: 3.2MB
  - `l2cache-jwt.gif`: 3.1MB
  - `regex-pattern-matcher.gif`: 2.8MB
  - `terminal-history.gif`: 2.7MB
  - `l2cache-sql-smart.gif`: 2.6MB
- **Impact**: Each GIF is downloaded in full on page load. A page with 3 GIFs at 3MB each = ~10MB payload before the user scrolls.
- **Fix**: Convert all GIFs to `<video autoplay loop muted playsinline>` with WebM/MP4. Videos compress 5-10x better than GIFs for identical visual quality.
  ```bash
  ffmpeg -i input.gif -c:v libwebm -b:v 0 -crf 33 -an output.webm
  ffmpeg -i input.gif -c:v libx264 -pix_fmt yuv420p -an output.mp4
  ```
  Then use: `<video autoplay loop muted playsinline><source src="x.webm" type="video/webm"><source src="x.mp4" type="video/mp4"></video>`

---

## High Priority Issues

### 3. Large PNG screenshots (3.3–4.3MB each)
- **Severity**: High
- **Evidence**: `screenshot-6-smart-albums.png` (4.3MB), `screenshot-5-developer.png` (4.2MB), etc.
- **Fix**: Convert to WebP with quality 80-85: `cwebp -q 82 input.png -o output.webp`. Expect 60-75% size reduction.

### 4. icon.png is 308KB
- **Severity**: High
- **Evidence**: `icon.png` used as favicon and nav logo is 308KB.
- **Impact**: Every page load downloads 308KB just for the logo.
- **Fix**: Export a 64×64 or 128×128 PNG favicon (~5-10KB). Use a separate 512×512 for apple-touch-icon. Convert nav usage to a smaller WebP.

### 5. No `loading="lazy"` on below-fold images
- **Severity**: High
- **Evidence**: Feature section GIFs and screenshots in blog posts load immediately. Native lazy loading defers off-screen images until the user scrolls near them.
- **Fix**: Add `loading="lazy"` to all `<img>` tags except the first one (hero/LCP element).

---

## Medium Priority Issues

### 6. Google Fonts loaded synchronously
- **Severity**: Medium
- **Evidence**: `<link href="https://fonts.googleapis.com/...">` in `<head>` with no `preconnect` or `font-display: swap` fallback consideration.
- **Fix**: Already has `<link rel="preconnect" href="https://fonts.googleapis.com">` — good. Consider self-hosting fonts or adding `&display=swap` to the Google Fonts URL.

### 7. No `<link rel="preload">` for hero video poster
- **Severity**: Medium
- **Fix**: Add `<link rel="preload" as="image" href="screenshots/hero-poster.jpg">` if a poster image is added.

---

## Performance Budget Targets

| Asset Type | Current | Target |
|---|---|---|
| Hero video | 25.4MB | < 5MB |
| Largest GIF | 8.3MB | < 200KB (as WebM video) |
| PNG screenshots | 3.3–4.3MB | < 200KB (WebP) |
| icon.png | 308KB | < 15KB |
| Total page weight (homepage) | ~35MB+ | < 3MB |

---

## What Works Well

- Static HTML served via Vercel CDN — no server-side rendering latency.
- `<video autoplay loop muted playsinline>` already used for hero (correct pattern).
- Google Fonts `preconnect` hints in place.
- Inline CSS in `theme.css` is 26KB — reasonable.
- No render-blocking scripts (all JS appears at end of body).
