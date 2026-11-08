# Sprint C6 — Today article & final pass

**Status:** Planned · **Date:** 2026-11-09

## Tasks

### T-C601 — `/en/developer-morning-context-today`
**Working title:** Your morning starts with context, not archaeology
**Covers:** the Today page: pick-up cards per project (what you asked, what the agent finished, the next step), cache state and resume on each card, Needs attention, the stats row, Weekly Brief and Copy standup.
**Sources:** `docs/PRD-Today-Developer-Home.md`, `docs/PRD-Work-Summaries-Your-Day.md`, `docs/PRD-Context-Budget.md` (pick-up card cache states).
**Wiring:** as C2; Today popup "Read more"; cross-link to `day-in-the-life-mac-developer`.

### T-C602 — Blog index refresh
`blog.html`: new articles at the top, grouped by topic (Coding agents, Context & cost, Clipboard, Projects & Worklog, Engineering).

### T-C603 — Featured picks
Swap the homepage "From the blog" band to: cold-cache cost (C2), session handoff (C2), MCP & hooks (C3), programmable clipboard (C4), timesheet & standup (C5), Claude Code lifesaver.

### T-C604 — Final checks and submit
- Full `check_home_links.py`, `validate_seo.py`, `seo_health_check.py`.
- Every popup has at least one "Read more" link; no new page is an orphan (each is linked from the homepage and `blog.html`).
- `submit_indexnow.py` for the new URLs (after deploy, with the user's go-ahead).
- Update [Content-README.md](Content-README.md) status and the gap table.

## Review
_To be filled in after the sprint._
