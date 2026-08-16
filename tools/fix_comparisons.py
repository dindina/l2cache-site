import os
import json

# Define the clean data
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
    },
    "raycast": {
        "competitor_name": "Raycast Clipboard History",
        "seo_title": "L2Cache vs. Raycast Clipboard History: Dedicated Native AI vs. Launcher Extension",
        "seo_description": "Comparing L2Cache and Raycast Clipboard History. See how dedicated memory footprint, Apple Intelligence screenshot OCR search, Touch ID credential masking, and coding smart transforms compare.",
        "intro_paragraph": "Raycast is an all-in-one launcher with a built-in clipboard history extension. While convenient for existing Raycast power users, it consumes significant background RAM (250MB+) and lacks dedicated on-device OCR search, code sanitization for LLM prompts, and hardware Touch ID credential locking. L2Cache is a focused, ultra-lightweight (<35MB) native clipboard intelligence engine built exclusively for macOS.",
        "matrix": [
            ("Pricing", "Free (during early access, yours to keep)", "Free / $96/yr (Raycast Pro)"),
            ("Background Memory (RAM)", "35 MB (Dedicated Native Swift)", "250MB–450MB (Full Electron/Node Launcher)"),
            ("Screenshot OCR Text Search", "Yes (Extracts & indexes text inside screenshots)", "No"),
            ("On-device AI (Apple Intelligence)", "Yes (100% on-device titles & Smart Albums)", "Cloud AI (Requires Raycast Pro subscription)"),
            ("Touch ID Encrypted Security", "Yes (Auto-locks API keys, credentials, SSNs)", "No (Plain text database)"),
            ("Smart Transforms (JSON, YAML, casing)", "Yes (Built-in 1-click developer transforms)", "Requires custom Raycast script commands"),
            ("Data Privacy", "100% Local database (Zero network telemetry)", "Local database with cloud telemetry")
        ],
        "advantages": [
            ("⚡", "Ultra-Lightweight Dedicated Memory Footprint", "Raycast is a full application launcher running multiple extensions in the background, routinely consuming 250MB to 500MB of RAM. L2Cache is written strictly in native Swift and GRDB SQLite, idling at under 35MB of memory while retaining full-text indexing over 100,000 clips."),
            ("🖼️", "Native Screenshot OCR Text Indexing", "When you screenshot a terminal error, API response, or design asset, L2Cache automatically performs on-device OCR using Apple Vision. You can search for words contained inside screenshots and copy text directly out of images—a feature completely absent in Raycast Clipboard History."),
            ("🛡️", "Sensitive Radar with Touch ID Key Masking", "Raycast stores API keys, database URLs, and passwords in plain text in its history list. L2Cache's Sensitive Radar automatically flags over 60 credential types (OpenAI, AWS, Stripe), masks them from screen sharing, and requires Touch ID to reveal or copy.")
        ],
        "faqs": [
            ("Can I use L2Cache alongside Raycast?", "Yes! Many developers use Raycast as their application launcher (⌘Space) and set L2Cache as their dedicated clipboard manager (⌘⇧V) for superior OCR, privacy, and smart code formatting."),
            ("Does L2Cache require Raycast Pro?", "No. L2Cache is an independent, native macOS app that is free during early access with all AI and OCR features running 100% on-device without subscriptions.")
        ]
    },
    "alfred": {
        "competitor_name": "Alfred Clipboard History",
        "seo_title": "L2Cache vs. Alfred Clipboard History: Modern AI & OCR vs. Classic Launcher",
        "seo_description": "Comparing L2Cache and Alfred Powerpack clipboard history. Compare modern UI speed, on-device OCR screenshot search, Apple Intelligence categorization, and developer formatting tools.",
        "intro_paragraph": "Alfred is a classic macOS productivity tool that includes a clipboard history viewer with the paid Powerpack. While robust and battle-tested, Alfred's clipboard viewer relies on legacy text matching, lacks screenshot OCR indexing, offers no on-device AI categorization, and doesn't provide built-in developer transforms for JSON, YAML, or regex. L2Cache provides a modern, AI-first alternative designed for today's macOS ecosystem.",
        "matrix": [
            ("Pricing", "Free (during early access, yours to keep)", "£34 (~$44 USD) Powerpack Single License"),
            ("Search Capabilities", "AI-powered natural language & semantic search", "Fuzzy text matching only"),
            ("Screenshot OCR Text Search", "Yes (Extracts and indexes text from screenshots)", "No"),
            ("On-device AI (Apple Intelligence)", "Yes (Auto-generated titles, Smart Albums)", "No"),
            ("Touch ID Encrypted Security", "Yes (Auto-locks API keys, credentials, SSNs)", "No (Plain text database)"),
            ("Smart Transforms (JSON, YAML, casing)", "Yes (Format JSON/YAML, minify, strip md)", "Requires custom Alfred Workflows"),
            ("UI Design & Aesthetics", "Modern macOS 15 floating panel with dark mode", "Classic legacy interface")
        ],
        "advantages": [
            ("🧠", "Apple Intelligence & Semantic Discovery", "Alfred requires exact keyword matches to find old snippets. L2Cache uses Apple Intelligence to automatically title and tag clips, enabling natural semantic search (e.g. 'the docker compose command for postgres') even if you don't recall the exact syntax."),
            ("📷", "On-Device Screenshot OCR Extraction", "L2Cache indexes text inside copied screenshots in real-time on Apple Silicon. You can search and copy code directly from images, whereas Alfred can only treat images as static files without text search."),
            ("💎", "Out-of-the-Box Developer Code Tools", "In Alfred, formatting JSON, unescaping strings, or converting casing requires finding and configuring external third-party Workflows. L2Cache includes built-in 1-click smart transforms for instant code cleanup.")
        ],
        "faqs": [
            ("Does Alfred have built-in OCR?", "No. Alfred does not perform OCR on images or screenshots. L2Cache performs on-device OCR on every captured image using macOS Apple Vision framework."),
            ("Is L2Cache completely free?", "Yes. L2Cache is free while in early access, and early access users keep it free for life with all future updates included.")
        ]
    },
    "pastepal": {
        "competitor_name": "PastePal",
        "seo_title": "L2Cache vs. PastePal: Mac Clipboard Managers Compared",
        "seo_description": "A detailed comparison of L2Cache and PastePal for macOS. Compare on-device Apple Intelligence, developer smart transforms, Touch ID security, and pricing.",
        "intro_paragraph": "PastePal is a well-designed native clipboard manager for Apple devices with iCloud synchronization. While visually polished, it lacks on-device AI categorization, developer-focused code formatting tools, and automated credential masking. L2Cache offers an AI-first alternative with robust developer utilities and zero subscription costs.",
        "matrix": [
            ("Pricing", "Free (during early access, yours to keep)", "$14.99 Lifetime or $4.99/yr"),
            ("On-device AI (Apple Intelligence)", "Yes (Auto-generated titles, Smart Albums)", "No"),
            ("Search Capabilities", "Semantic AI & FTS5 full-text search", "Keyword search only"),
            ("Touch ID Encrypted Security", "Yes (Auto-locks API keys, credentials, SSNs)", "Manual locking only"),
            ("Smart Transforms (JSON, YAML, casing)", "Yes (Format JSON/YAML, minify, strip md)", "No"),
            ("Screenshot OCR Text Search", "Yes (Extracts and index text from screenshots)", "Basic OCR on iOS only"),
            ("Data Privacy", "100% Local database (Never leaves your Mac)", "iCloud sync")
        ],
        "advantages": [
            ("🧠", "On-Device AI Categorization", "L2Cache automatically summarizes long code snippets, generates human-readable titles, and sorts clips into Smart Albums using local Apple Intelligence. PastePal requires manual organization and tagging."),
            ("🛠️", "Built-In Developer Workflows", "L2Cache includes specialized developer tools: stripping markdown code fences, formatting serialized JSON logs, unescaping strings, and testing regex patterns directly from your clipboard history."),
            ("🔒", "Active Sensitive Data Radar", "L2Cache automatically scans incoming clips for private API keys, database connection strings, and tokens, locking them behind Touch ID before they can be exposed on screen.")
        ],
        "faqs": [
            ("How does L2Cache compare to PastePal in terms of performance?", "Both apps are built natively in Swift for macOS. L2Cache specifically optimizes SQLite with FTS5 indexing and async GRDB concurrency, achieving sub-100ms panel latency even with 50,000+ items."),
            ("Does L2Cache require an internet connection?", "No. L2Cache operates 100% locally on your Mac's physical hardware with zero cloud dependencies.")
        ]
    },
    "copyclip": {
        "competitor_name": "CopyClip",
        "seo_title": "L2Cache vs. CopyClip: Modern AI Upgrade for Mac Clipboard Management",
        "seo_description": "Comparing CopyClip and L2Cache. Compare full-text search, OCR, Touch ID credential masking, and developer transforms.",
        "intro_paragraph": "CopyClip is a minimalist, basic menu-bar clipboard history tool for macOS. While lightweight, it is limited to plain text only, has no search bar in the free tier, and lacks OCR, security, and smart code transforms. L2Cache provides a modern, feature-complete upgrade designed for power users and developers.",
        "matrix": [
            ("Pricing", "Free (during early access, yours to keep)", "Free (Basic) / $7.99 (CopyClip 2)"),
            ("Search Capabilities", "AI-powered natural language & semantic search", "None (Free) / Basic Search (CopyClip 2)"),
            ("Supported Media", "Text, Rich Text, Images, Code, Colors, Files", "Plain text only"),
            ("Screenshot OCR Text Search", "Yes (Extracts and index text from screenshots)", "No"),
            ("On-device AI (Apple Intelligence)", "Yes (Auto-generated titles, Smart Albums)", "No"),
            ("Touch ID Encrypted Security", "Yes (Auto-locks API keys, credentials, SSNs)", "No"),
            ("Smart Transforms (JSON, YAML, casing)", "Yes (Format JSON/YAML, minify, strip md)", "No")
        ],
        "advantages": [
            ("🔍", "Instant FTS5 & Semantic Search", "CopyClip requires scrolling through a long menu list to find past clips. L2Cache offers an instant floating panel with sub-millisecond full-text and semantic search."),
            ("📷", "Rich Media & Image OCR", "CopyClip only captures plain text strings. L2Cache captures rich text, color codes, URLs, files, and images—indexing text inside images via OCR so everything remains searchable."),
            ("🛡️", "Touch ID Credential Security", "CopyClip stores all copied text in plain text. L2Cache detects private credentials and hides them behind Touch ID authentication.")
        ],
        "faqs": [
            ("Why upgrade from CopyClip to L2Cache?", "L2Cache adds rich media capture, on-device AI categorization, screenshot OCR text search, developer smart transforms, and Touch ID credential protection while remaining fast and lightweight."),
            ("Is L2Cache free?", "Yes. L2Cache is free during early access with no ads or subscription requirements.")
        ]
    }
}

