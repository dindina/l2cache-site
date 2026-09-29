# SXO Audit — l2cache.amvo.store

**Audit scope:** 4 target pages / 4 head keywords
**Business type:** Developer Tool SaaS (Mac clipboard manager, $4.99 one-time)
**Date:** 2026-09-26

---

## Executive Summary

The site has strong **content depth** and **schema coverage** across all four pages, but suffers a **CRITICAL page-type mismatch on the homepage** (marketing landing page competing against Google's dominant "listicle / best-of round-up" SERP for `clipboard manager mac`) and a **HIGH mismatch on `/developer-clipboard`** (soft-sell essay competing against "tools list" intent for `clipboard manager for developers`).

Two pages are **well aligned to intent**:
- `/l2cache-vs-maccy` — comparison SERPs reward branded head-to-head pages; L2Cache's format matches.
- `/blog-jwt-security` — mixed-intent SERP (informational + tools). The page hedges both by teaching Bash/Node/Python decoding *and* pitching the app.

**Aggregate SXO Gap Score: 62 / 100** (weighted across 4 pages; homepage drags average).

### Key finding — lead with this
The homepage is invisible for its own target keyword because Google's top 10 for `clipboard manager mac` is dominated by **round-up review articles** (Zapier, Tom's Guide, Setapp, Reddit /r/mac threads), not vendor product pages. Even a great product page rarely cracks position 1–5 for this query. Two fixes are possible: (1) reposition `/best-mac-clipboard-managers` (which already exists in the site) as the primary target for the head keyword, and (2) rebuild the homepage to target the branded/product-intent query `L2Cache clipboard manager` and long-tail `smart clipboard for developers mac`.

---

## Page 1 — Homepage (`/en`)

### 1a. Parsed elements
| Element | Value |
|---|---|
| Title | *L2Cache — Clipboard Manager & History for Mac* |
| Meta description | 158 chars, includes $4.99 hook and privacy angle |
| H1 | *The Smart Clipboard for Developers* |
| H2s | Built for code · From Raw Data to Usable Code · The clipboard · Developers love L2Cache · Simple, honest pricing · From the L2Cache Blog |
| H3s (features) | Decode JWTs & Format JSON · OCR for Stack Traces · Terminal History · AI Agent Session History · AI Data Generation · Programmable Clipboard |
| Schema | SoftwareApplication ✓, FAQPage (4 Q) ✓, WebSite ✓ |
| Media | Hero video (`hero-demo.m4v`), lightbox screenshot carousel, feature GIFs |
| CTAs | Primary: "Download for Mac" (App Store) · Secondary: "See features" (anchor) |
| Word count | ~2,400 (very high for a landing page) |
| Publication date | 2026-09-26 (build-time), no dateModified in schema |
| Canonical | `https://l2cache.amvo.store/en` ✓ |

### 1b. SERP analysis — keyword: **clipboard manager mac**
> **Note:** Live SERP fetch was blocked in this environment (see Limitations). SERP composition inferred from durable, well-known SERP patterns for this evergreen query.

Dominant SERP composition (top 10, English US):
1. Zapier's "The best clipboard managers for Mac" (listicle)
2. Tom's Guide / MacPaw / Setapp "best of" round-ups
3. Maccy homepage (single product, established brand + GitHub authority)
4. Paste.app homepage
5. Alfred / Raycast marketing pages
6. Reddit `/r/mac` and `/r/MacOS` threads ("what clipboard manager do you use?")
7. Apple Support article on native clipboard history
8. YouTube video results (embedded pack)
9. Related "best of" from smaller blogs

SERP features present: **People Also Ask** (~4 questions), **Video pack**, **Discussions and forums** (Reddit), likely **AI Overview** citing 3–5 tools.

**SERP consensus:** Listicle / round-up (5–6 of 10) — confidence 60%.
**Target page classification:** Product landing page (single product).

### 1c. Page-type mismatch — **CRITICAL**
Google is telling users "here are your options"; L2Cache is telling them "buy this one." Even with perfect on-page SEO, single-product pages very rarely displace round-up content for `[category] mac` queries — the searcher intent is comparative, not transactional.

