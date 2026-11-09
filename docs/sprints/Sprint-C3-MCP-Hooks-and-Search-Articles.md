# Sprint C3 — MCP, hooks & search articles

**Status:** ✅ Done · **Date:** 2026-11-09
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
- **T-C301** `coding-agent-memory-mcp-hooks.html` (~8 min): the two directions; the 12 read-only MCP tools in two tables; result size and prompt-cache stability; MCP clients from Settings › MCP; what hooks record (edits, commands, work summaries, verified fix records) and add (handoff, recent clips, facts compaction dropped, cost warnings); per-agent hook table; why both; privacy.
- **T-C302** `universal-search-mac-developer.html` (~6 min): what's indexed, Top Hit and grouping, ranking, ⌘P preview, scope pills and Tab, scope tokens and `@project`, ↵ / ⌘↵ per kind, agent results open at the matching message, empty state, all local.
- **Wiring:** `build.py`, `validate_seo.py`, `blog.html` (after the featured card, above C2), `sitemap.html`, `llms.txt`; homepage footer Guides & blog (+2), MCP & Hooks "Read more" (MCP article + handoff; the resume-guide link moved out), Search "Read more" (search article + screenshot search). Cross-links: handoff ↔ MCP article, search ↔ `screenshot-ocr-mac` (one new paragraph on that page), MCP ↔ search.
- **Changes from plan:** the hooks table splits support per feature, because it differs by agent (see facts). The quick panel shortcut isn't mentioned (see below). Mobile table padding tightened in all four C2/C3 articles so the widest table fits at 390px.
- **Verify:** `build.py` OK; `site_i18n.py extract` → 584 strings; `check_home_links.py` → 77 internal links resolve; `validate_seo.py` passed (45 pages) after rewording "full transcripts", a blocked claim. Both articles at 390px (every table fits, no page scroll) and 1440px.

### Facts table
| Claim | Source |
|---|---|
| 12 tools, read-only, names and returns | `docs/MCP-Tools-Reference.md`; `l2cache-mcp.js` `TOOLS` (12 `schema(...)` entries) |
| Agent tools default 5 results, max 10; excerpts; fixed tool list for prompt cache | `l2cache-mcp.js` constants; MCP reference §Design |
| Server instructions say call `get_session_summary` first | `l2cache-mcp.js` `INSTRUCTIONS` |
| MCP clients: Claude Desktop, Claude Code, Antigravity & Cursor, Codex; "just ask your agent" | `MCPSettingsPane.swift` snippet rows |
| Snapshot in `~/.l2cache`, no network ports; osascript JXA, no binary | `MCPSettingsPane.swift`; `l2cache-mcp.js` header |
| Sensitive clips and excluded apps filtered at the snapshot; `is_sensitive = 0` in every clip query | MCP reference §3; `l2cache-mcp.js` |
| Turning off agent history drops it from the snapshot | `MCPSettingsPane.swift` toggle footer |
| Live capture: all four; handoff: not Copilot; clipboard: Claude, Codex, Grok | `HookInstaller.hookEntries`; `injectHandoffIfAvailable`; `clipboardProviderDirectories` |
| Work summaries: Claude + Codex; cold guard: Claude + Codex; compaction facts: Claude + Codex | `workSummaryProviders`, `coldGuardProviders`, `compactReinjectionProviders` |
| Clipboard injection: ≤5 clips, last 30 min, unseen, not pasted | `ClipContextWriter.swift` header, `maxItems` |
| Compaction re-adds ≤5 missing facts (files since commit, failing command, next step) | `CompactFactsFile.swift` |
| Fix records only when verified by a test or build; action bubble shows earlier fix | `ClipContextWriter.resolutionInstruction`; PRD-Error-to-Resolution-Memory |
| Work summary checked against recorded file changes; feeds Your Day | PRD-Work-Summaries-Your-Day goals 2–3 |
| Search kinds: project, doc, clip, folder, agent, terminal, commit; pill names | `GlobalSearch.swift` `Kind`; `GlobalSearchModel.pillTitle` |
| Clip FTS covers AI title, summary, tags, OCR text, link title; porter stemming | `ClipStore.swift` `clips_fts` |
| Agents, Terminal, Files need Developer Pro | `GlobalSearchEmptyState.swift` |
| Top Hit when ≥2 kinds; 70/30 relevance/recency; title and project boosts | `GlobalSearchRanking.swift` |
| Tokens and the trailing-space rule | `GlobalSearchQuery.swift` |
| ↵ / ⌘↵ labels, ⌘C, ⇥, esc, ⌘P | `GlobalSearchFooter.swift` |
| Agent result scrolls to the matching message | `AgentConversationView.scrollToTargetEventIfNeeded`; commit 111438d2 |
| Recent searches, recently opened, syntax | `GlobalSearchEmptyState.swift` |
| ⌘K in Developer Home | `HomeRootView.swift` `.keyboardShortcut("k", .command)` |
| AI headline not mentioned | memory: needs a new sprint; not in 111438d2 |

### Found along the way (not changed)
- **Quick panel shortcut.** The app's default is **⌘⇧V** (`PanelController.swift`, unchanged since Sprint 5), and a code comment says Option-only shortcuts don't work in sandboxed apps on macOS 15+. But the homepage (hero list, FAQ, `home.json`), `ai-agent-jsonl-and-session-resume-guide.html`, the old `index.html`, onboarding (`OnboardingSetupSteps.swift`) and the welcome clip (`ClipStore.swift`) all say ⌥Space. Needs a decision on which is right before fixing either side.
- Sprint docs 36 and 37 still say "Planned", but the work shipped in `111438d2`.
