#!/usr/bin/env python3
import os
import json

# Competitor comparison data structure
COMPETITORS = {
    "maccy": {
        "competitor_name": "Maccy",
        "seo_title": "L2Cache vs. Maccy: Which Mac Clipboard Manager is Better?",
        "seo_description": "A detailed comparison of L2Cache and Maccy. See how their pricing, on-device AI search, developer transforms, and Touch ID credentials encryption stack up.",
        "intro_paragraph": "Maccy is a popular, lightweight, and open-source clipboard manager for macOS designed for speed and keyboard-first navigation. However, if you want on-device AI search, automated OCR text extraction from screenshots, and advanced developer smart transforms, L2Cache offers a significant step up. Here is a side-by-side comparison.",
        "matrix": [
            ("Pricing", "Free (during early access, yours to keep)", "Free (GitHub) / $9.99 (App Store)"),
            ("Search Capabilities", "AI-powered natural language & semantic search", "Fuzzy text search only"),
            ("On-device AI (Apple Intelligence)", "Yes (Auto-generated titles, Smart Albums)", "No"),
            ("Touch ID Encrypted Security", "Yes (Auto-locks API keys, credentials, SSNs)", "No (Plain text SQLite storage)"),
            ("Screenshot OCR Text Search", "Yes (Extracts and index text from screenshots)", "No"),
            ("Smart Transforms (JSON, YAML, casing)", "Yes (Format JSON/YAML, minify, strip md)", "No"),
            ("Smart Albums (Auto-grouping)", "Yes (Automatic categories via local AI)", "No"),
            ("Data Privacy", "100% Local database (Never leaves your Mac)", "100% Local database")
        ],
        "advantages": [
            ("🧠", "On-Device AI & Semantic Search", "While Maccy uses simple fuzzy matching (meaning you have to remember exact words), L2Cache uses on-device Apple Intelligence. You can search for abstract concepts like 'that command to clear docker logs' and L2Cache will find it instantly, even if the query doesn't match the exact characters."),
            ("🛡️", "Touch ID Credentials Protection", "Maccy stores all captured clipboard items, including sensitive environment variables, passwords, and private API keys, in plain text. L2Cache's 'Sensitive Radar' automatically detects API keys (Stripe, OpenAI, AWS), credit cards, and SSNs, encrypts them, and locks them behind Touch ID so they are never exposed in plain text."),
            ("📷", "Screenshot OCR Text Extraction", "A common developer workflow is taking a screenshot of a terminal error stack trace. With L2Cache, all images are OCR-scanned locally, making the text inside images completely searchable. You can copy the error text directly out of the screenshot and feed it to your IDE or coding agent—a feature Maccy doesn't support.")
        ],
        "faqs": [
            ("Is L2Cache as fast as Maccy?", "Yes. While L2Cache packs advanced AI and OCR features, its core clipboard capturing runs in under 100ms and the panel opens instantly. It is built strictly for macOS native performance."),
            ("Do I need an internet connection for L2Cache's AI?", "No. Unlike other tools that send your clipboard contents to cloud AI models, L2Cache runs all AI and OCR processing entirely locally on your Mac's hardware using Apple Intelligence foundation models. Your data never leaves your machine.")
        ]
    },
    "paste": {
        "competitor_name": "Paste",
        "seo_title": "L2Cache vs. Paste App: The Best Mac Clipboard Manager Compared",
        "seo_description": "Comparing L2Cache and Paste App. Discover the differences in pricing models, visual UI layouts, developer-focused smart formatting, and local data security.",
        "intro_paragraph": "Paste is a highly visual, aesthetic clipboard manager that uses a card-based layout at the bottom of the screen and syncs history across Apple devices. However, its mandatory subscription pricing and lack of developer-focused code tools make it expensive for programmers. L2Cache offers a free-for-life alternative with robust security and AI-powered workflow features.",
        "matrix": [
            ("Pricing", "Free (during early access, yours to keep)", "$29.99/year subscription"),
            ("Search Capabilities", "AI-powered natural language & semantic search", "Basic text search"),
            ("On-device AI (Apple Intelligence)", "Yes (Auto-generated titles, Smart Albums)", "No"),
            ("Touch ID Encrypted Security", "Yes (Auto-locks API keys, credentials, SSNs)", "No (Plain text iCloud storage)"),
            ("Screenshot OCR Text Search", "Yes (Extracts and index text from screenshots)", "No (Thumbnail search only)"),
            ("Smart Transforms (JSON, YAML, casing)", "Yes (Format JSON/YAML, minify, strip md)", "No"),
            ("Smart Albums (Auto-grouping)", "Yes (Automatic categories via local AI)", "No (Manual Pinboards only)"),
            ("Data Privacy", "100% Local database (Never leaves your Mac)", "Syncs to iCloud (Cloud storage)")
        ],
        "advantages": [
            ("💰", "Subscription-Free Developer Tool", "Paste App requires a recurring $29.99/year subscription. L2Cache is completely free while in early access, and everyone who joins now keeps all features and future updates free for life. There are no ads, upsells, or hidden subscriptions."),
            ("🛠️", "Developer Code Transforms", "Developers frequently need to strip Markdown code fences, format JSON/YAML payloads, or change casing (camelCase to snake_case). L2Cache includes a built-in 'Smart Transform' panel to clean and format code instantly on copy. Paste only stores raw clips with no coding utility."),
            ("🛡️", "Strict On-Device Privacy & Key Locking", "Paste syncs your entire clipboard history—including sensitive API tokens and credentials—to iCloud. L2Cache keeps all clipboard databases strictly local on your physical Mac. It also detects sensitive data automatically, locking it securely behind Touch ID.")
        ],
        "faqs": [
            ("Does L2Cache support iCloud syncing like Paste?", "Not currently. To maintain 100% local privacy, L2Cache keeps your clipboard history isolated to each Mac. Each Mac maintains its own secure, local database. iCloud sync is planned for a future version, but will be completely optional."),
            ("How does L2Cache's UI compare to Paste?", "While Paste uses a large horizontal carousel at the bottom of the screen, L2Cache uses a sleek, compact side panel that opens in under 100ms. It is designed to stay out of your way and let you search and copy using keyboard shortcuts.")
        ]
    },
    "clipy": {
        "competitor_name": "Clipy",
        "seo_title": "L2Cache vs. Clipy: Modern Alternative for Mac Clipboard Management",
        "seo_description": "Comparing the classic Clipy manager with the modern, AI-powered L2Cache. Compare features, interface design, developer productivity tools, and security.",
        "intro_paragraph": "Clipy is a classic, lightweight open-source clipboard manager for Mac that operates out of the menu bar. While it has been a developer favorite for years, it has not been actively updated and lacks critical modern features like full-text search, OCR, security locking, and intelligent categorization. L2Cache provides a modern, secure upgrade for today's macOS workflow.",
        "matrix": [
            ("Pricing", "Free (during early access, yours to keep)", "Free (Open Source)"),
            ("Search Capabilities", "AI-powered natural language & semantic search", "No Search (Menu dropdown only)"),
            ("On-device AI (Apple Intelligence)", "Yes (Auto-generated titles, Smart Albums)", "No"),
            ("Touch ID Encrypted Security", "Yes (Auto-locks API keys, credentials, SSNs)", "No"),
            ("Screenshot OCR Text Search", "Yes (Extracts and index text from screenshots)", "No"),
            ("Smart Transforms (JSON, YAML, casing)", "Yes (Format JSON/YAML, minify, strip md)", "No"),
            ("Smart Albums (Auto-grouping)", "Yes (Automatic categories via local AI)", "No (Manual folders only)"),
            ("Data Privacy", "100% Local database (Never leaves your Mac)", "100% Local database")
        ],
        "advantages": [
            ("🔍", "Full-Text & Semantic Search", "Clipy does not have a search bar. To find an old snippet, you must manually hover through nested menu dropdowns. L2Cache lets you open a command panel in under 100ms and search through your entire history using natural, plain-English phrases."),
            ("🔒", "Active Security and Credential Protection", "Clipy stores everything in a simple configuration file in plain text. If you copy an API token or SSH key, it sits exposed in your menu bar list. L2Cache's 'Sensitive Radar' detects credentials instantly, locks them behind Touch ID, and masks them from plain sight."),
            ("⚡", "Apple Intelligence & OCR integration", "L2Cache integrates with modern macOS features, leveraging Apple Silicon to automatically name screenshots, index the text inside images using OCR, and auto-group snippets into smart albums. Clipy is a legacy tool built for older Intel Macs and doesn't support modern Apple Intelligence features.")
        ],
        "faqs": [
            ("Is Clipy still maintained?", "Clipy has not received major updates in several years. It still works on modern macOS, but it lacks optimization for Apple Silicon, modern security protocols, and advanced search functionality."),
            ("Can I import my Clipy snippets into L2Cache?", "L2Cache automatically captures anything you copy. To migrate, you can simply trigger or copy your saved snippets in Clipy, and L2Cache will automatically index and organize them for you.")
        ]
    }
}

