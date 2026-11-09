# Sprint C4 — Programmable clipboard article

**Status:** ✅ Done · **Date:** 2026-11-09
**Fills the gap for:** the big Clipboard tile and Clipboard popup (smart bubble).

## Tasks

### T-C401 — `/en/programmable-clipboard-mac`
**Working title:** A programmable clipboard for Mac: smart actions at your cursor
**Covers:** the copy → bubble → transform → paste flow (and why it's App Store-safe: no accessibility APIs or simulated paste); collapsed pill vs expanded menu; content types it recognises (JSON, JWT, SQL, CSV, URLs, colours, regex, AWS ARNs, connection strings, Docker images, K8s manifests, Terraform, logs, terminal commands…) with two or three real actions each; custom actions as shell scripts or AI prompts, scoped by content type; cloud AI indicator; large-clip limits; sensitive clips.
**Sources:** `docs/contextual-smart-actions-feature.md`, `L2cache/Features/ActionBubble/ActionBubbleView.swift` (header titles), `L2cache/Features/SmartPaster/SmartTransform.swift` (action labels), `L2cache/Services/CustomActionStore.swift`, the content-type manual test docs. Use only labels that exist in code.

### T-C402 — Refresh `/en/custom-actions`
Keep its path and core content (W-series rule). Add a short intro linking to the new article and update any wording that contradicts the shipped bubble.

## Wiring
`build.py`, `sitemap.xml`, `llms.txt`, `blog.html`, footer (Product → "Programmable clipboard"), Clipboard popup "Read more"; cross-links to `clipboard-history-mac`, `json-formatter-mac`, `jwt-decoder-mac`, `regex-clipboard-mac`.

## Verify
Facts table; `build.py`, `check_home_links.py`, `validate_seo.py`; 1440px and 390px.

## Review
- **T-C401** `programmable-clipboard-mac.html` (~7 min): copy → bubble → pick → paste; dismissal (≈4 s, paused on hover, click-away or Esc, never takes focus); why no Accessibility or simulated paste; last-used action first; 16-row table of content types with real labels; Related History and Previously fixed; custom actions (Shell Command / AI Prompt, content types, playground, jq example); when it appears (three modes); privacy and limits; free vs Pro.
- **T-C402** `custom-actions.html`: path and recipes kept. New intro paragraph linking the article; content-type list matched to the picker (Docker images not "Docker commands", plus ARNs, system logs, terminal commands, HTTP); stdout step mentions the playground. **Also fixed:** the page was 1185px wide at 390px (recipe grid track didn't shrink below its code blocks) and showed two Download buttons on phones. Now `minmax(0, 1fr)` tracks, `min-width: 0` cards, and `.nav-cta` hidden ≤700px.
- **Wiring:** `build.py`, `validate_seo.py`, `blog.html` (after the featured card), `sitemap.html`, `llms.txt` (next to Custom Actions), footer Product → "Programmable clipboard", Clipboard popup "Read more" (first). Cross-links: custom-actions ↔ article, article → clipboard-history-mac, json-formatter-mac, jwt-decoder-mac, regex-clipboard-mac, coding-agent-memory-mcp-hooks.
- **Changes from plan:** terminal commands aren't in the article's bubble list (the bubble never shows for them; actions are in the panel). Connection strings are named as recognised, with no action list, because they have no type-specific labels. No "100+ actions" count claim.
- **Verify:** `build.py` OK; `site_i18n.py extract` → 586 strings; `check_home_links.py` → 79 internal links resolve; `validate_seo.py` passed (46 pages). Article at 390px (all tables fit) and 1440px; custom-actions at 390px (no page scroll, one Download button).

### Facts table
| Claim | Source |
|---|---|
| Only pasteboard read/write; no Accessibility or simulated paste | `docs/contextual-smart-actions-feature.md` |
| Bubble at mouse location; doesn't take focus; auto-dismiss 4 s, paused while hovered; click-away and Esc close | `ActionBubbleController.swift` `present`, `scheduleDismiss(after: 4.0)`, monitors |
| Last-used action per content type promoted first | `ActionBubbleController.swift` "Last Used Action Persistence" |
| Header titles (Code / Table / Docker / … Actions) | `ActionBubbleView.swift` title switch |
| Action labels in the table | `SmartTransform.swift` `builtInTransforms`, `addJSONActions`, `addSQLActions`, `addHTTPActions`, `addYAMLActions`, `addXMLActions`, `addSystemLogActions` |
| "Execute cURL — sends request"; AI actions marked | `addHTTPActions`; `isAI` |
| Related History / Previously fixed / Bug Fix Memory | `ActionBubbleView.swift` ~L910–940; `ErrorResolutionService` |
| Custom action kinds, `/bin/bash -c` with stdin, AI appends the clip, playground | `CustomSmartAction.swift`; `CustomActionsSettingsView.swift` |
| Custom action content types; "Text" = all non-binary | `CustomActionsSettingsView.availableTypes`; `SmartTransform.transforms(for:)` |
| Custom Actions heading in the bubble | `ActionBubbleView.swift` L293 |
| Modes: Code & developer items (default) / All content types / Selected types only; toggle | `SettingsClipboardPane.swift`; `SettingsStore` defaults |
| Default-mode types | `ContentType.isCodeRelated` (+ regex) |
| No bubble for sensitive, image, file or terminal command clips; no actions on sensitive clips | `SettingsStore.shouldShowActionBubble`; `SmartTransform.transforms(for:)` guard |
| Cloud AI marker when the AI mode is cloud and AI actions are offered | `ActionBubbleView.usesCloudAI` |
| Menu built from the first 4,000 chars; transform gets the full text | `builtInTransforms` comment and `prefix(4000)` |
| No bubble for L2Cache's own writes | `presentIfNeeded` suppression and source-app checks |
| Free: first built-in + first custom action; editing custom actions needs Pro | `ActionBubbleController` `isAllowed`; `CustomActionsSettingsView` gate |

### Found along the way (not changed)
- **Trial length mismatch.** Custom Actions settings say "Your 14-day trial has ended"; the homepage says "15-day Pro trial". One of them is wrong.
- **Mobile nav on legacy pages.** 18 English pages share the `nav-cta` / `nav-mobile-cta` pair; custom-actions showed both buttons on phones. The others likely do too. Candidate for C6's final pass.
- Ruby recipes on custom-actions assume Ruby is installed; left as is.
