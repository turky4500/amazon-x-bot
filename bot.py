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
LAST_DEALS_FILE = "last_deals.json"

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

# ========== حفظ واسترجاع الروابط المرسلة ==========
def save_last_deals(links):
    try:
        with open(LAST_DEALS_FILE, "w", encoding="utf-8") as f:
            json.dump(links, f)
    except:
        pass

def get_last_deals():
    try:
        with open(LAST_DEALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# ========== جلب المنتجات من صفحة الأكثر مبيعاً (ثابتة أكثر) ==========
def fetch_bestsellers():
    url = "https://www.amazon.sa/gp/bestsellers"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except:
        return []

    soup = BeautifulSoup(r.text, "lxml")
    products = []

    # الطريقة الأولى: البحث عن عناوين المنتجات داخل div مخصص
    for item in soup.select("div.p13n-sc-truncate-desktop-type2"):
        title = item.get_text(strip=True)
        parent = item.find_parent("a")
        if parent and parent.get("href"):
            link = parent["href"]
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link.split('?')[0]  # تنظيف الرابط
            # استخراج ASIN للتأكد من صحة الرابط
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', link)
            if asin_match:
                products.append({"title": title, "link": link})
        if len(products) >= 12:
            break

    # إذا لم نجد بالطريقة الأولى، نبحث بطريقة بديلة
    if not products:
        for link_elem in soup.select("a.a-link-normal[href*='/dp/']"):
            link = link_elem.get("href")
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link.split('?')[0]
            title_elem = link_elem.select_one("span") or link_elem.find("div")
            title = title_elem.get_text(strip=True) if title_elem else "منتج مميز"
            if link and "/dp/" in link:
                products.append({"title": title, "link": link})
            if len(products) >= 12:
                break

    return products

# ========== تصفية المنتجات الجديدة ==========
def filter_new(all_deals, last_links):
    if not last_links:
        return all_deals
    return [d for d in all_deals if d['link'] not in last_links]

# ========== بناء الرسالة ==========
def build_message(deals):
    if not deals:
        return None
    phrase = random.choice(MARKETING_PHRASES)
    msg = f"🛍️ <b>{phrase}</b>\n\n✨ <i>أحدث العروض الحصرية من أمازون السعودية:</i>\n\n"
    for i, item in enumerate(deals[:6], 1):
        aff_link = f"{item['link']}?tag={ASSOCIATE_TAG}"
        title = item['title'][:70] + "..." if len(item['title']) > 70 else item['title']
        msg += f"{i}. <b>{title}</b>\n🔗 {aff_link}\n\n"
    msg += "💡 <i>اضغط على الرابط مباشرة للشراء مع شحن سريع وإرجاع مجاني.</i>"
    return msg

# ========== الإرسال إلى تيليجرام ==========
def post_to_telegram():
    print("🔄 جاري جلب أفضل العروض من أمازون...")
    deals = fetch_bestsellers()

    # قائمة احتياطية قوية فقط في حال فشل الجلب التام
    if not deals:
        print("❌ فشل الجلب، استخدام قائمة احتياطية محدثة.")
        deals = [
            {"title": "سماعة آبل إيربودز برو (الجيل الثاني)", "link": "https://www.amazon.sa/dp/B0CHX56W98"},
            {"title": "قلاية فيليبس الهوائية سعة 4.1 لتر", "link": "https://www.amazon.sa/dp/B08XWWPNC6"},
            {"title": "ماكينة حلاقة فيليبس مالتي جروم 7000", "link": "https://www.amazon.sa/dp/B071RZMB4B"},
            {"title": "سامسونج جالكسي S24 الترا", "link": "https://www.amazon.sa/dp/B0CSB24PTP"},
        ]

    last_links = get_last_deals()
    new_deals = filter_new(deals, last_links)

    if not new_deals:
        # إذا كلها مكررة، نرسل عشوائياً من الكل ونحدث القائمة
        selected = random.sample(deals, min(6, len(deals)))
        save_last_deals([d['link'] for d in selected])
    else:
        selected = new_deals[:6]
        updated = last_links + [d['link'] for d in selected]
        save_last_deals(updated[-20:])

    msg = build_message(selected)
    if not msg:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            print("✅ تم إرسال قائمة العروض بنجاح!")
        else:
            print(f"❌ فشل الإرسال: {resp.text}")
    except Exception as e:
        print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    post_to_telegram()
