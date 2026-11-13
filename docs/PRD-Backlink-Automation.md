# Backlink automation for the pillar essays

**Status:** In progress (S1, S3 dev.to done) · **As of:** 2026-11-13 · **Rules:** `SEO_STRATEGY.md` §8 (backlinks), §16 (agent authority levels, guardrails)

## Goal

Each week, find and prepare honest backlink opportunities for the pillar essays, so the only manual work is a few minutes of approving in a tracker. Anything published under your name, or any message sent to a person, waits for your approval (§16 Level 2). Nothing is posted to forums or comment threads automatically.

## Decisions (from you, 2026-11-13)

| | Choice |
|---|---|
| Channels | Syndication, discussion finder, outreach drafts, unlinked mentions |
| Review | A private claude.ai tracker page with a shared database |
| Accounts | dev.to, Hashnode, GitHub (dindina). No Gmail: pitches are copied from the tracker and you send them |
| Runs on | A weekly cloud routine (Monday 8:00 Sydney) |

## Pillars

`scripts/backlinks/pillars.json` lists every essay that the automation promotes: its URL, main keyword and related keywords, the LLM question, and its key findings (all already in `docs/medium/SEO-GEO-Review.md`). Starts with M1–M5. A new essay is promoted by adding one entry.

## The four channels

### 1. Syndication (dev.to, Hashnode)
- Converts each live essay to Markdown (tables kept, since both sites render them) and publishes it with the canonical link set to the l2cache.app page (dev.to `canonical_url`, Hashnode `originalArticleURL`). Search credit stays with the site.
- Adds tags from the pillar's keywords, a cover image (the first chart), and one line at the end pointing to the original and its script.
- **Approval:** each essay appears in the tracker as "Ready to syndicate". On approval, the next run publishes it as a **draft** on both sites; a "Publish" toggle in the tracker publishes it for real. One essay a week, staggered after its Medium import.
- Records the post IDs, so nothing is ever posted twice.

### 2. Discussion finder (Reddit, Hacker News, Stack Overflow)
- Searches the public APIs (Reddit search JSON, HN Algolia, Stack Exchange) for the last 7 days of threads and questions matching each pillar's keywords and LLM question, e.g. "tests pass but exit code 0", "Claude Code cache expired cost".
- Scores each one by how closely it matches, how recent it is, and whether it's still open. Keeps the top 5 a week.
- Drafts a reply that **answers the question in the thread on its own terms**, and adds the essay link only where the data genuinely helps. Flags each subreddit's self-promotion rule when it's known.
- **You post it yourself** (a "Copy reply" button and the thread link). The tool never posts.

### 3. Outreach drafts
- **Awesome lists:** GitHub search for maintained lists (e.g. awesome-claude-code, awesome-mcp-servers, awesome-ai-agents, awesome-developer-productivity, awesome-macos) that were active in the last 90 days, accept contributions, and have a section the essay fits. Drafts the exact line to add, following each list's CONTRIBUTING rules. On approval, the next run opens the PR from `dindina`.
- **Newsletters and resource pages:** finds newsletters and roundup pages covering Claude Code, coding agents and developer productivity (from web search and public submission pages). Drafts a short, personalised pitch that leads with the finding, not the product (§8 pitch structure). On approval, you copy and send it, or use the submission form it links to.
- One first message and at most two follow-ups (drafted 7 and 14 days later, again for approval). Declined or unsubscribed contacts are never contacted again.

### 4. Unlinked mentions
- Web search for "L2Cache", the essay titles and their distinctive figures (e.g. "120 of 127", "cold session tax"). Fetches each result page and checks whether it links to l2cache.app.
- Mentions without a link become a drafted, polite link request for your approval.

## Tracker (claude.ai page with a database)

One row per opportunity:

| Field | Values |
|---|---|
| Channel | Syndication · Discussion · Awesome list · Newsletter · Mention |
| Pillar | Which essay |
| Where | Site or thread name, URL |
| Why it fits | One line from the run |
| Draft | Reply, pitch, PR line or syndication preview |
| Status | New → Approved / Skipped → Done (posted, PR opened, sent) → Linked / Declined / No reply |
| Acquired URL, link check | Filled in by verification |