# Write clean JSON
json_path = "/Users/dinesh/tech/l2cache-site/comparisons_data.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(COMPETITORS, f, indent=2, ensure_ascii=False)

# Write clean generator script that reads from JSON
gen_script = """#!/usr/bin/env python3
import os
import json

def load_template():
    with open("comparison-template.html", "r", encoding="utf-8") as f:
        return f.read()

def generate_pages():
    template = load_template()
    with open("comparisons_data.json", "r", encoding="utf-8") as f:
        competitors = json.load(f)
        
    for slug, data in competitors.items():
        comp_name = data["competitor_name"]
        matrix_rows = ""
        for feature, l2, comp in data["matrix"]:
            l2_class = "check-yes" if ("Yes" in l2 or "Free" in l2 or "Local" in l2 or "35 MB" in l2) else ""
            comp_class = "check-no" if ("No" in comp or "$" in comp or "£" in comp or "250MB" in comp) else ""
            matrix_rows += f"        <tr>\\n          <td><strong>{feature}</strong></td>\\n          <td class=\\"{l2_class}\\">{l2}</td>\\n          <td class=\\"{comp_class}\\">{comp}</td>\\n        </tr>\\n"

        adv_html = ""
        for icon, title, desc in data["advantages"]:
            adv_html += f"  <div class=\\"advantage-block\\">\\n    <div class=\\"advantage-title\\">\\n      <span class=\\"advantage-icon\\">{icon}</span>\\n      {title}\\n    </div>\\n    <p>{desc}</p>\\n  </div>\\n"

        faq_html = ""
        faq_schema_items = []
        for q, a in data["faqs"]:
            faq_html += f"    <div class=\\"faq-item\\">\\n      <div class=\\"faq-question\\">{q}</div>\\n      <div class=\\"faq-answer\\">{a}</div>\\n    </div>\\n"
            faq_schema_items.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })

        faq_schema_json = f'''  <script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema_items}, indent=4)}
  </script>'''

        page_html = template
        page_html = page_html.replace("{{seo_title}}", data["seo_title"])
        page_html = page_html.replace("{{seo_description}}", data["seo_description"])
        page_html = page_html.replace("{{canonical_url}}", f"https://l2cache.amvo.store/en/l2cache-vs-{slug}")
        page_html = page_html.replace("{{competitor_name}}", comp_name)
        page_html = page_html.replace("{{intro_paragraph}}", data["intro_paragraph"])
        page_html = page_html.replace("{{comparison_table_rows}}", matrix_rows)
        page_html = page_html.replace("{{l2cache_advantages_html}}", adv_html)
        page_html = page_html.replace("{{faq_schema_json}}", faq_schema_json)
        page_html = page_html.replace("{{faq_html}}", faq_html)

        out_file = f"l2cache-vs-{slug}.html"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"Generated comparison page: {out_file}")

if __name__ == "__main__":
    generate_pages()
"""

with open("/Users/dinesh/tech/l2cache-site/generate_comparisons.py", "w", encoding="utf-8") as f:
    f.write(gen_script)

print("Created comparisons_data.json and clean generate_comparisons.py!")
