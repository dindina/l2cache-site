# Phase 1 — Privacy and Network Claim Audit

**Status:** Static source audit complete; runtime verification pending  
**Date:** 15 October 2026  
**Scope:** L2Cache application source, website source, public privacy copy, and dependency declarations  
**Not included:** Packet capture, App Store privacy-label review, legal advice, or third-party provider policy review

## Executive Conclusion

The redesigned website must not claim that nothing ever leaves the Mac, that all AI is on-device, or that the product makes zero network requests.

The application's core history is local and several strong privacy protections are implemented. However, the code also contains optional or action-specific outbound paths for Anthropic Claude, Google Gemini, Google Translate, URL metadata, favicons, the skills catalogue, and coding-agent retrieval. The website itself loads Vercel Web Analytics.

The correct positioning is **local-first with transparent network boundaries**, not “air-gapped,” “zero cloud egress,” or “nothing is ever transmitted.”

## Verified Local Processing and Storage

| Area | Finding | Claim status |
|---|---|---|
| Core history database | SQLite/GRDB storage is local to the Mac | Supported |
| Clipboard and agent history | Read from local pasteboard, configured folders, and local session files | Supported with permission qualification |
| OCR | Apple Vision processing is local | Supported |
| Sensitive-data detection | Performed locally before AI processing | Supported |
| Embeddings/search | Local application services and SQLite full-text search | Supported; exact OS availability should be qualified |
| Apple Intelligence | On-device when available and enabled | Supported with OS/hardware qualification |
| Ollama | Requests use `127.0.0.1` | Supported as a local/self-hosted option |
| Rule-based mode | No AI provider is used | Supported |
| Application telemetry SDKs | No Sentry, Firebase Analytics, Amplitude, Mixpanel, PostHog, or Segment dependency was found | Supported as a static-code observation, not a runtime guarantee |

## Verified Privacy Protections

1. Excluded applications are checked before clipboard items are built or stored.
2. Sensitive clips are skipped by the AI processing queue.
3. Only shareable notes from non-sensitive clips are loaded for AI processing.
4. OCR text is tested for sensitive content before downstream AI, embedding, title generation, or Smart Actions.
5. Agent Access copy states that sensitive clips and excluded applications are omitted.
6. Claude and Gemini API keys are accessed through the existing Keychain service.
7. Presentation mode masks names, paths, prompts, and commands for screen sharing or capture.
8. Cloud actions can display a cloud indicator warning that selected content may be sent externally.

These protections are meaningful and should be explained. They do not justify a global “nothing leaves the Mac” claim.

## Outbound Data Paths

| Path | Trigger | Destination | Potential data | Website disclosure needed |
|---|---|---|---|---|
| Claude AI provider | Cloud mode or Smart Paster fallback when a Claude key exists | Anthropic API | Selected clip/transformation content, instructions, summaries | Yes |
| Gemini AI provider | Cloud mode or Smart Paster fallback when a Gemini key exists | Google Generative Language API | Selected clip/transformation content, instructions, summaries | Yes |
| Coding-agent retrieval | User connects Agent Access and an agent retrieves an item | The connected agent's model provider | Retrieved non-sensitive clip/folder/recovery content | Yes |
| Google Translate action | User invokes translation | Google Translate endpoint | Up to 5,000 characters of selected text | Yes |
| URL metadata enrichment | URL clip is captured and enrichment is allowed | The copied URL's host and platform metadata endpoints | URL, IP/network metadata, request headers | Yes, at least in policy |
| Favicons | A URL/domain preview is rendered | The referenced domain | Domain request and IP/network metadata | Yes, at least in policy |
| Skills catalogue | User opens suggestions/search | `skills.sh` | Search/category request and network metadata | Yes, at least in policy |
| TikTok metadata | Applicable URL enrichment | TikTok oEmbed | Copied TikTok URL and network metadata | Yes, at least in policy |
| App Store/support/product links | User explicitly opens a link | Apple or product website | Normal browser navigation metadata | Standard link disclosure only |
| Vercel Web Analytics | Website page load unless excluded | Vercel | Website visit analytics according to Vercel configuration | Website privacy notice required |