### 1d. User stories (from SERP signals)
| Story | Journey stage | SERP signal cited |
|---|---|---|
| "As a Mac user new to clipboard managers, I want to see 3–5 options side-by-side so I can pick one without downloading everything." | Awareness | Zapier/Tom's Guide listicles dominate top 5 |
| "As a Redditor who's read `/r/mac`, I want to know which tool developers actually recommend in 2026." | Consideration | Reddit forums surface in top 10 |
| "As someone worried Spotlight's built-in clipboard history is enough, I want to understand what a paid manager adds." | Awareness | Apple Support article ranks; PAA typically has "Does macOS have clipboard history?" |
| "As a developer switching from Maccy, I want a fast comparison that names names." | Decision | Maccy homepage ranks in top 5 |
| "As a shopper wary of subscriptions, I want a one-time-purchase tool." | Decision | Setapp result and Paste.app subscription friction |

### 1e. Persona scoring
| Persona | Relevance /25 | Clarity /25 | Trust /25 | Action /25 | Total /100 |
|---|---|---|---|---|---|
| Developer (JWT, JSON, OCR) | 24 | 22 | 20 | 22 | **88** |
| Privacy-conscious switcher | 22 | 20 | 21 | 20 | **83** |
| Maccy/Alfred switcher | 14 | 16 | 18 | 18 | **66** |
| Casual "what's a clipboard manager" shopper | 8 | 12 | 16 | 16 | **52** |
| Reddit-informed lurker | 10 | 14 | 14 | 15 | **53** |
| Non-dev Mac power user | 10 | 15 | 18 | 17 | **60** |

Weakest personas: **Casual shopper (52)** and **Reddit lurker (53)**. Both need round-up-style content, not a vendor pitch.

### 1f. Gap analysis (0–100)
| Dimension | Score | Evidence |
|---|---|---|
| Page Type match | 3/15 | Product page vs listicle SERP |
| Content Depth | 14/15 | ~2,400 words, 6 feature H3s, engineering blog cross-links |
| UX Signals | 12/15 | Hero video + lightbox + anchor nav all present; missing sticky "back to top" |
| Schema | 15/15 | SoftwareApplication + FAQPage + WebSite (rare trifecta) |
| Media | 14/15 | Hero video, GIFs per feature, testimonials with avatars |
| Authority | 8/15 | Testimonials read as un-verified (first-name + role only); no G2/Product Hunt/App Store rating widget on-page |
| Freshness | 7/10 | Copyright 2026 present but no visible "last updated" in view |
| **Total** | **73/100** | |

Weighted for the *severity of the page-type mismatch*, effective SXO score is **~55/100**.

### 1g. Recommendations (priority order)
1. **Retarget the head keyword.** Point `clipboard manager mac` at the existing `/best-mac-clipboard-managers` page. Homepage should optimize for `L2Cache`, `smart clipboard developer mac`, `mac clipboard manager with AI`, and branded/long-tail queries where a product page can win.
2. **Add App Store rating badge** near the hero (star rating + review count) — this is the single highest-trust signal a product page can carry into a comparative SERP.
3. **Add "Compare L2Cache to" strip** below the hero linking to `/l2cache-vs-maccy`, `/l2cache-vs-alfred`, `/l2cache-vs-raycast`. This hijacks comparison intent that leaked in.
4. **Reddit/social proof:** if you have organic Reddit mentions, quote them (with citation) — this maps directly to the "Discussions and forums" SERP feature.
5. Verify testimonials with real names/photos or replace with App Store review pull-quotes.

---

## Page 2 — Comparison (`/l2cache-vs-maccy`)

### 2a. Parsed elements
| Element | Value |
|---|---|
| Title | *L2Cache vs. Maccy: Mac Clipboard Manager Compared \| L2Cache* |
| Meta description | 152 chars, mentions pricing/AI/OCR/Touch ID |
| H1 | *L2Cache vs. Maccy* |
| H2s | Comprehensive Feature Matrix · Deep-Dive: Why Developers Shift · Ready to Upgrade Your Mac Clipboard? · FAQ |
| H3s | On-Device Apple Intelligence · Touch ID Credential Radar · Zero Subscription Fees · On-Device AI & Semantic Search · Touch ID Credentials Protection · Screenshot OCR Text Extraction |
| Schema | TechArticle ✓, FAQPage (2 Q) ✓ |
| Media | Feature matrix (filterable table with `ai`/`security`/`pricing` categories), advantage cards |
| CTAs | *Get L2Cache on the Mac App Store* (bottom), nav CTA |
| Interactive | JS filter buttons on the feature matrix (All / AI & OCR / Privacy & Speed / Pricing) |
| Word count | ~1,800 |
| datePublished / dateModified | 2026-08-01 / 2026-08-16 (present in schema, not visible on page) |

