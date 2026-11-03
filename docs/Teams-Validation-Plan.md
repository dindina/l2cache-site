# Teams Validation Plan — go / no-go for Session Intelligence for Teams

**Status:** Active · written 2026-11-03
**Decision date:** Monday 2027-01-05
**Related:** [PRD-Teams-Waitlist.md](PRD-Teams-Waitlist.md) (the page), `teams/` (site), `supabase/teams_waitlist.sql`

## The question

Should Session Intelligence for Teams (working name) become the main product, with the L2Cache Mac app in maintenance, or should it stay an idea?

We answer it with evidence from real teams before writing any product code. The thresholds below are set **now**, before results come in, so excitement or disappointment doesn't make the call.

## What we already know (measured)

From `scripts/cold_share.py` on the founder's own Claude Code use, last 30 days to 2026-11-03 (9,130 requests, 98% Opus). One heavy user, so treat it as an upper bound, not a team average.

- Cold reloads: **0.9% of tokens but ≈10% of cost** (cost weighted by Anthropic's price multipliers: read 0.1×, 5m write 1.25×, 1h write 2×, output 5×).
- ≈9.7% of cost was avoidable compared with a warm turn; 55 of 56 cold turns were 1-hour caches expiring, all on contexts ≥ 50k.
- Five very large sessions (544k–880k) were ≈7.7% of total cost; four of them hit rate limits.
- Cache writes overall were 34% of cost: carrying large context is expensive even when warm.

Rerun monthly: `python3 scripts/cold_share.py 30`. Once the guard has been on for a month, the cold share should drop.

## Timeline

| Phase | Dates | Outcome |
|---|---|---|
| 0. Ship and switch | 2026-11-03 → 2026-11-16 | L2Cache 2.0 released and in maintenance; waitlist live |
| 1. Validate | 2026-11-17 → 2026-12-28 (6 weeks) | Signups, calls, pilot commitments |
| 2. Decide | 2027-01-05 | Go / interest-only / stop, using the table below |

The last two weeks overlap the holidays, so expect fewer replies after 2026-12-19. Front-load outreach and calls into weeks 1–4.

## Phase 0 — ship and switch (by 2026-11-16)

### L2Cache 2.0
- [ ] Finish testing the code-complete 2.0 work and release it.
- [ ] Switch to **maintenance mode**:
  - **In:** crash and data-loss fixes, macOS compatibility, App Store review issues, reply to support email within 2 working days.
  - **Out:** new features, redesigns, new sprints.
  - Time cap: about half a day a week, unless something breaks.
- [ ] Add one line to the 2.0 "What's new" panel and the `l2cache.app` changelog: building a team version, link to `teams.amvo.store`. This is how existing users hear about it.

### Waitlist live
- [ ] Add the `teams.amvo.store` domain to the Vercel project (plus a CNAME record if amvo.store's DNS isn't on Vercel).
- [ ] Run `supabase/teams_waitlist.sql` in the IronTrack Supabase project.
- [ ] Add `SUPABASE_URL` and `SUPABASE_SECRET_KEY` in Vercel (Production and Preview).
- [ ] Preview deploy (not `deploy.sh`, which goes straight to production). Submit once and confirm the row in Supabase.
- [ ] Production deploy. Submit once more from a phone.
- [ ] Test the link preview by pasting `https://teams.amvo.store` into Slack and an email.

## Phase 1 — validate (6 weeks)

### Who counts

A **qualified signup** is a team of **2 or more developers** using **Claude Code or Codex**. Solo developers are welcome on the list but don't count toward the decision. Only email and team size are required, so a team that skipped the agents question counts as "to confirm": ask by email or on the call.

Track two segments separately:
- **Product teams** (build their own software).
- **Agencies and consultancies** (bill clients for work). They may value per-client cost and time reports more, and pay more.

```sql
-- Qualified signups so far (run in the Supabase SQL editor)
select count(*) filter (where agents && array['claude-code','codex']) as qualified,
       count(*) filter (where agents = '{}') as to_confirm
from public.teams_waitlist
where team_size <> '1';
```

### Outreach

Aim for about **150 direct touches** over the 6 weeks. Personal messages beat posts.

| Channel | What | Target |
|---|---|---|
| People you know | Leads and CTOs at small companies using coding agents; ex-colleagues | 30 personal messages |
| L2Cache users | "What's new" line, changelog, replies to support emails | passive, ongoing |
| LinkedIn | Personal note to engineering leads at 5–50 person companies | 60 messages |
| Agencies | Small dev agencies and consultancies using agents (LinkedIn, local agency networks) | 20 of the 60 LinkedIn messages |
| Communities | Claude Code / Codex communities, Hacker News "Show HN" once the page is live, relevant subreddits and Discords | 4–6 posts, following each community's self-promotion rules |
| Your content | One post on the cold-restart problem (the "≈20×" cost) with real numbers from your own sessions | 1–2 posts |

#### Message template (personal)

> Hi {name} — I make L2Cache, a Mac app for developers who work with coding agents. I'm exploring a team version: what each agent session costs, catching expensive cold restarts before they happen, and handoffs between sessions, without uploading anyone's conversations.
>
> Does your team use Claude Code or Codex? If so, I'd love 20 minutes to hear how you handle agent usage today. No pitch, just learning. Overview: https://teams.amvo.store

#### Post template (community)

> I built a guard for Claude Code that catches cold-cache resumes: when you resume a big session after its cache expired, the next message re-writes the whole context, about 20× the cost of a warm turn. It warns you and offers a fresh session with a handoff instead.
>
> I'm now exploring a team version (usage, cold-restart and "what shipped" reports, with conversations staying on each machine). If your team uses agents, I'd value your take: https://teams.amvo.store

### Discovery calls

Goal: **10 calls** with team leads or CTOs. Book a call with every qualified signup who wrote something in "biggest pain", and with anyone from outreach who replies.

#### Call script (20 minutes)

Listen; don't pitch until the last 5 minutes. Note their exact words.

1. **Context (3 min)**
   - How many developers use coding agents? Which ones? On which OS?
   - Roughly what do you spend on agents a month, and on which plans (API, Max, Team)?
2. **Current state (7 min)**
   - How do you find out what your team worked on this week? How long does it take you, and how often do you have to chase someone for an update?
   - How do you know what the team spends on agents today? Who looks at it, and how often?
   - Tell me about the last time agent cost or usage surprised you.
   - What happens when someone resumes a session the next day, or picks up a teammate's work?
   - Have you tried anything for this (vendor dashboards, a gateway, ccusage, spreadsheets)? What was missing?
3. **Privacy (3 min)**
   - Would your developers accept a tool that reads agent transcripts on their machine and sends only numbers and approved summaries? What would worry them?
4. **Show (4 min)**
   - Show `teams.amvo.store`: pickup card, guard, report. Which part matters most? Which part wouldn't you use?
5. **The ask (3 min)**
   - "If this existed in 6–8 weeks, would you install it on your team for a 4-week pilot?"
   - "What would it need to be worth paying per developer per month?" Then anchor: "Would $12 be easy? $15? $25?" Note where they hesitate. If $25 is easy for most, the price is too low.
   - "Of these, which would make you pay?" Show the form's list: team updates (what everyone worked on), proactive session alerts, usage report, seat and plan advisor, quota forecast, secret-leak alerts, agent safety inventory, PR recaps, per-client reports, team memory. Note their top one.
   - Agencies only: "Would per-client agent cost and time help you bill or justify invoices?"
   - Who decides on buying a tool like this?

### Tracking

One sheet (Google Sheet or Numbers), one row per team:

| Column | Example |
|---|---|
| Team / company | Acme |
| Contact, role | Jo, CTO |
| Source | LinkedIn / L2Cache user / community / referral |
| Team size, agents, OS | 12 · Claude Code, Codex · macOS + WSL |
| Signed up (date) | 2026-11-20 |
| Call (date) | 2026-11-24 |
| Biggest pain (their words) | "No idea who's burning the Max quota" |
| Most valued feature | Report |
| Privacy concern | none / some / blocker |
| Segment | product team / agency |
| Would pay for (top pick) | seat advisor |
| Pilot? | yes / maybe / no |
| Price reaction | "$15 fine, $25 needs approval" |
| Next step | send pilot invite |

Weekly, every Monday: update the counts below and add one line of notes.

| Week | Touches | Signups (qualified) | Calls | Pilot yes | Notes |
|---|---|---|---|---|---|
| 1 (11-17) | | | | | |
| 2 (11-24) | | | | | |
| 3 (12-01) | | | | | |
| 4 (12-08) | | | | | |
| 5 (12-15) | | | | | |
| 6 (12-22) | | | | | |

### Feature demand

The form asks "Which of these would make you pay?" (stored in `wanted`):

```sql
select w as feature, count(*) as teams
from public.teams_waitlist, unnest(wanted) as w
where team_size <> '1'
group by w order by teams desc;
```

## Pricing hypothesis (to test in calls)

| Plan | Price | Contents |
|---|---|---|
| Free (individual) | $0 | Collector, pickup cards, session history, guard, handoffs, context nudges |
| Team | $15/dev/month monthly, $12 annual, min 3 seats | Report, digest, outcomes, what shipped, team memory, plus the first lead features that win |
| Small-team flat (alternative) | $49/month up to 5 devs | Same as Team |
| Business (later) | $25+/dev | SSO, team-totals-only mode, longer history, export/API |

Reasoning: below engineering-analytics tools (LinearB ≈$29, Swarmia ≈$15–40 per developer, from third-party pricing sites), and about 10% of a Claude Team premium seat (≈$100–125), which matches the measured avoidable-waste ceiling. A free individual tier overlaps with L2Cache's agent features; acceptable while L2Cache is in maintenance.

## Running costs (estimates, check vendor pricing)

- Metadata only reaches the cloud: ≈2 MB per developer per month (≈300 requests/day × ≈200 bytes). No server-side AI; recaps are written by each developer's agent.
- Waitlist now: $0–20/month. Pilot: ≈$25–50. ≈500 developers: ≈$100–250, against ≈$6–7.5k/month revenue at $12–15.
- Check now: Vercel Hobby is for non-commercial use (Pro ≈$20/member). Free Supabase projects pause when inactive, which would make signups fail; check the IronTrack project's plan.
- Non-server: Windows code-signing certificate, payment fees, email delivery; security audits only if selling to larger companies.

## Phase 2 — decide (2027-01-05)

| Result by 2026-12-28 | Decision |
|---|---|
| **≥ 30 qualified signups**, **≥ 10 calls**, and **≥ 3 teams committed** to a pilot or pre-payment | **Go.** Teams becomes the main product. L2Cache stays in maintenance. Start the core binary (macOS first), with the pilot teams as first users. |
| Signups and calls, but **< 3 pilot commitments** | **Interest without urgency.** L2Cache stays the main product. Keep the waitlist up, write down what the calls said was missing, revisit in 3 months. |
| **< 15 qualified signups** after real outreach | **Stop Teams.** Thank the signups, take the page down or leave it as is, and put the time back into L2Cache. |

A "committed" team has agreed to a pilot start date or paid a deposit. "Sounds great, keep me posted" doesn't count.

### Also decide on 2027-01-05

- **Name:** pick a real product name if the answer is Go. The working name is a placeholder.
- **Price:** from the call reactions, set a starting per-developer monthly price.
- **First build scope:** which 3–4 features the pilot teams actually asked for, using the `wanted` counts and the calls' top picks. Expected: pickup cards, guard, team updates ("what shipped"), usage and cold-restart report, plus whichever lead feature wins (seat advisor, secret-leak alerts or PR recaps).
- **Segment:** product teams, agencies, or both.

## What would change this plan

- **A vendor ships it.** If Anthropic or Cursor launches cold-restart detection or cross-agent team reports during the 6 weeks, note it. It doesn't stop the test, but ask in every remaining call whether the vendor feature is enough.
- **Privacy is a blocker.** If 3 or more calls say transcript reading is a no-go even locally, that's a stop signal regardless of signup numbers.
- **Strong pull early.** If 3 teams commit before week 4, you can decide early.

## Not doing during validation

- No product code for Teams: no collector, no backend, no dashboard.
- No paid ads.
- No new L2Cache features.
