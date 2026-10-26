# Sprint W3 — Translations & Localized Assets

**Status:** Planned (2026-10-26)
**Goal:** The 2.0 homepage fully translated into every launch locale, written around the terms people actually search for.
**Depends on:** W2 (keyed homepage, validation gates).
**Scope:** `locales/l2cache/<lang>/home.json`, localized images in `prototypes/native-mac/img/`.

---

## Tasks

### T-W301 — Glossary
- Build `locales/l2cache/glossary.json` from the app's `Localizable.xcstrings` (Developer Home, Worklog, Coding Agents, Clipboard, Pick up where you left off…), so site and app use the same terms.
- Reuse the App Store screenshot copy (`L2Cache/screenshots/l2cache2.0/frames/copy.json`) where the messages match.

### T-W302 — Native keywords for title, H1 and description
- Per market, find the searched term for the core intents: clipboard history Mac, developer memory, resume coding-agent session, terminal history Mac.
- Priority markets first: ja, de, fr, zh-Hans. Write `<title>`, meta description and H1 around those terms instead of translating the English headline literally.

### T-W303 — Translate the homepage
- Fill `home.json` for de, es, fr, it, ja, ko, pt-BR, ru, vi, zh-Hans, FAQ and alt text included.
- Title ≤ 60 characters and description ≤ 155 characters per locale (CJK measured in display width).

### T-W304 — Localized visuals
- Where an image contains English marketing text, use the localized App Store frames; app UI captures stay English (same decision as the App Store set).
- WebP, same file-size budget as `ce18fab`.

### T-W305 — Render check and native review
- Render every locale and check for overflow, bad line breaks (the ja/zh/ko issues fixed in the App Store frames) and font fallback.
- You (or a native speaker) review at least ja, de, zh-Hans before launch.

---

## Done when
- All 11 locales build with `validate_seo.py` passing — no leftover English, no missing keys.
- Every locale checked visually; native review notes resolved.
