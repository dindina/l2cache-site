with open("regex-clipboard-mac.html", "r") as f:
    html = f.read()

# Find the full table and replace it
import re

new_table = """<table style="table-layout: fixed; width: 100%; border-collapse: collapse; text-align: left; background: rgba(255,255,255,0.03); border-radius: 12px; overflow: hidden; border: 1px solid var(--border);">
      <thead>
        <tr style="background: rgba(127,119,221,0.1); border-bottom: 1px solid var(--border);">
          <th style="padding: 16px 20px; font-family: var(--sans); font-weight: 600; color: var(--text); width: 30%;">Method</th>
          <th style="padding: 16px 20px; font-family: var(--sans); font-weight: 600; color: var(--text); width: 70%;">Code Snippet</th>
        </tr>
      </thead>
      <tbody>
        <!-- Bash =~ -->
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top;">
            <strong>Bash Native (=~)</strong>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0; line-height: 1.5;">No external tools needed. Bash's built-in <code>=~</code> operator matches a string against a regex pattern natively inside the shell.</p>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>email="test@example.com"
[[ "$email" =~ ^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9.]+$ ]] && echo "Match" || echo "No Match"</code></pre></div>
          </td>
        </tr>
        <!-- Bash grep -->
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top;">
            <strong>Bash (grep)</strong>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0; line-height: 1.5;">Uses <code>pbpaste</code> to read the clipboard, <code>grep -oE</code> to extract all email matches, and <code>pbcopy</code> to write results back.</p>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>pbpaste | grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}' | pbcopy</code></pre></div>
          </td>
        </tr>
        <!-- Ruby -->
        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top;">
            <strong>Ruby One-Liner</strong>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0; line-height: 1.5;">Extracts all UUIDs from the clipboard. Ruby's native regex engine is pre-installed on older Macs, or available via Homebrew.</p>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>pbpaste | ruby -ne 'puts $_.scan(/\\b[0-9a-fA-F\\-]{36}\\b/)' | pbcopy</code></pre></div>
          </td>
        </tr>
        <!-- Python -->
        <tr>
          <td style="padding: 20px; vertical-align: top;">
            <strong>Python Script</strong>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px; margin-bottom: 0; line-height: 1.5;">Reads clipboard via <code>subprocess</code> and extracts AWS Access Key IDs using Python's <code>re</code> module. Handles case-insensitivity natively.</p>
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
    </table>"""

# Replace entire table block
html = re.sub(
    r'<table style="width: 100%; border-collapse:.*?</table>',
    new_table,
    html,
    flags=re.DOTALL
)

with open("regex-clipboard-mac.html", "w") as f:
    f.write(html)

print("Table rewritten successfully!")
