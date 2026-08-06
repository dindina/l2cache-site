import json

with open('locales.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

key_free_trial = "free trial, then<br>$6.99 one-time"
key_pro = "Free 14-day trial · No credit card · Search anything you've ever copied · Upgrade to Pro for $6.99"
key_purchase = "$6.99 · one-time purchase · 14-day free trial"
key_sup = "<sup>$</sup>6.99"

updates = {
    "fr": {
        key_free_trial: "d'essai gratuit, puis<br>6,99€ en une seule fois",
        key_pro: "Essai gratuit de 14 jours · Aucune carte de crédit · Recherchez tout ce que vous avez copié · Passez à la version Pro pour 6,99€",
        key_purchase: "6,99€ · achat unique · essai gratuit de 14 jours",
        key_sup: "6,99<sup>€</sup>"
    },
    "de": {
        key_free_trial: "kostenlos testen, dann<br>6,99€ einmalig",
        key_pro: "Kostenlose 14-Tage-Testversion · Keine Kreditkarte · Durchsuchen Sie alles, was Sie je kopiert haben · Upgrade auf Pro für 6,99€",
        key_purchase: "6,99€ · Einmaliger Kauf · 14 Tage kostenlose Testversion",
        key_sup: "6,99<sup>€</sup>"
    },
    "it": {
        key_free_trial: "di prova gratuita, poi<br>6,99€ una tantum",
        key_pro: "Prova gratuita di 14 giorni · Nessuna carta di credito · Cerca qualsiasi cosa tu abbia mai copiato · Passa a Pro per 6,99€",
        key_purchase: "6,99€ · acquisto una tantum · prova gratuita di 14 giorni",
        key_sup: "6,99<sup>€</sup>"
    },
    "es": {
        key_free_trial: "de prueba gratis, luego<br>6,99€ un pago único",
        key_pro: "Prueba gratuita de 14 días · Sin tarjeta de crédito · Busca cualquier cosa que hayas copiado · Actualiza a Pro por 6,99€",
        key_purchase: "6,99€ · compra única · prueba gratuita de 14 días",
        key_sup: "6,99<sup>€</sup>"
    },
    "ko": {
        key_free_trial: "무료 체험 후<br>₩6,600.00 일회성 구매",
        key_pro: "14일 무료 평가판 · 신용카드 불필요 · 복사했던 모든 것 검색 · ₩6,600.00로 Pro 업그레이드",
        key_purchase: "₩6,600.00 · 일회성 구매 · 14일 무료 평가판",
        key_sup: "<sup>₩</sup>6,600.00"
    },
    "ja": {
        key_free_trial: "無料トライアル、その後<br>¥1,100.00の一括払い",
        key_pro: "14日間無料トライアル · クレジットカード不要 · これまでにコピーしたすべてのものを検索 · ¥1,100.00でProにアップグレード",
        key_purchase: "¥1,100.00 · 買い切り · 14日間の無料トライアル",
        key_sup: "<sup>¥</sup>1,100.00"
    },
    "zh-Hans": {
        key_free_trial: "免费试用，之后<br>一次性支付 ¥48.00",
        key_pro: "14 天免费试用 · 无需信用卡 · 搜索你复制过的任何内容 · 升级到专业版只需 ¥48.00",
        key_purchase: "¥48.00 · 一次性购买 · 14 天免费试用",
        key_sup: "<sup>¥</sup>48.00"
    },
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
            # Force add if missing, since some languages missed the HTML tags in translation!
            data[lang][k] = v

with open('locales.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

