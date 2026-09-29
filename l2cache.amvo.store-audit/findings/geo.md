# GEO / AI Search Readiness Audit — l2cache.amvo.store/en

- **URL audited:** https://l2cache.amvo.store/en
- **Business type:** Developer Tool SaaS — native macOS clipboard manager, $4.99 one-time (Mac App Store)
- **Audit date:** 2026-09-26
- **Source of truth for this audit:** local build artifacts under `/Users/dinesh/tech/l2cache-site/out/l2cache/` (Bash and WebFetch were sandbox-blocked during this session, so live crawler probing and third-party mention analysis could not be performed; all HTML/robots/llms findings are read directly from the deployed build output that Vercel serves).

---

## 1. GEO Health Score

**Overall: 78 / 100** — Strong foundation; primary gaps are off-page (brand mention signals) and a few high-leverage on-page adjustments (question-based H2s, dated bylines, `hasPart`/`Product` schema binding, `Review` schema for testimonials).

| Dimension | Weight | Score | Weighted | Notes |
|---|---|---|---|---|
| Citability (extractable passages) | 25% | 70 | 17.5 | Body copy is short and marketing-styled; llms-full.txt is the strong citation surface. Homepage lacks question-based H2s and 40–60 word direct-answer paragraphs. |
| Structural Readability | 20% | 88 | 17.6 | Clean single H1, hierarchical H2/H3, hreflang for 10 locales, canonical, semantic sections, valid sitemap.xml, three JSON-LD blocks. |
| Multi-Modal Content | 15% | 82 | 12.3 | Ten annotated hero screenshots with descriptive alt text, feature GIFs with alt text, side-by-side JWT before/after code block, no video/YouTube embed. |
| Authority & Brand Signals | 20% | 55 | 11.0 | `author=Amvo` meta, App Store listing, publisher schema, but no visible `datePublished`/`dateModified`, no author bio, testimonials use first-name-only (no verifiable Person/Review schema), no linked Wikipedia/Reddit/YouTube entity. |
| Technical Accessibility | 20% | 98 | 19.6 | Fully server-rendered static HTML on Vercel, robots.txt allows all, sitemap.xml, llms.txt + llms-full.txt both present, no JS-gated content, no login walls. |
| **Total** | | | **78.0** | |

---

## 2. AI Crawler Access Status (robots.txt)

`https://l2cache.amvo.store/robots.txt` (verbatim contents):

```
User-agent: *
Allow: /

Sitemap: https://l2cache.amvo.store/sitemap.xml
```

Because there is only a wildcard `User-agent: *` with a global `Allow: /`, **every named AI crawler inherits full access**. There are no bot-specific `Disallow` rules.

| Crawler | Governs | Status | Effect |
|---|---|---|---|
| OAI-SearchBot | ChatGPT Search citations | Allowed (wildcard) | Eligible for ChatGPT Search inclusion. |
| Claude-SearchBot | Claude web search citations | Allowed (wildcard) | Eligible for Claude search inclusion. |
| PerplexityBot | Perplexity answer citations | Allowed (wildcard) | Eligible for Perplexity inclusion. |
| Googlebot | Google Search + AI Overviews | Allowed (wildcard) | Eligible for Google AI Overviews. |
| Bingbot | Bing + Copilot | Allowed (wildcard) | Eligible for Copilot answers. |
| Applebot | Siri / Spotlight / Safari suggestions | Allowed (wildcard) | Eligible. |
| GPTBot | OpenAI *training* (not ChatGPT Search) | Allowed (wildcard) | Training use permitted; not a citation signal. |
| ClaudeBot | Anthropic *training* (not Claude search) | Allowed (wildcard) | Training use permitted; not a citation signal. |
| Google-Extended | Gemini/Vertex training & grounding only | Allowed (wildcard) | Training/grounding use permitted; does not affect Google Search / AI Overviews inclusion. |
| Applebot-Extended | Apple Intelligence training only | Allowed (wildcard) | Training use permitted; does not affect Siri/Safari discoverability. |
| CCBot | Common Crawl (indirect LLM training) | Allowed (wildcard) | Training exposure permitted. |
| cohere-ai | Cohere training | Allowed (wildcard) | Training exposure permitted. |

