# Phase 1 Discovery — L2Cache Next-Generation Website

**Status:** Prototype-ready; production launch gates remain  
**Started:** 15 October 2026  
**Source of truth:** current L2Cache application repository, current website repository, live Vercel responses, and public App Store metadata

## Provisional Defaults and Placeholders

The project may continue using these working values. They are not final commercial or legal claims.

| Field | Working value | Status |
|---|---|---|
| Canonical host | `https://l2cache.app` | Provisional default |
| English homepage | `/` | Provisional default |
| Product capitalization | `L2Cache` | Provisional default |
| Creative direction | Living Project Timeline | Provisional default |
| Primary CTA | Mac App Store | Provisional default |
| Secondary CTA | `[[DIRECT_DOWNLOAD_URL]]` | Placeholder; omit if direct distribution is retired |
| Publisher | `[[PUBLISHER_NAME]]` | Placeholder |
| 2.0 Pro price | `[[PRO_PRICE]]` | Placeholder |
| Grandfathering cutoff | `[[GRANDFATHERING_CUTOFF]]` | Placeholder |
| Cloud AI launch status | `[[CLOUD_AI_LAUNCH_STATUS]]` | Placeholder |
| Launch locales | `[[LAUNCH_LOCALES]]` | Placeholder |

Prototype copy may refer to “a one-time Pro unlock” but must not display a numeric price. Unresolved tokens must be rejected by production build validation.

## 1. Executive Findings

1. The redesigned product should lead with **developer memory**, not clipboard management.
2. The app's new primary experience is Developer Home: Today, Timeline, Tickets, Projects, Clipboard, Connections, Folders, Coding Agents, Terminal, and Milestones.
3. The app supports five coding-agent providers at the data-model level: Claude Code, Codex, GitHub Copilot, Grok Build, and Google Antigravity. Feature depth varies by provider and needs a capability matrix before marketing copy is final.
4. The application defaults to Apple Intelligence where available, supports local Ollama, and also supports optional Claude and Gemini cloud APIs. Existing “no cloud AI mode” website guidance is stale.
5. The current development target is L2Cache 1.5.0 build 138 with macOS 13.0 as the application deployment target. The live US App Store listing is version 1.4.6 and also reports macOS 13.0 minimum.
6. The live App Store app is free to download and describes a 15-day trial plus a one-time Pro unlock. The 2.0 release price and grandfathering cutoff are explicitly undecided in source code. A local StoreKit test configuration uses USD 6.99, but it is not sufficient evidence for the public 2.0 price.
7. `l2cache.app` currently redirects to `www.l2cache.app`, which redirects to `/en`. The website source still emits `l2cache.amvo.store` in canonicals, schema, sitemaps, robots, editorial content, and some application links.
8. The website is a multi-property Vercel repository. Its host rewrites for L2Cache, Amvo Store, and Hingejoy must be preserved during the redesign.
9. The website working tree already contains uncommitted homepage/build changes and several design experiments. Phase 1 will not overwrite them.

## 2. Verified Product Baseline

| Area | Current evidence | Website use |
|---|---|---|
| Product category | Developer Home and memory features span projects, agents, terminal, Git, tickets, folders, OCR, and clipboard | Lead with “developer memory for Mac” |
| App version in development | `MARKETING_VERSION = 1.5.0`, build 138 | Do not expose until release is confirmed |
| Live App Store version | 1.4.6, updated 3 October 2026 | Current public fallback |
| Minimum macOS | Application target 13.0; App Store metadata 13.0 | Safe current claim: macOS 13 or later, pending 2.0 release confirmation |
| Trial | 15 days | Safe if unchanged for 2.0 |
| Purchase model | Non-consumable Pro unlock; no subscription in StoreKit implementation | Safe: one-time Pro unlock, but price is pending |
| Live download price | Free in US App Store | Describe as free download, not “free product” |
| 2.0 price | Undecided in `DeveloperProGrandfathering` | Do not publish a number |
| App Store ID | 6774423992 | Use official App Store CTA where appropriate |
| Coding-agent providers | Claude Code, Codex, GitHub Copilot, Grok Build, Google Antigravity | Provider names are verified; feature depth requires matrix |
| AI modes | Apple Intelligence, local Ollama, optional Claude API, optional Gemini API | Privacy copy must describe user choice and data boundary |
| Default AI mode | Apple Intelligence | May be described as the recommended default, subject to OS/hardware availability |
| Storage/search | Local SQLite/GRDB and full-text search are established architecture | Use precise local-storage wording; avoid claiming all processing is local when cloud mode is enabled |
| Presentation safety | Presentation mode masks names, paths, prompts, and commands | Use it for website captures |

