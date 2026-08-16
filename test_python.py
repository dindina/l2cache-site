import sys, base64, json
def dec(s):
    return json.loads(base64.b64decode(s + '=' * (-len(s) % 4)))
h, p, s = sys.argv[1].split('.')
print(json.dumps({'header': dec(h), 'payload': dec(p), 'signature': s}, indent=2))
