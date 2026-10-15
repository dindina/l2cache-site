# L2Cache Publishable Claims Matrix

**Status:** Prototype copy baseline; production claims remain subject to the gates below  
**Date:** 15 October 2026  
**Applies to:** Next-generation `l2cache.app` website

## How to Use This Matrix

- **Approved for prototype:** May appear in visual prototypes and draft pages.
- **Qualified:** May appear only with the qualification shown.
- **Placeholder:** Keep the explicit `[[PLACEHOLDER]]` token or omit the statement.
- **Blocked:** Must not appear publicly without new evidence and approval.

Prototype approval is not legal approval. The production build must reject unresolved placeholder tokens.

## Positioning and Product

| Proposed claim | Status | Required wording or boundary | Evidence |
|---|---|---|---|
| L2Cache is developer memory for Mac | Approved for prototype | Treat this as the category descriptor, not a trademark claim | Redesigned Developer Home spans projects, agents, terminal, Git, tickets, folders, OCR, and clipboard |
| Pick up where you left off | Approved for prototype | Outcome-led headline; demonstrate it with a real resume flow | Today and project recovery surfaces |
| Your history is stored locally on your Mac | Approved for prototype | “History” refers to the core application database and indexed sources | Local SQLite/GRDB architecture |
| Search across projects, coding-agent sessions, terminal history, Git activity, screenshots, and clipboard content | Approved for prototype | Do not imply every source or field is always available | Command-K and source-specific search paths |
| Reconstruct a project's story across tools and time | Approved for prototype | Present as a product workflow, not a guarantee of complete capture | Project Story and Timeline surfaces |
| Generate an editable standup from recorded activity | Approved for prototype | Do not call it automatic or complete without showing editability | Today/Timeline standup flow |
| Presentation mode masks private names, paths, prompts, and commands | Approved for prototype | Say “masks,” not “anonymises all data” | Presentation-mode implementation |
| macOS 13 or later | Qualified | Current public and development baseline; reconfirm for the 2.0 release | Project deployment target and App Store metadata |
| Version 1.5.0 | Blocked for launch | Development build only; use the live App Store version until release | Xcode settings versus live listing |

## Coding Agents

| Proposed claim | Status | Required wording or boundary | Evidence |
|---|---|---|---|
| Session history from Claude Code, Codex, GitHub Copilot, Grok Build, and Google Antigravity | Qualified | Add: “Available details and live-continuity features vary by agent.” | Dedicated local-history adapters for all five |
| Resume supported sessions with the provider's CLI | Qualified | The CLI and original session must still be installed and available | Provider-specific resume commands |
| Live hooks and handoff for Claude Code, Codex, Copilot, and Grok Build | Qualified | Do not include Antigravity | Continuity implementation |
| Browse plans from Claude Code and Antigravity | Qualified | Do not imply plans for the other three providers | Plans storage scanners |
| Browse installed skills and usage for Claude Code and Codex | Qualified | Do not imply coverage for the other three providers | Skills catalogue and invocation parsers |
| Full integration with every coding agent | Blocked | Capability depth is provider-dependent | Provider capability audit |
| Complete transcripts or everything your agent did | Blocked | Import intentionally excludes some categories and fidelity varies | Capture configuration and adapters |
| Cross-agent cost or performance comparison | Blocked | Requires representative fixtures and a published methodology | Runtime fixture work pending |

## Privacy, AI, and Network Behavior

| Proposed claim | Status | Required wording or boundary | Evidence |
|---|---|---|---|
| Local-first | Approved for prototype | Pair with a visible explanation of optional network boundaries | Static privacy/network audit |
| On-device Apple Intelligence where available | Qualified | Availability depends on hardware, OS, and user settings | AI provider configuration |
| Local Ollama support | Approved for prototype | User-configured local service | Loopback Ollama path |
| Rule-based processing without an AI provider | Approved for prototype | Avoid implying every feature works identically | Rule-based mode |
| Sensitive clips are excluded from AI processing | Qualified | Current verified application queue behavior; runtime verification remains a launch gate | Sensitive-content checks |
| You control which applications and folders L2Cache captures | Qualified | Reflect actual permissions and exclusions in final UI | Exclusion and folder configuration paths |
| Optional network features identify their provider boundary | Blocked pending product verification | Publish only after runtime/UI review confirms the boundary at each trigger | Runtime network audit pending |
| 100% offline / air-gapped / zero cloud egress | Blocked | Optional and action-specific outbound paths exist | Static network audit |
| Nothing ever leaves your Mac | Blocked | Cloud AI, agent retrieval, translation, metadata, favicon, and catalogue paths exist | Static network audit |
| All AI runs on-device | Blocked | Claude and Gemini implementations exist | AI provider implementations |
| No analytics | Blocked | Website uses Vercel Web Analytics; app and website must be described separately | Website build audit |

## Commerce and Distribution

| Proposed claim | Status | Required wording or boundary | Evidence |
|---|---|---|---|
| Download free from the Mac App Store | Qualified | “Free download” is not “all features are free” | Current US App Store listing |
| 15-day trial | Qualified | Reconfirm immediately before the 2.0 launch | StoreKit source and current listing |
| One-time Pro unlock; no subscription | Qualified | Do not include a numeric price until approved | Non-consumable StoreKit product |
| Pro costs `[[PRO_PRICE]]` | Placeholder | Must fail production validation until replaced | Commercial decision pending |
| Existing customers before `[[GRANDFATHERING_CUTOFF]]` keep Pro | Placeholder | Do not paraphrase before policy is approved | Commercial decision pending |
| Direct download | Placeholder | Use `[[DIRECT_DOWNLOAD_URL]]` or omit the secondary CTA | Distribution decision pending |

## Identity and Locale Placeholders

| Field | Current token | Production requirement |
|---|---|---|
| Publisher | `[[PUBLISHER_NAME]]` | Match website, schema, App Store, support, and official profiles |
| Cloud AI launch status | `[[CLOUD_AI_LAUNCH_STATUS]]` | Match visible product behavior and privacy policy |
| Launch locales | `[[LAUNCH_LOCALES]]` | Publish only maintained translations with reciprocal `hreflang` |

## Production Copy Gates

1. Complete runtime network verification, including the saved-key Smart Paster fallback.
2. Reconcile the privacy policy, App Store privacy labels, product UI, and website analytics disclosure.
3. Exercise representative fixtures for all five coding-agent providers.
4. Replace or deliberately remove every placeholder token.
5. Confirm the shipping version, macOS requirement, trial, price, grandfathering, and download paths.
6. Have product/legal ownership approve the final privacy and commerce wording.

