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

# Core dictionary mapping English strings to their translations in various languages.
with open("locales.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

HTML_FILES = ["index.html", "support.html", "privacy.html", "intelligence.html", "changelog.html"]
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
        <select onchange="window.location.href = '/' + this.value + window.location.pathname.replace(/^\\/({lang_codes})(\\/|$)/, '/');" style="background: rgba(255,255,255,0.1); border: 1px solid var(--border); color: var(--text); padding: 4px 8px; border-radius: 6px; font-size: 13px; font-family: var(--sans);">
            {options}
        </select>
    </div>
    """
    return switcher

def fix_links(html_content, lang):
    """ Prefix local links with /lang/ to maintain language context """
    for file in HTML_FILES:
        # Avoid double replacing or replacing external links
        html_content = re.sub(f'href="{file}(#[^"]*)?"', f'href="/{lang}/{file}\\1"', html_content)
    return html_content

def build():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)
    os.makedirs(L2CACHE_OUT_DIR)

    # Copy L2Cache assets
    for asset in ["icon.png", "screenshots"]:
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

            # Replace strings
            if lang != "en" and lang in TRANSLATIONS:
                # Sort keys by length descending to avoid partial replacements breaking longer strings
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

            # Inject language switcher into nav and footer
            switcher_html = get_language_switcher_html(lang)
            if '</nav>' in content:
                content = content.replace('</nav>', f'{switcher_html}\n</nav>')
            if '</footer>' in content:
                content = content.replace('</footer>', f'{switcher_html}\n</footer>')

            # Adjust link prefixes
            content = fix_links(content, lang)

            # Fix asset paths to be absolute from the root
            content = re.sub(r'(src|href)="icon\.png"', r'\1="/icon.png"', content)
            content = re.sub(r'(src|href)="screenshots/', r'\1="/screenshots/', content)
            
            # Update html lang attribute and prevent auto-translation
            content = re.sub(r'<html lang="en">', f'<html lang="{lang}" translate="no" class="notranslate">', content)
            
            # Add google notranslate meta tag for extra safety
            if '<head>' in content:
                content = content.replace('<head>', '<head>\n  <meta name="google" content="notranslate" />')

            with open(os.path.join(lang_dir, file), "w", encoding="utf-8") as f:
                f.write(content)

    # We let Vercel handle the root redirect to /en/ so it doesn't conflict with amvo.store routing

    # Copy vercel.json if exists to out dir? No, vercel.json should be at root.

if __name__ == "__main__":
    build()
    print("Build complete.")
