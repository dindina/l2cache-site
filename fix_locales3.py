import json

with open('locales.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

key_free_trial = "free trial, then<br>$6.99 one-time"
key_pro = "Free 14-day trial · No credit card · Search anything you've ever copied · Upgrade to Pro for $6.99"
key_purchase = "$6.99 · one-time purchase · 14-day free trial"
key_sup = "<sup>$</sup>6.99"

updates = {
    "ja": {
        key_free_trial: "無料トライアル、その後<br>1000¥の一括払い",
        key_pro: "14日間無料トライアル · クレジットカード不要 · これまでにコピーしたすべてのものを検索 · 1000¥でProにアップグレード",
        key_purchase: "1000¥ · 買い切り · 14日間の無料トライアル",
        key_sup: "1000<sup>¥</sup>"
    }
}

for lang, vals in updates.items():
    if lang in data:
        for k, v in vals.items():
            data[lang][k] = v

with open('locales.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

