import re

with open("regex-clipboard-mac.html", "r") as f:
    html = f.read()

new_row = """        <tr style="border-bottom: 1px solid var(--border);">
          <td style="padding: 20px; vertical-align: top;">
            <strong>Bash Native Match (=~)</strong><br><br>
            <span style="font-size: 14px; color: var(--text-muted);">If you are running a script or command directly in a Bash terminal, you don't even need external tools like Python or grep. Bash has a built-in regular expression matching operator (<code>=~</code>). The <code>[[ ... =~ ... ]]</code> construct evaluates the string against the regex pattern natively inside the shell.</span>
          </td>
          <td style="padding: 20px; vertical-align: top;">
            <div class="snippet-container" style="margin-bottom:0;"><button class="copy-btn" onclick="copyCode(this)">Copy</button><pre><code>email="test@example.com"
[[ "$email" =~ ^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$ ]] && echo "Match" || echo "No Match"</code></pre></div>
          </td>
        </tr>
"""

# Insert right after <tbody>
html = html.replace("<tbody>", "<tbody>\n" + new_row)

with open("regex-clipboard-mac.html", "w") as f:
    f.write(html)

with open("/Users/dinesh/.gemini/antigravity-ide/brain/ee7b57cb-20bc-46c4-94e0-ecf31e104df6/medium_regex_article.md", "r") as f:
    md = f.read()

new_md_section = """### 1. Bash Native Regex Match (=~)
If you are running a script or command directly in a Bash terminal, you don't even need external tools like Python or grep. Bash has a built-in regular expression matching operator (`=~`).

```bash
email="test@example.com"
[[ "$email" =~ ^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$ ]] && echo "Match" || echo "No Match"
```

How it works: The `[[ ... =~ ... ]]` construct evaluates the string against the regex pattern natively inside the shell.

### 2. Bash (grep)"""

md = md.replace("### 1. Bash (grep)", new_md_section)
# shift remaining numbers
md = md.replace("### 2. Ruby One-Liner", "### 3. Ruby One-Liner")
md = md.replace("### 3. Python Script", "### 4. Python Script")
# update the intro text "three ways" to "four ways"
md = md.replace("Here are three ways", "Here are four ways")
md = md.replace("here are three foolproof ways", "here are four foolproof ways")

with open("/Users/dinesh/.gemini/antigravity-ide/brain/ee7b57cb-20bc-46c4-94e0-ecf31e104df6/medium_regex_article.md", "w") as f:
    f.write(md)

print("Updates applied.")
