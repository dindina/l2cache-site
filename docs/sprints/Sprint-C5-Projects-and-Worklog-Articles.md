# Sprint C5 — Projects & Worklog articles

**Status:** Planned · **Date:** 2026-11-09
**Fills the gap for:** the Projects tile and the Worklog features (in the Projects popup and the demo sidebar).

## Articles

### T-C501 — `/en/project-story-git-timeline-mac`
**Working title:** See how your project got here: commits, sessions and tests on one timeline
**Covers:** Project Story (commit graph and timeline read from `.git`; L2Cache never runs Git); milestones and their evidence labels (Git verified, Test verified, You noted, L2Cache inferred); how agent sessions, test runs and releases line up per project; Needs attention (failed runs, unpushed commits, pushed-but-unmerged branches).
**Sources:** `docs/PRD-Developer-Home-Redesign.md`, `docs/L2Cache-2.0-Redesign-Summary.md`, `L2cache/Services/WorkActivity/` (MilestoneBoard, MilestoneActions).

### T-C502 — `/en/developer-timesheet-standup-from-activity`
**Working title:** Your hours, already counted: a timesheet and standup from your coding activity
**Covers:** tickets detected from branches and commits; approximate hours per day and how they're estimated; correcting and copying into a timesheet tool; the editable standup and Weekly Brief; Your Day work summaries (Claude Code and Codex only); all local.
**Sources:** `docs/PRD-Tickets-and-Timesheet.md`, `docs/PRD-Work-Summaries-Your-Day.md`.

## Wiring
`build.py`, `sitemap.xml`, `llms.txt`, `blog.html`, footer, Projects popup "Read more" (both); cross-link to `day-in-the-life-mac-developer`.

## Verify
Facts table; `build.py`, `check_home_links.py`, `validate_seo.py`; 1440px and 390px.

## Review
_To be filled in after the sprint._
