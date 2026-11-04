# Session Insights Dashboard

## Milestone 1: Analytics Data Foundation

### Scope

- [x] Preserve canonical event timestamps, model metadata, and token usage while parsing supported session formats.
- [x] Normalize tool call identity, result status, exit code, duration, file paths, and file operation type when the source log provides them.
- [x] Add a backward-compatible `metrics` and `coverage` object to each session.
- [x] Replace fabricated fallback dollar costs with measured cost or an explicit “usage unavailable” state.
- [x] Bump the parser cache schema so stale IndexedDB records are rebuilt safely.
- [x] Keep the current project tree, grid, transcript, search, filters, and provider support working.

### Acceptance

- [x] Existing sample sessions still load and render.
- [x] A transcript containing usage/model/timestamps exposes those values in the normalized session record.
- [x] A transcript without analytics metadata remains usable and reports missing coverage without invented token or cost values.
- [x] File arguments from supported tool calls produce deduplicated normalized file operations.
- [x] Failed tool results retain an error/status signal that later insights can consume.
- [x] Focused parser checks cover both metadata-rich and metadata-poor transcripts.

### Explicit non-goals for this milestone

- No insights dashboard UI yet.
- No hotspot scoring, prompt coaching, or workflow recommendations yet.
- No external pricing service or dependency.
- No attempt to infer token counts when the source does not provide them.

## Review

- Added canonical per-event analytics enrichment and session-level `model`, `metrics`, `coverage`, and `filesTouched` records.
- Preserved explicit source costs only; project summaries now disclose measured coverage or show `usage unavailable`.
- Kept stale cached indexes available while requiring refresh or re-import for the new analytics schema.
- Added dependency-free verification for Claude usage, Anthropic cache tokens, Codex cumulative usage, tool/result correlation, failed patches, cumulative cost, and sparse logs.
- Verified with `rtk proxy node tools/verify-session-normalization.js`, `rtk npm run build`, `rtk git diff --check`, and a browser smoke test of the sample project tree.

## Milestone 2: Action Inbox

### Scope

- [x] Add an Insights view alongside Project Tree, Grid Tiles, and Full History.
- [x] Rank repeated failures, missing verification, frequently revisited files, repeated edits, and analytics coverage gaps.
- [x] Show evidence, impact, confidence, and one concrete action for every recommendation.
- [x] Respect the existing project, branch, agent, and search scope.
- [x] Support opening relevant sessions, copying a follow-up prompt, and dismissing a recommendation.

### Acceptance

- [x] Sample data renders the Action Inbox without breaking existing views.
- [x] Recommendations are derived only from observable session data.
- [x] Empty and filtered states explain why no recommendations are shown.
- [x] Existing parser verification and site build continue to pass.

### Review

- Added a scoped Action Inbox with summary coverage, ranked evidence cards, confidence labels, and plain-language impact.
- Added evidence navigation, follow-up prompt copying, and session-local dismissal.
- Added focused checks for repeated failures, missing verification, and incomplete analytics coverage.
- Verified the parser/insight harness, full site build, diff whitespace, built dashboard rendering, and evidence navigation.

# L2Cache for Teams — waitlist page (spec: docs/PRD-Teams-Waitlist.md)

- [x] Feature mockups (12 cards, example data) — `prototypes/teams-mockups/` · verified 1280px + 375px, no page overflow
- [x] Approve mockups
- [x] `teams/index.html` + `teams/styles.css` + `teams/script.js` — sections, form, light page + dark windows, mobile
- [x] `api/waitlist.js` — validate, honeypot, insert via Supabase REST (service role, env vars)
- [x] `supabase/teams_waitlist.sql` — table + RLS on, no policies
- [x] `vercel.json` — `/api/*` and `/teams` rewrites ahead of the catch-all
- [x] `build.py` — copy `teams/` to `out/l2cache/teams/`, sitemap entry
- [x] `privacy.html` — waitlist data section
- [x] Verify: build, validate_seo, check_routes, function checks, light/dark/375px
- [ ] You: run SQL in IronTrack Supabase, add Vercel env vars
- [ ] Preview deploy → real signup lands → approve production

