# L2Cache Next-Generation Homepage Creative Brief

**Status:** Approved working direction for Phase 2 prototypes  
**Date:** 15 October 2026  
**Concept:** The Living Project Timeline

## The One-Sentence Idea

Follow one believable software project through a day and show how L2Cache preserves the thread between coding agents, Git, terminal work, tickets, screenshots, and clipboard moments—then turns that thread into the next useful action.

The application is the protagonist. The website should feel like a product documentary with an editorial Mac sensibility, not a stack of feature cards.

## Visitor Outcome

After the hero and first product sequence, a visitor should be able to say:

> L2Cache is a Mac app that remembers my development activity across tools so I can understand what happened and resume work quickly.

## Audience

Primary: macOS developers who move between repositories, terminals, branches, tickets, and AI coding agents.  
Secondary: privacy-conscious power users and engineering leads who need searchable history, standups, or weekly recaps.

## Working Hero Copy

**Eyebrow:** Developer memory for Mac  
**Headline:** Pick up where you left off.  
**Support:** L2Cache connects your projects, coding-agent sessions, terminal history, Git activity, screenshots, and clipboard content so the thread of your work is ready when you return.  
**Primary CTA:** Download on the Mac App Store  
**Secondary CTA:** Watch the project come back to life

The secondary action scrolls into the first product sequence. It is not a decorative video button.

## Narrative Sequence

### 1. The return

A restrained application window opens on Today. The user sees the last project state, an open loop, and one clear resume action. A fine project-coloured thread starts at the last recorded event and continues down the page.

**Purpose:** Explain the product category and promise in one screen.  
**Proof asset:** Today screen with synthetic project data and a genuine resume action.

### 2. The day reconstructs itself

As the visitor moves down the page, the thread connects a coding-agent session, failed terminal command, successful fix, commit, ticket, and milestone. Each event adds new information; nothing repeats the hero claim.

**Purpose:** Make “developer memory” concrete.  
**Interaction:** The active event changes the corresponding detail inside the app window. Without JavaScript, every event remains visible as a readable ordered timeline.

### 3. Every project keeps its story

The composition widens into Project Story. Decisions, recovery points, branches, tests, commits, and sessions form a readable narrative around one project instead of appearing as disconnected activity counters.

**Purpose:** Establish L2Cache as more than a clipboard utility.  
**Proof asset:** Project Story with one decision and one recovery point.

### 4. Coding agents finally have a history

A provider rail introduces Claude Code, Codex, GitHub Copilot, Grok Build, and Google Antigravity as sources of local session history. A capability disclosure makes the differing depth explicit.

**Purpose:** Own the coding-agent history use case without overclaiming parity.  
**Required label:** “Session history from,” never “Full integrations.”  
**Disclosure:** “Available details and live-continuity features vary by agent.”

### 5. Find the thread with Command-K

The visitor can try a small set of prewritten, synthetic queries. Results come from projects, agent sessions, terminal commands, screenshots/OCR, and clipboard items.

**Purpose:** Demonstrate cross-source retrieval.  
**Privacy rule:** The demo never records or sends typed query text. In the first prototype, use selectable examples rather than free-form input.

### 6. Local-first, with honest boundaries

A simple system diagram places the local history database at the centre. On-device Apple Intelligence, local Ollama, and rule-based processing sit within the Mac boundary. Optional or action-specific services sit outside and are visibly labelled.

**Purpose:** Build trust through precision.  
**Do not use:** shields, locks, “military-grade,” air-gap, zero-egress, or absolute offline claims.

### 7. A capability map, not a card grid

Today, Timeline, Tickets, Projects, Clipboard, Connections, Folders, Coding Agents, Terminal, and Milestones appear as destinations on the same project thread. Each destination has one concrete job and links to a focused product page.

**Purpose:** Reveal breadth after the core mental model is understood.

### 8. Continue the work

End by returning to the open loop from the hero. The same project now has enough context to continue. Place the App Store CTA beside concise commerce wording: free download, 15-day trial, one-time Pro unlock, with no numeric price until `[[PRO_PRICE]]` is resolved.

**Purpose:** Resolve the narrative and convert.

