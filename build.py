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

# Translations temporarily disabled. Serving English on all routes.
# with open("locales.json", "r", encoding="utf-8") as f:
#     TRANSLATIONS = json.load(f)

HTML_FILES = ["index.html", "support.html", "privacy.html", "intelligence.html", "changelog.html", "clipboard-history-mac.html", "mac-command-history.html", "comparison.html", "developer-clipboard.html", "custom-actions.html", "jwt-decoder-mac.html", "json-formatter-mac.html", "regex-clipboard-mac.html", "screenshot-ocr-mac.html", "sql-test-data-generator.html", "sitemap.html", "blog.html", "blog-regex-clipboard.html", "blog-sql-test-data.html", "blog-jwt-security.html", "blog-sqlite-fts5-hangs.html", "blog-swift-sqlite-concurrency.html", "blog-apple-intelligence-clipboard.html", "blog-developer-workflow-apple-intelligence.html", "blog-zero-cloud-mac-desktop-ai.html"]
OUT_DIR = "out"
L2CACHE_OUT_DIR = os.path.join(OUT_DIR, "l2cache")
AMVO_OUT_DIR = os.path.join(OUT_DIR, "amvo-store")

def get_language_switcher_html(current_lang):
    options = ""
    for code, name in LANGUAGES.items():
        selected = "selected" if code == current_lang else ""
        options += f'<option value="{code}" {selected}>{name}</option>'
    
    lang_codes = "|".join(LANGUAGES.keys())
    
    switcher = f"""
    <div class="lang-switcher" style="margin-left: 20px;">
        <select onchange="window.location.href = window.location.pathname.replace(/\\/({lang_codes})\\//, '/' + this.value + '/');" style="background: rgba(255,255,255,0.1); border: 1px solid var(--border); color: var(--text); padding: 4px 8px; border-radius: 6px; font-size: 13px; font-family: var(--sans);">
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
    for asset in ["icon.png", "screenshots", "theme.css"]:
        if os.path.exists(asset):
            if os.path.isdir(asset):
                shutil.copytree(asset, os.path.join(L2CACHE_OUT_DIR, asset))
            else:
                shutil.copy(asset, os.path.join(L2CACHE_OUT_DIR, asset))
                
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

            # Translation replacement removed temporarily (serving English only)
                    
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
            
            # Note: 
            # 1. We keep <html lang="en"> (no replacement) because content is English.
            # 2. We remove <meta name="google" content="notranslate"> so Chrome offers translation natively.
            # 3. We remove broken hreflang tags since all pages are now duplicate English.

            with open(os.path.join(lang_dir, file), "w", encoding="utf-8") as f:
                f.write(content)

    # Generate sitemap.xml
    sitemap_path = os.path.join(L2CACHE_OUT_DIR, "sitemap.xml")
    base_url = "https://l2cache.amvo.store"
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        # Translations are disabled, so submit only canonical English URLs.
        # Add localized URLs only when they contain translated content, have
        # self-referencing canonicals, and reciprocal hreflang annotations.
        for file in HTML_FILES:
            if not os.path.exists(file):
                continue
            clean_path = "" if file == "index.html" else file.removesuffix(".html")
            url_path = f"{base_url}/en/{clean_path}"
            f.write('  <url>\n')
            f.write(f'    <loc>{url_path}</loc>\n')
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