## Review — Teams waitlist page (2026-11-03)
- Page: `teams/` → `/teams` (absolute asset paths; `teams` added to the single-segment `/en/:page` redirect exclusions, or `/teams` would 308 to a 404).
- API: `api/waitlist.js`; `/api/(.*)` rewrite placed before the host and catch-all rewrites. 9 offline tests in `scripts/test_waitlist_api.js`.
- Verified: build, `validate_seo.py` (teams page + sitemap), `check_routes.js` 384/0, end-to-end form → real handler → stubbed Supabase row, 1280px and 375px with no page overflow.
- Not verified yet: live Supabase insert and Vercel function routing (need SQL + env vars + preview deploy).

### Update — moved to teams.amvo.store (2026-11-03)
- Working name "Session Intelligence for Teams"; `teams/` → `out/teams/`, host rewrite `teams.amvo.store → /teams/$1`; own privacy page, robots, sitemap, og.png (1200×630).
- Reverted from l2cache.app: `/teams` route, sitemap entry, `teams` redirect exclusion, privacy.html waitlist section.
- `teams.amvo.store` added to the `missing` host list of 14 l2cache.app redirects (else `/privacy` → `/en/privacy`).
- Analytics tag injected into out/teams (privacy page states Vercel Web Analytics).
- Verified: validate_seo (incl. out/teams canonical), check_routes 383/0, API tests 9/9, form → handler → stub insert, /privacy 200, 1280px + 375px no overflow.
- Needs you: add `teams.amvo.store` domain to the Vercel project, run SQL, add env vars, preview deploy.

### Live — 2026-11-03
- teams.amvo.store live via ./deploy.sh; page, /privacy, og.png, assets 200; l2cache.app, hingejoy, amvo.store unaffected.
- Production signup test: POST /api/waitlist → 200 {"ok":true} (row waitlist-test@amvo.store, delete in Supabase).
- Open: rotate Supabase secret key (exposed via clipboard hook) + redeploy; commit and merge teams work to main (prod auto-deploys from main, a main push would drop it); L2Cache sensitive detection misses `sb_secret_` keys.

## Teams page — ChatGPT review applied (2026-11-03)
- [x] Proactive session intelligence section (`#proactive`): detect → suggest table; 3 unbuilt detections tagged Planned; nav link "Detection"
- [x] "How we got ≈20×" disclosure under the problem cards (2× ÷ 0.1×, 12.5× for 5m, context only, measured 0.9% tokens / ≈10% cost)
- [x] Form: only email, team size, consent required; the rest folded into "Tell us more"; `proactive-alerts` added to `wanted` (API + 13 tests pass)
- [x] Privacy: "Stays on each machine" / "What the team receives" columns
- [x] Verified 1280px + 390px, no overflow; minimal POST → 200 locally; validate_seo passes
- [x] Moved Pickup Cards mockup from hero into "What you'll get" (`#features`) with explicit developer copy; hero simplified to headline, CTAs, and agent strip
- [x] Added "Team skills: share custom agent tools across the repo" mockup card (Planned) and `team-skills` option to waitlist form & API
- [ ] User runs ./deploy.sh

# 2.0 homepage — add features from app Sprints 36–48 (planned 2026-11-04)

Source: `prototypes/native-mac/index.html` → built to `out/l2cache/` (English only; translations stay last, W3).
Page copy last updated 2026-10-26 (`fd066ca`); app Sprints 36–48 shipped after that.

## What's new since the page was written
| App work | Status | Where it lands on the page |
|---|---|---|
| S36–37 Universal ⌘K search: Top Hit, scope pills, `@project` tokens, recents, agent hits open at the matched message | Shipped (`111438d`) | Search section bullets |
| S38–40, 45–46 Context budget: pickup card shows session size and whether the cache is warm or cold, one-click "start fresh" / compact, cache-expiry alert, "Where your tokens go", 5-hour/weekly limit pacing, Context Audit in onboarding | 38, 40, 45 complete; 39 signed off; 46 live checks open | **New section** "Know what a session costs before you resume" between Agents and MCP & Hooks |
| S41 terminal nudge when a session gets heavy (zero model tokens) | Live terminal check pending | Hooks list |
| S47 safer compaction: re-inject facts `/compact` dropped | Live `/compact` checks pending | Hooks list |
| S48 cold resume guard: warns and stops the first costly prompt once on a cold session; `/clear` starts fresh with the handoff | Complete | Hooks list + new section |
| S42–44 agent history over MCP: past fixes, decisions, work summaries, single events; lean pointer handoff | 42 complete; 43–44 live check pending | MCP tool list (6 → 11 tools) + FAQ |