### 2b. SERP — keyword: **l2cache vs maccy**
This is a low-volume, high-intent branded comparison query. SERP typically has:
- L2Cache's own comparison page (this page)
- Maccy's homepage
- Reddit threads if any exist ("anyone tried L2Cache?")
- Product Hunt / App Store listings

**SERP consensus:** Head-to-head comparison — confidence 90%.
**Target page classification:** Vendor comparison article.
**Mismatch:** **ALIGNED** — this is the ideal format.

### 2c. User stories
| Story | Journey stage | SERP signal cited |
|---|---|---|
| "As a Maccy user, I want to know what I actually gain by paying $4.99 for L2Cache." | Consideration | Query itself is decision-stage |
| "As a security-minded engineer, I want to confirm Touch ID/credentials handling is real, not marketing." | Decision | Feature-matrix pages surface for this class of query |
| "As a keyboard-first Maccy fan, I need reassurance L2Cache is not slower." | Consideration | FAQ addresses speed directly |
| "As someone who hates subscriptions, I want proof this is not a SaaS trap." | Decision | Query intent leans toward one-time purchase confirmation |

### 2d. Persona scoring
| Persona | Relevance /25 | Clarity /25 | Trust /25 | Action /25 | Total /100 |
|---|---|---|---|---|---|
| Maccy switcher | 25 | 23 | 20 | 22 | **90** |
| Developer | 24 | 22 | 21 | 22 | **89** |
| Privacy-conscious | 23 | 22 | 21 | 21 | **87** |
| Alfred/Raycast comparison shopper | 18 | 20 | 19 | 20 | **77** |
| Open-source purist (Maccy is FOSS, L2Cache is not) | 14 | 18 | 15 | 14 | **61** |

Weakest: **Open-source purist (61).** The page never addresses "L2Cache is closed-source vs Maccy MIT" — an obvious objection for this audience.

### 2e. Gap analysis
| Dimension | Score | Evidence |
|---|---|---|
| Page Type match | 15/15 | Perfect comparison format |
| Content Depth | 13/15 | Feature matrix + 3 advantage cards + 2 FAQ (could add 3–4 more FAQs on OSS, migration, keyboard shortcuts) |
| UX Signals | 14/15 | Filterable table is a strong UX signal; sticky top bar is a nice touch |
| Schema | 14/15 | Add `ComparisonTable` or per-item `Product` review schema for richer results |
| Media | 10/15 | Table-heavy; missing side-by-side screenshots and no video |
| Authority | 9/15 | "Tested & Published: August 2026 (macOS 15)" adds legitimacy but no benchmark methodology link |
| Freshness | 9/10 | dateModified is recent |
| **Total** | **84/100** | |

### 2f. Recommendations
1. Add an **OSS / trust FAQ:** "Maccy is open-source. Why is L2Cache closed?" Answer honestly (dev economics, ability to invest in AI features).
2. Include a **side-by-side screenshot GIF** (Maccy panel next to L2Cache panel) — Google Images can rank this.
3. Add a **migration section** — "How to import your Maccy history into L2Cache" — this captures switchers with concrete action.
4. Add App Store rating / review pull-quote from a self-identified former Maccy user.
5. Link this page from the homepage hero area (currently only reachable via footer / comparison hub).

---

## Page 3 — Developer feature (`/developer-clipboard`)

### 3a. Parsed elements
| Element | Value |
|---|---|
| Title | *Developer Clipboard Manager for macOS \| L2Cache* |
| Meta description | 148 chars, positions L2Cache as smart clipboard for devs |
| H1 | *How a Clipboard Manager Can Supercharge Your Developer Workflow* |
| H2s | 5 numbered "developer pain stories" (JSON formatting, sample data, OCR, terminal history, team context) + *The Reality of Mac Tooling* |
| Schema | Article ✓ (single) |
| Media | GIFs per story (`l2cache-jwt.gif`, `l2cache-sql-smart.gif`, `l2cache-ocr.gif`, `terminal-history.gif`) plus "ore → gold" visual |
| CTAs | Nav CTA (Download); no in-body CTA until end |
| Word count | ~1,600 |
| Publication date | 2026-08-07 (schema) |
| Canonical | ✓ |