## 3. Product Story Inventory

### Developer Home

- **Today:** active focus, previous state, open loop, next action, attention items, activity summary, standup, weekly insight.
- **Timeline:** calendar view of sessions, commits, builds/tests, terminal activity, and clips; standup and PDF export.
- **Tickets:** recognises configured ticket formats in branches, commits, and agent sessions.
- **Projects:** activity overview, branches, commits, agent sessions, project story, decisions, insights, recovery points, weekly recap, and copied context.
- **Clipboard:** captured content, sensitive state, OCR text, editing, and smart actions.
- **Connections:** groups related items into workflows/runbooks.
- **Folders:** indexes selected folders, including screenshots, for search and project context.
- **Coding Agents:** sessions, plans, skills, MCP/rules, hooks, and insights.
- **Terminal:** captured commands, working directories, exit state, failures, and related successful commands.
- **Milestones:** inferred and user-managed progress with evidence.
- **Global Search:** Command-K search across major memory sources.

### Strongest homepage proof points

1. Resume the latest coding-agent session with its project context.
2. Reconstruct a project's story across agents, Git, terminal, tickets, and clips.
3. Generate an editable standup from recorded activity.
4. Search across developer history with Command-K.
5. Use presentation mode to hide private names, paths, prompts, and commands.

## 4. Coding-Agent Capability Audit

### Verified provider enum

- Claude Code
- Codex
- GitHub Copilot
- Grok Build
- Google Antigravity

### Verified common surface

- Agent history configuration exists for all five providers.
- The session browser exposes provider filtering for all five.
- Plans currently show explicit scanning support for Claude Code and Google Antigravity.
- Rules/MCP/hooks and live continuity support are provider-specific.
- Resume commands are provider-specific.

### Required before copy lock

Create a provider-by-capability matrix covering:

- Historical import
- Live capture/hooks
- Full transcript search
- One-click or terminal resume
- Plans
- Skills and usage
- MCP/rules inspection
- Token and cost analytics
- Git/project association
- Required folder permissions

Do not use a single “supports” logo strip until this matrix is complete.

## 5. Privacy and AI Claim Matrix

| Claim | Status | Notes |
|---|---|---|
| “Data is stored locally on your Mac” | Supported | Core application database is local |
| “L2Cache works without a cloud account” | Likely supported | Validate all 2.0 onboarding paths before publishing |
| “All AI is on-device” | Not supported | Optional Claude and Gemini API modes exist |
| “On-device AI is the default” | Supported with qualification | Apple Intelligence is the configured default; availability depends on OS/hardware/settings |
| “Local AI through Ollama is available” | Supported | User-configured local model |
| “Cloud AI is opt-in” | Needs behavioural verification | Settings require API keys, but final UI/default flow should be tested |
| “Sensitive clips are never exposed to agents” | Supported for Agent Access path | Settings copy excludes sensitive clips and excluded apps; validate other cloud AI paths separately |
| “No telemetry” | Needs current audit | App Store copy says no telemetry; website uses analytics. Product binaries and policies need separate verification |
| “No content leaves the Mac” | Not supported globally | Agent lookups and cloud AI can send selected content to model providers |
| “Presentation mode masks private data” | Supported | Names, paths, prompts, and commands are masked |

### Recommended privacy framing

