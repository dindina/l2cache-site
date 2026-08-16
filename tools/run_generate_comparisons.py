import os
import json

def load_template():
    with open("/Users/dinesh/tech/l2cache-site/comparison-template.html", "r", encoding="utf-8") as f:
        return f.read()

from update_site_comparisons import COMPETITORS_UPDATE

def generate_pages():
    template = load_template()
    for slug, data in COMPETITORS_UPDATE.items():
        comp_name = data["competitor_name"]
        matrix_rows = ""
        for feature, l2, comp in data["matrix"]:
            l2_class = "check-yes" if ("Yes" in l2 or "Free" in l2 or "Local" in l2 or "35 MB" in l2) else ""
            comp_class = "check-no" if ("No" in comp or "$" in comp or "£" in comp or "250MB" in comp) else ""
            matrix_rows += f"""        <tr>
          <td><strong>{feature}</strong></td>
          <td class="{l2_class}">{l2}</td>
          <td class="{comp_class}">{comp}</td>
        </tr>\n"""

        adv_html = ""
        for icon, title, desc in data["advantages"]:
            adv_html += f"""  <div class="advantage-block">
    <div class="advantage-title">
      <span class="advantage-icon">{icon}</span>
      {title}
    </div>
    <p>{desc}</p>
  </div>\n"""

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
{json.dumps({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faq_schema_items
}, indent=4)}
  </script>"""

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

        out_file = f"/Users/dinesh/tech/l2cache-site/l2cache-vs-{slug}.html"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"Generated comparison page: {out_file}")

if __name__ == "__main__":
    generate_pages()
