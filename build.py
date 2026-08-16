import os
import re
import json
import shutil

LANGUAGES = {
    "en": "English",
    "zh-Hans": "Chinese (Simplified)",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "pt-BR": "Portuguese (Brazil)",
    "es": "Spanish",
    "vi": "Vietnamese"
}

APP_STORE_COUNTRIES = {
    "en": "us",
    "zh-Hans": "cn",
    "fr": "fr",
    "de": "de",
    "it": "it",
    "ja": "jp",
    "ko": "kr",
    "pt-BR": "br",
    "es": "es",
    "vi": "vn"
}

with open("locales.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

HTML_FILES = ["index.html", "support.html", "privacy.html", "intelligence.html", "changelog.html", "clipboard-history-mac.html", "mac-command-history.html", "comparison.html", "benchmark.html", "best-mac-clipboard-managers.html", "clipboard-privacy-report.html", "developer-clipboard.html", "custom-actions.html", "jwt-decoder-mac.html", "json-formatter-mac.html", "regex-clipboard-mac.html", "screenshot-ocr-mac.html", "sql-test-data-generator.html", "sitemap.html", "blog.html", "blog-clipboard-automation-developer-workflows.html", "blog-regex-clipboard.html", "blog-sql-test-data.html", "blog-jwt-security.html", "blog-sqlite-fts5-hangs.html", "blog-swift-sqlite-concurrency.html", "blog-apple-intelligence-clipboard.html", "blog-developer-workflow-apple-intelligence.html", "blog-zero-cloud-mac-desktop-ai.html"]
OUT_DIR = "out"
L2CACHE_OUT_DIR = os.path.join(OUT_DIR, "l2cache")
AMVO_OUT_DIR = os.path.join(OUT_DIR, "amvo-store")

# Clean, canonical site path for a source file (matches the deployed '/lang/...' slug).
def build_page_clean_path(file):
    # index.html is the site root -> '/en' (no trailing slash; Vercel stores it
    # that way and it's the URL Google indexes). Everything else keeps its slug.
    return "" if file == "index.html" else file.removesuffix(".html")


def localized_page(lang, file):
    """Absolute canonical URL for a page in a given locale."""
    clean = build_page_clean_path(file)
    if file == "index.html":
        return f"https://l2cache.amvo.store/{lang}"
    return f"https://l2cache.amvo.store/{lang}/{clean}"


def hreflang_tags(file):
    """Alternate-locale <link> block for a page across all LANGUAGES.
    Self-referencing entry included so each page fully maps its locale set.
    x-default points at English. Returns '' when the list would be empty."""
    alts = []
    for code in LANGUAGES.keys():
        alts.append(
            '    <link rel="alternate" hreflang="{}" href="{}" />'.format(
                code, localized_page(code, file)
            )
        )
    if not alts:
        return ""
    alts.append(
        '    <link rel="alternate" hreflang="x-default" href="{}" />'.format(
            localized_page("en", file)
        )
    )
    return "\n" + "\n".join(alts)


def rewrite_canonical(html, lang, file):
    """Replace the hardcoded /en/ canonical with a self-referencing one for the
    current locale, and append hreflang alternates right after it. Why this
    matters: templates ship a single /en/ canonical; without rewriting, all
    localized pages self-declare themselves duplicates of English (the GSC
    'Duplicate without user-selected canonical' error). This gives each locale
    its own canonical + reciprocal hreflang."""
    canonical = localized_page(lang, file)
    block = "  <link rel=\"canonical\" href=\"{}\" />{}".format(
        canonical, hreflang_tags(file)
    )
    # Match the existing canonical tag regardless of trailing slash / quote style.
    html, _ = re.subn(
        r'\s*<link\s+rel="canonical"[^>]*/?>',
        lambda m: block,
        html,
        count=1,
    )
    # Keep og:url / twitter:url in sync with the locale canonical (they are
    # hardcoded to the /en/ URL in the source templates).
    html = re.sub(
        r'(<meta\s+property=\"og:url\"\s+content=\")[^\"]*(\".*?/?>)',
        lambda m: f'{m.group(1)}{canonical}{m.group(2)}',
        html,
        count=1,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r'(<meta\s+name=\"twitter:url\"\s+content=\")[^\"]*(\".*?/?>)',
        lambda m: f'{m.group(1)}{canonical}{m.group(2)}',
        html,
        count=1,
        flags=re.IGNORECASE,
    )
    return html


def get_language_switcher_html(current_lang):
    options = ""
    for code, name in LANGUAGES.items():
        selected = "selected" if code == current_lang else ""
        options += f'<option value="{code}" {selected}>{name}</option>'
    
    lang_codes_js = str(list(LANGUAGES.keys()))
    
    switcher = f"""
    <div class="lang-switcher" style="margin-left: 20px;">
        <select onchange="let p=window.location.pathname.split('/').filter(Boolean); if({lang_codes_js}.includes(p[0])){{p[0]=this.value;}}else{{p.unshift(this.value);}} window.location.href='/' + p.join('/') + (p.length===1 ? '/' : '');" style="background: rgba(255,255,255,0.1); border: 1px solid var(--border); color: var(--text); padding: 4px 8px; border-radius: 6px; font-size: 13px; font-family: var(--sans);">
            {options}
        </select>
    </div>
    """
    return switcher

def fix_links(html_content, lang):
    """Prefix local links with /lang/ and use Vercel's canonical clean URLs."""
    for file in HTML_FILES:
        # Avoid double replacing or replacing external links
        clean_path = "" if file == "index.html" else file.removesuffix(".html")
        html_content = re.sub(
            f'href="{file}(#[^"]*)?"',
            f'href="/{lang}/{clean_path}\\1"',
            html_content,
        )
    return html_content

def build():
    import subprocess
    import glob
    print("Generating competitor comparisons...")
    subprocess.run(["python3", "generate_comparisons.py"])
    
    # Dynamically include generated comparison pages
    for comp_file in glob.glob("l2cache-vs-*.html"):
        if comp_file not in HTML_FILES:
            HTML_FILES.append(comp_file)

    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)
    os.makedirs(L2CACHE_OUT_DIR)

    # Copy L2Cache assets
    for asset in ["icon.png", "screenshots", "theme.css", "tools", "benchmark_dataset_2026.csv"]:
        if os.path.exists(asset):
            if os.path.isdir(asset):
                shutil.copytree(asset, os.path.join(L2CACHE_OUT_DIR, asset))
            else:
                shutil.copy(asset, os.path.join(L2CACHE_OUT_DIR, asset))

    # Also copy tools into en/tools
    if os.path.exists("tools"):
        shutil.copytree("tools", os.path.join(L2CACHE_OUT_DIR, "en", "tools"))
                
    # Copy amvo-store
    if os.path.exists("amvo-store"):
        shutil.copytree("amvo-store", AMVO_OUT_DIR)

    for lang in LANGUAGES.keys():
        lang_dir = os.path.join(L2CACHE_OUT_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        print(f"Building for {lang}...")
        
        for file in HTML_FILES:
            if not os.path.exists(file):
                continue
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()

            # Translate content
            if lang != "en" and lang in TRANSLATIONS:
                sorted_keys = sorted(TRANSLATIONS[lang].keys(), key=len, reverse=True)
                for en_str in sorted_keys:
                    loc_str = TRANSLATIONS[lang][en_str]
                    content = content.replace(en_str, loc_str)
                    
            # Localize screenshots if available
            if lang != "en":
                def replace_screenshot(match):
                    base = match.group(1)
                    ext = match.group(2)
                    loc_name = f"{base}-{lang}.html{ext}"
                    if os.path.exists(os.path.join("screenshots", loc_name)):
                        return f'screenshots/{loc_name}'
                    return match.group(0)
                content = re.sub(r'screenshots/([^"/]+)(\.png)', replace_screenshot, content)

            # Localize App Store links
            if lang != "en":
                country_code = APP_STORE_COUNTRIES.get(lang, "us")
                if country_code != "us":
                    content = content.replace('apps.apple.com/us/', f'apps.apple.com/{country_code}/')

            # Inject language switcher into nav and footer (skip for untranslated files)
            if file not in ["clipboard-history-mac.html", "mac-command-history.html"]:
                switcher_html = get_language_switcher_html(lang)
                if '</nav>' in content:
                    content = content.replace('</nav>', f'{switcher_html}\n</nav>')
                if '</footer>' in content:
                    content = content.replace('</footer>', f'{switcher_html}\n</footer>')

            # Adjust link prefixes
            content = fix_links(content, lang)

            # Fix asset paths to be relative from the lang directory (works locally and on Vercel)
            content = re.sub(r'(src|href)="icon\.png"', r'\1="../icon.png"', content)
            content = re.sub(r'(src|href)="screenshots/', r'\1="../screenshots/', content)
            content = content.replace('href="theme.css"', 'href="../theme.css"')
            
            # Update html lang attribute
            if lang != "en":
                content = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', content)

            # SEO: self-referencing canonical for THIS locale + reciprocal hreflang.
            # Prevents GSC 'Duplicate without user-selected canonical' for localized pages.
            content = rewrite_canonical(content, lang, file)

            with open(os.path.join(lang_dir, file), "w", encoding="utf-8") as f:
                f.write(content)

    # Generate sitemap.xml (canonical URLs + reciprocal hreflang alternates for
    # every locale, so Google treats localized pages as translations, not dupes).
    sitemap_path = os.path.join(L2CACHE_OUT_DIR, "sitemap.xml")
    base_url = "https://l2cache.amvo.store"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n')
        f.write('          xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
        for file in HTML_FILES:
            if not os.path.exists(file):
                continue
            clean = build_page_clean_path(file)
            f.write('  <url>\n')
            f.write(f'    <loc>{localized_page("en", file)}</loc>\n')
            # xhtml:link alternates for all locales (incl. self + x-default)
            for code in LANGUAGES.keys():
                f.write(f'    <xhtml:link rel="alternate" hreflang="{code}" '
                        f'href="{localized_page(code, file)}" />\n')
            f.write(f'    <xhtml:link rel="alternate" hreflang="x-default" '
                    f'href="{localized_page("en", file)}" />\n')
            f.write('  </url>\n')
            
        # Add Tools to Sitemap
        if os.path.exists("tools"):
            tool_files = [f for f in sorted(os.listdir("tools")) if f.endswith('.html')]
            for tf in tool_files:
                clean_tf = "" if tf == "index.html" else f"/{tf.removesuffix('.html')}"
                f.write('  <url>\n')
                f.write(f'    <loc>{base_url}/en/tools{clean_tf}</loc>\n')
                f.write('  </url>\n')
                
        f.write('</urlset>\n')

    # Generate robots.txt
    robots_path = os.path.join(L2CACHE_OUT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write("User-agent: *\n")
        f.write("Allow: /\n\n")
        f.write(f"Sitemap: {base_url}/sitemap.xml\n")

    # We let Vercel handle the root redirect to /en/ so it doesn't conflict with amvo.store routing

if __name__ == "__main__":
    build()
    print("Build complete.")
