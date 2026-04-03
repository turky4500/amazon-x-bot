import requests
import os
import random
import json
import re
from bs4 import BeautifulSoup

# ========== الإعدادات الأساسية ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"        # ضع معرف قناتك هنا
ASSOCIATE_TAG = "tkwin-21"               # كود الأرباح الخاص بك
LAST_DEAL_FILE = "last_deal.json"        # ملف لحفظ آخر منتج تم إرساله

# ========== 30 عبارة تسويقية جذابة ==========
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
    """إضافة عبارة تسويقية عشوائية قبل عنوان المنتج"""
    phrase = random.choice(MARKETING_PHRASES)
    return f"{phrase}\n\n{title}"

def save_last_deal(deal):
    """حفظ آخر منتج تم إرساله"""
    try:
        with open(LAST_DEAL_FILE, "w", encoding="utf-8") as f:
            json.dump(deal, f, ensure_ascii=False)
        print("📝 تم حفظ آخر منتج.")
    except Exception as e:
        print(f"⚠️ خطأ في الحفظ: {e}")

def get_last_deal():
    """قراءة آخر منتج تم إرساله"""
    try:
        with open(LAST_DEAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception:
        return None

def fetch_bestsellers():
    """جلب المنتجات من صفحة الأكثر مبيعاً في أمازون السعودية"""
    url = "https://www.amazon.sa/gp/bestsellers"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ فشل الاتصال بأمازون: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    products = []

    # الطريقة الأساسية للبحث
    for item in soup.select("div.p13n-sc-truncate-desktop-type2"):
        title = item.get_text(strip=True)
        parent = item.find_parent("a")
        if parent and parent.get("href"):
            link = parent["href"]
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link.split('?')[0]
            # التأكد من أن الرابط يحتوي على ASIN صحيح
            if re.search(r'/dp/([A-Z0-9]{10})', link):
                products.append({"title": title, "link": link})
        if len(products) >= 10:
            break

    # طريقة بديلة إذا فشلت الأولى
    if not products:
        for a in soup.select("a.a-link-normal[href*='/dp/']"):
            link = a.get("href")
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link.split('?')[0]
            title_elem = a.select_one("span") or a.find("div")
            title = title_elem.get_text(strip=True) if title_elem else "منتج مميز"
            if link and "/dp/" in link:
                products.append({"title": title, "link": link})
            if len(products) >= 10:
                break

    return products

def select_unique_deal(deals, last_deal):
    """اختيار منتج مختلف عن آخر منتج تم إرساله"""
    if not deals:
        return None
    if last_deal is None:
        return random.choice(deals)
    # تصفية المنتجات التي لا تساوي آخر منتج (مقارنة بالرابط)
    unique_deals = [d for d in deals if d["link"] != last_deal.get("link")]
    if not unique_deals:
        # إذا كانت كل المنتجات مكررة، نرسل أول منتج
        return deals[0]
    return random.choice(unique_deals)

def post_to_telegram():
    """الدالة الرئيسية: جلب العروض، اختيار منتج فريد، إرساله مع عبارة تسويقية"""
    print("🔄 جاري جلب العروض من أمازون...")
    deals = fetch_bestsellers()

    # قائمة احتياطية في حالة فشل الجلب
    if not deals:
        print("❌ لا توجد عروض متاحة. سيتم استخدام العروض الاحتياطية.")
        deals = [
            {"title": "سماعة آبل إيربودز برو (الجيل الثاني)", "link": "https://www.amazon.sa/dp/B0CHX56W98"},
            {"title": "قلاية فيليبس الهوائية سعة 4.1 لتر", "link": "https://www.amazon.sa/dp/B08XWWPNC6"},
            {"title": "ماكينة حلاقة فيليبس مالتي جروم 7000", "link": "https://www.amazon.sa/dp/B071RZMB4B"},
            {"title": "سامسونج جالكسي S24 الترا", "link": "https://www.amazon.sa/dp/B0CSB24PTP"},
        ]

    last_deal = get_last_deal()
    deal = select_unique_deal(deals, last_deal)
    if deal is None:
        print("❌ لا يمكن اختيار منتج. الخروج.")
        return

    # إضافة كود الأرباح للرابط الطويل (بدون تقصير)
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"

    # إضافة عبارة تسويقية للعنوان
    title_with_phrase = add_marketing_phrase(deal['title'])

    # بناء نص الرسالة
    message_text = (
        f"<b>{title_with_phrase}</b>\n\n"
        f"🔗 <b>رابط الشراء المباشر:</b>\n{final_link}"
    )

    # إرسال إلى تيليجرام
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False  # معاينة الصفحة
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ تم إرسال العرض بنجاح!")
            save_last_deal(deal)
        else:
            print(f"❌ فشل الإرسال: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ في الإرسال: {e}")

if __name__ == "__main__":
    post_to_telegram()
