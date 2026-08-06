import json

with open('locales.json', 'r', encoding='utf-8') as f:
    locales = json.load(f)

key_replacements = {
    "14 days": {
        "new_key": "Free",
        "translations": {
            "zh-Hans": "免费",
            "fr": "Gratuit",
            "de": "Kostenlos",
            "it": "Gratis",
            "ja": "無料",
            "ko": "무료",
            "pt-BR": "Gratuito",
            "es": "Gratis",
            "vi": "Miễn phí"
        }
    },
    "free trial, then<br>$6.99 one-time": {
        "new_key": "for a limited time<br>get it now",
        "translations": {
            "zh-Hans": "限时免费<br>立即获取",
            "fr": "pour une durée limitée<br>obtenez-le maintenant",
            "de": "für kurze Zeit<br>jetzt holen",
            "it": "per un periodo limitato<br>scaricalo ora",
            "ja": "期間限定<br>今すぐゲット",
            "ko": "한시적 무료<br>지금 받으세요",
            "pt-BR": "por tempo limitado<br>baixe agora",
            "es": "por tiempo limitado<br>consíguelo ahora",
            "vi": "trong thời gian giới hạn<br>tải ngay"
        }
    },
    "Free 14-day trial · No credit card · Search anything you've ever copied · Upgrade to Pro for $6.99": {
        "new_key": "Free for a limited time · No credit card · Search anything you've ever copied",
        "translations": {
            "zh-Hans": "限时免费 · 无需信用卡 · 搜索你复制过的任何内容",
            "fr": "Gratuit pour une durée limitée · Aucune carte de crédit · Recherchez tout ce que vous avez copié",
            "de": "Für kurze Zeit kostenlos · Keine Kreditkarte · Durchsuchen Sie alles, was Sie jemals kopiert haben",
            "it": "Gratis per un periodo limitato · Nessuna carta di credito · Cerca qualsiasi cosa tu abbia mai copiato",
            "ja": "期間限定で無料 · クレジットカード不要 · コピーしたすべての履歴を検索",
            "ko": "한시적 무료 · 신용카드 불필요 · 복사했던 모든 내용을 검색하세요",
            "pt-BR": "Gratuito por tempo limitado · Sem cartão de crédito · Pesquise qualquer coisa que você já copiou",
            "es": "Gratis por tiempo limitado · Sin tarjeta de crédito · Busca cualquier cosa que hayas copiado",
            "vi": "Miễn phí trong thời gian giới hạn · Không cần thẻ tín dụng · Tìm kiếm mọi thứ bạn đã từng sao chép"
        }
    },
    "No subscription. No upsell. Pay once, use forever.": {
        "new_key": "No subscription. No upsell. Free for a limited time.",
        "translations": {
            "zh-Hans": "没有订阅。没有追加销售。限时免费。",
            "fr": "Pas d'abonnement. Pas de vente incitative. Gratuit pour une durée limitée.",
            "de": "Kein Abo. Kein Upselling. Für kurze Zeit kostenlos.",
            "it": "Nessun abbonamento. Nessun upsell. Gratis per un periodo limitato.",
            "ja": "サブスクリプションなし。アップセルなし。期間限定で無料。",
            "ko": "구독 없음. 추가 결제 없음. 한시적 무료.",
            "pt-BR": "Sem assinatura. Sem vendas adicionais. Gratuito por tempo limitado.",
            "es": "Sin suscripciones. Sin ventas adicionales. Gratis por tiempo limitado.",
            "vi": "Không đăng ký. Không bán thêm. Miễn phí trong thời gian giới hạn."
        }
    },
    "<sup>$</sup>6.99": {
        "new_key": "Free",
        "translations": {
            "zh-Hans": "免费",
            "fr": "Gratuit",
            "de": "Kostenlos",
            "it": "Gratis",
            "ja": "無料",
            "ko": "무료",
            "pt-BR": "Gratuito",
            "es": "Gratis",
            "vi": "Miễn phí"
        }
    },
    "introductory price · one-time purchase · all future updates included": {
        "new_key": "for a limited time · all future updates included",
        "translations": {
            "zh-Hans": "限时免费 · 包含所有未来更新",
            "fr": "pour une durée limitée · toutes les mises à jour futures incluses",
            "de": "für kurze Zeit · alle zukünftigen Updates inklusive",
            "it": "per un periodo limitato · tutti i futuri aggiornamenti inclusi",
            "ja": "期間限定 · 今後のすべてのアップデートが含まれます",
            "ko": "한시적 무료 · 향후 모든 업데이트 포함",
            "pt-BR": "por tempo limitado · todas as atualizações futuras incluídas",
            "es": "por tiempo limitado · todas las actualizaciones futuras incluidas",
            "vi": "trong thời gian giới hạn · bao gồm tất cả các bản cập nhật trong tương lai"
        }
    },
    "macOS 13 Ventura or later · 14-day free trial": {
        "new_key": "macOS 13 Ventura or later · Free for a limited time",
        "translations": {
            "zh-Hans": "macOS 13 Ventura 或更高版本 · 限时免费",
            "fr": "macOS 13 Ventura ou ultérieur · Gratuit pour une durée limitée",
            "de": "macOS 13 Ventura oder neuer · Für kurze Zeit kostenlos",
            "it": "macOS 13 Ventura o successivo · Gratis per un periodo limitato",
            "ja": "macOS 13 Ventura以降 · 期間限定で無料",
            "ko": "macOS 13 Ventura 이상 · 한시적 무료",
            "pt-BR": "macOS 13 Ventura ou posterior · Gratuito por tempo limitado",
            "es": "macOS 13 Ventura o posterior · Gratis por tiempo limitado",
            "vi": "macOS 13 Ventura trở lên · Miễn phí trong thời gian giới hạn"
        }
    },
    "$6.99 · one-time purchase · 14-day free trial": {
        "new_key": "Free for a limited time",
        "translations": {
            "zh-Hans": "限时免费",
            "fr": "Gratuit pour une durée limitée",
            "de": "Für kurze Zeit kostenlos",
            "it": "Gratis per un periodo limitato",
            "ja": "期間限定で無料",
            "ko": "한시적 무료",
            "pt-BR": "Gratuito por tempo limitado",
            "es": "Gratis por tiempo limitado",
            "vi": "Miễn phí trong thời gian giới hạn"
        }
    }
}

for old_key, update_info in key_replacements.items():
    new_key = update_info["new_key"]
    translations = update_info["translations"]
    
    for lang, trans_dict in locales.items():
        if old_key in trans_dict:
            del trans_dict[old_key]
        trans_dict[new_key] = translations.get(lang, translations["en"] if "en" in translations else new_key)

with open('locales.json', 'w', encoding='utf-8') as f:
    json.dump(locales, f, ensure_ascii=False, indent=2)

print("Updated locales.json")
