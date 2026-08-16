import subprocess, re
text = subprocess.check_output('pbpaste', text=True)
matches = re.findall(r'(?i)AKIA[0-9A-Z]{16}', text)
subprocess.run(['pbcopy'], input='\n'.join(matches), text=True)
print(f"Extracted {len(matches)} keys.")
