# PRD — Session Intelligence for Teams waitlist page (working name)

**Status:** Draft for approval · 2026-11-03
**URL:** `https://teams.amvo.store` (served from `teams/` by host rewrite in the l2cache-site Vercel project)
**Name:** "Session Intelligence for Teams" is a placeholder, presented as "from the makers of L2Cache" so it isn't confused with the Mac app. No status badges on features (removed 2026-11-03 at the user's request); mockups of features already in the Mac app stay L2Cache screens with the caption "Shown in L2Cache for Mac, where this runs today"; unbuilt lead features keep a "Planned" tag; team-only mockups use the working name.
**Goal:** A page to send to small teams (5–50 devs using coding agents) that explains L2Cache for Teams and collects waitlist signups with enough detail to prioritise the first build.

## Product being pitched

L2Cache for Teams is a **separate product** from the Mac app. **Session intelligence only** — no clipboard, panel, screenshots or snippets.

Features (pitched as "what you'll get", product is pre-launch). Each gets a mockup card.
"Basis" = what already exists in the Mac app that the feature is built from.

### Where things run

- **Local web app** (`http://localhost:4317`, served by the collector, any OS): pickup cards and full session history. Conversations never leave the machine.
- **Terminal** (agent hooks): guard, handoff, context budget, team memory lookups.
- **Cloud team view** (`l2cache.app/team`): metadata, cache waste, commits, recaps the developer approved, weekly digest.

### For each developer — local web app (the headline features)

| # | Feature | What it does | Mockup | Basis |
|---|---|---|---|---|
| A | **Pickup cards** | Same card as the Mac app's Home. Per recent session: title, agent · project, situation headline ("Cheap to continue for 49 min." / "A fresh session could save you from carrying unnecessary context."), current-session tokens with cache state, fresh + handoff estimate when cold, Copy `/compact` / Start fresh with handoff, session recap (last user request, last agent action, commit + push state), branch chip, Copy resume command. | Two cards: warm and cold (match `pickup-card-session-recap-handoff` screenshot) | Developer Home pickup card (Sprints 41–48) |
| B | **Session history** | Every Claude Code and Codex session, grouped by project and day, with the full conversation, tool calls, files changed and linked commits; search across all of it. | Browser: project sidebar, session list, conversation pane | Home agent session browser + detail |

### For each developer — in the terminal

| # | Feature | What it does | Mockup | Basis |
|---|---|---|---|---|
| 1 | **Cold Resume Guard** | On resume, warns that the cache expired and the next message reloads N tokens (≈20× a warm turn); stops the first message once; `/clear` is the cheap path. | Terminal: `claude --resume` → L2Cache warning → blocked first prompt | PRD-Cold-Resume-Guard (Sprint 48) |
| 2 | **Fresh start with handoff** | `/clear` starts an empty session and injects a handoff: done, pending, last exchange, possibly-done next step. | Terminal: `/clear` → injected handoff block | Agent Continuity hooks, handoff work |
| 3 | **Context budget** | Live context size and cache time left; warns when a session gets heavy; suggests compact vs fresh. | Status line + "heavy session" warning | PRD-Context-Budget |
| 4 | **Team memory** | The agent asks L2Cache before debugging: "this error was fixed before — here's the fix, files, and the test that proved it." Shared across the team. | Agent transcript: MCP lookup → prior fix by a teammate | **New for Teams** — not in the Mac app (its PRD is only Proposed). Collector hook asks the agent for a structured fix summary; developer approves; collector strips secrets and uploads; collector MCP searches local then team fixes. Est. 2–3 sprints after collector + backend. Risks: wrong matches, fix text is content not metadata, needs volume. |

### For the team — web dashboard and digest (new)

