import json

with open('locales.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

key_free_trial = "free trial, then<br>$6.99 one-time"
key_pro = "Free 14-day trial · No credit card · Search anything you've ever copied · Upgrade to Pro for $6.99"
key_purchase = "$6.99 · one-time purchase · 14-day free trial"
key_sup = "<sup>$</sup>6.99"

updates = {
    "vi": {
        key_free_trial: "dùng thử miễn phí, sau đó<br>₫119,000.00 thanh toán một lần",
        key_pro: "Dùng thử miễn phí 14 ngày · Không cần thẻ tín dụng · Tìm kiếm mọi thứ bạn đã từng sao chép · Nâng cấp lên bản Pro với giá ₫119,000.00",
        key_purchase: "₫119,000.00 · mua một lần · 14 ngày dùng thử miễn phí",
        key_sup: "<sup>₫</sup>119,000.00"
    }
}

for lang, vals in updates.items():
    if lang in data:
        for k, v in vals.items():
            data[lang][k] = v

with open('locales.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