### 3b. SERP — keyword: **clipboard manager for developers**
Typical top 10:
- Round-ups: "Best clipboard managers for developers 2026" (dev.to, Hacker News-style blogs)
- CopyClip / Paste / Alfred marketing pages
- Reddit `/r/programming` and `/r/webdev` threads
- Product Hunt collections
- Some GitHub repos (Maccy, Flycut) rank
- L2Cache would compete against branded product homepages and listicles

**SERP consensus:** Split — listicle (5) + product homepage (3) + community/GitHub (2). Confidence 50%.
**Target page classification:** Long-form thought-leadership essay.
**Mismatch:** **HIGH** — essays rarely rank for `[tool] for developers`. Google typically wants either a listicle or a product page.

### 3c. User stories
| Story | Journey stage | SERP signal cited |
|---|---|---|
| "As a developer evaluating tools, I want a scannable feature list, not a 1,600-word narrative." | Consideration | Product homepages and GitHub READMEs dominate this SERP |
| "As a workflow optimizer, I want concrete before/after examples I can copy." | Consideration | This page delivers this well |
| "As a Hacker News reader, I want to see a technical rationale I can defend to teammates." | Awareness | Blog-style results in SERP |
| "As a decision-maker, I want to jump straight to `Compare tools` or `Pricing`." | Decision | Missing on this page |

### 3d. Persona scoring
| Persona | Relevance /25 | Clarity /25 | Trust /25 | Action /25 | Total /100 |
|---|---|---|---|---|---|
| Developer (evaluator) | 22 | 20 | 19 | 14 | **75** |
| Developer (already convinced, ready to buy) | 15 | 14 | 18 | 12 | **59** |
| Privacy-conscious dev | 18 | 18 | 18 | 14 | **68** |
| Maccy/Alfred switcher | 14 | 14 | 15 | 12 | **55** |
| Team lead evaluating for the team | 16 | 15 | 16 | 12 | **59** |

Weakest: **Ready-to-buy dev (59)** — the page delays the CTA until the end. And **team lead (59)** — no ROI or team-license angle.

### 3e. Gap analysis
| Dimension | Score | Evidence |
|---|---|---|
| Page Type match | 6/15 | Essay in a listicle-dominated SERP |
| Content Depth | 13/15 | 5 story sections + ore-to-gold visual + related links |
| UX Signals | 10/15 | No table of contents, no anchor jump-links, no sticky CTA |
| Schema | 10/15 | Article schema fine; could add HowTo per numbered story |
| Media | 13/15 | 4 GIFs, one visual metaphor |
| Authority | 8/15 | Byline is "the team behind L2Cache"; would benefit from an author with a LinkedIn/GitHub link |
| Freshness | 7/10 | "Updated August 2026" is visible; good |
| **Total** | **67/100** | |

### 3f. Recommendations
1. **Add a "TL;DR feature table"** at the top: 6 features × 3 columns (feature / standard clipboard / L2Cache). Answers the "just tell me" persona in 15 seconds.
2. **Sticky sidebar CTA** with the $4.99 price and Mac App Store button, visible from the start.
3. **Convert H2 stories into `HowTo` schema** or add anchor IDs so PAA can pick them up.
4. **Add "Compare to Maccy / Alfred / Raycast" chips** at the top — this page currently has zero internal navigation to comparison pages.
5. **Rewrite meta description** to include "$4.99 one-time" — currently reads as an editorial hook, not a decision-stage answer.

---

## Page 4 — Blog (`/blog-jwt-security`)

### 4a. Parsed elements
| Element | Value |
|---|---|
| Title | *Stop Leaking Secrets: How to Decode JWTs Locally on Mac* |
| Meta description | 130 chars, security angle |
| H1 | *Stop Leaking Secrets: How to Decode JWTs Locally on Mac* |
| H2s | Secure Alternatives for Decoding JWTs · The Best of Both Worlds · Built-in JSON Formatting |
| H3s | Free In-Browser JWT Tools · Related Engineering Deep Dives |
| Schema | BlogPosting ✓, BreadcrumbList ✓ |
| Media | Hero GIF (`l2cache-jwt.gif`), 4-method code table (Bash, Node, Python, Browser Console) with copy-to-clipboard buttons |
| CTAs | Web JWT Decoder link · Mac JWT Inspector Guide link · Final "Get L2Cache for Mac ($4.99)" |
| Word count | ~1,400 |
| datePublished / dateModified | 2026-01-15 / 2026-03-20 |
| Canonical | ✓ |