### 9. Evidence and navigation

Finish with a small, visible FAQ based on real search intent and links to product pages, integrations, guides, privacy, support, changelog, about/publisher information, and developer utilities.

## Visual System

### Art direction

- Deep graphite and warm off-white surfaces, derived from a native Mac workspace rather than a cyberpunk dashboard.
- One semantic accent colour per example project. The hero project colour becomes the page's connecting thread.
- Large product captures with enough scale to read; avoid floating piles of tiny screenshots.
- Editorial typography paired with restrained monospace metadata.
- Fine rules, timestamps, branch labels, and status marks supply texture without fake terminal noise.
- Glass is limited to controls and transient overlays; primary content uses solid, high-contrast surfaces.

### What makes it recognisably L2Cache

- Real navigation names and product hierarchy.
- A continuous project thread linking otherwise separate tools.
- Native Mac window composition.
- Presentation-mode fixtures and plausible developer activity.
- Recovery, resume, story, and memory as repeated interaction ideas—not repeated slogans.

### Explicit anti-patterns

- No neon orb, aurora background, oversized gradient headline, bento-grid parade, or endless rounded cards.
- No fake testimonials, company logos, usage counts, awards, benchmarks, or security badges.
- No generic three-step “capture, organise, transform” block.
- No scroll-jacking, forced horizontal scroll, or animation that hides the reading order.
- No template copy or template-specific visual metaphor that does not map to L2Cache.

## Motion Specification

1. The project thread draws only as the related content enters view.
2. App-window state changes use short crossfades or native-feeling panel transitions.
3. Timeline events may settle into place with small depth changes; no constant floating.
4. Command-K demonstrates selection, result grouping, and preview—not simulated typing theatre.
5. The final resume action visually closes the open loop introduced in the hero.
6. `prefers-reduced-motion` shows the final states immediately and removes parallax, drawing, and auto-advance.
7. All narrative content remains present and ordered when JavaScript is unavailable.

MotionSites may inform pacing and transition mechanics, but the composition, assets, interaction logic, and copy must be original.

## Responsive Behavior

- **Desktop:** Sticky product stage beside the vertical story, with the project thread connecting both.
- **Tablet:** Product stage moves inline between story chapters; no miniature two-column layout.
- **Mobile:** A linear editorial sequence with full-width captures and compact event summaries. Do not autoplay video or pin the viewport.
- **Long content:** Copy and labels may wrap without clipping; provider names and project paths must tolerate realistic lengths.

## Accessibility and Performance

- WCAG 2.2 AA contrast, semantic landmarks, one H1, logical heading order, visible focus, keyboard-operable demos.
- Every product sequence has static explanatory copy and meaningful image alternatives.
- No information conveyed only by colour or motion.
- LCP target below 2.5 seconds, INP below 200 ms, CLS below 0.1 at the 75th percentile.
- Initial hero should use an optimised still image or HTML/CSS composition; defer nonessential motion.
- Self-host or use system fonts where licensing allows; subset any display face.

## Required Fixture and Capture Set

Use one synthetic project consistently across the homepage. Suggested placeholder project: **Northstar**, a local Mac developer tool. Final naming and content may change.

1. Today with last state, open loop, next action, and attention item.
2. Timeline containing agent, terminal, commit, ticket, test, and clipboard events.
3. Project Story with a decision, milestone, and recovery point.
4. Coding Agents session list plus one safe conversation detail.
5. Plans/skills/rules screens only where the provider matrix supports them.
6. Command-K results across at least four source types.
7. Terminal failure followed by a related successful command.
8. Presentation mode comparison for capture safety.

All data must be synthetic or verified as presentation-safe. Avoid real usernames, repository paths, prompts, ticket IDs, API keys, URLs with private tokens, and customer material.

## Prototype Deliverables

Phase 2 should create two isolated, non-production concepts:

1. **Living Project Timeline** — the primary direction described above.
2. **Developer Daybook** — a quieter editorial variant using the same content and claim boundaries.

Each concept must cover desktop, mobile, and reduced-motion states. Selection is based on product clarity, distinctiveness, credibility, accessibility, and likely performance—not visual spectacle alone.

