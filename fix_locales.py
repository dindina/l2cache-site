import json

with open('locales.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

key_free_trial = "free trial, then<br>$6.99 one-time"
key_pro = "Free 14-day trial · No credit card · Search anything you've ever copied · Upgrade to Pro for $6.99"
key_purchase = "$6.99 · one-time purchase · 14-day free trial"
key_sup = "<sup>$</sup>6.99"

updates = {
    "pt-BR": {
        key_free_trial: "de teste grátis, depois<br>R$18.49 em pagamento único",
        key_pro: "Teste grátis de 14 dias · Sem cartão de crédito · Pesquise tudo que você já copiou · Atualize para o Pro por R$18.49",
        key_purchase: "R$18.49 · compra única · teste grátis de 14 dias",
        key_sup: "<sup>R$</sup>18.49"
    }
}

for lang, vals in updates.items():
    if lang in data:
        for k, v in vals.items():
            if k in data[lang]:
                data[lang][k] = v

with open('locales.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

