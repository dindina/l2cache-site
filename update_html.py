import re

with open("blog-jwt-security.html", "r") as f:
    html = f.read()

style_addition = """    footer a:hover { color: var(--text-muted); }
    .snippet-container { position: relative; margin-bottom: 24px; }
    .snippet-container pre { background: rgba(255,255,255,0.08); padding: 16px; border-radius: 8px; overflow-x: auto; font-family: var(--mono); font-size: 14px; margin-bottom: 0; color: #e0ffe8; }
    .copy-btn { position: absolute; top: 8px; right: 8px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.7); font-family: var(--sans); font-size: 12px; padding: 4px 8px; border-radius: 4px; cursor: pointer; transition: all 0.2s; }
    .copy-btn:hover { background: rgba(255,255,255,0.2); color: #fff; }"""

html = html.replace("    footer a:hover { color: var(--text-muted); }", style_addition)

script_addition = """
<script>
function copyCode(btn) {
  const code = btn.nextElementSibling.innerText;
  navigator.clipboard.writeText(code).then(() => {
    btn.innerText = 'Copied!';
    setTimeout(() => { btn.innerText = 'Copy'; }, 2000);
  });
}
</script>
</body>"""

html = html.replace("</body>", script_addition)

pre_regex = re.compile(r'<pre style="[^"]*"><code>(.*?)</code></pre>', re.DOTALL)

def replace_pre(match):
    code_content = match.group(1)
    return f'<div class="snippet-container"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>{code_content}</code></pre></div>'

html = pre_regex.sub(replace_pre, html)

with open("blog-jwt-security.html", "w") as f:
    f.write(html)
