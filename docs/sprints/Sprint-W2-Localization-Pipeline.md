# Sprint W2 — Localization Pipeline

**Status:** Done (2026-10-26) — translations are W3; deploy wiring is W4
**Goal:** Build the 2.0 homepage per locale from keyed strings, with the whole `<head>` localized and a build that fails on leftover English.
**Depends on:** W1 (launch locales, canonical host).
**Scope:** `tools/site_i18n.py` (new), `locales/l2cache/<lang>/home.json` (new), `locales/l2cache/keep.json` (new), `prototypes/native-mac/styles.css`. Legacy pages and the old `locales.json` find-and-replace stay as they are until W4.

**Design change (2026-10-26):** instead of rewriting the prototype into a `{{key}}` template, the English HTML stays the source and **the English text of each segment is its key** (like the app's `.xcstrings`). A segment is the inner HTML of the outermost text element containing only text and inline tags, so `<kbd>`, `<code>` and `<strong>` stay inside their sentence. Editing English copy makes that segment "missing" in every locale until it is translated again.

```
python3 tools/site_i18n.py extract   # locales/l2cache/en/home.json (186 strings)
python3 tools/site_i18n.py check     # all locales complete, tags preserved, nothing left in English
python3 tools/site_i18n.py build     # out/home/: / and /<lang>; refuses to build if check fails
```

---

## Tasks

### T-W201 — Template the 2.0 homepage ✅ (English-as-key, see above)
- Replace every user-visible string in `prototypes/native-mac/index.html` with a key (`{{hero.title}}`), including `<title>`, meta description, `og:*`, `twitter:*`, image `alt`, and the FAQ / SoftwareApplication JSON-LD text.
- English values go to `locales/l2cache/en/home.json`. The English render must be byte-identical to today's page apart from whitespace (diff check).

### T-W202 — Per-locale render ✅ (`site_i18n.render`)
- Render one page per launch locale: English at `/`, others at `/{lang}`.
- Per locale: `<html lang>`, self-referencing canonical and `og:url`, `og:locale` + `og:locale:alternate`, JSON-LD strings and `inLanguage`, App Store country link (ru added), home link `/<lang>`, root-relative assets.
- Regional price: not needed — the `Offer` is a free download (`price: 0`).
- Host comes from `SITE_URL` only; nothing hardcodes a domain.

### T-W203 — hreflang ✅ in the page head (sitemap alternates move to W4 with the build integration)
- Reciprocal alternates across the launch locales only; `x-default` and `en` → `/`.
- Same alternates in `sitemap.xml` (`xhtml:link`).
- A locale missing any key gets no page and no alternate.

### T-W204 — Crawlable language switcher ✅ footer links, `aria-current` on the active language
- Replace the `<select onchange>` with plain `<a href hreflang lang>` links to the same page in each language (falling back to that language's homepage).

### T-W205 — Validation gates ✅ in `site_i18n.py check` (tested: missing key, dropped `<kbd>`, untranslated English; brand names allowed via `keep.json`)
- Fail on: a missing key; any English sentence of 25+ characters in a non-English page (excluding product names and code); unresolved `[[...]]` placeholders; non-reciprocal hreflang; a canonical that isn't self-referencing.
- Run the gates in `deploy.sh` without `|| true` → **W4**, when the homepage build joins the deploy (until then a failing check would block unrelated deploys).
- Known gap: `script.js` builds the gallery dot label `"Screenshot N: …"` in English; translate it in W3 via a `data-` attribute on the dialog.

---

## Done when
- `python3 build.py` produces `/` and `/{lang}` for the 2.0 homepage from keys, with an English page identical to the prototype.
- `validate_seo.py` fails on a deliberately removed key and on a pasted English sentence, and passes otherwise.
