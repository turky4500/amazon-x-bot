import requests
import os
import random
import json
import re
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"
LAST_DEAL_FILE = "last_deal.json"

MARKETING_PHRASES = [
    "🔥 عرض لمدة 24 ساعة فقط",
    "⚡ خصم يصل إلى 50%",
    "🎁 شامل ضمان لمدة سنتين",
    "🚀 الشحن المجاني اليوم فقط",
    "💎 الأكثر مبيعاً في أمازون",
    "🏆 أفضل سعر خلال 30 يوماً",
    "✨ إدخال رائع للمنزل",
    "💥 كمية محدودة - لا تفوتك",
    "📦 وصول سريع خلال 24 ساعة",
    "🛒 أضف إلى السلة الآن",
    "⭐ تقييم 4.5 نجوم فما فوق",
    "🎯 صفقة اليوم الحصرية"
]

def add_marketing_phrase(title):
    return f"{random.choice(MARKETING_PHRASES)}\n\n{title}"

def save_last_deal(deal):
    with open(LAST_DEAL_FILE, "w", encoding="utf-8") as f:
        json.dump(deal, f, ensure_ascii=False)

def get_last_deal():
    try:
        with open(LAST_DEAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def fetch_todays_deals():
    """جلب العروض من صفحة Today's Deals (عروض اليوم)"""
    url = "https://www.amazon.sa/deals"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        print("🔄 جاري جلب عروض اليوم من أمازون...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "lxml")
    products = []
    
    # البحث عن بطاقات العروض (قد يتغير selector لكن هذه الأحدث)
    cards = soup.select("div[data-testid='product-card']")
    if not cards:
        # محاولة بديلة
        cards = soup.select("div.a-section[data-component-type='s-search-result']")
    
    for card in cards[:20]:  # نأخذ أول 20 عرضاً
        # استخراج الرابط
        link_elem = card.find("a", href=True)
        if not link_elem:
            continue
        link = link_elem["href"]
        if not link.startswith("http"):
            link = "https://www.amazon.sa" + link.split('?')[0]
        
        # التأكد من صحة الرابط (يحتوي على /dp/)
        if not re.search(r'/dp/([A-Z0-9]{10})', link):
            continue
        
        # استخراج العنوان
        title_elem = card.find("span", {"class": "a-truncate-full"}) or card.find("h2") or card.find("span", {"class": "a-size-base-plus"})
        title = title_elem.get_text(strip=True) if title_elem else "منتج مميز"
        
        # تنظيف العنوان من المسافات الزائدة
        title = ' '.join(title.split())
        
        products.append({"title": title, "link": link})
        if len(products) >= 10:
            break
    
    print(f"✅ تم استخراج {len(products)} عرضاً من عروض اليوم")
    return products

def post_to_telegram():
    print("🔄 بدء تشغيل بوت عروض اليوم...")
    deals = fetch_todays_deals()
    
    if not deals:
        print("❌ لا توجد عروض اليوم. لن يتم إرسال أي شيء.")
        return
    
    last_deal = get_last_deal()
    if last_deal:
        deals = [d for d in deals if d["link"] != last_deal["link"]]
    
    if not deals:
        print("⚠️ جميع العروض مكررة، سيتم إرسال أول عرض.")
        deals = fetch_todays_deals()[:1]
    
    deal = random.choice(deals)
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    title_with_phrase = add_marketing_phrase(deal['title'])
    
    message = f"<b>{title_with_phrase}</b>\n\n🔗 <b>رابط الشراء المباشر:</b>\n{final_link}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print("✅ تم إرسال عرض اليوم بنجاح!")
            save_last_deal(deal)
        else:
            print(f"❌ فشل الإرسال: {r.text}")
    except Exception as e:
        print(f"⚠️ خطأ في الإرسال: {e}")

if __name__ == "__main__":
    post_to_telegram()
