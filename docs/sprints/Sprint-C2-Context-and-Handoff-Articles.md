# Sprint C2 — Context & handoff articles

**Status:** ✅ Done · **Date:** 2026-11-09
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
- **T-C201** `claude-code-cold-cache-resume-cost.html` (~7 min): cache basics, 5 min vs 1 h TTL by billing, cold ÷ warm table, worked example (241k Opus 5.5: $0.05 warm vs $1.93 cold), resume is free until the first prompt, `/usage` cache line, four options (compact while warm + idle compaction, `/clear` + handoff, keep warm, just send), L2Cache's three warnings and guard details.
- **T-C202** `coding-agent-session-handoff.html` (~6 min): why long sessions cost more, the handoff format (example data), three delivery paths, agent support table, privacy, when to start fresh.
- **Wiring:** `build.py` HTML_FILES, `validate_seo.py` PUBLIC_PAGES, `blog.html` (right after the featured card), `sitemap.html`, `llms.txt`; homepage footer Guides & blog (+2), Context & cost "Read more" (both articles; replaced the resume-guide link), token spotlight fine print link, cross-links between the two articles and to `claude-code-session-history-mac`. The built `sitemap.xml` comes from HTML_FILES; the root `sitemap.xml` isn't used by the build, so it was left alone.
- **Change from plan:** MCP & Hooks "Read more" also links the handoff article (the hooks deliver it). The ≈20× in the plan became "12× to 40×" after checking prices.
- **Verify:** `build.py` OK, `site_i18n.py extract` → 581 strings, `check_home_links.py` → 74 internal links resolve, `validate_seo.py` passed (43 pages). Both articles at 390px and 1440px with no horizontal scroll; Context & cost popup and fine-print link checked at 1440px.

### Facts table
| Claim | Source |
|---|---|
| Write 1.25× (5 min) / 2× (1 h); read 0.1×, 0.05× on Opus 5.5 and Sonnet 5.5; Opus 5.5 $4 / $8 / $0.20 | platform.claude.com prompt-caching docs, fetched 2026-11-09 |
| 1 h TTL on subscription within plan; 5 min on API key, credits, cloud; subagents and compaction 5 min; `promptCacheTtl` 2.1.242+ | code.claude.com/docs/en/prompt-caching, 2026-11-09 |
| `/compact` cheap warm, costly cold; `/clear` costs nothing; idle compaction (1 h TTL, ≥200k, ~1 h idle, Mac awake) | code.claude.com costs + prompt-caching pages; PRD-Context-Budget §1.6 |
| `/usage` Prompt cache line, 2.1.251+ | code.claude.com/docs/en/costs |
| Resume makes no model request until the first prompt | PRD-Cold-Resume-Guard spike S-1 |
| Cold rewrites 60–66% of cost above 600k; median 5 / mean 10 requests per prompt; break-even ~1–2 prompts | Research-Exit-Cost §3–4 |
| Re-investigation and corrections ~2× after a task change | Research-Session-Freshness |
| Very heavy >400k, Heavy 150–400k; heartbeat ≤2 per idle, not 20:00–07:00, never sent by L2Cache | PRD-Context-Budget tiers, §6.1 |
| Guard: warning copy, one stop, ↑ Return, `/clear` within 30 min same folder, `-p` never blocked, 50k default, 30-min long-idle | PRD-Cold-Resume-Guard; HookInstaller.swift |
| Settings labels: Warn when resuming a cold session / Stop the first message / Minimum size 25k–100k | SettingsCodingAgentsPane.swift |
| Codex runs the guard, `/new`, assumes 5-min TTL | AgentContinuityService `coldGuardProviders`; HookInstaller cold_check |
| Capture: Claude, Codex, Copilot, Grok; auto handoff all but Copilot; MCP Claude + Codex | HookInstaller `hookEntries`; `injectHandoffIfAvailable`; `AgentMCPConnection.supports` |
| Handoff injection on by default when hooks connect; needs the app running | AgentContinuityService `connectHooksByDefault`; PRD-Cold-Resume-Guard Part 4 |
| Handoff ≤1.5k tokens, fields, MCP pointer vs Decisions / Rejected | PRD-Context-Budget §5.2 |
| Handoff files 0600, pruned after 7 days | PRD-Cold-Resume-Guard CR-5 |

### Found along the way (app, not changed)
The hook's resume warning hard-codes "≈ 20× a warm turn". On Opus 5.5 and Sonnet 5.5 with a 1-hour cache it's ≈40× (Research-Exit-Cost open question 5). The article says the figure is rounded.
