import re

with open("blog-jwt-security.html", "r") as f:
    html = f.read()

target = """<div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>echo "$JWT" | jq -R -s 'gsub("\\n"; "") | split(".") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'</code></pre></div>"""

replacement = """<div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code># Decode once
echo "$JWT" | jq -R -s 'gsub("\\n"; "") | split(".") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'

# Or add an alias to your ~/.zshrc
alias decodejwt="jq -R -s 'gsub(\\\"\\\\n\\\"; \\\"\\\") | split(\\\".\\\") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'"

# Then use it like this:
echo "$JWT" | decodejwt</code></pre></div>"""

if target in html:
    html = html.replace(target, replacement)
    with open("blog-jwt-security.html", "w") as f:
        f.write(html)
    print("HTML Replaced successfully!")
else:
    print("Target HTML not found!")

with open("/Users/dinesh/.gemini/antigravity-ide/brain/ee7b57cb-20bc-46c4-94e0-ecf31e104df6/medium_syndicated_articles.md", "r") as f:
    md = f.read()

md_target = """**1. The Bash & jq One-Liner**
If you have `jq` installed, you can parse the full JWT (header, payload, and signature) directly in your terminal, handling newlines automatically:
```bash
echo "$JWT" | jq -R -s 'gsub("\\n"; "") | split(".") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'
```"""

md_replacement = """**1. The Bash & jq One-Liner**
If you have `jq` installed, you can parse the full JWT (header, payload, and signature) directly in your terminal, handling newlines automatically:
```bash
# Decode once
echo "$JWT" | jq -R -s 'gsub("\\n"; "") | split(".") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'

# Or add an alias to your ~/.zshrc
alias decodejwt="jq -R -s 'gsub(\\\"\\\\n\\\"; \\\"\\\") | split(\\\".\\\") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'"

# Then use it like this:
echo "$JWT" | decodejwt
```"""

if md_target in md:
    md = md.replace(md_target, md_replacement)
    with open("/Users/dinesh/.gemini/antigravity-ide/brain/ee7b57cb-20bc-46c4-94e0-ecf31e104df6/medium_syndicated_articles.md", "w") as f:
        f.write(md)
    print("MD Replaced successfully!")
else:
    print("Target MD not found!")