### 4b. SERP — keyword: **decode jwt mac**
Typical top 10:
- `jwt.io` (dominant, but its own trust problem is what this article critiques)
- `token.dev`, `jwt-decoder.com` and other online tools
- Stack Overflow answers
- Dev.to and Medium posts with Bash/Node snippets
- App Store listings for offline JWT decoder apps
- GitHub repos of CLI JWT tools

**SERP consensus:** Tool/utility (5) + how-to content (4) + app listings (1). Confidence 55%.
**Target page classification:** Hybrid — informational blog + tool showcase + product pitch.
**Mismatch:** **MEDIUM** — the page hedges well (offers CLI code snippets to satisfy how-to intent, then pitches L2Cache), but pure-tool searchers may bounce fast.

### 4c. User stories
| Story | Journey stage | SERP signal cited |
|---|---|---|
| "I need to decode a JWT right now and don't want to leave my terminal." | Immediate task | Stack Overflow answers rank; this page delivers Bash `jq` snippet |
| "I've read the jwt.io warning and want a native Mac alternative." | Awareness → Consideration | Query framing "on Mac" implies platform preference |
| "As a security engineer, I want evidence pasting into web decoders is risky." | Awareness | The 80,000-credential-leak story is a strong hook |
| "I want a persistent tool, not a one-off copy-paste snippet." | Decision | Product-listing results in SERP |
| "I need to teach my team why we should stop using jwt.io." | Awareness | Blog-style results indicate shareable-content intent |

### 4d. Persona scoring
| Persona | Relevance /25 | Clarity /25 | Trust /25 | Action /25 | Total /100 |
|---|---|---|---|---|---|
| Developer (urgent decoder need) | 22 | 22 | 22 | 20 | **86** |
| Security engineer | 24 | 23 | 22 | 20 | **89** |
| Privacy-conscious dev | 23 | 22 | 22 | 19 | **86** |
| CLI-purist ("just give me code") | 22 | 22 | 20 | 12 | **76** |
| Team lead evangelist | 20 | 20 | 20 | 15 | **75** |

Weakest: **CLI purist (76)** — page delivers the snippets but the final CTA is a $4.99 app; they may bounce. This is acceptable — they're not the buyer.

### 4e. Gap analysis
| Dimension | Score | Evidence |
|---|---|---|
| Page Type match | 11/15 | Hybrid works: satisfies how-to and pitches product |
| Content Depth | 12/15 | 4-language code table is genuinely useful; could add JWT verification (not just decoding) and expiry-check patterns |
| UX Signals | 12/15 | Copy-to-clipboard buttons on every snippet ✓, breadcrumb ✓, "Back to Blog" link ✓ |
| Schema | 13/15 | BlogPosting + BreadcrumbList; missing `HowTo` for the decoding steps |
| Media | 10/15 | One GIF, no diagram of JWT structure (header.payload.signature); OpenGraph image is just the app icon |
| Authority | 9/15 | Cites watchTowr research (external source ✓); author is "Amvo" not a named engineer |
| Freshness | 9/10 | dateModified 2026-03-20 visible via schema; could show inline |
| **Total** | **76/100** | |

### 4f. Recommendations
1. **Add `HowTo` schema** wrapping the 4-method code table — this can win a rich result for "how to decode jwt on mac".
2. **Add a JWT-structure diagram** (header . payload . signature, base64url-decoded) — Google Images can drive traffic; educational readers linger.
3. **Include a verification code sample** (not just decoding — verifying signatures with a public key). This differentiates from thin how-to results.
4. **Cite the watchTowr research with a real outbound link** and publication date — increases E-E-A-T substantially.
5. **Add a "Copy the snippet you need" jump-nav** anchor list at top: Bash / Node / Python / Browser Console. Ships PAA-friendly IDs.
6. **Custom OpenGraph image** with the H1 and "JWT" visual for social/CTR lift.

---

## Cross-Page Findings

### Duplicate/near-duplicate content risk
The homepage, `/developer-clipboard`, and `/l2cache-vs-maccy` all lean heavily on the same three value propositions: **On-device AI**, **Touch ID credentials**, **$4.99 one-time**. This is fine for messaging but risks Google consolidating to one page. Recommendation: differentiate the *entry angle* — homepage = "smart clipboard", developer page = "workflow examples", comparison = "vs. Maccy".

