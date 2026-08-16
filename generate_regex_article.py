import re

with open("regex-clipboard-mac.html", "r") as f:
    html = f.read()

new_article = """<article class="article-wrap">
    <div class="eyebrow">Security & Dev Tools</div>
    <h1>Stop Pasting Logs Online: How to Extract Regex from Mac Clipboard</h1>
    <p class="lede">Using online tools like <code>regex101.com</code> to parse clipboard logs is a massive security risk. Here are three ways to extract UUIDs, Emails, and API Keys locally on macOS.</p>
    
    <p>As a developer, you often copy huge chunks of log files or JSON payloads just to extract a few specific items—like a list of UUIDs, email addresses, or IP addresses. The natural instinct is to paste the massive log into an online Regex tester to quickly parse out what you need.</p>

    <p><strong>But doing this with production logs is a critical security risk.</strong> You are unknowingly exposing internal system architecture, PII (Personally Identifiable Information), or even access tokens to third-party servers.</p>
    
    <p>Instead of risking a data leak, here are three foolproof ways to extract regex matches from your macOS clipboard entirely locally, directly from the terminal.</p>

    <br>
    <h2>Secure Offline Alternatives for Regex Extraction</h2>
    
    <table style="width: 100%; border-collapse: collapse; margin-top: 24px; margin-bottom: 48px; border: 1px solid var(--border); border-radius: 12px; overflow: hidden;">
      <thead>
        <tr style="background: rgba(127,119,221,0.1); border-bottom: 1px solid var(--border);">
          <th style="padding: 16px; text-align: left; font-family: var(--sans); font-size: 14px; width: 30%;">Method</th>
          <th style="padding: 16px; text-align: left; font-family: var(--sans); font-size: 14px; width: 70%;">Code Snippet</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top;">
            <strong>Bash (grep)</strong><br><br>
            <span style="font-size: 14px; color: var(--text-muted);">The classic terminal approach. Uses <code>pbpaste</code> to read the clipboard, <code>grep -oE</code> to extract all matches (e.g., Email addresses), and <code>pbcopy</code> to write the results back.</span>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>pbpaste | grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | pbcopy</code></pre></div>
          </td>
        </tr>
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top;">
            <strong>Ruby One-Liner</strong><br><br>
            <span style="font-size: 14px; color: var(--text-muted);">Ruby is incredibly powerful for text processing. This one-liner extracts all UUIDs from the clipboard using Ruby's native regex engine.</span>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>pbpaste | ruby -ne 'puts $_.scan(/\b[0-9a-fA-F\-]{36}\b/)' | pbcopy</code></pre></div>
          </td>
        </tr>
        <tr>
          <td style="padding: 20px; vertical-align: top;">
            <strong>Python Script</strong><br><br>
            <span style="font-size: 14px; color: var(--text-muted);">If you need to handle multiline logic or case-insensitivity easily, a small Python script handles clipboard reading via <code>subprocess</code> natively. This script extracts AWS Access Keys.</span>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>import subprocess, re
text = subprocess.check_output('pbpaste', text=True)
matches = re.findall(r'(?i)AKIA[0-9A-Z]{16}', text)
subprocess.run(['pbcopy'], input='\\n'.join(matches), text=True)
print(f"Extracted {len(matches)} keys.")</code></pre></div>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>The Best of Both Worlds: L2Cache Smart Actions</h2>
    <p>Writing and remembering shell scripts for every log file is tedious. What if your clipboard manager had <code>grep</code> built-in?</p>

    <p><strong>L2Cache</strong> is a native macOS clipboard manager that completely reimagines pattern matching. Instead of dropping into a terminal, L2Cache automatically parses your clipboard on the fly using native Swift Regex. </p>

    <img src="screenshots/regex-pattern-matcher.gif" alt="Regex Clipboard Mac" style="width:100%; max-width:800px; display:block; margin: 40px auto; border-radius:12px; border:1px solid var(--border); box-shadow:0 10px 30px rgba(0,0,0,0.3);"/>

    <p>With <strong>Smart Actions</strong>, L2Cache instantly recognizes structured data—like IPs, UUIDs, or URLs—within massive logs and presents them as clickable buttons. You don't have to write a single script. Need to extract a custom API token? Just type a regex pattern directly into L2Cache's search bar, and it filters your local SQLite history in milliseconds.</p>

    <p>Most importantly: <strong>Everything happens 100% offline.</strong> L2Cache never sends your clipboard data to the cloud, ensuring your production logs remain completely secure on your Mac.</p>

    <div class="cta-card">
      <h2>Stop writing shell scripts for logs.</h2>
      <p>Download L2Cache today and get powerful, offline Regex extraction right from your menu bar.</p>
      <a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="btn-primary" target="_blank" rel="noopener">Download L2Cache on the App Store</a>
      <div class="cta-note">$6.99 one-time purchase. No subscriptions.</div>
    </div>
  </article>"""

# Replace <article>...</article>
html = re.sub(r'<article class="article-wrap">.*?</article>', new_article, html, flags=re.DOTALL)

# Add JS if missing
js_code = """<script>
function copyCode(btn) {
  const code = btn.nextElementSibling.innerText;
  navigator.clipboard.writeText(code).then(() => {
    btn.innerText = 'Copied!';
    setTimeout(() => { btn.innerText = 'Copy'; }, 2000);
  });
}
</script>
"""
if "function copyCode" not in html:
    html = html.replace("</body>", js_code + "</body>")

with open("regex-clipboard-mac.html", "w") as f:
    f.write(html)

print("Updated HTML!")
