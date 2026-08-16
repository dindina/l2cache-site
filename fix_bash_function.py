import re

with open("blog-jwt-security.html", "r") as f:
    html = f.read()

target_html = """# Or add an alias to your ~/.zshrc
alias decodejwt="jq -R -s 'gsub(\\"\\\\n\\"; \\"\\") | split(\\".\\") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'"

# Then use it like this:
echo "$JWT" | decodejwt</code></pre></div>"""

replacement_html = """# Or add a function to your ~/.zshrc
decodejwt() { echo "$1" | jq -R -s 'gsub(\\"\\\\n\\"; \\"\\") | split(\\".\\") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'; }

# Then pass the token as an argument:
decodejwt "YOUR_JWT_STRING"</code></pre></div>"""

if target_html in html:
    html = html.replace(target_html, replacement_html)
    with open("blog-jwt-security.html", "w") as f:
        f.write(html)
    print("HTML Replaced successfully!")
else:
    print("Target HTML not found!")

with open("/Users/dinesh/.gemini/antigravity-ide/brain/ee7b57cb-20bc-46c4-94e0-ecf31e104df6/medium_syndicated_articles.md", "r") as f:
    md = f.read()

md_target = """# Or add an alias to your ~/.zshrc
alias decodejwt="jq -R -s 'gsub(\\\"\\\\n\\\"; \\\"\\\") | split(\\\".\\\") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'"

# Then use it like this:
echo "$JWT" | decodejwt"""

md_replacement = """# Or add a function to your ~/.zshrc
decodejwt() { echo "$1" | jq -R -s 'gsub(\\\"\\\\n\\\"; \\\"\\\") | split(\\\".\\\") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'; }

# Then pass the token as an argument:
decodejwt "YOUR_JWT_STRING\""""

if md_target in md:
    md = md.replace(md_target, md_replacement)
    with open("/Users/dinesh/.gemini/antigravity-ide/brain/ee7b57cb-20bc-46c4-94e0-ecf31e104df6/medium_syndicated_articles.md", "w") as f:
        f.write(md)
    print("MD Replaced successfully!")
else:
    print("Target MD not found!")
