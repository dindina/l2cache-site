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