| # | Feature | What it does | Mockup | Basis |
|---|---|---|---|---|
| C | **Usage & cold-restart report** (for the manager/CTO) | One page, filterable by week, developer, repo and agent. **Tiles:** sessions, total tokens, est. cost (API) or quota used (Max/Pro), cold restarts, tokens reloaded by cold restarts, restarts the guard turned into fresh + handoff. **Chart:** tokens per day, stacked by type (cache read, cache write, input, output), cold-reload share highlighted. **Per-developer table:** sessions, tokens, cold restarts, wasted reload tokens, avg peak context, rate-limit hits, guard follow-rate. **Top wasteful sessions:** project, session, turns, peak context, times resumed cold, wasted cold-rewrite tokens, rate-limit hit. Export CSV. | Dashboard page: KPI tiles, stacked bar chart, developer table, top-5 wasteful table | Context Budget + the "Top 5 most wasteful sessions" audit (Claude `usage` objects deduped by `message.id`) |
| 5 | **Weekly team digest** | Slack/email every Monday: the report's headline numbers (tokens, cold restarts, waste avoided) plus what shipped and who got stuck. | Slack message card | New; summarises C + 7 |
| 6 | **Spend tied to outcomes** | Tokens and cost per developer, repo and session, each linked to the commits it produced; cold-reload waste shown separately. | Dashboard table + small bar chart | Work summaries, git events (local today) |
| 7 | **What shipped** | Team version of "Your Day": work grouped by feature per developer, verified against file changes, uncommitted work flagged. | Dashboard feed card | PRD-Work-Summaries-Your-Day |

### Trust

| # | Feature | What it does | Mockup | Basis |
|---|---|---|---|---|
| 8 | **You see what your team sees** | Each developer has a panel listing exactly what was uploaded (metadata + approved summaries) and what never leaves the machine. Pause sharing anytime. | Two-column "Shared / Stays on your machine" panel | New |

Cross-agent support (Claude Code, Codex first) is shown as an agent-badge strip, not a card.
Page order: A and B lead (hero shows the pickup card), then 1–4, then C (manager report) and 5–7, then 8.
Report visibility default: per-developer rows visible to admins; a team setting switches the report to team totals only (for works-council / GDPR orgs). Report data is metadata only — no prompts, no conversation text.
Mockups use fictional names and example numbers, labelled "Example".

Positioning line: **developer-first, private by design**.
- Transcripts are read and summarised **on each developer's machine**; raw conversations never leave it.
- Only metadata (tokens, cost, cache events, commit SHAs) and developer-visible summaries reach the team view.
- Developers see exactly what their team sees. No keystroke tracking, no productivity scores.

## Claims rules (must pass `validate_seo.py` blocked-claims gate)

- Everything is framed as upcoming ("What you'll get", "Join the waitlist"); no "available now", no pricing, no customer counts.
- Platforms: "macOS first, Windows and Linux planned" — no claim of Windows support.
- Agents: "Claude Code and Codex first" — no Cursor/Copilot support claims.
- No "zero network requests" / "100% offline" phrasing (the team view is a cloud service by design).

## Page sections

1. Hero — headline, one-line value, CTA to form.
2. The problem — agent spend is invisible, cold reloads waste quota, work gets redone. A "How we got ≈20×" disclosure gives the basis: 1h cache write 2× vs cache read 0.1× of base input price (12.5× for a 5m cache), reloaded context only, plus the measured 0.9% of tokens / ≈10% of cost.
3. Features — the six above, as cards.
3b. Proactive session intelligence (`#proactive`) — a "when it detects → it suggests" table. Rows backed by existing features (cold resume, heavy context, unfinished work at /clear or compact, a fix the team already made) carry no tag; goal drift, repeated file investigation and growth without edits or commits carry the "Planned" tag.
4. Private by design — "Stays on each machine" vs "What the team receives" (two-column), then the sharing mockup.
5. How it works — 3 steps: install one collector → pickup cards and history open in your browser, hooks guard the terminal → your team gets spend, commits and approved recaps.
6. Waitlist form.
7. FAQ — "Do you read our transcripts?", "Windows?", "Which agents?", "Price?" ("set before launch").
8. Footer — links to l2cache.app and the privacy policy.

