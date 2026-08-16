# Fix 1: CTA heading in regex-clipboard-mac.html
with open("regex-clipboard-mac.html", "r") as f:
    html = f.read()

html = html.replace(
    "<h2>Stop writing shell scripts for logs.</h2>",
    "<h2>Stop Pasting Logs Online. Extract Regex Locally.</h2>"
)

with open("regex-clipboard-mac.html", "w") as f:
    f.write(html)

print("CTA heading updated!")

# Fix 2: lang-switcher CSS in theme.css
with open("theme.css", "r") as f:
    css = f.read()

old_css = """.lang-switcher select {
  background: rgba(0, 0, 0, 0.06) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}"""

new_css = """.lang-switcher select {
  background: #1a1a2e !important;
  border: 1px solid rgba(127,119,221,0.35) !important;
  color: #e0e0f0 !important;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
}
.lang-switcher select option {
  background: #1a1a2e;
  color: #e0e0f0;
}"""

if old_css in css:
    css = css.replace(old_css, new_css)
    with open("theme.css", "w") as f:
        f.write(css)
    print("Lang-switcher CSS fixed!")
else:
    print("CSS target not found — check manually")
    print(repr(css[css.find(".lang-switcher"):css.find(".lang-switcher")+200]))
