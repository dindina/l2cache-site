import re

with open("blog-jwt-security.html", "r") as f:
    html = f.read()

# I will just write a regex to replace the entire table div
start_marker = '<div style="overflow-x: auto; margin-bottom: 32px;">'
end_marker = '</div>\n  \n  <p>All of these solutions'

if start_marker in html:
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker) + len('</div>')
    
    new_table = """  <div style="margin-bottom: 32px;">
    <table style="table-layout: fixed; width: 100%; border-collapse: collapse; text-align: left; background: rgba(255,255,255,0.03); border-radius: 12px; overflow: hidden; border: 1px solid var(--border);">
      <thead>
        <tr style="background: rgba(127,119,221,0.1); border-bottom: 1px solid var(--border);">
          <th style="padding: 16px 20px; font-family: var(--sans); font-weight: 600; color: var(--text); width: 30%;">Method</th>
          <th style="padding: 16px 20px; font-family: var(--sans); font-weight: 600; color: var(--text); width: 70%;">Code Snippet</th>
        </tr>
      </thead>
      <tbody>
        <!-- Bash -->
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top;">
            <strong>Bash & jq</strong>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0; line-height: 1.5;">Parse the full JWT directly in your terminal. Automatically handles newlines.</p>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>echo "$JWT" | jq -R -s 'gsub("\\n"; "") | split(".") | {header: (.[0] | @base64d | fromjson), payload: (.[1] | @base64d | fromjson), signature: .[2]}'</code></pre></div>
          </td>
        </tr>
        <!-- Node.js -->
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top;">
            <strong>Node.js</strong>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0; line-height: 1.5;">A tiny local script (<code>decode.js</code>) that outputs the fully structured token using built-in buffers.</p>
          </td>
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
          <td style="padding: 20px; vertical-align: top;">
            <strong>Python</strong>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0; line-height: 1.5;">A quick Python script that manually handles the missing Base64Url padding before parsing.</p>
          </td>
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
          <td style="padding: 20px; vertical-align: top;">
            <strong>Browser Console</strong>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0; line-height: 1.5;">Zero-install method. Paste into the DevTools Console (F12) to process entirely offline in the browser.</p>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>const decodeJWT = (t) => t.split('.').slice(0, 2).map(p => JSON.parse(atob(p.replace(/-/g, '+').replace(/_/g, '/'))));
console.log(decodeJWT("YOUR_JWT_HERE"));</code></pre></div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>"""

    html = html[:start_idx] + new_table + html[end_idx:]
    with open("blog-jwt-security.html", "w") as f:
        f.write(html)
    print("Replaced successfully!")
else:
    print("Target not found!")
