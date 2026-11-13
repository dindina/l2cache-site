"""Single source for the price shown on the site.

Pages write tokens like {{PRICE}}; build.py and site_i18n.py call apply() on the output.
Text that only makes sense during the launch offer goes inside {{LAUNCH_ONLY}}…{{/LAUNCH_ONLY}};
it is kept while "launch" is true and removed otherwise.
To change the price, edit pricing.json at the repo root and rebuild.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICING_FILE = os.path.join(ROOT, "pricing.json")
SYMBOLS = {"USD": "$"}
TOKEN = re.compile(r"\{\{([A-Z][A-Z_]*)\}\}")
LAUNCH_BLOCK = re.compile(r"\{\{LAUNCH_ONLY\}\}(.*?)\{\{/LAUNCH_ONLY\}\}", re.S)


def _money(raw, currency):
    # "29.00" -> "$29", "19.99" -> "$19.99"
    amount = raw[:-3] if raw.endswith(".00") else raw
    return f"{SYMBOLS.get(currency, currency + ' ')}{amount}"


def tokens(path=PRICING_FILE):
    with open(path, encoding="utf-8") as f:
        p = json.load(f)
    price, regular = _money(p["price"], p["currency"]), _money(p["regular_price"], p["currency"])
    launch = p["launch"]
    return {
        "PRICE": price if launch else regular,
        "PRICE_RAW": p["price"] if launch else p["regular_price"],
        "REGULAR_PRICE": regular,
        "REGULAR_PRICE_RAW": p["regular_price"],
        "CURRENCY": p["currency"],
        "TRIAL_DAYS": str(p["trial_days"]),
        "PRICE_LINE": f"{price} launch price ({regular} regular)" if launch else regular,
        "_LAUNCH": launch,
    }


def apply(text, values=None):
    """Replace every {{TOKEN}}; an unknown token stops the build."""
    values = values or tokens()
    text = LAUNCH_BLOCK.sub(lambda m: m.group(1) if values["_LAUNCH"] else "", text)

    def sub(m):
        if m.group(1) not in values or m.group(1).startswith("_"):
            raise SystemExit(f"pricing: unknown token {m.group(0)}")
        return values[m.group(1)]

    return TOKEN.sub(sub, text)


def apply_file(path, values=None):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    new = apply(text, values)
    if new != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)


if __name__ == "__main__":
    for k, v in tokens().items():
        if not k.startswith("_"):
            print(f"{{{{{k}}}}} = {v}")