## P0 Findings

### 1. Public privacy copy is materially stale

The current policy says:

- “Everything stays on your Mac.”
- “No data is transmitted.”
- “No clipboard content is ever sent to any external server or AI provider.”
- “We share no data with third parties.”

Those absolutes conflict with implemented outbound paths and must be replaced before the redesigned site launches.

### 2. Homepage privacy claims are also stale

The current homepage includes “100% on-device,” “zero cloud egress,” “air-gapped local SQLite,” and similar language. These claims must not be migrated.

### 3. Cloud fallback is not governed only by the visible provider selector

The current AI settings hide the cloud selector and reset `.cloud` to Apple Intelligence. However, Smart Paster checks for saved Claude or Gemini keys after Apple Intelligence fails and can call the corresponding cloud provider regardless of the visible mode selector. Keys may also persist from an earlier configuration.

This behaviour requires product review. Until it is resolved, the website cannot claim that cloud processing happens only after the user selects “Cloud AI.”

### 4. Cloud-provider response logging needs engineering review

The cloud provider logs prefixes of error bodies and raw model responses. Model responses can reproduce or summarise user content. This should be reviewed against the repository rule that sensitive user content must not be logged.

No application-code change is included in this website planning phase.

### 5. Website analytics and app telemetry must be described separately

No external analytics SDK was found in the Mac app dependencies. The website build injects Vercel Web Analytics. The privacy policy should have distinct sections for:

- The Mac application
- Optional third-party AI/features
- The public website

“The app has no usage telemetry” may be supportable after runtime verification. “We have no analytics” is not accurate for the website.

### 6. Credential hygiene issue remains

The website SEO tooling contains a hardcoded Bing Webmaster API credential. Rotate it, remove it from source, and use environment/secret storage. The credential value is intentionally not reproduced in this document.

## Recommended Public Privacy Framework

### Short homepage statement

> Your developer history is stored locally on your Mac. L2Cache can work with on-device Apple Intelligence, local Ollama, or rule-based processing. Features that contact a website, coding agent, translation service, or optional cloud AI provider should identify that boundary before content is sent.

This is a working statement, not final legal copy.

### Privacy-page structure

1. What L2Cache stores locally.
2. Folder, clipboard, terminal, Git, and coding-agent permissions.
3. Sensitive-content detection and application exclusions.
4. On-device Apple Intelligence and local Ollama.
5. Optional third-party AI providers and exactly what is sent.
6. Coding-agent retrieval and model-provider boundary.
7. URL metadata, favicons, translations, and skills catalogue requests.
8. Website analytics, cookies/local storage, and retention.
9. Data deletion, export, and retention controls.
10. Third-party processors and links to their policies.
11. Contact, policy version, and change history.

## Approved Claim Vocabulary

- “Local-first”
- “Your history is stored on your Mac”
- “On-device Apple Intelligence where available”
- “Local Ollama support”
- “Rule-based mode works without an AI provider”
- “Sensitive clips are excluded from AI processing”
- “You control which applications and folders L2Cache can capture”
- “Optional network features have explicit provider boundaries” after UI/runtime verification

## Blocked Claim Vocabulary

- “100% offline”
- “Air-gapped”
- “Zero cloud egress”
- “Nothing ever leaves your Mac”
- “No third parties”
- “No analytics” without distinguishing app and website
- “All AI runs on-device”
- “Cloud AI is always explicitly selected” until the fallback path is resolved

## Runtime Verification Required

1. Exercise a clean install on macOS 13, the current development OS, and macOS 26 where available.
2. Capture outbound requests for each AI mode and Smart Action.
3. Verify behaviour when legacy Claude/Gemini keys exist while the cloud selector is hidden.
4. Confirm sensitive clips and sensitive OCR never reach external providers.
5. Confirm URL enrichment, favicon, translation, skills, and agent retrieval triggers.
6. Verify website analytics data fields, cookie/local-storage behaviour, retention, and consent requirements.
7. Reconcile the final policy with App Store privacy labels and product UI.
8. Remove or redact any model-response logging that can contain user content.

