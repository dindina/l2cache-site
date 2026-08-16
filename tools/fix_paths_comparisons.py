import os

script_code = """#!/usr/bin/env python3
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_template():
    template_path = os.path.join(BASE_DIR, "comparison-template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

def get_row_category(feature_name):
    name = feature_name.lower()
    if any(k in name for k in ["pricing", "cost", "license", "fee"]):
        return "pricing"
    if any(k in name for k in ["ai", "ocr", "intelligence", "search", "album", "vision"]):
        return "ai"
    if any(k in name for k in ["security", "touch id", "privacy", "memory", "ram", "database", "transform", "credential"]):
        return "security"
    return "all"

def format_l2cache_cell(text):
    t = text.strip()
    if "Free" in t or "early access" in t.lower():
        return f'<span class="rich-badge badge-win-gold">🎁 {t}</span>'
    elif "35 MB" in t or "34 MB" in t:
        return f'<span class="rich-badge badge-win-emerald">⚡ {t}</span>'
    elif "Touch ID" in t or "Hardware" in t:
        return f'<span class="rich-badge badge-win-emerald">🛡️ {t}</span>'
    elif "OCR" in t or "Vision" in t:
        return f'<span class="rich-badge badge-win-emerald">📷 {t}</span>'
    elif "Apple Intelligence" in t or "Semantic" in t or "AI" in t:
        return f'<span class="rich-badge badge-win-emerald">🧠 {t}</span>'
    elif "Local" in t or "Yes" in t:
        return f'<span class="rich-badge badge-win-emerald">✅ {t}</span>'
    else:
        return f'<span class="rich-badge badge-win-emerald">✨ {t}</span>'

def format_comp_cell(text):
    t = text.strip()
    if "$" in t or "£" in t or "/year" in t or "subscription" in t.lower():
        return f'<span class="rich-badge badge-loss-red">💳 {t}</span>'
    elif "250MB" in t or "342 MB" in t or "Heavy" in t:
        return f'<span class="rich-badge badge-loss-red">🐢 {t}</span>'
    elif "Plain text" in t or "exposed" in t.lower() or "telemetry" in t.lower():
        return f'<span class="rich-badge badge-loss-red">⚠️ {t}</span>'
    elif "No" in t or "None" in t or "❌" in t:
        return f'<span class="rich-badge badge-loss-red">❌ {t}</span>'
    elif "Cloud" in t or "iCloud" in t:
        return f'<span class="rich-badge badge-neutral">☁️ {t}</span>'
    else:
        return f'<span class="rich-badge badge-neutral">{t}</span>'

def generate_pages():
    template = load_template()
    json_path = os.path.join(BASE_DIR, "comparisons_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        competitors = json.load(f)

    for slug, data in competitors.items():
        comp_name = data["competitor_name"]
        
        matrix_rows = ""
        for feature, l2, comp in data["matrix"]:
            cat = get_row_category(feature)
            l2_formatted = format_l2cache_cell(l2)
            comp_formatted = format_comp_cell(comp)

            matrix_rows += f'''          <tr data-cat="{cat}">
            <td><strong>{feature}</strong></td>
            <td class="col-l2-win">{l2_formatted}</td>
            <td>{comp_formatted}</td>
          </tr>\\n'''

        adv_html = ""
        for icon, title, desc in data["advantages"]:
            adv_html += f'''    <div class="advantage-card">
      <div class="advantage-header">
        <div class="advantage-icon-box">{icon}</div>
        <h3>{title}</h3>
      </div>
      <p>{desc}</p>
    </div>\\n'''

        faq_html = ""
        faq_schema_items = []
        for q, a in data["faqs"]:
            faq_html += f'''      <div class="faq-item">
        <div class="faq-q">❓ {q}</div>
        <div class="faq-a">{a}</div>
      </div>\\n'''
            faq_schema_items.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })

        faq_schema_json = '  <script type="application/ld+json">\\n' + json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema_items
        }, indent=4) + '\\n  </script>'

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

        out_file = os.path.join(BASE_DIR, f"l2cache-vs-{slug}.html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"Generated rich comparison page: {out_file}")

if __name__ == "__main__":
    generate_pages()
"""

with open("/Users/dinesh/tech/l2cache-site/generate_comparisons.py", "w", encoding="utf-8") as f:
    f.write(script_code)

print("Updated /Users/dinesh/tech/l2cache-site/generate_comparisons.py cleanly with relative BASE_DIR paths!")
