import re

with open("blog-jwt-security.html", "r") as f:
    html = f.read()

target = """  <p><strong>1. The Bash & jq One-Liner:</strong></p>
  <p>If you have <a href="https://jqlang.github.io/jq/" style="color: var(--purple);">jq</a> installed, you can parse the full JWT (header, payload, and signature) directly in your terminal, handling newlines automatically:</p>
<div class="snippet-container"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>echo "$JWT" | jq -R -s 'gsub("\\n"; "") | split(".") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'</code></pre></div>
  
  <p><strong>2. A Quick Node.js Script:</strong></p>
  <p>If you prefer JavaScript, you can write a tiny local script (<code>decode.js</code>) that outputs the fully structured token:</p>
<div class="snippet-container"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>const token = process.argv[2];
const [header, payload, signature] = token.split('.');
console.log(JSON.stringify({
  header: JSON.parse(Buffer.from(header, 'base64').toString()),
  payload: JSON.parse(Buffer.from(payload, 'base64').toString()),
  signature
}, null, 2));</code></pre></div>
  
  <p><strong>3. Python Decoder:</strong></p>
  <p>Python makes this easy as well, provided you handle the missing Base64Url padding correctly:</p>
<div class="snippet-container"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>import sys, base64, json
def dec(s):
    return json.loads(base64.b64decode(s + '=' * (-len(s) % 4)))
h, p, s = sys.argv[1].split('.')
print(json.dumps({'header': dec(h), 'payload': dec(p), 'signature': s}, indent=2))</code></pre></div>

  <p><strong>4. The "Zero-Install" Browser Method (Fully Offline):</strong></p>
  <p>Even though sites like <code>jwt.io</code> process tokens online, your browser can do it completely locally. Open your browser's Developer Tools (Press <code>F12</code> or <code>Cmd+Option+I</code>), go to the <strong>Console</strong> tab, paste this snippet, and hit Enter:</p>
<div class="snippet-container"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>const decodeJWT = (t) => t.split('.').slice(0, 2).map(p => JSON.parse(atob(p.replace(/-/g, '+').replace(/_/g, '/'))));
console.log(decodeJWT("YOUR_JWT_HERE"));</code></pre></div>"""

replacement = """  <div style="overflow-x: auto; margin-bottom: 32px;">
    <table style="width: 100%; border-collapse: collapse; text-align: left; background: rgba(255,255,255,0.03); border-radius: 12px; overflow: hidden; border: 1px solid var(--border);">
      <thead>
        <tr style="background: rgba(127,119,221,0.1); border-bottom: 1px solid var(--border);">
          <th style="padding: 16px 20px; font-family: var(--sans); font-weight: 600; color: var(--text);">Method</th>
          <th style="padding: 16px 20px; font-family: var(--sans); font-weight: 600; color: var(--text);">Description</th>
          <th style="padding: 16px 20px; font-family: var(--sans); font-weight: 600; color: var(--text);">Code Snippet</th>
        </tr>
      </thead>
      <tbody>
        <!-- Bash -->
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top; white-space: nowrap;"><strong>Bash & jq</strong></td>
          <td style="padding: 20px; vertical-align: top; color: var(--text-muted);">Parse the full JWT directly in your terminal.<br>Automatically handles newlines.</td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>echo "$JWT" | jq -R -s 'gsub("\\n"; "") | split(".") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'</code></pre></div>
          </td>
        </tr>
        <!-- Node.js -->
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top; white-space: nowrap;"><strong>Node.js</strong></td>
          <td style="padding: 20px; vertical-align: top; color: var(--text-muted);">A tiny local script (<code>decode.js</code>) that outputs<br>the fully structured token using built-in buffers.</td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>const token = process.argv[2];
const [header, payload, signature] = token.split('.');
console.log(JSON.stringify({
  header: JSON.parse(Buffer.from(header, 'base64').toString()),
  payload: JSON.parse(Buffer.from(payload, 'base64').toString()),
  signature
}, null, 2));</code></pre></div>
          </td>
        </tr>
        <!-- Python -->
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top; white-space: nowrap;"><strong>Python</strong></td>
          <td style="padding: 20px; vertical-align: top; color: var(--text-muted);">A quick Python script that manually handles<br>the missing Base64Url padding before parsing.</td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>import sys, base64, json
def dec(s):
    return json.loads(base64.b64decode(s + '=' * (-len(s) % 4)))
h, p, s = sys.argv[1].split('.')
print(json.dumps({'header': dec(h), 'payload': dec(p), 'signature': s}, indent=2))</code></pre></div>
          </td>
        </tr>
        <!-- Browser -->
        <tr>
          <td style="padding: 20px; vertical-align: top; white-space: nowrap;"><strong>Browser Console</strong></td>
          <td style="padding: 20px; vertical-align: top; color: var(--text-muted);">Zero-install method. Paste into the DevTools Console (F12)<br>to process entirely offline in the browser.</td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>const decodeJWT = (t) => t.split('.').slice(0, 2).map(p => JSON.parse(atob(p.replace(/-/g, '+').replace(/_/g, '/'))));
console.log(decodeJWT("YOUR_JWT_HERE"));</code></pre></div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>"""

if target in html:
    html = html.replace(target, replacement)
    with open("blog-jwt-security.html", "w") as f:
        f.write(html)
    print("Replaced successfully!")
else:
    print("Target not found!")