> Local-first by default. Your history is stored on your Mac. On-device options include Apple Intelligence and Ollama. If you choose a cloud AI provider or let a connected coding agent retrieve a clip, the relevant content is sent to that provider; L2Cache should state this boundary clearly at the point of use and on the website.

Final wording requires review against the current privacy policy and all network paths.

### P0 copy/legal mismatch found

The current public privacy page says the app has no cloud AI, no analytics, no third-party sharing, and never transmits clipboard content. The current homepage repeats “100% on-device,” “zero cloud egress,” and “no clipboard content is ever sent.” These absolute statements do not describe every path present in the redesigned codebase:

- Claude and Gemini cloud-provider implementations exist.
- Agent Access explicitly says clips retrieved by a coding agent are sent to that agent's model provider.
- The website itself uses analytics mechanisms, which must be distinguished from telemetry in the Mac application.
- The AI settings currently hide the cloud selector (`showCloudOption: false`), so cloud AI's 2.0 launch status is not yet established.

Before launch, privacy counsel/product ownership should approve one precise policy covering local storage, on-device processing, hidden or experimental cloud functionality, agent retrieval, third-party providers, website analytics, and sensitive-content exclusions. Until then, absolute “nothing ever leaves the Mac” copy is blocked.

## 6. Pricing and Distribution Baseline

### Verified

- Official Mac App Store ID: `6774423992`.
- Live US listing is free to download.
- Live listing says “15-day free trial” and “one-time purchase to unlock Pro forever.”
- Source defines a 15-day Developer Pro trial.
- Source implements a non-consumable StoreKit Pro unlock.
- No subscription group exists in the StoreKit implementation.

### Not yet approved for the new site

- The final 2.0 Pro price.
- Whether 1.x customers are all grandfathered and the cutoff date.
- Whether direct-download licensing and Mac App Store pricing are identical.
- Whether the primary homepage CTA is App Store only, direct download, or a two-option chooser.
- Whether the public name will be normalised from `L2cache` to `L2Cache` in App Store Connect.

## 7. Current Website and SEO Baseline

### Repository architecture

- Static source pages built by `build.py` into `out/`.
- Vercel `cleanUrls` and no trailing slash.
- Host-specific rewrites serve L2Cache, Amvo Store, and Hingejoy from one deployment.
- Current build configuration includes 45 primary HTML sources, 10 language codes, and one fully localised source page in the current working tree.
- A previous audit recorded 119 generated URLs; the exact production inventory must be recrawled after the current uncommitted build work is resolved.

### Existing SEO strengths

- Static, crawlable HTML.
- Canonical and social metadata pipeline.
- Sitemap and robots support.
- Structured data on important pages.
- Existing comparison, benchmark, privacy, developer-tool, terminal, clipboard, and coding-agent content.
- An SEO validator already checks canonicals, social metadata, sitemap coverage, and `hreflang` rules.

### Critical migration issues

- `l2cache.app` redirects to `www.l2cache.app`, then `/en`.
- Source and public App Store seller metadata still reference `l2cache.amvo.store`.
- The source repository contains more than one thousand old-domain references across HTML, Markdown, build configuration, schema, images, and utilities.
- The application itself still contains several `l2cache.amvo.store` links.
- Domain migration must be path-preserving and coordinated across website, app, App Store Connect, Search Console, Bing Webmaster Tools, and external profiles.

## 8. Asset Baseline

- The website contains approximately 150 screenshot/media files, largely representing the 1.x product.
- The public App Store currently has ten 1.x screenshots.
- Existing website experiments include Apple, 3D, cosmic, glow, “impressive,” Jack, and Finlytic-style treatments.
- These are useful references but are not treated as approved direction.

### New capture list

1. Today with a realistic active project and resume action.
2. Project Story with commits, sessions, tests, and a recovery point.
3. Coding Agents session browser and conversation detail.
4. Coding Agents plans, skills, rules, and insights.
5. Timeline month/day detail.
6. Command-K cross-source search.
7. Terminal failure-to-success context.
8. Connections/runbook view.
9. Clipboard OCR and smart actions.
10. Presentation mode comparison.

