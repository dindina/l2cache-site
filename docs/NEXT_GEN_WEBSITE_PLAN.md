# L2Cache Next-Generation Website Plan

**Status:** Approved for discovery  
**Created:** 15 October 2026  
**Website repository:** `/Users/dinesh/tech/l2cache-site`  
**Production domain:** `l2cache.app` on Vercel

## Placeholder Register

Phase 1 may proceed with the following explicit placeholders. These tokens are planning and prototype values only and must never appear in a production build.

| Field | Provisional value |
|---|---|
| Canonical host | `https://l2cache.app` |
| English homepage | `/` |
| Product name | `L2Cache` |
| Publisher | `[[PUBLISHER_NAME]]` |
| 2.0 Pro price | `[[PRO_PRICE]]` |
| Grandfathering cutoff | `[[GRANDFATHERING_CUTOFF]]` |
| Primary CTA | Mac App Store |
| Secondary CTA | `[[DIRECT_DOWNLOAD_URL]]` if direct distribution remains supported |
| Cloud AI launch status | `[[CLOUD_AI_LAUNCH_STATUS]]` |
| Launch locales | `[[LAUNCH_LOCALES]]` |

The eventual build must fail validation if an unresolved `[[PLACEHOLDER]]` token is present in public output.

## 1. Objective

Create a distinctive, fast, accessible, search-first website for the redesigned L2Cache application. The new site must present L2Cache as a private developer-memory workspace for Mac while preserving the useful search equity, URLs, research, comparisons, support content, and legal content already built by the existing website.

The website must not look or read like a generic AI-generated landing page. Motion and visual effects must explain the product story rather than decorate a sequence of interchangeable feature cards.

## 2. Product Positioning

### Category

**Developer memory for Mac**

L2Cache is broader than a clipboard manager. It connects work that is normally scattered across projects, coding-agent sessions, terminal history, Git activity, tickets, indexed folders, screenshots, and clipboard content.

### Primary promise

**Pick up where you left off.**

### Working product definition

> L2Cache is a developer-memory workspace for Mac that connects projects, coding-agent sessions, terminal history, Git activity, screenshots, and clipboard content so developers can recover context and continue work.

This wording is provisional until the Phase 1 claim matrix is approved. Privacy and AI wording must distinguish on-device defaults from optional cloud providers.

### Messaging hierarchy

1. Resume work without reconstructing context.
2. See the story of a project across tools and time.
3. Search developer activity from one place.
4. Keep local-first control, with clear disclosure when optional cloud AI is enabled.
5. Use clipboard intelligence as one capability within the broader developer-memory product.

## 3. Audience

### Primary

- macOS developers using AI coding agents.
- Developers who move between multiple repositories, branches, terminals, and sessions.
- Privacy-conscious developers who want local-first capture and search.

### Secondary

- Engineering leads who prepare standups or weekly recaps.
- Power users who need searchable clipboard, terminal, screenshot, or folder history.
- Developers comparing Claude Code, Codex, Copilot, Grok Build, or Antigravity workflows.

## 4. Creative Direction

### Recommended direction: The Living Project Timeline

The page follows one believable project through a day. A continuous project-coloured thread connects an agent session, terminal command, commit, ticket, screenshot, clipboard item, test result, milestone, and resume action. The L2Cache application window is the visual protagonist.

### Visual language

- Deep graphite surfaces informed by the redesigned app.
- Project colours used semantically, not as random gradients.
- Editorial spacing and typography with restrained monospace detail.
- Large, real application captures using presentation mode.
- Calm glass and depth effects that remain readable in dark and light environments.
- Motion derived from timeline, search, connection, and resume behaviours.
- No generic neon orb, card wall, fake terminal, invented metric, or stock testimonial treatment.

### MotionSites use

MotionSites may be used as a licensed structural and motion reference. The final page must be an original L2Cache composition. Template copy, generic demonstrations, and visual elements that do not map to real product behaviour will not be carried over.

### Required motion rules

- Motion must reveal a relationship or state change.
- Content remains understandable without JavaScript.
- Respect `prefers-reduced-motion`.
- Do not autoplay large video on mobile.
- Avoid scroll-jacking and motion that delays access to content.

## 5. Homepage Narrative

1. **Hero — Pick up where you left off**  
   A real Today screen with an active project and a resume action. Primary CTA goes to the current official distribution path; secondary CTA opens a short product walkthrough.

