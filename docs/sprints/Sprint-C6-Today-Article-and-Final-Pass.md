# Sprint C6 — Today article & final pass

**Status:** ✅ Done (IndexNow pending deploy) · **Date:** 2026-11-09

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
- **T-C601** `developer-morning-context-today.html` (4 min): Pick up where you left off (session recap, context strip with cache state and Start fresh with handoff, Continue This Session, Recap ›, carried-over days), why cache state matters in the morning, the stats row (incl. Claude Code / Codex weekly usage), Needs attention (dismiss for a week, All clear), Other active projects, Copy standup and Weekly Brief (on by itself on Mondays), presentation mode, the setup checklist, all local. Wired into `build.py`, `validate_seo.py`, `sitemap.html`, `llms.txt`, footer Product ("Today page"), Today popup "Read more" (first). `day-in-the-life` links to it.
- **T-C602** `blog.html`: topic chips, then five sections with a heading and one-line intro: Context & cost (2), Coding agents (9), Today, projects & Worklog (4), Clipboard & search (12), Engineering & guides (4). All 30 existing cards plus Today were placed, with the same card markup. Subtitle updated. The chips are a `div role="navigation"` so they don't pick up the site's `nav` styles.
- **T-C603** Homepage "From the blog": cold-cache cost, session handoff, MCP & hooks, programmable clipboard, timesheet & standup, Claude Code lifesaver. Heading changed to "Guides for developers working with coding agents."
- **Read times:** recomputed from word counts (230 wpm) for all 8 new articles; most C2–C5 estimates were 1–2 min high. Now 8 / 5 / 6 / 4 / 6 / 5 / 4 / 4. The earlier sprint reviews keep their original estimates.
- **Mobile pass on legacy pages (the doubled Download button):** 17 English pages had no phone nav rules. The link row overflowed (blog was 641px wide) and the wrong Download button showed. One rule in `theme.css` hides `.nav-links` and `.nav-cta` and shows `.nav-mobile-cta` at ≤700px. `.footer-links` now wraps. Page fixes: `intelligence` (its text column was **0px wide** on phones; the row now stacks), `changelog` (list items were flex rows, splitting labels into columns and overflowing; now normal text; the timeline line now sits at the left on phones). All 18 nav pages plus both new-article pages measured at 390px with no page scroll.
- **T-C604:** `check_home_links.py` → 85 internal links resolve; `validate_seo.py` passed (49 pages); `seo_health_check.py` completed; all 8 popups have "Read more"; all 8 new articles linked from the homepage and `blog.html`. `Content-README.md` updated. **IndexNow not run.** It needs the deploy and your go-ahead: `python3 submit_indexnow.py` with the 8 new URLs and `/en/blog`.

### Facts table (T-C601)
| Claim | Source |
|---|---|
| Layout: header (Weekly Brief, Copy standup, presentation mode), checklist, stats, brief, Your Day + Needs attention, Other active projects | `TodayView.swift`, `TodaySections.swift` |
| "Pick up where you left off" / "Where you left off" / carried-over days | `YourDayCard.swift` |
| Row: context strip, recap (You asked · Last update · Commit), Recap ›, branch chip | `YourDayRow.swift` |
| Continue This Session copies the resume command | `YourDayRow` → `CopyResumeButton`; `AgentSessionLauncher.swift` |
| GitHub link only when pushed | `YourDayCard` "Open … on GitHub"; `WorkDayBuilder` comment |
| Context strip warm/cold lines and Start fresh with handoff | `ContextStrip.swift`; PRD-Context-Budget §4.1 |
| Stats: projects, commits, need attention, Claude Code / Codex weekly usage | `TodayStatsStrip`; live-limits view (Sprint 46) |
| Needs attention: dismiss for a week, show all, All clear | `TodaySections.swift` |
| Other projects: editor, Terminal, Copy resume, 7-day bars in project colours | `TodaySections.swift` |
| Weekly Brief on Mondays by default, toggle | `TodayView.isWeeklyBriefingVisible` (`isMondayEdition`) |
| Standup template / AI limited to facts | `StandupWriter.swift` |
| Setup checklist: projects folder, agent folders | `TodaySetupChecklist` in `TodayView` |
| Presentation mode masks | `PresentationMasker.swift` |
