import requests
import os
import random
import json
import re
import time
import logging
from datetime import datetime
from bs4 import BeautifulSoup

# ========== الإعدادات الأساسية ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"
LAST_DEAL_FILE = "last_deal.json"
# ========== تحديد مصدر العروض ==========
SOURCE = "bestsellers"  # غيّر إلى "todays_deals" أو "prime_deals" حسب الرغبة

# ========== 30 عبارة تسويقية ==========
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
    "🎯 صفقة اليوم الحصرية",
    "🔋 شحن مجاني لجميع المدن",
    "💰 استرداد الضريبة متاح",
    "📉 سعر منخفض قياسي",
    "🏅 موصى به من قبل الخبراء",
    "🎉 أقوى عروض الصيف",
    "💪 جودة عالية بثمن منخفض",
    "🎁 هدية مجانية مع كل طلب",
    "⏳ يتبقى فقط 5 قطع",
    "🏠 مناسب لكل العائلة",
    "📱 متوافق مع أحدث الإصدارات",
    "🔒 شراء آمن 100%",
    "👨‍👩‍👧‍👦 هدية مثالية للأحباب",
    "🏷️ كود خصم إضافي عند الدفع",
    "🌟 منتج حاصل على جائزة",
    "🎯 العرض لمشاهدي القناة فقط",
    "🔄 إرجاع مجاني خلال 30 يوماً",
    "🏆 اختيار المحررين",
    "🎁 عرض خاص بمناسبة التخفيضات"
]

def add_marketing_phrase(title):
    phrase = random.choice(MARKETING_PHRASES)
    return f"{phrase}\n\n{title}"

def save_last_deal(deal):
    try:
        with open(LAST_DEAL_FILE, "w", encoding="utf-8") as f:
            json.dump(deal, f, ensure_ascii=False)
        print("📝 تم حفظ آخر منتج.")
    except Exception as e:
        print(f"⚠️ خطأ في الحفظ: {e}")

def get_last_deal():
    try:
        with open(LAST_DEAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def is_valid_amazon_link(link):
    return bool(re.search(r'/dp/([A-Z0-9]{10})', link))

def fetch_bestsellers():
    url = "https://www.amazon.sa/gp/bestsellers"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        print("🔄 جاري جلب العروض من صفحة الأكثر مبيعاً...")
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
            if is_valid_amazon_link(link):
                products.append({"title": title, "link": link})
        if len(products) >= 10:
            break
    print(f"✅ تم استخراج {len(products)} منتجاً.")
    return products

def fetch_todays_deals():
    url = "https://www.amazon.sa/deals"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        print("🔄 جاري جلب العروض من صفحة عروض اليوم...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")
        return []
    soup = BeautifulSoup(response.text, "lxml")
    products = []
    for item in soup.select("div[data-testid='product-card']"):
        link_elem = item.find("a", href=True)
        if link_elem:
            link = link_elem["href"]
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link.split('?')[0]
            if is_valid_amazon_link(link):
                title_elem = item.find("span", {"class": "a-truncate-full"}) or item.find("h2")
                title = title_elem.get_text(strip=True) if title_elem else "منتج مميز"
                products.append({"title": title, "link": link})
        if len(products) >= 10:
            break
    print(f"✅ تم استخراج {len(products)} منتجاً.")
    return products

def fetch_prime_deals():
    url = "https://www.amazon.sa/prime/deals"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        print("🔄 جاري جلب العروض من صفحة عروض البرايم...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ فشل الاتصال: {e}")
        return []
    soup = BeautifulSoup(response.text, "lxml")
    products = []
    for item in soup.select("div[data-testid='product-card']"):
        link_elem = item.find("a", href=True)
        if link_elem:
            link = link_elem["href"]
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link.split('?')[0]
            if is_valid_amazon_link(link):
                title_elem = item.find("span", {"class": "a-truncate-full"}) or item.find("h2")
                title = title_elem.get_text(strip=True) if title_elem else "منتج مميز"
                products.append({"title": title, "link": link})
        if len(products) >= 10:
            break
    print(f"✅ تم استخراج {len(products)} منتجاً.")
    return products

def fetch_deals():
    src = SOURCE.lower()
    if src == "bestsellers":
        return fetch_bestsellers()
    elif src == "todays_deals":
        return fetch_todays_deals()
    elif src == "prime_deals":
        return fetch_prime_deals()
    else:
        print(f"⚠️ مصدر غير معروف: {SOURCE}. سيتم استخدام الأكثر مبيعاً.")
        return fetch_bestsellers()

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
    print("🔄 بدء تشغيل البوت...")
    deals = fetch_deals()
    if not deals:
        print("❌ لا توجد عروض. لن يتم الإرسال.")
        return
    last = get_last_deal()
    deal = select_unique_deal(deals, last)
    if not deal:
        return
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    title_with_phrase = add_marketing_phrase(deal['title'])
    msg = f"<b>{title_with_phrase}</b>\n\n🔗 <b>رابط الشراء المباشر:</b>\n{final_link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
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
        print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    post_to_telegram()
