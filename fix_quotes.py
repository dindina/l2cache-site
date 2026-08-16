import re

with open("blog-jwt-security.html", "r") as f:
    html = f.read()

# Replace the escaped quotes with normal quotes in the html
target = r"""decodejwt() { echo "$1" | jq -R -s 'gsub(\"\\n\"; \"\") | split(\".\") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'; }"""
replacement = r"""decodejwt() { echo "$1" | jq -R -s 'gsub("\n"; "") | split(".") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'; }"""

if target in html:
    html = html.replace(target, replacement)
    with open("blog-jwt-security.html", "w") as f:
        f.write(html)
    print("HTML fixed!")
else:
    print("HTML target not found!")

with open("/Users/dinesh/.gemini/antigravity-ide/brain/ee7b57cb-20bc-46c4-94e0-ecf31e104df6/medium_syndicated_articles.md", "r") as f:
    md = f.read()

if target in md:
    md = md.replace(target, replacement)
    with open("/Users/dinesh/.gemini/antigravity-ide/brain/ee7b57cb-20bc-46c4-94e0-ecf31e104df6/medium_syndicated_articles.md", "w") as f:
        f.write(md)
    print("MD fixed!")
else:
    print("MD target not found!")

