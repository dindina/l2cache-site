import re, pathlib
root = pathlib.Path.home() / "tech/l2cache-site"
src = (root / "prototypes/teams-mockups/index.html").read_text()

def mock(sec_id):
    start = src.index(f'<section class="feature" id="{sec_id}">')
    end = src.index('</section>', start)
    body = src[start:end]
    fc = body.index('<div class="feature-copy">')
    fc_end = body.index('</div>', fc) + len('</div>')
    html = body[fc_end:].strip()
    return rebrand(html) if sec_id in TEAM_ONLY else html

TODAY = ''
NEW = ''
SITE = "https://teams.amvo.store"
TEAM_ONLY = {"memory", "report", "digest", "outcomes", "shipped", "sharing", "skills"}
MARK = ('<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#7638d9"/>'
        '<circle cx="16" cy="16" r="8.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-dasharray="40 14" stroke-linecap="round"/>'
        '<circle cx="16" cy="16" r="2.6" fill="#fff"/></svg>')
FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%237638d9'/>"
           "<circle cx='16' cy='16' r='8.5' fill='none' stroke='white' stroke-width='2.4' stroke-dasharray='40 14' stroke-linecap='round'/><circle cx='16' cy='16' r='2.6' fill='white'/></svg>")

def rebrand(html):
    for a, b in [('<b>l2cache.app</b>', '<b>teams.amvo.store</b>'),
                 ('L2Cache for Teams<span class="app">', 'Session Intelligence<span class="app">'),
                 ('<div class="l2">L2</div>', '<div class="l2">SI</div>'),
                 ('l2cache · get_error_resolutions', 'team memory · get_error_resolutions')]:
        html = html.replace(a, b)
    return html

def feature(sec_id, title, status, copy, example=True):
    note = "Example data" if sec_id in TEAM_ONLY else "Shown in L2Cache for Mac, where this runs today"
    ex = f'<span class="example">{note}{" · example data" if example and sec_id not in TEAM_ONLY else ""}</span>'
    return f'''
  <section class="feature" id="{sec_id}">
    <div class="feature-copy">
      <h3>{title}{status}</h3>
      <p>{copy}</p>
    </div>
    {mock(sec_id)}
    {ex}
  </section>'''

agents_strip = src[src.index('<div class="agents">'):src.index('</div>', src.index('<div class="agents">'))+6]

page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Session Intelligence for Teams — Coding-Agent Usage, Cold Restarts and Handoffs</title>
  <meta name="description" content="Know what your team worked on with coding agents and what it cost, stop expensive cold restarts, and pick up any session with a handoff. Conversations stay on each machine.">
  <link rel="canonical" href="https://teams.amvo.store/">
  <meta name="theme-color" content="#f7f6f3">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Session Intelligence for Teams">
  <meta property="og:url" content="https://teams.amvo.store/">
  <meta property="og:title" content="Session Intelligence for Teams">
  <meta property="og:description" content="Know what your team worked on with coding agents, and what it cost. Updates without chasing, a cold-restart guard and handoffs. Join the waitlist.">
  <meta property="og:image" content="https://teams.amvo.store/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://teams.amvo.store/og.png">
  <meta name="twitter:title" content="Session Intelligence for Teams">
  <meta name="twitter:description" content="Know what your team worked on with coding agents, and what it cost. Join the waitlist.">
  <link rel="icon" href="{FAVICON}">
  <link rel="stylesheet" href="/styles.css">
  <script src="/script.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="/">{MARK}<span>Session Intelligence <em>for Teams</em></span></a>
    <ul class="nav-links">
      <li><a href="#features">Features</a></li>
      <li><a href="#proactive">Detection</a></li>
      <li><a href="#shipped">For leads</a></li>
      <li><a href="#privacy">Privacy</a></li>
      <li><a href="#faq">FAQ</a></li>
    </ul>
    <a class="btn btn-primary btn-small" href="#join"><span>Join<span class="long"> the waitlist</span></span></a>
  </nav>
