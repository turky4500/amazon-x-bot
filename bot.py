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

def extract_products_from_soup(soup):
    """محاولة استخراج المنتجات بعدة طرق من الصفحة"""
    products = []
    # الطريقة 1: البحث عن روابط تحتوي على /dp/ داخل بطاقات المنتجات
    for a in soup.find_all("a", href=True):
        href = a['href']
        if '/dp/' in href:
            # تأكد من أن الرابط كامل
            if not href.startswith('http'):
                href = "https://www.amazon.sa" + href.split('?')[0]
            if re.search(r'/dp/([A-Z0-9]{10})', href):
                title_elem = a.find('span', class_=re.compile('title')) or a.find('h2') or a.find('span')
                title = title_elem.get_text(strip=True) if title_elem else 'منتج مميز'
                if len(title) > 5 and href not in [p['link'] for p in products]:
                    products.append({"title": title, "link": href})
                    if len(products) >= 10:
                        break
    return products

def fetch_todays_deals():
    """محاولة جلب عروض اليوم باستخدام طرق مرنة"""
    url = "https://www.amazon.sa/deals"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        print("🔄 جاري جلب عروض اليوم...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ فشل الاتصال بصفحة العروض: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "lxml")
    products = extract_products_from_soup(soup)
    
    if products:
        print(f"✅ تم استخراج {len(products)} عرضاً من عروض اليوم")
    else:
        print("⚠️ لم يتم العثور على عروض في صفحة اليوم، سيتم استخدام الأكثر مبيعاً كبديل.")
        # جلب من الأكثر مبيعاً
        products = fetch_bestsellers()
    return products

def fetch_bestsellers():
    """جلب المنتجات من صفحة الأكثر مبيعاً (بديل)"""
    url = "https://www.amazon.sa/gp/bestsellers"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        print("🔄 جاري جلب الأكثر مبيعاً...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")
        return []
    soup = BeautifulSoup(response.text, "lxml")
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
    print(f"✅ تم استخراج {len(products)} منتجاً من الأكثر مبيعاً")
    return products

def post_to_telegram():
    print("🔄 بدء تشغيل البوت...")
    deals = fetch_todays_deals()
    
    if not deals:
        print("❌ لا توجد عروض متاحة على الإطلاق. لن يتم الإرسال.")
        return
    
    last_deal = get_last_deal()
    if last_deal:
        deals = [d for d in deals if d["link"] != last_deal["link"]]
    
    if not deals:
        print("⚠️ جميع العروض مكررة، سيتم إرسال أول عرض متاح.")
        deals = fetch_todays_deals()[:1] if fetch_todays_deals() else fetch_bestsellers()[:1]
        if not deals:
            return
    
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
            print("✅ تم الإرسال بنجاح!")
            save_last_deal(deal)
        else:
            print(f"❌ فشل الإرسال: {r.text}")
    except Exception as e:
        print(f"⚠️ خطأ في الإرسال: {e}")

if __name__ == "__main__":
    post_to_telegram()
