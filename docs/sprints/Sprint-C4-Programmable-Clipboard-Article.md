# Sprint C4 — Programmable clipboard article

**Status:** Planned · **Date:** 2026-11-09
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
_To be filled in after the sprint._