</header>

<main id="main" class="wrap">

  <section class="hero">
    <p class="eyebrow">Early access · from the makers of L2Cache</p>
    <h1>Session intelligence for teams that code with agents.</h1>
    <p class="lede">Pick up any agent session at the right cost, stop expensive cold restarts, and see what your team worked on and what it cost — without chasing anyone or uploading conversations.</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="#join">Join the waitlist</a>
      <a class="btn btn-ghost" href="#features">See what you'll get</a>
    </div>
    <p class="fineprint">macOS first · Windows and Linux planned · Claude Code and Codex first</p>
    {agents_strip}
  </section>

  <section class="section" id="problem">
    <div class="section-head">
      <p class="eyebrow">The problem</p>
      <h2>Agents made coding faster. Nobody can see what the sessions cost.</h2>
    </div>
    <div class="problems">
      <div class="problem"><span class="big">≈20×</span><h3>Cold restarts cost the most</h3><p>Resume a big session after its cache expired and the next message re-writes the whole context, about 20 times the cost of reading it from a warm cache. Nothing tells you it happened.</p></div>
      <div class="problem"><span class="big">Tokens ≠ work</span><h3>Usage without outcomes</h3><p>Vendor dashboards count usage per tool. They don't show which sessions became commits, which ones stalled, or what was wasted.</p></div>
      <div class="problem"><span class="big">Day 2</span><h3>Context gets lost</h3><p>After a /clear, a new day or a hand-over to a teammate, the agent starts over and work gets redone.</p></div>
    </div>
    <details class="method">
      <summary>How we got ≈20×</summary>
      <div class="method-body">
        <p>Under Anthropic's standard prompt-cache pricing, writing context into a 1-hour cache costs 2× the model's base input price per token. Reading that context from a warm cache costs 0.1×.</p>
        <p>When the cache has expired, resuming a session can require writing the existing context again instead of reading it from cache:</p>
        <p><strong>2 ÷ 0.1 = 20× the cost for that context.</strong></p>
        <p>With a 5-minute cache, the write costs 1.25×, giving a <strong>12.5×</strong> comparison.</p>
        <p>This is the cost of reloading the existing context, not the entire turn. The new message and generated reply still cost the same either way. For a large session, however, reloading the context can dominate the cost.</p>
        <h4>What we observed</h4>
        <p>Across one heavy Claude Code user's sessions over 30 days, cold reloads accounted for:</p>
        <ul>
          <li><strong>0.9% of total tokens</strong></li>
          <li><strong>Approximately 10% of estimated API cost</strong></li>
        </ul>
        <p>Your team's results will vary by model, cache duration, session size and usage patterns. L2cache measures your team's actual usage rather than assuming everyone experiences the same impact.</p>
      </div>
    </details>
  </section>

  <section class="section" id="features">
    <div class="section-head">
      <p class="eyebrow">What you'll get</p>
      <h2>For every developer, in the browser and the terminal.</h2>
      <p>The collector runs on each developer's machine. Session history and pickup cards open locally in the browser; the guard and handoffs work through the agent's own hooks.</p>
    </div>
{feature("pickup", "Pickup cards: know what continuing will cost before you type", TODAY, "Every recent session gets a card on the developer's machine: context size, whether the prompt cache is warm or expired, the cheapest path back in (compact vs. fresh start with handoff), and a recap of where you left off. Opens locally in your browser.")}
{feature("history", "Every agent session, searchable", TODAY, "Claude Code and Codex sessions grouped by project and day, with the conversation, tool calls, files changed and the commits they produced. Served locally in your browser; conversations never leave your machine.")}
{feature("guard", "Cold Resume Guard: stops the expensive message, once", TODAY, "On resume, you're told the cache expired and how much the next message would reload. It pauses that first message once and points to the cheaper path. Send again to continue anyway.", example=False)}
{feature("handoff", "/clear, and the agent already knows where you were", TODAY, "The new session starts empty and receives a short handoff: what's done, what's pending, the last exchange, and steps that may already be finished, so nothing is redone.", example=False)}
{feature("budget", "A nudge when a session gets heavy", TODAY, "Every request re-reads the whole context. You get a note in the terminal when a session crosses a heavy threshold, shown only to you and costing the model nothing, and once more before you walk away from a very heavy one.", example=False)}
{feature("skills", 'Team skills: share custom agent tools across the repo<span class="status planned-tag">Planned</span>', TODAY, "When an engineer builds a specialized skill or custom MCP tool—like a database migration validator, test data generator, or deployment helper—one click makes it available to every teammate's agent. No copy-pasting prompts in Slack.")}
{feature("memory", 'Team memory: “someone already fixed this”<span class="status planned-tag">Planned</span>', TODAY, "Before debugging, the agent asks whether the team solved this error before, and gets the cause, the fix, the files and the test that proved it. Fixes are shared only after the developer who made them approves.")}
  </section>

  <section class="section" id="proactive">
    <div class="section-head">
      <p class="eyebrow">Proactive session intelligence</p>
      <h2>Catches session problems before the developer notices.</h2>
      <p>The collector follows each session on the developer's machine while it runs. When it spots a problem, the suggested next step appears in the terminal, before the expensive or wasted turn.</p>
    </div>
    <div class="detect-wrap">
      <table class="detect">
        <thead><tr><th scope="col">When it detects</th><th scope="col">It suggests</th></tr></thead>
        <tbody>
          <tr><td>A big session is resumed after its cache expired</td><td>Start fresh with a handoff, or continue knowing what it costs</td></tr>
          <tr><td>The session's context crosses a heavy threshold</td><td>Compact, or /clear and continue from a handoff</td></tr>
          <tr><td>Unfinished work when a session is cleared or compacted</td><td>Write a handoff: done, pending and the last exchange</td></tr>
          <tr><td>An error the team already fixed appears again</td><td>Reuse the team's fix: cause, files and the test that proved it</td></tr>
          <tr><td>The session's goal has changed significantly<span class="status planned-tag">Planned</span></td><td>Start a fresh session for the new task</td></tr>
          <tr><td>The same files are investigated again and again<span class="status planned-tag">Planned</span></td><td>Bring back what earlier sessions found</td></tr>
          <tr><td>Context keeps growing with no edits or commits<span class="status planned-tag">Planned</span></td><td>Review the approach, or hand off</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="section-head">
      <p class="eyebrow">For the team lead and CTO</p>
      <h2>Updates without chasing. Costs without surprises.</h2>
      <p>The team view is built from numbers, commit SHAs and the recaps each developer approves. No prompts, no code, no conversation text.</p>
    </div>
{feature("shipped", "Know what your team worked on, without chasing", NEW, "Standup updates that write themselves. Each developer's day is grouped by feature, written by the agent that did the work, checked against the files that actually changed, and shared once the developer approves it. Work in progress, uncommitted changes and where someone got stuck are all there, so you stop asking for updates and developers stop writing them.")}
{feature("report", "Usage &amp; cold-restart report", NEW, "Sessions, tokens by type, cold restarts and what they reloaded, how many the guard prevented, and the sessions that cost the most. Filter by week, developer, repo or agent, and export CSV. Subscription seats show tokens and quota; API seats show estimated cost.")}
{feature("digest", "The weekly digest", NEW, "The report's headline numbers, what shipped and where people got stuck, posted to your team channel or sent by email every Monday.")}
{feature("outcomes", "Spend tied to outcomes", NEW, "Usage grouped by piece of work and linked to the commits it produced. Work that used a lot of tokens with no commit yet is easy to spot.")}
    <div class="planned">
      <h3>Also planned for leads<span class="status planned-tag">Planned</span></h3>
      <div class="problems">
        <div class="problem"><h3>Seat and plan advisor</h3><p>See who is on the wrong seat or plan for how they actually use agents: who is hitting limits on a standard seat, and who is paying for capacity they never use.</p></div>
        <div class="problem"><h3>Secret-leak alerts</h3><p>API keys or <code>.env</code> contents pasted into an agent session are detected on the developer's machine. The team sees an alert and which session, never the secret.</p></div>
        <div class="problem"><h3>Session recap on pull requests</h3><p>Each pull request gets a short recap of how it was built with the agent: what was tried, what was tested. Reviewers see the why, not just the diff.</p></div>
      </div>
      <p class="fineprint">Tell us in the form which of these would make you pay. It decides what we build first.</p>
    </div>
  </section>

  <section class="section" id="privacy">
    <div class="section-head">
      <p class="eyebrow">Private by design</p>
      <h2>Your conversations stay on your machine. You can check.</h2>
      <p>Transcripts are read and summarised locally. The team sees numbers and the recaps and fixes you approve. Every developer can see exactly what was sent and pause sharing at any time. No keystroke tracking, no productivity scores.</p>
    </div>
    <div class="boundary">
      <div><h3>Stays on each machine</h3><ul><li>Prompts and replies</li><li>Source code, diffs and terminal output</li><li>Full transcripts and session history</li></ul></div>
      <div><h3>What the team receives</h3><ul><li>Usage, cache and session numbers</li><li>Commit SHAs</li><li>Recaps and fixes the developer approves</li></ul></div>
    </div>
{feature("sharing", "You see what your team sees", NEW, "A sharing page in the local app lists what was uploaded and what never leaves your machine, with an approval step for every recap and fix.")}
  </section>

  <section class="section" id="how">
    <div class="section-head">
      <p class="eyebrow">How it works</p>
      <h2>Three steps, no change to how you work.</h2>
    </div>
    <ol class="steps">
      <li><h3>Install the collector</h3><p>One command on each developer's machine. It reads agent sessions locally and adds hooks to Claude Code and Codex.</p></li>
      <li><h3>Work as usual</h3><p>Pickup cards and session history open in your browser. The guard and handoffs work in the terminal.</p></li>
      <li><h3>See the team picture</h3><p>Spend, cold restarts, what shipped and the weekly digest, built from metadata and approved recaps.</p></li>
    </ol>
  </section>

  <section class="section" id="join">
    <div class="join">
      <div class="join-copy">
        <p class="eyebrow">Early access</p>
        <h2>Join the waitlist.</h2>
        <p>We're starting with a small number of teams. Tell us about yours and we'll be in touch when early access opens.</p>
        <ul>
          <li>Built for teams of 2–50 developers</li>
          <li>Claude Code and Codex first</li>
          <li>macOS first, Windows and Linux planned</li>
        </ul>
      </div>
      <div>
        <form id="waitlist-form" novalidate>
          <div>
            <label for="wl-email">Work email</label>
            <input id="wl-email" name="email" type="email" autocomplete="email" maxlength="254" required>
          </div>
          <div>
            <label for="wl-size">How many developers use coding agents?</label>
            <select id="wl-size" name="team_size" required>
              <option value="">Choose…</option>
              <option>1</option><option>2–5</option><option>6–15</option><option>16–50</option><option>50+</option>
            </select>
          </div>
          <details class="more">
          <summary>Tell us more about your team <span class="opt">(optional, helps us pick early teams)</span></summary>
          <div class="row2">
            <div><label for="wl-name">Name</label><input id="wl-name" name="name" type="text" autocomplete="name" maxlength="120"></div>
            <div><label for="wl-company">Company</label><input id="wl-company" name="company" type="text" autocomplete="organization" maxlength="120"></div>
          </div>
          <fieldset>
            <legend>What do they code on?</legend>
            <div class="checks">
              <label><input type="checkbox" name="os" value="macos">macOS</label>
              <label><input type="checkbox" name="os" value="windows">Windows</label>
              <label><input type="checkbox" name="os" value="wsl">Windows + WSL</label>
              <label><input type="checkbox" name="os" value="linux">Linux</label>
            </div>
          </fieldset>
          <fieldset>
            <legend>Which agents do they use?</legend>
            <div class="checks">
              <label><input type="checkbox" name="agents" value="claude-code">Claude Code</label>
              <label><input type="checkbox" name="agents" value="codex">Codex</label>
              <label><input type="checkbox" name="agents" value="cursor">Cursor</label>
              <label><input type="checkbox" name="agents" value="copilot">GitHub Copilot</label>
              <label><input type="checkbox" name="agents" value="gemini-cli">Gemini CLI</label>
              <label><input type="checkbox" name="agents" value="other">Other</label>
            </div>
          </fieldset>
          <fieldset>
            <legend>Which of these would make you pay?</legend>
            <div class="checks">
              <label><input type="checkbox" name="wanted" value="team-updates">Daily or weekly team updates (what everyone worked on)</label>
              <label><input type="checkbox" name="wanted" value="proactive-alerts">Proactive session alerts (goal drift, repeated work, stalls)</label>
              <label><input type="checkbox" name="wanted" value="usage-report">Usage &amp; cold-restart report</label>
              <label><input type="checkbox" name="wanted" value="seat-advisor">Seat and plan advisor</label>
              <label><input type="checkbox" name="wanted" value="quota-forecast">Quota and rate-limit forecast</label>
              <label><input type="checkbox" name="wanted" value="secret-alerts">Secret-leak alerts</label>
              <label><input type="checkbox" name="wanted" value="safety-inventory">Agent safety inventory (MCP servers, permissions)</label>
              <label><input type="checkbox" name="wanted" value="pr-recaps">Session recap on pull requests</label>
              <label><input type="checkbox" name="wanted" value="client-reports">Cost and time per client project</label>
              <label><input type="checkbox" name="wanted" value="team-memory">Team memory</label>
              <label><input type="checkbox" name="wanted" value="team-skills">Shareable team skills &amp; custom tools</label>
            </div>
          </fieldset>
          <div>
            <label for="wl-pain">What's the biggest pain with agents on your team?</label>
            <textarea id="wl-pain" name="pain" maxlength="500"></textarea>
          </div>
          </details>
          <div class="hp" aria-hidden="true">
            <label for="wl-website">Website</label>
            <input id="wl-website" name="website" type="text" tabindex="-1" autocomplete="off">
          </div>
          <label class="consent"><input type="checkbox" name="consent" required><span>Email me about early access. We use your details only for that and to plan the product. See the <a href="/privacy">privacy policy</a>.</span></label>
          <div><button class="btn btn-primary" type="submit">Join the waitlist</button></div>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>
        <div class="done" hidden tabindex="-1">
          <span class="tick" aria-hidden="true">✓</span>
          <h3>You're on the list.</h3>
          <p>We'll email you when early access opens. Reply to that email any time to tell us more about your team.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="faq">
    <div class="section-head"><p class="eyebrow">FAQ</p><h2>Questions teams ask.</h2></div>
    <div class="faq">
      <details><summary>Do you read our developers' conversations?</summary><p>No. The collector reads agent transcripts on each developer's own machine to work out session size, cache state and recaps. Prompts, replies, code and diffs are never uploaded. The team view receives numbers, commit SHAs, and the recaps and fixes each developer approves.</p></details>
      <details><summary>How does this relate to L2Cache?</summary><p>It's a separate product from the makers of L2Cache, the Mac app for developer memory. It covers agent sessions only: no clipboard, screenshots or snippets. Several of the developer features already run in the L2Cache Mac app, and the screenshots for them are from it; they're being rebuilt to run on every platform. The team features are being built new.</p></details>
      <details><summary>Which agents does it support?</summary><p>Claude Code and Codex first. Tell us in the form which other agents your team uses; that decides what comes next.</p></details>
      <details><summary>Does it work on Windows and Linux?</summary><p>The collector and the local web app are being built to run on macOS, Windows (including WSL) and Linux. macOS comes first.</p></details>
      <details><summary>Does it work with Claude subscriptions as well as API keys?</summary><p>Yes. Usage is read from the agent's own session files, so subscription seats are included. They're shown as tokens and quota; API-billed seats also get an estimated cost.</p></details>
      <details><summary>Can managers see individual developers?</summary><p>By default, admins see per-developer usage numbers, never conversations. A team setting switches the report to team totals only.</p></details>
      <details><summary>How much will it cost?</summary><p>Pricing will be per developer per month and announced before launch. Teams on the waitlist hear first.</p></details>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap footer-row">
    <a class="brand" href="/">{MARK}<span>Session Intelligence</span></a>
    <span class="spacer"></span>
    <span>From the makers of <a href="https://l2cache.app/">L2Cache</a></span>
    <a href="/privacy">Privacy</a>
    <a href="mailto:support@amvo.store">Contact</a>
    <span>All people, projects and numbers in the mockups are examples.</span>
  </div>