## Plan
- [x] T1 Search section: replace bullets with Top Hit + scope pills, `@project` scoping, open at the matched message
- [x] T2 New "context & cost" section (copy + 3–4 bullets, one screenshot of the pickup card's context strip); add nav link
- [x] T2b Proactive session warnings, their own block in the new section (shipped and checked):
  - Cache expiring soon: macOS notification, menu-bar badge and quick-panel top row before a heavy Claude session's cache expires (S45, `CacheExpiryMonitor`)
  - Keep warm: optional, capped prompt to keep a heavy session's cache warm (S45)
  - Cold resume guard: terminal warning, and the first costly prompt is stopped once on a cold session; `/clear` starts fresh with the handoff (S48)
  - Not yet: 5-hour/weekly limit pace alerts (S46) and the heavy-session terminal nudge (S41) wait for live checks; Session Health signals (`PRD-Proactive-Notifications.md`) are Proposed, not built, so the page must not claim them
- [x] T3 Hooks list: add cold resume guard only (S41 nudge and S47 compaction wait for live checks)
- [x] T4 MCP list: add `search_agent_history`, `get_session_summary`, `get_error_resolutions`, `get_decisions`, `get_agent_event`
- [x] T5 Verify the "MCP needs macOS 15 or later" claim still holds after the osascript server (`09aff8c`); fix page + FAQ if not
- [x] T6 FAQ: add "Does L2Cache help with Claude Code token use / cold resumes?"; update the MCP answer
- [x] T7 Mockups: replaced static screenshots across the entire page (Hero, Today, Agents, Context, Projects, Search, Clipboard) with responsive HTML app mockups; unified example story across all sections to Atlas (Auth token retry / ATL-142); removed dead screenshot modal and deleted 8 unused screenshot files
- [x] T8 JSON-LD `featureList` + meta description: add context/cost line
- [x] T9 Copy rules: no "20× cheaper"/"saves N×" claims; cost wording matches the app's honest copy (`6362a94`, `f830227`); blocked-claims gate passes
- [x] T10 Rebuild (`python3 build.py`), `scripts/check_routes.js`, `site_i18n.py check`, review at localhost:8780, then hand over for approval (no deploy)

## Decisions needed
- D1 ✅ (2026-11-04) Only checked work goes on the page now. S41, 43, 44, 46, 47 are added once their live checks pass. The new section leaves out 5-hour/weekly pacing (S46) and the lean pointer handoff (S44).
- D2 Pro price: is $4.99 the 2.0 unlock? (carried over)
- D3 Privacy policy: approve the live version (carried over)

## Review — 2.0 page features & HTML mockups (2026-11-04)
- New "Context & cost" section (#context, in the nav): pickup card facts on one side, warnings (cache expiring soon, keep warm, cold resume guard) on the other. All copy checked against Settings text and defaults in the app.
- ⌘K: top hit, kind filter, `@project`, opens at the matched message. MCP: 11 tools, plus earlier fixes, decisions and summaries. Hooks: cold resume guard. FAQ + JSON-LD: new token-use question, featureList line.
- T5: dropped "macOS 15 or later" for MCP. It came from the old helper binary target (removed in `09aff8c`); the osascript server has no OS gate in the app.
- HTML mockups: All sections (Hero Developer Home, Today, Coding Agents, Context & Cost, Projects & Worklog, ⌘K Search, Clipboard & Terminal) now use responsive HTML/CSS mockups rather than static screenshots, rendering sharp typography on all devices.
- Unified Atlas developer story: Across Hero, Today, Coding Agents, Context & Cost, Projects, Search, and Terminal/Clipboard, all data now consistently tracks the Atlas project (`fix/ATL-142-auth-retry`, "Auth token retry", commit `7b2a7f4`, `AuthRetryTests`, `TokenManager.swift`, with companion projects Nimbus, Relay, Lumen).
- Cleaned dead gallery code & assets: Removed the `<dialog id="screenshot-modal">` element, removed ~190 lines of carousel JavaScript and ~290 lines of modal/zoom-hint CSS; deleted 8 obsolete screenshot images saving ~750 KB.
- Checks: JSON-LD parses, `site_i18n extract` (390 strings), build OK, `check_routes.js` 383/0 failures, `validate_seo.py` passed (blocked claims included), no horizontal scroll at 390px.