def load_template():
    with open("comparison-template.html", "r", encoding="utf-8") as f:
        return f.read()

def generate_pages():
    template = load_template()
    
    for slug, data in COMPETITORS.items():
        comp_name = data["competitor_name"]
        
        # 1. Build matrix rows
        matrix_rows = ""
        for feature, l2, comp in data["matrix"]:
            l2_class = "check-yes" if "Yes" in l2 or "Free" in l2 or "Local" in l2 else ""
            comp_class = "check-no" if "No" in comp or "$" in comp else ""
            
            matrix_rows += f"""        <tr>
          <td><strong>{feature}</strong></td>
          <td class="{l2_class}">{l2}</td>
          <td class="{comp_class}">{comp}</td>
        </tr>\n"""
        
        # 2. Build advantages HTML
        adv_html = ""
        for icon, title, desc in data["advantages"]:
            adv_html += f"""  <div class="advantage-block">
    <div class="advantage-title">
      <span class="advantage-icon">{icon}</span>
      {title}
    </div>
    <p>{desc}</p>
  </div>\n"""
          
        # 3. Build FAQs HTML and JSON Schema
        faq_html = ""
        faq_schema_items = []
        for q, a in data["faqs"]:
            faq_html += f"""    <div class="faq-item">
      <div class="faq-question">{q}</div>
      <div class="faq-answer">{a}</div>
    </div>\n"""
            faq_schema_items.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })
            
        faq_schema_json = f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": {json.dumps(faq_schema_items, indent=4)}
  }}
  </script>"""

        # Replace placeholders in template
        page_html = template
        page_html = page_html.replace("{{seo_title}}", data["seo_title"])
        page_html = page_html.replace("{{seo_description}}", data["seo_description"])
        page_html = page_html.replace("{{canonical_url}}", f"https://l2cache.amvo.store/en/l2cache-vs-{slug}.html")
        page_html = page_html.replace("{{competitor_name}}", comp_name)
        page_html = page_html.replace("{{intro_paragraph}}", data["intro_paragraph"])
        page_html = page_html.replace("{{comparison_table_rows}}", matrix_rows)
        page_html = page_html.replace("{{l2cache_advantages_html}}", adv_html)
        page_html = page_html.replace("{{faq_schema_json}}", faq_schema_json)
        page_html = page_html.replace("{{faq_html}}", faq_html)
        
        output_filename = f"l2cache-vs-{slug}.html"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(page_html)
            
        print(f"Generated comparison page: {output_filename}")

if __name__ == "__main__":
    generate_pages()