</footer>
</body>
</html>
'''
PRIVACY = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Privacy — Session Intelligence for Teams</title>
  <meta name="description" content="What the Session Intelligence for Teams waitlist collects, why, where it is stored and how to have it deleted.">
  <link rel="canonical" href="https://teams.amvo.store/privacy">
  <meta name="color-scheme" content="light">
  <link rel="icon" href="{FAVICON}">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="/">{MARK}<span>Session Intelligence <em>for Teams</em></span></a>
    <a class="btn btn-primary btn-small" href="/#join"><span>Join<span class="long"> the waitlist</span></span></a>
  </nav>
</header>
<main class="wrap legal">
  <h1>Privacy</h1>
  <p class="fineprint">Last updated 3 November 2026 · Session Intelligence for Teams is a working name for a product in development by Amvotech, the makers of L2Cache.</p>

  <h2>The waitlist</h2>
  <p>When you join the waitlist we store what you enter: your email, and optionally your name, company, team size, the operating systems and coding agents your team uses, and your comment. We also store where you came from (a referring site or campaign tag), your browser's user-agent string and the time you signed up.</p>
  <p>We use this only to contact you about early access and to plan the product. We don't sell or share it, and we don't add you to other mailing lists.</p>

  <h2>Where it is stored</h2>
  <p>Signups are stored in a database hosted by Supabase. The form sends them through a server function hosted by Vercel; the database is not reachable from the web page.</p>

  <h2>Analytics</h2>
  <p>This site uses Vercel Web Analytics to count page visits without cookies.</p>

  <h2>Deleting your details</h2>
  <p>Email <a href="mailto:support@amvo.store">support@amvo.store</a> from the address you signed up with and we'll delete your entry.</p>

  <h2>The product itself</h2>
  <p>This page covers the waitlist only. The product is designed so that agent conversations, code and diffs stay on each developer's machine; a full privacy policy for it will be published before launch.</p>
</main>
<footer class="site-footer">
  <div class="wrap footer-row">
    <a class="brand" href="/">{MARK}<span>Session Intelligence</span></a>
    <span class="spacer"></span>
    <span>From the makers of <a href="https://l2cache.app/">L2Cache</a></span>
    <a href="mailto:support@amvo.store">Contact</a>
  </div>
</footer>
</body>
</html>
'''

(root / "teams/index.html").write_text(page)
(root / "teams/privacy.html").write_text(PRIVACY.format(MARK=MARK, FAVICON=FAVICON))
print("written", len(page))