All captures must use synthetic project names and content, or the application's presentation mode plus a dedicated fixture dataset.

## 9. Working Brand Recommendation

### Name

Use **L2Cache** consistently on the website. App Store and bundle display name currently use `L2cache`; final public naming needs an explicit decision and coordinated update.

### Descriptor

**Developer memory for Mac**

### Recommended hero

**Eyebrow:** Developer memory for Mac  
**Headline:** Pick up where you left off.  
**Support:** L2Cache connects your projects, coding-agent sessions, terminal history, Git activity, screenshots, and clipboard content so the thread of your work is always ready to resume.

Privacy text should not be added to this support line until the final approved claim is concise and accurate.

### Voice

- Direct and technically literate.
- Calm, specific, and evidence-based.
- Outcome-first, without hype.
- Native-Mac sensibility.
- Explain unfamiliar “developer memory” language through concrete product moments.

## 10. Placeholder Decisions Before Production Copy Lock

1. Replace `[[PUBLISHER_NAME]]` with the final public publisher identity.
2. Replace `[[PRO_PRICE]]` and `[[GRANDFATHERING_CUTOFF]]` when 2.0 commerce is decided.
3. Replace or remove `[[DIRECT_DOWNLOAD_URL]]` after distribution scope is confirmed.
4. Replace `[[CLOUD_AI_LAUNCH_STATUS]]` after the 2.0 feature flag and privacy treatment are confirmed.
5. Replace `[[LAUNCH_LOCALES]]` after translation scope is approved.
6. Confirm the provisional apex-domain, root-English, `L2Cache`, Living Project Timeline, and App Store CTA defaults before production cutover.
7. Finalise the provider capability matrix after fixture verification.
8. Finalise analytics policy, consent requirements, retention, and private-data exclusions.

## 11. Phase 1 Completion Status

- [x] Inspect redesigned app navigation and core product surfaces.
- [x] Verify current development version and deployment target.
- [x] Verify public App Store version, minimum OS, trial language, and distribution model.
- [x] Verify coding-agent provider enum.
- [x] Identify local and cloud AI modes.
- [x] Inspect current domain, Vercel redirect, source canonical, sitemap, and host routing.
- [x] Identify current website working-tree risk and existing design experiments.
- [x] Produce initial provider-by-capability matrix from implementation paths.
- [x] Identify the current privacy-page and redesigned-app claim conflict.
- [x] Establish provisional domain, naming, CTA, and creative defaults.
- [x] Establish placeholders for publisher, pricing, grandfathering, cloud-AI status, direct download, and launch locales.
- [x] Complete an initial static network/privacy audit and draft replacement claim boundaries.
- [ ] Complete runtime network verification and approve final legal privacy language. **Production launch gate; does not block isolated prototypes.**
- [x] Export the 195-artifact legacy URL inventory with a proposed disposition for every route.
- [x] Identify current Search Console impression leaders from the 15 September–15 October sample.
- [ ] Add backlink-level evidence from a maintained backlink source. **Pending because no maintained backlink export was available; no estimate has been invented.**
- [x] Select `https://l2cache.app` and `/` as the approved working canonical defaults.
- [x] Track publisher, pricing, grandfathering, cloud-AI status, direct download, and launch locales as explicit non-production placeholders.
- [x] Adopt `HOMEPAGE_CREATIVE_BRIEF.md` and its screenshot fixture list as the working Phase 2 direction.

See `PHASE_1_COMPLETION.md` for the handoff boundary and the launch gates carried into later phases.

## 12. Phase 1 Exit Criteria

Phase 1 is complete when:

- Product positioning and homepage message are approved.
- Every homepage claim has an evidence status.
- Provider support is represented accurately.
- Privacy language reflects local, agent, and optional cloud data paths.
- Pricing and distribution fields are either final or tracked by explicit non-production placeholders.
- Canonical host and locale strategy have approved provisional defaults.
- All legacy URLs have a keep, improve, merge, redirect, or retire disposition.
- The creative brief and capture list are approved for prototyping.

