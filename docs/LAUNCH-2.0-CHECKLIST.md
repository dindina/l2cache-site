# L2Cache 2.0 launch-day checklist (website)

**Status:** Waiting for the 2.0 App Store release (expected week of 2026-11-09).
**Already done:** the site runs on `l2cache.app` (main domain, `www` redirects to it). Old `l2cache.amvo.store` URLs permanently redirect to the same page on `l2cache.app` (live since the 2026-11-03 deploy; kept on by decision 2026-11-09). All C1–C6 content is live with "coming soon" labels.

Do these in order once 2.0 is live in the App Store.

## 1. Remove the pre-release labels (commit 87a5acd added them)
- [ ] Homepage `prototypes/native-mac/index.html`: the `prerelease-pill` above the headline, the `prerelease-note` under the download button, and "The App Store has version 1.4.6 today; 2.0 is coming soon." in the pricing fine print. The `.prerelease-*` rules in `styles.css` can go too.
- [ ] Seven articles: delete the `<div class="prerelease-box" …>` after the meta line, plus its CSS: `claude-code-cold-cache-resume-cost`, `coding-agent-session-handoff`, `coding-agent-memory-mcp-hooks`, `universal-search-mac-developer`, `project-story-git-timeline-mac`, `developer-timesheet-standup-from-activity`, `developer-morning-context-today`.
- [ ] `blog.html`: remove " · Coming in 2.0" from the seven blog tags.
- [ ] `day-in-the-life-mac-developer.html`: "Coming in L2Cache 2.0: the Today page shows…" → "L2Cache's Today page shows…", and "2.0 builds one" → "L2Cache builds one".
- [ ] `grep -rn "Coming in\|coming soon\|1\.4\.6" --include=*.html .` comes back clean (outside `out/`).

## 2. Tighten the redirects (one hop each) — done and deployed 2026-11-11
- [x] Old-host language homepages (`/de`, `/fr`, `/it`, `/es`, `/ja`, `/ko`, `/pt-BR`, `/vi`, `/zh-Hans`, `/zh-hans`, `/pt-br`, `/{lang}/index.html`) take 2–3 hops via `l2cache.app/{lang}`. Point them straight at `https://l2cache.app/` until translated homepages (W3) exist.
- [x] Old-host `/tools` goes `/en/tools/` → `/en/tools`. Add an explicit `/tools` → `https://l2cache.app/en/tools` rule before `/tools/:tool*`.
- [x] Leave `/{lang}/page.html` (2 hops through Vercel's clean-URL redirect); Google follows it.

## 3. Build, check, deploy
- [ ] `python3 build.py`, `python3 scripts/site_i18n.py extract`, `python3 scripts/site_i18n.py build --only-complete`
- [ ] `python3 scripts/check_home_links.py`, `python3 validate_seo.py`
- [ ] `npx vercel deploy --prod --yes`
- [ ] Re-run the 204-row inventory check against production (every row: one 308, the expected destination, a 200 at the end).

## 4. Tell search engines
- [ ] Google Search Console: submit `https://l2cache.app/sitemap.xml` on the `l2cache.app` property; run **Change of address** from the old property if it's offered. Keep the old sitemap submitted for about 4 weeks.
- [ ] Bing Webmaster Tools: verify `l2cache.app`, use **Site Move** from `l2cache.amvo.store`, and submit the new sitemap.
- [ ] `python3 submit_indexnow.py` for the 8 new articles and `/en/blog`.

## 5. Links you control
- [ ] App Store Connect: marketing, support and privacy URLs → `l2cache.app` (all locales).
- [ ] GitHub, dev.to and Medium profile and article links.
- [ ] The 9 `l2cache.amvo.store` links in the app (W5-T504) go out with the next app build if they didn't make 2.0.

## 6. Monitor (4 weeks, Sprint W6)
- [ ] Weekly: indexed pages, 404s, Google-selected canonical, impressions for `protect` pages vs the W1 baseline. Fix Search Console script access first (`fetch_gsc_stats.py` returned 403).
- [ ] If a `protect` page loses more than 50% of its impressions after 3 weeks, investigate before changing anything else.
- [ ] Never remove the old-domain redirects: installed copies of the app link to `l2cache.amvo.store`.

## 7. Housekeeping (after launch has settled)
- [ ] Move the homepage source out of `prototypes/native-mac/` (it's the live 2.0 homepage, not a prototype) to a folder such as `home/`. Update the path in `build.py`, `scripts/site_i18n.py` (`SOURCE_DIR`), `scripts/check_home_links.py`, this checklist and `docs/PRD-Teams-Waitlist.md`. Then `python3 build.py` and `python3 scripts/check_home_links.py` must pass, and `out/l2cache/index.html` must be unchanged apart from the move. Deferred from 2026-11-10 to keep launch-week builds stable.
