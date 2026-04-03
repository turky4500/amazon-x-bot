import requests
import os
import random
import json
import re
from bs4 import BeautifulSoup

# ========== الإعدادات الأساسية ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"
LAST_DEAL_FILE = "last_deal.json"

# ========== 30 عبارة تسويقية ==========
MARKETING_PHRASES = [
    "🔥 عرض لمدة 24 ساعة فقط", "⚡ خصم يصل إلى 50%", "🎁 شامل ضمان لمدة سنتين",
    "🚀 الشحن المجاني اليوم فقط", "💎 الأكثر مبيعاً في أمازون", "🏆 أفضل سعر خلال 30 يوماً",
    "✨ إدخال رائع للمنزل", "💥 كمية محدودة - لا تفوتك", "📦 وصول سريع خلال 24 ساعة",
    "🛒 أضف إلى السلة الآن", "⭐ تقييم 4.5 نجوم فما فوق", "🎯 صفقة اليوم الحصرية",
    "🔋 شحن مجاني لجميع المدن", "💰 استرداد الضريبة متاح", "📉 سعر منخفض قياسي",
    "🏅 موصى به من قبل الخبراء", "🎉 أقوى عروض الصيف", "💪 جودة عالية بثمن منخفض",
    "🎁 هدية مجانية مع كل طلب", "⏳ يتبقى فقط 5 قطع", "🏠 مناسب لكل العائلة",
    "📱 متوافق مع أحدث الإصدارات", "🔒 شراء آمن 100%", "👨‍👩‍👧‍👦 هدية مثالية للأحباب",
    "🏷️ كود خصم إضافي عند الدفع", "🌟 منتج حاصل على جائزة", "🎯 العرض لمشاهدي القناة فقط",
    "🔄 إرجاع مجاني خلال 30 يوماً", "🏆 اختيار المحررين", "🎁 عرض خاص بمناسبة التخفيضات"
]

def add_marketing_phrase(title):
    phrase = random.choice(MARKETING_PHRASES)
    return f"{phrase}\n\n{title}"

def save_last_deal(deal):
    try:
        with open(LAST_DEAL_FILE, "w", encoding="utf-8") as f:
            json.dump(deal, f, ensure_ascii=False)
    except:
        pass

def get_last_deal():
    try:
        with open(LAST_DEAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def fetch_bestsellers():
    url = "https://www.amazon.sa/gp/bestsellers"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    products = []
    for item in soup.select("div.p13n-sc-truncate-desktop-type2"):
        title = item.get_text(strip=True)
        parent = item.find_parent("a")
        if parent and parent.get("href"):
            link = parent["href"]
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link.split('?')[0]
            if re.search(r'/dp/([A-Z0-9]{10})', link):
                products.append({"title": title, "link": link})
        if len(products) >= 10:
            break
    return products

def select_unique_deal(deals, last_deal):
    if not deals:
        return None
    if last_deal is None:
        return random.choice(deals)
    unique = [d for d in deals if d["link"] != last_deal.get("link")]
    if not unique:
        return deals[0]
    return random.choice(unique)

def post_to_telegram():
    print("🔄 جاري جلب العروض...")
    deals = fetch_bestsellers()
    if not deals:
        deals = [
            {"title": "سماعة آبل إيربودز برو (الجيل الثاني)", "link": "https://www.amazon.sa/dp/B0CHX56W98"},
            {"title": "قلاية فيليبس الهوائية سعة 4.1 لتر", "link": "https://www.amazon.sa/dp/B08XWWPNC6"},
        ]
    last = get_last_deal()
    deal = select_unique_deal(deals, last)
    if not deal:
        return
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    title_with_phrase = add_marketing_phrase(deal['title'])
    message_text = f"<b>{title_with_phrase}</b>\n\n🔗 <b>رابط الشراء المباشر:</b>\n{final_link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            print("✅ تم إرسال عرض واحد بنجاح!")
            save_last_deal(deal)
        else:
            print(f"❌ فشل: {resp.text}")
    except Exception as e:
        print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    post_to_telegram()
