with open("regex-clipboard-mac.html", "r") as f:
    html = f.read()

old_desc = 'No external tools needed. Bash\'s built-in <code>=~</code> operator matches a string against a regex pattern natively inside the shell.'

new_desc = 'No external tools needed. Add this function to your <code>~/.zshrc</code> — it takes any text as <code>$1</code> and a regex pattern as <code>$2</code>, matching entirely inside the shell with no external tools.'

old_code = '''email="test@example.com"
[[ "$email" =~ ^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9.]+$ ]] && echo "Match" || echo "No Match"'''

new_code = '''# Add to ~/.zshrc
matchregex() {
  [[ "$1" =~ $2 ]] && echo "Match: $1" || echo "No Match: $1"
}

# Usage — pass text as $1 and pattern as $2:
matchregex "test@example.com" "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9.]+$"
matchregex "123e4567-e89b-12d3-a456-426614174000" "^[0-9a-fA-F-]{36}$"'''

html = html.replace(old_desc, new_desc)
html = html.replace(old_code, new_code)

with open("regex-clipboard-mac.html", "w") as f:
    f.write(html)

print("Updated!" if old_code not in html else "FAILED - old code still present")