Style: reuse the 2.0 homepage tokens (`prototypes/native-mac/styles.css` colours, type), light + dark mode, mobile-first. Self-contained `teams/` folder so it can move to its own domain later.

## Waitlist form

| Field | Type | Required |
|---|---|---|
| Work email | email | yes |
| Team size | select: 1, 2–5, 6–15, 16–50, 50+ | yes |
| Name | text | no |
| Company | text | no |
| Developer OS | multi: macOS, Windows, Windows + WSL, Linux | no |
| Agents used | multi: Claude Code, Codex, Cursor, Copilot, Gemini CLI, Other | no |
| Would pay for | multi: team updates (what everyone worked on), proactive session alerts, usage report, seat and plan advisor, quota forecast, secret-leak alerts, agent safety inventory, PR recaps, per-client reports, team memory (`wanted`) | no |
| Biggest pain | textarea, 500 chars | no |
| Consent | checkbox: "Email me about early access" | yes |

Only email, team size and consent are required; every optional field sits in a collapsed "Tell us more about your team" block so signing up takes seconds. Ask the rest on the call.

Hidden: honeypot field, `source` (utm/referrer), submitted page path.
Success: inline "You're on the list" message; no redirect. Duplicate email: same success message (no enumeration).

## Architecture

```
browser form ──POST JSON──▶ /api/waitlist (Vercel Node function)
                               │ validate, honeypot, length caps
                               ▼
                 Supabase (IronTrack project) REST: teams_waitlist
```

- Function uses `SUPABASE_URL` + `SUPABASE_SECRET_KEY` from Vercel env vars; the key is never sent to the browser.
- No new npm dependency — plain `fetch` to PostgREST with `Prefer: resolution=ignore-duplicates`.
- `vercel.json`: add `/api/(.*)` rewrite before the catch-all `/(.*) → /l2cache/$1`, and `/teams` → `/l2cache/teams/index.html`.
- `build.py`: copy `teams/` into `out/l2cache/teams/`, add to sitemap.

## Database (IronTrack Supabase project, separate table)

```sql
create table public.teams_waitlist (
  id           uuid primary key default gen_random_uuid(),
  email        text not null unique check (char_length(email) <= 254),
  name         text check (char_length(name) <= 120),
  company      text check (char_length(company) <= 120),
  team_size    text not null,
  os           text[] not null default '{}',
  agents       text[] not null default '{}',
  pain         text check (char_length(pain) <= 500),
  consent      boolean not null,
  source       text,
  user_agent   text,
  created_at   timestamptz not null default now()
);
alter table public.teams_waitlist enable row level security;
-- No policies: anon/authenticated clients cannot read or write; only the service role (server-side) can.
```

Shipped as `supabase/teams_waitlist.sql` in the site repo; you run it once in the Supabase SQL editor.

## Privacy

- Add a "L2Cache for Teams waitlist" section to `privacy.html`: what's collected, why, stored in Supabase, delete on request via support email.
- Vercel Analytics already injected by `build.py` — no extra trackers.

## Out of scope

Confirmation emails, admin UI, captcha, localisation, the team product itself.

## Needs you (can't be done from here)

1. Run `supabase/teams_waitlist.sql` in the IronTrack project's SQL editor.
2. Add `SUPABASE_URL` and `SUPABASE_SECRET_KEY` to the Vercel project (Production + Preview).
3. Approve the preview deploy before production.

## Verification

- Local: `python3 build.py`, `python3 validate_seo.py`, open `out/l2cache/teams/index.html`; light/dark, 375px width.
- Function: unit-style check with a stub fetch (valid, missing fields, honeypot, oversize, duplicate).
- Preview deploy: real submission lands in Supabase; duplicate returns success; `/api/waitlist` not swallowed by the catch-all rewrite; existing routes (`/`, `/en/...`, hingejoy, amvo.store) unchanged via `scripts/check_routes.js`.