2. **Your day, reconstructed**  
   Demonstrate last state, open loops, attention items, next action, standup, and weekly insight.

3. **Every project keeps its story**  
   Connect agent sessions, terminal commands, commits, branches, tests, tickets, milestones, decisions, and recovery points.

4. **Your coding agents finally have a history**  
   Show verified providers and the exact level of history, live capture, resume, plans, skills, rules, and analytics supported for each.

5. **Search everything with Command-K**  
   A lightweight, accessible demonstration of cross-source search.

6. **Private by architecture**  
   Explain local storage, local processing options, sensitive-content exclusions, presentation mode, and the explicit boundary where user-selected cloud providers receive content.

7. **Capability map**  
   Today, Timeline, Tickets, Projects, Clipboard, Connections, Folders, Coding Agents, Terminal, and Milestones. Each entry adds new information and links to a focused page.

8. **Pricing and download**  
   Use live StoreKit/App Store facts. Do not hard-code the 2.0 Pro price before it is decided.

9. **Search-intent FAQ and footer**  
   Answer real questions and link to product pages, integrations, guides, privacy, support, changelog, and publisher information.

## 6. Information Architecture

```text
/
├── product/
│   ├── developer-home/
│   ├── projects/
│   ├── coding-agent-history/
│   ├── terminal-history/
│   ├── clipboard/
│   ├── screenshot-ocr/
│   └── privacy/
├── integrations/
│   ├── claude-code/
│   ├── codex/
│   ├── github-copilot/
│   ├── grok-build/
│   └── google-antigravity/
├── compare/
├── guides/
├── research/
├── blog/
├── changelog/
├── about/
├── support/
└── privacy/
```

Existing URLs should remain in place or receive one-to-one permanent redirects. New folders describe the desired long-term architecture; they are not permission to rename currently ranking pages without evidence.

## 7. Technical Direction

### Recommended architecture

Use a static-first component system, with Astro as the leading candidate. Render all important copy and navigation as HTML. Add client-side JavaScript only for product demonstrations and purposeful motion.

Before committing to Astro, Phase 1 must document parity requirements from the current Python build: locale generation, host rewrites, clean URLs, sitemap creation, canonical rewriting, content utilities, and Vercel output layout.

### Hosting

- Continue deploying on Vercel.
- Preserve the repository's other hosted properties and host-specific rewrites.
- Use preview deployments for review.
- Do not switch production traffic until redirect, canonical, SEO, and content-parity checks pass.

### Performance budgets

- LCP below 2.5 seconds at the 75th percentile.
- INP below 200 milliseconds at the 75th percentile.
- CLS below 0.1 at the 75th percentile.
- Minimal critical JavaScript.
- Responsive AVIF/WebP images with explicit dimensions.
- Self-hosted or system fonts where licensing permits.
- No animation dependency that materially compromises the budgets.

### Accessibility baseline

- WCAG 2.2 AA target.
- Semantic landmarks and heading hierarchy.
- Full keyboard access and visible focus.
- Sufficient colour contrast.
- Reduced-motion experience.
- Captions/transcript for product video.
- Product demonstrations usable without pointer-only interaction.

## 8. SEO Requirements

### Domain and migration

- Select one permanent canonical host for `l2cache.app`.
- Redirect the alternate `www` or apex host to the canonical host.
- Permanently redirect every relevant `l2cache.amvo.store` URL to its equivalent new URL.
- Update canonical tags, Open Graph URLs, schema IDs, sitemap URLs, robots references, App Store seller URL, in-app links, and official profiles.
- Preserve URL paths wherever possible.
- Submit the new sitemap and use Search Console's migration workflow where applicable.

### Page-level requirements

- One clear primary search intent per indexable page.
- Unique title, description, H1, canonical, and social metadata.
- Crawlable copy present in the initial HTML.
- Descriptive internal links and breadcrumbs.
- Visible publication and update dates for editorial content.
- Evidence and methodology for comparisons, benchmarks, security, privacy, pricing, and performance claims.
- Structured data only when it matches visible content.

### Structured data

- `Organization`
- `WebSite`
- `SoftwareApplication`
- `WebPage`
- `BreadcrumbList`
- `Article` or `BlogPosting` for editorial content
- `VideoObject` only for a real, accessible video
- `FAQPage` only for visible, non-promotional FAQ content