**Verdict:** Maximally permissive. This is the right default for a product looking for AI-search visibility. **Consider a deliberate policy decision on training-only bots (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, cohere-ai) — blocking them would not affect ChatGPT Search, Claude search, Gemini/AI Overviews, or Siri visibility**, since those channels are governed by different (already-allowed) crawlers. Recommend keeping training bots allowed until you have a specific reason to opt out (compensation strategy, brand training-data concerns, etc.).

---

## 3. llms.txt & RSL 1.0 Status

- **`/llms.txt`** — Present at `/Users/dinesh/tech/l2cache-site/out/l2cache/llms.txt`, 65 lines, well-formed to the [llmstxt.org](https://llmstxt.org) spec: H1 title, `>` blockquote summary, `## Core Pages & Features`, `## Developer Web Utilities`, `## Competitor Comparisons`, `## Technical Blog & Architecture Deep Dives`, `## Technical Specifications`, and `## Optional Full Documentation`. Every entry uses the canonical `- [Title](URL): description` bullet form.
- **`/llms-full.txt`** — Present at `/Users/dinesh/tech/l2cache-site/out/l2cache/llms-full.txt`, 120 lines. Covers executive summary, privacy invariants, architecture (SQLite FTS5, WAL, thread model), password-manager exclusion list, resource footprint, feature catalog, dev-tools catalog, and a competitor matrix with concrete numbers. This is the highest-quality citation surface on the property.
- **RSL 1.0 licensing (`/.well-known/rsl.xml` or in-page RSL metadata):** Not detected. Given the maximally permissive robots.txt, the practical value of RSL is limited today, but adding it becomes worthwhile once training bots are blocked or a paid-license posture is desired.
- **`robots.txt` does not reference `llms.txt`** — not required by the spec, but adding a `# LLM guidance: https://l2cache.amvo.store/llms.txt` comment is a low-cost discoverability hint.

Recommended one-line addition to `out/l2cache/llms.txt` header block: an explicit `<publisher> — <date>` line (e.g., `Published by Amvotech · Last updated 2026-09-26`) so downstream LLMs anchor a recency signal to the file.

---

## 4. Citability Analysis (passage-level extraction potential)

Total visible body word count on `/en` ≈ **1,055 words** (excluding navigation, script, style). Skew is heavy toward short marketing lines. AI citation research points to **134–167 words** as the sweet-spot passage length, with a **direct answer in the first 40–60 words** of each section.

### Strengths
- Every claim on the page is concrete and self-contained: "$4.99 one-time purchase", "0 bytes of clip content sent to any server", "100ms panel opens", "Unlimited clipboard history", "under 15 MB RAM", "sub-millisecond search across 100,000+ entries" (in llms-full.txt). These are exactly the kind of numeric assertions LLMs cite.
- Testimonials contain direct product claims ("replaced Maccy for me", "extract a JWT payload or pretty-print JSON with a single shortcut"), providing quotable social proof.
- Feature cards pair a bold noun-phrase title with a one-sentence description in 20–40 words each — an extractable snippet unit.
- The three JSON-LD blocks (SoftwareApplication, FAQPage, WebSite) give crawlers a machine-readable answer surface for the four most common purchase-intent questions.

### Weaknesses
- **H2s are declarative slogans, not questions.** "The clipboard you always wanted", "Built for code. Not just text.", "Simple, honest pricing", "From Raw Data to Usable Code" — these do not match the way users query LLMs. Question-shaped H2s (e.g., "What makes L2Cache different from Maccy?", "Does L2Cache work on Intel Macs?") are more likely to be excerpted.
- **No 40–60 word direct-answer paragraph opens any section.** Each section opens with a stylized subhead, then jumps into a grid of icon-cards. LLMs prefer a paragraph that fully answers the section title before the visual list.
- **The 4-question FAQ block exists only in JSON-LD, not in visible HTML.** Rendering the FAQ visibly (with question `<h3>` + answer `<p>`) doubles its citation surface (schema + on-page text). Google AI Overviews and Perplexity both pull from visible HTML in addition to structured data.
- **No inline citation of external sources.** Statements like "0 bytes sent" and "sub-millisecond search" would be more citable if linked to `/en/clipboard-privacy-report` and `/en/benchmark` respectively at the point of claim (they currently live on separate pages).
- **Placeholder company logos.** "Trusted by engineers at innovative companies · GlobalTech · CloudNative · FinScale · Medly · DataMap" — these read as invented names, which LLMs treat as a low-trust signal. Either use real customer logos with linked case studies or remove the strip.
- **Testimonial authors are first-name-only ("Sarah J.", "Michael T.", "David R.").** No linkable identity → no verifiable `Review`/`Person` schema → treated as decorative, not a citation source.

### Passage-length breakdown (representative sections)
| Section | Approx. words | Assessment |
|---|---|---|
| Hero (H1 + sub + price tag) | ~35 | Too short for standalone citation, but paired with the schema it works. |
| Developer Tools intro | ~40 | Directional; add an outcome sentence. |
| "From Raw Data to Usable Code" | ~35 (+ code sample) | Great analogy but under-explains. Expand to ~140 words. |
| Feature cards (each) | ~25–45 | Ideal size; keep. |
| Pricing block | ~50 | Good, add ROI/comparison line ("vs. $14.99/year Paste subscription = break-even in 4 months"). |
| Testimonials (each) | ~30 | Good length, verification is the issue. |

---

## 5. Structural & Technical Signals

- **H1:** Single, unique — "The Smart Clipboard for Developers".
- **H2s (visible):** 6 — "Built for code. Not just text.", "From Raw Data to Usable Code", "The clipboard you always wanted", "Developers love L2Cache", "Simple, honest pricing", "From the L2Cache Blog". Clean hierarchy.
- **H3s (visible):** 9 feature-card and blog-card titles. All descriptive.
- **Canonical:** `<link rel="canonical" href="https://l2cache.amvo.store/en">` — correct.
- **hreflang cluster:** 10 locales + `x-default` all present, both in `<head>` and in sitemap.xml. Excellent international SEO/GEO hygiene.
- **Open Graph:** Complete — `og:type`, `og:site_name`, `og:url`, `og:title`, `og:description`, `og:image` (512×512 with alt).
- **JSON-LD blocks:** 3 detected.
    1. `SoftwareApplication` — includes `applicationCategory=DeveloperApplication`, `applicationSubCategory=Clipboard Manager`, `operatingSystem`, `offers` with price 4.99 USD, `publisher` Amvo. **Missing:** `aggregateRating`, `review`, `screenshot`, `featureList`, `softwareRequirements`.
    2. `FAQPage` — 4 Q/A pairs covering price, privacy, Mac compatibility, differentiation vs. built-in Spotlight clipboard. Content is good, but the same Q/A pairs are not rendered in visible HTML.
    3. `WebSite` — minimal (name, url, description). **Missing:** `SearchAction` potential (`/en/tools` or site search could be exposed as a `potentialAction`).
- **Publication dates:** No `datePublished` / `dateModified` on the homepage or in any schema block. This suppresses recency ranking on AI Overviews and reduces the probability of being cited over a competitor with fresh dates. `sitemap.xml` also omits `<lastmod>` for every URL.
- **Author markup:** `<meta name="author" content="Amvo">` only. No `Article`, `Organization`, or `Person` schema for the publisher.
- **Server-rendered vs. SPA:** Fully server-rendered static HTML (Python `build.py` outputs to `/out`, deployed via Vercel with `cleanUrls: true`). All content is present in the initial HTML response — ideal for crawlers that do not render JS (Claude-SearchBot, PerplexityBot, older Bingbot paths).
- **Security headers:** `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin` — good, no crawler impact.
- **Sitemap:** `/sitemap.xml` present, contains all major locale-agnostic English pages with `changefreq` and `priority`, plus `hreflang` alternates on the homepage entry. Missing `<lastmod>` values.
- **`_headers` / CSP / cache:** No `Content-Security-Policy` header configured in `vercel.json`. Not a GEO blocker.

---

## 6. Authority & Brand Mention Signals

Because live web access is blocked in this environment, external mention analysis is inferred from repo evidence (SEO_STRATEGY.md, dev.to draft, medium draft) and the on-site link graph.

| Signal | Correlation with AI citations | Status |
|---|---|---|
| Wikipedia entity | High | **Not detected on-site; likely absent.** No `sameAs` links to a Wikipedia page in schema. Create an entity stub for "L2Cache (macOS clipboard manager)" once independent coverage exists — do not self-publish. |
| Reddit presence | High | Not verifiable from repo. Priority: seed authentic threads in r/macapps, r/programming, r/webdev around specific pain points ("SQLite FTS5 hangs", "on-device AI clipboard", "$4.99 vs. $14.99/yr Paste"). |
| YouTube mentions | Strongest (~0.737) | **No YouTube channel or embedded video anywhere on the page.** Highest-ROI missing signal. Even one 60-second screen-recorded demo embedded on `/en` closes the biggest gap in your GEO profile. |
| LinkedIn / company page | Moderate | No `sameAs` to LinkedIn in `Organization` schema (there is no `Organization` schema on the homepage). |
| App Store presence | High (Apple Intelligence / Siri) | Present — App Store link on hero, pricing, and nav. Strong. |
| Domain Rating / backlinks | Weak (~0.266) | Not measured here. |
| Product Hunt | Moderate | Not linked from the site. |
| GitHub org | Moderate for dev tools | Not linked from the site. Even a lightweight `github.com/amvo` org with the marketing site's issue tracker or a public roadmap earns entity credibility. |
| dev.to / Medium articles | Moderate | Draft files exist in repo (`devto_claude_codex_session_viewer.md`, `medium_draft_screenshot_ocr.md`) — **publish these**. They are ready shipments of citable content. |

**Entity-graph priority:** Add a fourth JSON-LD block (`Organization` for Amvotech) with `sameAs` pointing to whichever of the following are real: Mac App Store publisher page, LinkedIn, X/Twitter, GitHub, Product Hunt, YouTube. This is the single most impactful structured-data change for cross-platform entity resolution.

---

## 7. Platform-Specific Scores

| Platform | Score | Rationale |
|---|---|---|
| **Google AI Overviews** | 78 | Strong technical fundamentals (SSR, schema, hreflang, sitemap). Held back by missing `dateModified`, no `aggregateRating`, no visible FAQ, weak external backlink evidence. Fixing dates + visible FAQ likely lifts to 85+. |
| **ChatGPT Search (OAI-SearchBot)** | 82 | llms.txt + llms-full.txt is exactly the surface OAI-SearchBot and its indexer favor. Numeric self-contained claims (RAM, latency, price) are quotable. Held back by placeholder company logos (trust) and no external corroboration. |
| **Perplexity** | 74 | Perplexity heavily favors sites with third-party citations and Reddit/HN presence. On-page structure is fine; off-page footprint is thin. |
| **Bing Copilot** | 76 | Bingbot allowed, schema is Bing-friendly (SoftwareApplication + FAQPage). Missing Bing Webmaster verification meta and no `Review` schema attached to testimonials. |
| **Claude search (Claude-SearchBot)** | 80 | Allowed, static HTML, dense llms-full.txt content — a Claude-friendly profile. Adding question-headings would push higher. |
| **Apple Intelligence / Siri (Applebot)** | 85 | Applebot allowed, native App Store listing, deep macOS-focused content, structured `SoftwareApplication` schema with `operatingSystem`. Best-positioned channel. |

Note: fewer than ~11% of domains are cited by both ChatGPT and Google AI Overviews, so platform-specific tuning matters. The two highest-payoff cross-platform moves are (a) visible FAQ block + dated content and (b) at least one YouTube demo video with a transcript on-page.

---

## 8. Top 5 Highest-Impact Changes (prioritized by ROI)

### 1. Render the FAQ block visibly on `/en` (Impact: High · Effort: 1 hour)
The `FAQPage` JSON-LD already contains four excellent Q/A pairs (price, privacy, Mac compatibility, vs. built-in Spotlight clipboard). Duplicate them into visible HTML immediately above the footer as `<h3>` questions with 60–100 word answers each. This roughly doubles their citation probability by giving AI Overviews and Perplexity both a schema signal and extractable body text. Add 4–6 more Q/A pairs targeting long-tail queries: "Is L2Cache open source?", "Does L2Cache work with 1Password?", "How is L2Cache different from Maccy?", "Can L2Cache decode JWTs offline?", "Does L2Cache send anything to OpenAI?", "What are the system requirements for AI features?".

### 2. Add `datePublished` / `dateModified` everywhere (Impact: High · Effort: 30 minutes)
Add both fields to all three JSON-LD blocks (`SoftwareApplication.datePublished`, `WebSite.dateModified`, and a new `Article`/`WebPage` block if desired). Add `<meta property="article:modified_time">` to `<head>`. Add `<lastmod>` to every entry in `sitemap.xml`. This is the single lowest-effort, highest-signal recency fix — recency is a strong ranker for AI Overviews. Wire it into `build.py` so every rebuild refreshes the timestamp.

### 3. Rewrite H2s as questions and add 40–60 word direct-answer paragraphs (Impact: High · Effort: 2–3 hours)
Convert:
- "Built for code. Not just text." → "What developer tools does L2Cache include?"
- "From Raw Data to Usable Code" → "How does L2Cache transform copied data automatically?"
- "The clipboard you always wanted" → "What features make L2Cache different from macOS's built-in clipboard?"
- "Simple, honest pricing" → "How much does L2Cache cost?"

Immediately below each rewritten H2, add one paragraph of 40–60 words that answers the question directly, before the visual grid. LLMs preferentially cite the first paragraph after a heading.

### 4. Publish one YouTube demo video and embed it on `/en` (Impact: Very High · Effort: 1 day)
YouTube mentions correlate with AI citations at r≈0.737 — the single strongest brand signal. Record a 60–90 second screen capture demonstrating the three highest-value flows (JWT decode, OCR from screenshot, terminal history search). Upload to a new `@l2cache` or `@amvotech` YouTube channel. Embed via `<iframe>` on `/en` and add `VideoObject` JSON-LD (`name`, `description`, `thumbnailUrl`, `uploadDate`, `contentUrl`, `embedUrl`, `transcript`). Add a transcript below the embed as visible text — Whisper-generated is fine, edit for accuracy. This creates two simultaneous citation surfaces (YouTube's own transcript index + your on-page transcript).

### 5. Replace placeholder logos with real proof + add verifiable testimonials (Impact: Medium-High · Effort: 2–4 hours)
"GlobalTech / CloudNative / FinScale / Medly / DataMap" look invented; LLMs and evaluators treat this as a weak trust signal that can taint everything above it. Options in descending order of impact:

- **Best:** Replace with real customer logos, each linking to a case study or a customer's public Mastodon/X/GitHub post about L2Cache.
- **Good:** Replace with real integration/technology logos ("Built with Swift · SQLite · Apple Intelligence · SwiftUI"), which is honest and citable.
- **Minimum:** Remove the strip entirely.

In parallel, upgrade testimonials to include full name + role + linkable identity (Mac App Store review permalink, dev.to profile, GitHub, LinkedIn), and add matching `Review` schema with `Person.sameAs` links. This turns three decorative quotes into three verifiable citations.

---

## 9. Additional Quick Wins (secondary, low effort)

- Add an `Organization` JSON-LD block for Amvotech with `sameAs` links to App Store publisher page, X, LinkedIn, GitHub, YouTube (once created).
- Add `aggregateRating` to `SoftwareApplication` schema pulled from the Mac App Store rating (must be truthful; do not fabricate).
- Add `screenshot` and `featureList` arrays to `SoftwareApplication` schema.
- Add `<lastmod>` to every URL in `sitemap.xml` (drive from git `mtime`).
- Add `# LLM guidance: https://l2cache.amvo.store/llms.txt` comment line to `robots.txt`.
- Publish the two Markdown drafts already in the repo (`devto_claude_codex_session_viewer.md`, `medium_draft_screenshot_ocr.md`) — this is content that already exists but is unshipped external mention volume.
- Add a `Product` / `SoftwareApplication.review` cross-reference so `Review` entities attach to the product entity for entity graph consolidation.
- Consider a `<publisher> · Last updated <date>` header line in `llms.txt` and `llms-full.txt`.
- Create Reddit seeding plan for r/macapps, r/programming, r/webdev (authentic, non-spam, tied to concrete engineering blog posts already published).
- Once RSL 1.0 stabilizes and if a training-bot block ever becomes policy, publish `/.well-known/rsl.xml`. Not urgent today.

---

## 10. Findings Summary (machine-readable)

```json
{
  "url": "https://l2cache.amvo.store/en",
  "geo_score": 78,
  "dimensions": {
    "citability": 70,
    "structural_readability": 88,
    "multimodal": 82,
    "authority_brand": 55,
    "technical_accessibility": 98
  },
  "robots_txt": {
    "present": true,
    "policy": "wildcard_allow_all",
    "ai_crawlers": {
      "OAI-SearchBot": "allowed",
      "Claude-SearchBot": "allowed",
      "PerplexityBot": "allowed",
      "Googlebot": "allowed",
      "Bingbot": "allowed",
      "Applebot": "allowed",
      "GPTBot_training": "allowed",
      "ClaudeBot_training": "allowed",
      "Google-Extended_training": "allowed",
      "Applebot-Extended_training": "allowed",
      "CCBot": "allowed",
      "cohere-ai": "allowed"
    }
  },
  "llms_txt": { "present": true, "well_formed": true, "sections": 6, "path": "/llms.txt" },
  "llms_full_txt": { "present": true, "well_formed": true, "path": "/llms-full.txt" },
  "rsl_1_0": { "present": false },
  "schema_jsonld": ["SoftwareApplication", "FAQPage", "WebSite"],
  "missing_schema": ["Organization", "VideoObject", "Review", "aggregateRating", "BreadcrumbList", "datePublished", "dateModified"],
  "rendering": "server_rendered_static_html",
  "hreflang_locales": 10,
  "canonical_present": true,
  "sitemap_present": true,
  "sitemap_lastmod": false,
  "brand_signals": {
    "wikipedia_entity": "not_detected",
    "youtube_channel": "not_detected",
    "reddit_presence": "unknown",
    "linkedin_sameAs": "not_detected",
    "app_store_listing": "present",
    "github_org": "not_detected"
  },
  "platform_scores": {
    "google_ai_overviews": 78,
    "chatgpt_search": 82,
    "perplexity": 74,
    "bing_copilot": 76,
    "claude_search": 80,
    "apple_intelligence": 85
  },
  "top_5_recommendations": [
    { "id": "visible_faq", "impact": "high", "effort_hours": 1 },
    { "id": "date_published_modified", "impact": "high", "effort_hours": 0.5 },
    { "id": "question_h2_plus_direct_answer", "impact": "high", "effort_hours": 3 },
    { "id": "youtube_demo_plus_embed_plus_transcript", "impact": "very_high", "effort_hours": 8 },
    { "id": "replace_placeholder_logos_and_verify_testimonials", "impact": "medium_high", "effort_hours": 4 }
  ],
  "audit_environment_notes": "Live web fetches (Bash and WebFetch) were sandbox-blocked during this session. All findings on robots.txt, llms.txt, sitemap, and HTML content are read directly from local Vercel build output at /Users/dinesh/tech/l2cache-site/out/l2cache/, which is the source served at l2cache.amvo.store. External brand-mention verification (Wikipedia, Reddit, YouTube, LinkedIn presence) could not be performed live and should be re-verified in a follow-up run with network access."
}
```
