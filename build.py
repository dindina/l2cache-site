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


REGIONAL_PRICING = {
    "en": {"price": "$4.99", "raw_price": "4.99", "currency": "USD", "tag": "$4.99 one-time purchase · Pay once, own forever · All updates included", "type": "one-time purchase · lifetime access · all future updates included", "privacy": "$4.99", "privacy_sub": "one-time purchase<br>pay once, own forever"},
    "zh-Hans": {"price": "¥38", "raw_price": "38", "currency": "CNY", "tag": "¥38 一次性购买 · 终身使用 · 包含后续所有更新", "type": "一次性购买 · 终身使用 · 包含后续所有更新", "privacy": "¥38", "privacy_sub": "一次性购买<br>终身使用"},
    "fr": {"price": "4,99 €", "raw_price": "4.99", "currency": "EUR", "tag": "4,99 € achat unique · payez une fois, possédez pour toujours · toutes mises à jour incluses", "type": "achat unique · accès à vie · toutes les mises à jour incluses", "privacy": "4,99 €", "privacy_sub": "achat unique<br>accès à vie"},
    "de": {"price": "4,99 €", "raw_price": "4.99", "currency": "EUR", "tag": "4,99 € Einmalkauf · Einmal zahlen, für immer nutzen · Alle Updates inklusive", "type": "Einmalkauf · lebenslanger Zugriff · alle Updates inklusive", "privacy": "4,99 €", "privacy_sub": "Einmalkauf<br>lebenslanger Zugriff"},
    "it": {"price": "4,99 €", "raw_price": "4.99", "currency": "EUR", "tag": "4,99 € acquisto una tantum · paga una volta, possiedi per sempre · tutti gli aggiornamenti inclusi", "type": "acquisto una tantum · accesso a vita · tutti gli aggiornamenti inclusi", "privacy": "4,99 €", "privacy_sub": "acquisto una tantum<br>accesso a vita"},
    "ja": {"price": "¥800", "raw_price": "800", "currency": "JPY", "tag": "¥800 買い切り · 一度のお支払いで永久利用 · すべての更新を含む", "type": "買い切り · 永久ライセンス · すべてのアップデートを含む", "privacy": "¥800", "privacy_sub": "買い切り<br>永久ライセンス"},
    "ko": {"price": "₩6,600", "raw_price": "6600", "currency": "KRW", "tag": "₩6,600 1회 결제 · 평생 소장 · 모든 업데이트 포함", "type": "1회 결제 · 평생 이용 · 모든 업데이트 포함", "privacy": "₩6,600", "privacy_sub": "1회 결제<br>평생 소장"},
    "pt-BR": {"price": "R$ 19,90", "raw_price": "19.90", "currency": "BRL", "tag": "R$ 19,90 pagamento único · pague uma vez, tenha para sempre · todas as atualizações inclusas", "type": "pagamento único · acesso vitalício · todas as atualizações inclusas", "privacy": "R$ 19,90", "privacy_sub": "pagamento único<br>acesso vitalício"},
    "es": {"price": "4,99 €", "raw_price": "4.99", "currency": "EUR", "tag": "4,99 € pago único · paga una vez, tuyo para siempre · todas las actualizaciones incluidas", "type": "pago único · acceso de por vida · todas las actualizaciones incluidas", "privacy": "4,99 €", "privacy_sub": "pago único<br>acceso de por vida"},
    "vi": {"price": "99.000 ₫", "raw_price": "99000", "currency": "VND", "tag": "99.000 ₫ mua một lần · sở hữu vĩnh viễn · bao gồm tất cả bản cập nhật", "type": "mua một lần · sở hữu vĩnh viễn · bao gồm tất cả cập nhật", "privacy": "99.000 ₫", "privacy_sub": "mua một lần<br>sở hữu vĩnh viễn"}
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

HTML_FILES = ["blog-screenshot-ocr-search.html", "blog-agent-history-analytics.html", "index.html", "support.html", "privacy.html", "intelligence.html", "changelog.html", "clipboard-history-mac.html", "mac-command-history.html", "comparison.html", "benchmark.html", "best-mac-clipboard-managers.html", "clipboard-privacy-report.html", "developer-clipboard.html", "custom-actions.html", "jwt-decoder-mac.html", "json-formatter-mac.html", "regex-clipboard-mac.html", "screenshot-ocr-mac.html", "sql-test-data-generator.html", "sitemap.html", "blog.html", "blog-clipboard-automation-developer-workflows.html", "blog-regex-clipboard.html", "blog-sql-test-data.html", "blog-jwt-security.html", "blog-sqlite-fts5-hangs.html", "blog-swift-sqlite-concurrency.html", "blog-apple-intelligence-clipboard.html", "blog-developer-workflow-apple-intelligence.html", "blog-zero-cloud-mac-desktop-ai.html"]
OUT_DIR = "out"
L2CACHE_OUT_DIR = os.path.join(OUT_DIR, "l2cache")
AMVO_OUT_DIR = os.path.join(OUT_DIR, "amvo-store")
VERCEL_ANALYTICS_TAG = '<script defer src="/_vercel/insights/script.js"></script>'


def inject_vercel_analytics(root_dir):
    """Add Vercel Web Analytics once to every generated L2Cache HTML page."""
    for current_dir, _, files in os.walk(root_dir):
        for filename in files:
            if not filename.endswith(".html"):
                continue

            path = os.path.join(current_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            if VERCEL_ANALYTICS_TAG in content:
                continue
            if "</head>" not in content:
                print(f"Warning: analytics not injected; missing </head>: {path}")
                continue

            content = content.replace(
                "</head>", f"  {VERCEL_ANALYTICS_TAG}\n</head>", 1
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

LOCALIZED_FILES = ["index.html"]

def build_page_clean_path(file):
    # index.html is the site root -> '/en' (no trailing slash; Vercel stores it
    # that way and it's the URL Google indexes). Everything else keeps its slug.
    return "" if file == "index.html" else file.removesuffix(".html")


def localized_page(lang, file):
    """Absolute canonical URL for a page in a given locale."""
    clean = build_page_clean_path(file)
    if file == "index.html":
        return f"https://l2cache.amvo.store/{lang}"
    return f"https://l2cache.amvo.store/en/{clean}" if file not in LOCALIZED_FILES else f"https://l2cache.amvo.store/{lang}/{clean}"


def hreflang_tags(file):
    """Alternate-locale <link> block for a page across all LANGUAGES.
    Only emitted for pages that are genuinely translated into all LANGUAGES.
    Untranslated English pages return '' to prevent hreflang mismatch errors."""
    if file not in LOCALIZED_FILES:
        return ""
    alts = []
    for code in LANGUAGES.keys():
        alts.append(
            '    <link rel="alternate" hreflang="{}" href="{}" />'.format(
                code, localized_page(code, file)
            )
        )
    alts.append(
        '    <link rel="alternate" hreflang="x-default" href="{}" />'.format(
            localized_page("en", file)
        )
    )
    return "\n" + "\n".join(alts)


def rewrite_canonical(html, lang, file):
    """Replace the hardcoded canonical with the proper canonical.
    For localized pages: self-referencing canonical for current locale + hreflang tags.
    For English-only pages: canonical pointing to /en/ without hreflang tags."""
    canonical = localized_page(lang, file) if file in LOCALIZED_FILES else localized_page("en", file)
    alts = hreflang_tags(file)
    block = f"  <link rel=\"canonical\" href=\"{canonical}\" />{alts}"
    # Match the existing canonical tag regardless of trailing slash / quote style.
    html, _ = re.subn(
        r'\s*<link\s+rel="canonical"[^>]*/?>',
        lambda m: block,
        html,
        count=1,
    )
    # Keep og:url / twitter:url in sync with the canonical
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
    """Prefix local links with /lang/ for localized files, and /en/ for English-only files."""
    for file in HTML_FILES:
        # Avoid double replacing or replacing external links
        clean_path = "" if file == "index.html" else file.removesuffix(".html")
        dest_lang = lang if file in LOCALIZED_FILES else "en"
        html_content = re.sub(
            f'href="{file}(#[^"]*)?"',
            f'href="/{dest_lang}/{clean_path}\\1"',
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
    for asset in ["icon.png", "screenshots", "theme.css", "tools", "benchmark_dataset_2026.csv", "llms.txt", "llms-full.txt"]:
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
        
        # Copy llms.txt and llms-full.txt to localized subpaths
        for llm_file in ["llms.txt", "llms-full.txt"]:
            if os.path.exists(llm_file):
                shutil.copy(llm_file, os.path.join(lang_dir, llm_file))
        
        # Only build translated pages for non-en locales (index.html)
        target_files = HTML_FILES if lang == "en" else LOCALIZED_FILES

        for file in target_files:
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

            # Localize pricing for specific region
            if lang in REGIONAL_PRICING:
                rp = REGIONAL_PRICING[lang]
                content = content.replace('<div class="pricing-amount">$4.99</div>', f'<div class="pricing-amount">{rp["price"]}</div>')
                content = content.replace('<div class="pricing-type">one-time purchase · lifetime access · all future updates included</div>', f'<div class="pricing-type">{rp["type"]}</div>')
                content = content.replace('<p class="price-tag">$4.99 one-time purchase · Pay once, own forever · All updates included</p>', f'<p class="price-tag">{rp["tag"]}</p>')
                content = content.replace('<div class="privacy-stat-value">$4.99</div>', f'<div class="privacy-stat-value">{rp["privacy"]}</div>')
                content = content.replace('<div class="privacy-stat-label">one-time purchase<br>pay once, own forever</div>', f'<div class="privacy-stat-label">{rp["privacy_sub"]}</div>')
                content = content.replace('"$4.99 one-time purchase (Lifetime access)"', f'"{rp["price"]} one-time purchase (Lifetime access)"')
                content = content.replace('"price": "4.99"', f'"price": "{rp["raw_price"]}"')
                content = content.replace('"priceCurrency": "USD"', f'"priceCurrency": "{rp["currency"]}"')

            # Localize App Store links
            if lang != "en":
                country_code = APP_STORE_COUNTRIES.get(lang, "us")
                if country_code != "us":
                    content = content.replace('apps.apple.com/us/', f'apps.apple.com/{country_code}/')

            # Inject language switcher into nav and footer (only for localized files)
            if file in LOCALIZED_FILES:
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
            content = rewrite_canonical(content, lang, file)

            with open(os.path.join(lang_dir, file), "w", encoding="utf-8") as f:
                f.write(content)

    # Generate sitemap.xml
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
            if file == "index.html":
                changefreq = "daily"
                priority = "1.0"
            elif file in ["intelligence.html", "clipboard-history-mac.html", "mac-command-history.html", "custom-actions.html", "developer-clipboard.html", "benchmark.html", "clipboard-privacy-report.html", "changelog.html"]:
                changefreq = "weekly"
                priority = "0.9"
            elif file.startswith("blog") or file.startswith("l2cache-vs-") or file == "best-mac-clipboard-managers.html":
                changefreq = "weekly"
                priority = "0.8"
            else:
                changefreq = "monthly"
                priority = "0.7"

            f.write('  <url>\n')
            f.write(f'    <loc>{localized_page("en", file)}</loc>\n')
            f.write(f'    <changefreq>{changefreq}</changefreq>\n')
            f.write(f'    <priority>{priority}</priority>\n')
            # xhtml:link alternates only for genuinely localized pages
            if file in LOCALIZED_FILES:
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
                changefreq = "weekly" if tf == "index.html" else "monthly"
                priority = "0.8" if tf == "index.html" else "0.7"
                f.write('  <url>\n')
                f.write(f'    <loc>{base_url}/en/tools{clean_tf}</loc>\n')
                f.write(f'    <changefreq>{changefreq}</changefreq>\n')
                f.write(f'    <priority>{priority}</priority>\n')
                f.write('  </url>\n')
                
        f.write('</urlset>\n')

    # Generate robots.txt
    robots_path = os.path.join(L2CACHE_OUT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write("User-agent: *\n")
        f.write("Allow: /\n\n")
        f.write(f"Sitemap: {base_url}/sitemap.xml\n")

    # Cover localized pages and copied static tools with one shared analytics
    # tag. The endpoint is served by Vercel after Web Analytics is enabled.
    inject_vercel_analytics(L2CACHE_OUT_DIR)

    # We let Vercel handle the root redirect to /en/ so it doesn't conflict with amvo.store routing

if __name__ == "__main__":
    build()
    print("Build complete.")