### International SEO

- Keep a locale indexable only when the page is genuinely translated and maintained.
- Emit one reciprocal `hreflang` entry per available locale plus `x-default`.
- Never point alternate language URLs at untranslated English content.

### Content clusters

1. Developer memory for Mac.
2. AI coding-agent history and session recovery.
3. Project timelines, milestones, tickets, and standups.
4. Terminal command history.
5. Clipboard, OCR, and local developer utilities.
6. Privacy and local/on-device AI choices.
7. Evidence-led comparisons and original research.

## 9. Analytics and Measurement

- Search Console and Bing Webmaster Tools coverage.
- Organic clicks and impressions by content cluster.
- Branded query visibility.
- App Store/download CTA clicks by landing page.
- Homepage section engagement only where useful.
- Core Web Vitals and JavaScript errors.
- Redirect errors, 404s, canonical selection, and index coverage after launch.

Analytics must not capture clipboard data, terminal content, agent-session content, search queries entered into demonstrations, file paths, or other private developer information.

## 10. Delivery Phases

### Phase 1 — Discovery and brand lock

- Inventory current product facts and feature support.
- Build a publishable-claims matrix.
- Confirm pricing, trial, distribution, macOS requirement, current and launch versions.
- Audit current URLs, domains, redirects, canonicals, translations, assets, and search estate.
- Establish final positioning, audience, voice, primary CTA, and canonical host.
- Identify real screens and demonstration data required for the site.
- Define migration constraints and approve the creative brief.
- Maintain unresolved commercial and identity values in the placeholder register until copy lock.

**Exit:** approved brief, claim matrix, provisional canonical/CTA defaults, placeholder register for unresolved commercial values, URL preservation plan, and screenshot list.

### Phase 2 — Visual prototype

- Produce the Living Project Timeline homepage prototype.
- Produce one restrained Developer Daybook variation.
- Validate desktop, tablet, mobile, reduced motion, and representative content length.

**Exit:** one approved visual direction and interaction specification.

### Phase 3 — Foundation

- Implement the static-first architecture and design tokens.
- Build global navigation, footer, content types, metadata helpers, schema helpers, image pipeline, sitemap, redirects, and accessibility primitives.
- Prove parity with the existing Vercel multi-host routing and SEO build requirements.

**Exit:** deployable foundation with automated SEO and build validation.

### Phase 4 — Homepage

- Implement the approved narrative using verified copy and real assets.
- Add purposeful motion, search demonstration, download CTA, responsive layouts, and reduced-motion treatment.

**Exit:** approved Vercel preview meeting accessibility and performance budgets.

### Phase 5 — Core product and integration pages

- Publish focused product, integration, privacy, about, support, and download pages.
- Establish the new internal-link architecture.

**Exit:** complete conversion path and core topical cluster.

### Phase 6 — Content and SEO migration

- Migrate, improve, consolidate, redirect, or deliberately retire existing pages based on evidence.
- Migrate genuine translations.
- Generate final redirect map and XML sitemaps.

**Exit:** every indexed or linked legacy URL accounted for.

### Phase 7 — QA, launch, and monitoring

- Complete visual, responsive, accessibility, SEO, structured-data, link, redirect, browser, and performance checks.
- Deploy through Vercel.
- Monitor indexing, crawl errors, rankings, Core Web Vitals, and conversions.

**Exit:** production site verified and post-launch monitoring active.

## 11. Guardrails

- Do not invent customers, testimonials, awards, usage numbers, benchmarks, integrations, or security claims.
- Do not describe optional cloud processing as on-device.
- Do not publish an undecided 2.0 price.
- Do not remove or rename ranking URLs without an evidence-backed migration entry.
- Do not replace the homepage with a template before product narrative and content are approved.
- Do not expose private example data in screenshots; use presentation mode or purpose-built fixtures.
- Do not overwrite the existing uncommitted website experiments.

## 12. Definition of Success

- A visitor can explain L2Cache's category and primary benefit after the hero and first demonstration.
- The site looks recognisably derived from L2Cache rather than from a generic AI template.
- Product, privacy, provider, pricing, and platform claims match current evidence.
- Existing valuable URLs and search equity survive the migration.
- The homepage and core pages meet the performance and accessibility budgets.
- Organic visitors have clear paths from informational content to a relevant product page and official download.