Buttons: Approve, Skip, Edit draft, Copy, Mark sent. A header shows this month's counts: prospects, approved, live links.

## Weekly run (cloud routine)

1. Act on rows you **approved** since the last run: publish syndication drafts, open PRs. Discussion replies and pitches are yours to send.
2. **Verify** every Done row: fetch the page, confirm a link to l2cache.app (and whether it's nofollow), and set Linked / not found. Rows with no reply after follow-ups become No reply.
3. **Discover:** at most 5 discussion threads, 5 outreach prospects and all new mentions; drop anything already in the tracker or on the decline list.
4. Write the new rows and a one-paragraph weekly summary at the top of the tracker.

## Guardrails (from §16, enforced in code)

- Nothing is posted to forums or comments by the tool; nothing is sent to a person without your approval.
- Weekly caps: 1 syndicated essay, 5 discussion drafts, 5 outreach drafts. No near-identical pitches (each draft must cite something specific to the recipient).
- No paid links, link exchanges or directories outside the §8 list.
- Claims in drafts come only from the pillar's key findings.
- Tokens live as routine secrets, never in the repo or the tracker.

## Open risks (checked first, in the spike)

1. **Can the cloud routine read and write the tracker database?** If not, the fallback is that the routine writes `docs/backlinks/prospects.json` to the repo and a small local step syncs it into the tracker.
2. **Can the routine open PRs on third-party repos as dindina?** Its GitHub access may be limited to l2cache-site. Fallback: a GitHub token secret with `public_repo` scope, or I open approved PRs from this Mac.
3. **Reddit API access from the cloud** may be rate-limited without OAuth. Fallback: HN and Stack Exchange only, plus Reddit via web search.

## Findings (2026-11-13)

- **Hashnode:** its GraphQL API became Pro-only (paid) on 2026-05-13, so free automated posting isn't possible. Options: pay for Pro, cross-post by hand in Hashnode's editor (its import sets the canonical), or skip Hashnode. Syndication is dev.to only until you choose.
- **Credentials in `.env`:** `DEV_TO_API_KEY` works (account dinesh_rajendran_46fc29b4). `GITHUB_TOKEN` works as dindina with `repo` scope (enough for list PRs from this Mac); it expires 2026-12-27.
- **Older dev.to posts** (10, from the clipboard-era site) have canonicals on `l2cache.amvo.store`. Those 308 to l2cache.app, so credit still flows, but pointing them straight at l2cache.app is cleaner and is one API call each.
- Dry runs write to `$TMPDIR/l2cache-syndication/`, never `out/` (Vercel deploys `out/`).

## Plan

- [ ] S0 Spike: routine ↔ tracker database, routine ↔ GitHub PRs, Reddit/HN/SE API access from the cloud
- [x] S1 `pillars.json` from the review doc (M1–M5)
- [ ] S2 Tracker page with the database (fields, buttons, counts)
- [x] S3 `scripts/backlinks/syndicate.py`: site page → Markdown, dev.to draft with canonical, idempotent (state.json + canonical match). M1 draft 5026170 created 2026-11-13, rerun updated it in place. Hashnode dropped, see below
- [ ] S4 Discussion finder + reply drafting
- [ ] S5 Awesome-list and newsletter discovery + pitch/PR drafting; PR opening on approval
- [ ] S6 Unlinked-mention search + link check
- [ ] S7 Link verification + follow-up drafting
- [ ] S8 Weekly cloud routine (Mon 8:00 Sydney) wiring S3–S7; one dry run you review end to end
- [ ] S9 Docs: this file → done notes; `SEO_STRATEGY.md` §8 points here

**You'll need to provide:** a dev.to API key, a Hashnode personal access token and publication, and (if S0 needs it) a GitHub token with `public_repo` scope.
