# Sprint C3 — MCP, hooks & search articles

**Status:** Planned · **Date:** 2026-11-09
**Fills the gap for:** the MCP & Hooks tile and the Search (⌘K) tile.

## Articles

### T-C301 — `/en/coding-agent-memory-mcp-hooks`
**Working title:** Give your coding agents memory: L2Cache's MCP server and hooks
**Covers:** the two directions (agents ask L2Cache via MCP; hooks brief every session); the MCP tools and what each returns (recent clips, clip by id, agent history search, session summary, decisions, error resolutions, recovery points, screenshots, memory folders); what hooks add per turn (recent clipboard, handoff, edits and failed commands, fixes remembered, work summaries, cold resume guard); supported agents (Claude Code, Claude desktop, Codex, Cursor, Antigravity for MCP; Claude Code, Codex, Copilot, Grok Build for hooks); setup is opt-in per agent in Settings; sensitive items never returned; runs locally (bundled JXA script, no binary).
**Sources:** `docs/MCP-Tools-Reference.md`, `docs/PRD-Agent-Continuity-Hooks-and-MCP.md`, `docs/PRD-Agent-Plugins.md`, `docs/PRD-Error-to-Resolution-Memory.md`, `docs/PRD-Work-Summaries-Your-Day.md`.

### T-C302 — `/en/universal-search-mac-developer`
**Working title:** One ⌘K search for everything you did as a developer
**Covers:** what's indexed (clips, agent sessions, terminal commands, commits, screenshots by OCR text, docs); best match first then grouped by kind; filters and `@project`; opening an agent result at the matching message; the ⌥Space quick panel; all local (SQLite FTS5).
**Sources:** `docs/PRD-Universal-Search-Redesign.md` (rev 2) and the shipped search code. Only describe what Sprints 36–37 actually shipped; check the AI headline status before mentioning it.

## Wiring
Same as C2: `build.py`, `sitemap.xml`, `llms.txt`, `blog.html`, footer, MCP & Hooks popup and Search popup "Read more"; cross-link C3-1 ↔ C2 handoff article, C3-2 ↔ `screenshot-ocr-mac`.

## Verify
Facts table in the review; `build.py`, `check_home_links.py`, `validate_seo.py`; 1440px and 390px checks.

## Review
_To be filled in after the sprint._
