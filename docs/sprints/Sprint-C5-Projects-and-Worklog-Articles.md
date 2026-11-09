# Sprint C5 — Projects & Worklog articles

**Status:** ✅ Done · **Date:** 2026-11-09
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
- **T-C501** `project-story-git-timeline-mac.html` (~7 min): Graph and Timeline views, what the timeline mixes (table), reads `.git` without running Git, the project overview lines, milestone kinds and journeys, the four evidence labels (table), board sections, your corrections and per-type actions, Needs attention, sharing (weekly recap, project standup, presentation mode), all local.
- **T-C502** `developer-timesheet-standup-from-activity.html` (~6 min): learning ticket formats (confirm first), work items and branch linking, how hours are estimated, corrections and Add Row, saved weeks and Recalculate, Copy as Table / Text / Export CSV / Copy Weekly Recap, the standup (template or AI limited to the facts), the Weekly Brief, the weekly recap, Your Day (Claude Code and Codex summaries, *not pushed*, *Unsummarised activity*), all local, Developer Pro.
- **Wiring:** `build.py`, `validate_seo.py`, `blog.html` (after the featured card), `sitemap.html`, `llms.txt`, footer Product (+ Project Story, Timesheet & standup), Projects popup gets its first "Read more" row (both articles). Cross-links: both articles ↔ each other and → `day-in-the-life-mac-developer`, which gets one paragraph linking back.
- **Also fixed:** `day-in-the-life-mac-developer` was 466px wide at 390px (its four-column table); the table now scrolls inside its box on phones.
- **Changes from plan:** the plan called it "Weekly Brief"; the app has both a **Weekly Brief** (Today button, summary written by AI or a template) and an editable **weekly recap** (Milestones). The article describes both. The homepage popup's "Weekly Brief & standup" line is kept, because the button exists.
- **Verify:** `build.py` OK; `site_i18n.py extract` → 590 strings; `check_home_links.py` → 83 internal links resolve; `validate_seo.py` passed (48 pages). Both articles and day-in-the-life at 390px (no page scroll); Projects popup at 1440px.

### Facts table
| Claim | Source |
|---|---|
| Project Story with Graph and Timeline; notes detached HEAD, operation in progress, shallow clone, no remote | `ProjectStorySection.swift` |
| Reads reflogs and the object store, never runs or writes Git, discards identities | `GitHistoryReader.swift`, `GitObjectReader.swift`, `ProjectGraphBuilder.swift`, `RepositoryScanner.swift` |
| Repos found from the projects folder in Settings; worktrees and submodules count | `RepositoryScanner.swift`; `ProjectDetailView` empty state |
| Timeline kinds: commit, merge, branch, tag, session, passed/failed run, recovery point, dependency, deploy | `TodaySnapshot.swift` timeline `Kind` |
| Sessions from Claude Code, Codex, Copilot, Grok, Antigravity | `WorkActivityExtractor.swift` per-provider state |
| Overview lines (working on, commits in 7 days, merges, releases, active branches, uncommitted, only on this Mac, pushed not merged, idle 30+ days, failed commands, unfinished agent tasks, commits since last pass) | `ProjectInsights.swift` |
| Milestone kinds MERGED / BIG DAY / STARTED / TESTS FIXED / RELEASED; journeys | `MilestoneBoard.swift`; `TodaySnapshot.Milestone.Kind` |
| Labels Git verified / Test verified / You noted / L2Cache inferred; inferred never shown as verified | `MilestoneBoard.swift` `MilestoneProvenance` |
| Sections Pinned / In progress / Completed this week / Shipped / Needs evidence / Earlier | `MilestoneBoard.SectionKind` |
| Milestone actions | `MilestoneActions.swift` |
| Needs attention kinds; collapse of 3+ items | `TodaySnapshot.AttentionItem.Kind`; `TodaySnapshotBuilder` |
| Weekly recap: include/exclude, edit, Mask names, Copy as Markdown / for Slack | `WeeklyRecap.swift`; `WeeklyRecapSheet.swift` |
| Copy project standup, last two days | `ProjectDetailView.swift` |
| Presentation mode masks names, paths, prompts, commands | `PresentationMasker.swift` |
| Ticket formats learned from branches, commits, sessions; confirm first; paste one | PRD-Tickets-and-Timesheet D1–D2; `TicketFormatSetupView.swift` |
| Branch work items, Link to …?, Assign to Ticket…; long-lived (main, >30 days) → project | `TicketDetailView.swift`; `TimesheetEngine` |
| 15-min idle gap, 5-min point credit, nearest-branch rule, quarter-hour rounding | `TimesheetEngine.swift`; `TimesheetView` caption |
| Estimated from your activity / Corrected by you; Add Row; saved weeks; Recalculate | `TimesheetView.swift`, `TimesheetGrid.swift` |
| Copy as Table / Copy as Text / Export CSV… / Copy Weekly Recap | `TimesheetView.swift` |
| Standup Yesterday/Today/Blockers; template with AI off; AI limited to the facts | `StandupWriter.swift` |
| Weekly Brief button; AI or template | `TodaySections.swift`; `WeeklyInsightWriter.swift` |
| Your Day: by feature, Claude Code + Codex summaries, not pushed, Unsummarised activity | `YourDayCard.swift`; `AgentContinuityService.workSummaryProviders`; PRD-Work-Summaries |
| Worklog needs Developer Pro | `HomeTicketsSection` "Worklog is part of Developer Pro" |
