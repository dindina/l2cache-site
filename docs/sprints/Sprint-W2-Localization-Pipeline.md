# Sprint W2 — Localization Pipeline

**Status:** Planned (2026-10-26)
**Goal:** Build the 2.0 homepage per locale from keyed strings, with the whole `<head>` localized and a build that fails on leftover English.
**Depends on:** W1 (launch locales, canonical host).
**Scope:** `prototypes/native-mac/` → template, `locales/l2cache/<lang>/home.json` (new), `build.py`, `validate_seo.py`. Legacy pages and the old `locales.json` find-and-replace stay as they are until W4.

---

## Tasks

### T-W201 — Template the 2.0 homepage
- Replace every user-visible string in `prototypes/native-mac/index.html` with a key (`{{hero.title}}`), including `<title>`, meta description, `og:*`, `twitter:*`, image `alt`, and the FAQ / SoftwareApplication JSON-LD text.
- English values go to `locales/l2cache/en/home.json`. The English render must be byte-identical to today's page apart from whitespace (diff check).

### T-W202 — Per-locale render in `build.py`
- Render one page per launch locale: English at `/`, others at `/{lang}`.
- Per locale: `<html lang>`, self-referencing canonical, `og:locale` + `og:locale:alternate`, JSON-LD `inLanguage`, App Store country link (existing `APP_STORE_COUNTRIES`), and regional price in the `Offer` (existing `REGIONAL_PRICING`).
- Host comes from `SITE_URL` only; nothing hardcodes a domain.

### T-W203 — hreflang
- Reciprocal alternates across the launch locales only; `x-default` and `en` → `/`.
- Same alternates in `sitemap.xml` (`xhtml:link`).
- A locale missing any key gets no page and no alternate.

### T-W204 — Crawlable language switcher
- Replace the `<select onchange>` with plain `<a href hreflang lang>` links to the same page in each language (falling back to that language's homepage).

### T-W205 — Validation gates in `validate_seo.py`
- Fail on: a missing key; any English sentence of 25+ characters in a non-English page (excluding product names and code); unresolved `[[...]]` placeholders; non-reciprocal hreflang; a canonical that isn't self-referencing.
- Run the gates in `deploy.sh` without `|| true`.

---

## Done when
- `python3 build.py` produces `/` and `/{lang}` for the 2.0 homepage from keys, with an English page identical to the prototype.
- `validate_seo.py` fails on a deliberately removed key and on a pasted English sentence, and passes otherwise.