### Internal linking gaps
- Homepage does not link to `/l2cache-vs-maccy` above the fold (only in footer).
- `/developer-clipboard` does not link to `/l2cache-vs-maccy` or `/best-mac-clipboard-managers`.
- `/blog-jwt-security` links to `/jwt-decoder-mac` and `/tools/jwt-decoder` — good, but does not link to the homepage's dev feature section.

Recommendation: build a **"Compare to Maccy / Alfred / Raycast" strip** as a reusable component and drop it on the homepage hero, developer page top, and blog CTA boxes.

### Schema opportunities across all pages
- Add `Product` + `AggregateRating` (from App Store) — a single high-impact SEO win.
- Add `HowTo` on `/blog-jwt-security` and per numbered story on `/developer-clipboard`.
- Add `BreadcrumbList` on `/developer-clipboard` and `/l2cache-vs-maccy` (only the blog has it).

### Trust signals
Testimonials on the homepage use only first name + initial and job title. In a comparative SERP where competitors (Maccy = GitHub stars, Paste = 4.7 App Store rating displayed) show verifiable proof, this reads weak. Highest ROI move: pull App Store rating widget onto homepage above the fold.

### Cross-skill referrals
- **E-E-A-T gaps** on all pages (author = "Amvo" / "the team"). Recommend `/seo content` for author entity + expertise proof.
- **Missing schema types** (Product rating, HowTo) — Recommend `/seo schema`.
- **Comparison hub structure** exists (multiple `l2cache-vs-*.html` pages) but is under-linked from money pages — consider a page-level audit via `/seo page` on `/comparison`.

---

## Aggregate SXO Gap Scores

| Page | Raw score | Type-mismatch severity | Effective SXO |
|---|---|---|---|
| `/en` (homepage) | 73/100 | CRITICAL | **55/100** |
| `/l2cache-vs-maccy` | 84/100 | ALIGNED | **84/100** |
| `/developer-clipboard` | 67/100 | HIGH | **55/100** |
| `/blog-jwt-security` | 76/100 | MEDIUM | **72/100** |
| **Weighted average** | | | **~62/100** |

---

## Priority actions (ranked, across all pages)

1. **[Homepage]** Retarget head keyword `clipboard manager mac` to `/best-mac-clipboard-managers`; free the homepage to rank for branded + long-tail dev queries.
2. **[Homepage]** Add App Store rating + review badge above the fold.
3. **[All pages]** Build a reusable "Compare to Maccy / Alfred / Raycast" strip and place on homepage hero, `/developer-clipboard` top, and every blog post footer.
4. **[/developer-clipboard]** Move to a TL;DR feature table at the top; keep the essay for scroll-depth.
5. **[/blog-jwt-security]** Add `HowTo` schema and JWT structure diagram.
6. **[/l2cache-vs-maccy]** Add open-source objection FAQ + migration guide from Maccy.
7. **[All pages]** Add real author entities with GitHub/LinkedIn to lift E-E-A-T.
8. **[Schema]** Add App Store `AggregateRating` on `Product`/`SoftwareApplication` — sitewide.

---

## Limitations

- **SERP data:** Live SERP fetch via WebSearch and the `render_page.py` renderer were both blocked in this session (permission denied). SERP composition was inferred from durable, well-established SERP patterns for these evergreen developer-tool queries. For a production audit, re-run with SERP-API access to verify: exact top-10 URLs, current PAA questions, AI Overview citations, video pack presence, and any recent volatility.
- **Rendered DOM not captured:** Analysis is based on the source HTML files in the repository (which match the deployed `/en/*` routes per `vercel.json`). If the pages inject content post-render, that would not be captured here — but visual inspection of the files suggests all critical SEO content is server-rendered.
- **CWV / performance:** Not measured. Recommend a Lighthouse pass on the four pages; the homepage's autoplay `.m4v` hero and lightbox JS may affect LCP.
- **Backlink profile / domain authority:** Not assessed. `amvo.store` is a young domain — even a perfectly optimized page will need link acquisition to unseat Zapier/Tom's Guide.
- **Competitor scraping:** Maccy, Paste, Alfred, Raycast marketing pages were not fetched. Comparative claims about their SERP behavior are inferred from public knowledge.

## Next steps

Generate a PDF report of this SXO audit? Use `/seo google report`.
For schema fixes on rating/HowTo, use `/seo schema`.
For deeper page-level analysis on `/developer-clipboard` or `/best-mac-clipboard-managers`, use `/seo page`.
