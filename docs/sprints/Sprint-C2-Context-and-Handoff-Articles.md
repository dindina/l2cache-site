# Sprint C2 — Context & handoff articles

**Status:** Planned · **Date:** 2026-11-09
**Fills the gap for:** the homepage's "Stop paying to reload old context" section and the Context & cost tile.

## Articles

### T-C201 — `/en/claude-code-cold-cache-resume-cost`
**Working title:** Why resuming a cold Claude Code session costs more (and what to do instead)
**Covers:** what the prompt cache is; 5-minute vs 1-hour TTL; why the first message after expiry rewrites the whole context as a cache write (≈2× input) instead of a cache read (≈0.1×), so ≈20× a warm turn; that it hits once; how to see it coming (context size, cache state); options: `/compact`, start fresh with a handoff, keep-warm heartbeat for Heavy sessions; how L2Cache's warnings and the cold resume guard work.
**Sources (app repo):** `docs/PRD-Context-Budget.md`, `docs/PRD-Cold-Resume-Guard.md`, `docs/Research-Session-Freshness.md`, `docs/Research-Exit-Cost.md`, Context-Budget manual tests. Pricing multipliers checked against Anthropic's current prompt-caching docs on the day.
**Do not claim:** quota-days (deferred), plan picker outside Settings, anything about Codex cache behaviour the code doesn't measure.

### T-C202 — `/en/coding-agent-session-handoff`
**Working title:** Start a fresh coding-agent session without losing context
**Covers:** why long sessions get expensive and slow; what a handoff carries (goal, active files, completed and pending items, where it left off); how `/clear` with L2Cache hooks injects it; which agents support live capture and handoff (Claude Code, Codex, GitHub Copilot, Grok Build); privacy (local, sensitive items excluded).
**Sources:** `docs/PRD-Agent-Continuity-Hooks-and-MCP.md`, `docs/PRD-Cold-Resume-Guard.md`, `docs/PRD-Agent-Plugins.md`.

## Wiring (both articles)
`build.py` `HTML_FILES`, `sitemap.xml`, `llms.txt`, `blog.html` (top of list), homepage footer (Guides & blog), Context & cost popup "Read more", token spotlight fine print link ("How the cold resume guard works"), cross-links to each other and to `claude-code-session-history-mac`.

## Verify
Facts table in the review (claim → source). `build.py`, `check_home_links.py`, `validate_seo.py`; pages checked at 1440px and 390px.

## Review
_To be filled in after the sprint._
