import requests
import os
import random
import json
from bs4 import BeautifulSoup

# ========== الإعدادات الأساسية ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"
LAST_DEAL_FILE = "last_deal.json"

# ========== قائمة العبارات التسويقية الجاذبة (30 عبارة) ==========
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

# ========== دالة إضافة عبارة تسويقية عشوائية ==========
def add_marketing_phrase(title):
    phrase = random.choice(MARKETING_PHRASES)
    return f"{phrase}\n\n{title}"

# ========== دالة تقصير الرابط ==========
def shorten_url(long_url):
    try:
        api_url = f"https://tinyurl.com/api-create.php?url={long_url}"
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200 and response.text.startswith("https://tinyurl.com/"):
            print(f"🔗 تم تقصير الرابط بنجاح: {response.text}")
            return response.text
        else:
            print(f"⚠️ فشل تقصير الرابط، سيتم إرسال الرابط الطويل.")
            return long_url
    except Exception as e:
        print(f"⚠️ خطأ أثناء تقصير الرابط: {e}")
        return long_url

# ========== دالة حفظ آخر منتج ==========
def save_last_deal(deal):
    try:
        with open(LAST_DEAL_FILE, "w", encoding="utf-8") as f:
            json.dump(deal, f, ensure_ascii=False, indent=2)
        print("📝 تم حفظ آخر منتج بنجاح.")
    except Exception as e:
        print(f"⚠️ خطأ أثناء حفظ آخر منتج: {e}")

# ========== دالة قراءة آخر منتج ==========
def get_last_deal():
    try:
        with open(LAST_DEAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("ℹ️ لا يوجد ملف سابق. سيتم إرسال أول منتج.")
        return None
    except Exception as e:
        print(f"⚠️ خطأ أثناء قراءة آخر منتج: {e}")
        return None

# ========== دالة جلب العروض من أمازون ==========
def fetch_amazon_deals():
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
    product_items = soup.select("div.p13n-sc-truncate-desktop-type2")
    
    if not product_items:
        print("⚠️ لم يتم العثور على منتجات. ربما تغيرت بنية الصفحة.")
        return []
    
    deals = []
    for item in product_items[:10]:
        title = item.get_text(strip=True)
        parent_link = item.find_parent("a")
        if parent_link and parent_link.get("href"):
            link = parent_link["href"]
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link
        else:
            continue
        
        deals.append({
            "title": title,
            "link": link
        })
    
    return deals

# ========== دالة اختيار منتج مختلف ==========
def select_unique_deal(deals, last_deal):
    if not deals:
        return None
    
    if last_deal is None:
        return random.choice(deals)
    
    unique_deals = [d for d in deals if d["link"] != last_deal.get("link")]
    
    if not unique_deals:
        print("⚠️ جميع المنتجات الحالية مكررة لآخر منتج. سيتم إرسال المنتج الأول.")
        return deals[0]
    
    return random.choice(unique_deals)

# ========== دالة الإرسال إلى تيليجرام ==========
def post_to_telegram():
    print("🔄 جاري جلب العروض من أمازون...")
    deals = fetch_amazon_deals()
    
    if not deals:
        print("❌ لا توجد عروض متاحة. سيتم استخدام العروض الاحتياطية.")
        deals = [
            {"title": "🔥 سماعة آبل إيربودز برو (الجيل الثاني) الأصلية", "link": "https://www.amazon.sa/dp/B0CHX56W98"},
            {"title": "🚀 قلاية فيليبس الهوائية سعة 4.1 لتر", "link": "https://www.amazon.sa/dp/B08XWWPNC6"},
            {"title": "⚡️ ماكينة حلاقة فيليبس مالتي جروم سلسلة 7000", "link": "https://www.amazon.sa/dp/B071RZMB4B"},
        ]
    
    last_deal = get_last_deal()
    deal = select_unique_deal(deals, last_deal)
    if deal is None:
        print("❌ لا يمكن اختيار منتج. الخروج.")
        return
    
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    short_link = shorten_url(final_link)
    title_with_phrase = add_marketing_phrase(deal['title'])
    
    message_text = (
        f"<b>{title_with_phrase}</b>\n\n"
        f"🔗 <b>رابط الشراء المباشر:</b>\n{short_link}"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ تم الإرسال بنجاح مع عبارة تسويقية!")
            save_last_deal(deal)
        else:
            print(f"❌ فشل الإرسال: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ في الإرسال: {e}")

# ========== تشغيل البوت ==========
if __name__ == "__main__":
    post_to_telegram()
