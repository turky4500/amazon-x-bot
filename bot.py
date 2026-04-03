import requests
import os
import random
import json
from bs4 import BeautifulSoup

# ========== الإعدادات الأساسية ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"      # ضع معرف قناتك هنا
ASSOCIATE_TAG = "tkwin-21"             # كود الأرباح الخاص بك
LAST_DEALS_FILE = "last_deals.json"    # لحفظ الروابط المرسلة سابقاً

# ========== 30 عبارة تسويقية جذابة ==========
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

# ========== دوال حفظ واسترجاع الروابط المرسلة ==========
def save_last_deals(links_list):
    """حفظ قائمة الروابط المرسلة مؤخراً"""
    try:
        with open(LAST_DEALS_FILE, "w", encoding="utf-8") as f:
            json.dump(links_list, f, ensure_ascii=False)
        print("📝 تم حفظ آخر الروابط المرسلة.")
    except Exception as e:
        print(f"⚠️ خطأ في الحفظ: {e}")

def get_last_deals():
    """استرجاع الروابط المرسلة سابقاً"""
    try:
        with open(LAST_DEALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []

# ========== جلب المنتجات من صفحة العروض (Today's Deals) ==========
def fetch_deals_from_amazon():
    """تجلب قائمة بالمنتجات من صفحة العروض في أمازون السعودية"""
    url = "https://www.amazon.sa/deals"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ فشل الاتصال بصفحة العروض: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    # البحث عن بطاقات المنتجات (يتغير حسب تحديث أمازون)
    products = soup.select("div[data-testid='product-card']")
    if not products:
        # محاولة بديلة للبحث
        products = soup.select("div.a-section[data-component-type='s-search-result']")
    if not products:
        print("⚠️ لم يتم العثور على منتجات. ربما تغيرت بنية الصفحة.")
        return []

    deals = []
    for prod in products[:15]:  # نأخذ 15 منتجاً لنتصفى منها لاحقاً
        # استخراج الرابط
        link_elem = prod.find("a", href=True)
        if not link_elem:
            continue
        link = link_elem['href']
        if not link.startswith("http"):
            link = "https://www.amazon.sa" + link.split('?')[0]  # تنظيف الرابط من المعلمات الزائدة
        
        # استخراج العنوان
        title_elem = prod.find("span", {"class": "a-truncate-full"}) or prod.find("h2") or prod.find("span", {"class": "a-size-base-plus"})
        title = title_elem.get_text(strip=True) if title_elem else "منتج مميز"
        
        deals.append({"title": title, "link": link})
    
    return deals

# ========== تصفية المنتجات الجديدة (التي لم ترسل مؤخراً) ==========
def filter_new_deals(all_deals, last_links):
    """ترجع المنتجات التي لم تظهر في آخر 20 رابطاً مرسلاً"""
    if not last_links:
        return all_deals
    last_set = set(last_links)
    new = [d for d in all_deals if d['link'] not in last_set]
    return new

# ========== بناء الرسالة النهائية (قائمة منتجات) ==========
def build_message(deals_list):
    """بناء نص الرسالة مع عبارة تسويقية في الأعلى وقائمة المنتجات"""
    if not deals_list:
        return None
    # اختيار عبارة تسويقية عشوائية للرسالة كلها
    top_phrase = random.choice(MARKETING_PHRASES)
    message = f"🛍️ <b>{top_phrase}</b>\n\n✨ <i>أحدث العروض الحصرية من أمازون السعودية:</i>\n\n"
    
    for idx, item in enumerate(deals_list[:8], 1):  # نرسل 8 منتجات كحد أقصى
        # الرابط الطويل مع كود الأرباح (بدون تقصير)
        affiliate_link = f"{item['link']}?tag={ASSOCIATE_TAG}"
        # اختصار العنوان إذا كان طويلاً جداً
        short_title = item['title'][:80] + "..." if len(item['title']) > 80 else item['title']
        message += f"{idx}. <b>{short_title}</b>\n🔗 {affiliate_link}\n\n"
    
    message += "💡 <i>اضغط على الرابط مباشرة للشراء مع شحن سريع وإرجاع مجاني.</i>"
    return message

# ========== الدالة الرئيسية للإرسال ==========
def post_to_telegram():
    print("🔄 جاري جلب أحدث العروض من أمازون...")
    all_deals = fetch_deals_from_amazon()
    
    if not all_deals:
        print("❌ فشل جلب العروض، سيتم استخدام عروض احتياطية.")
        all_deals = [
            {"title": "سماعة آبل إيربودز برو (الجيل الثاني)", "link": "https://www.amazon.sa/dp/B0CHX56W98"},
            {"title": "قلاية فيليبس الهوائية سعة 4.1 لتر", "link": "https://www.amazon.sa/dp/B08XWWPNC6"},
            {"title": "ماكينة حلاقة فيليبس مالتي جروم 7000", "link": "https://www.amazon.sa/dp/B071RZMB4B"},
            {"title": "سامسونج جالكسي S24 الترا", "link": "https://www.amazon.sa/dp/B0CSB24PTP"},
        ]
    
    last_links = get_last_deals()
    new_deals = filter_new_deals(all_deals, last_links)
    
    if not new_deals:
        # إذا كل المنتجات مكررة، نرسل عشوائياً من الكل ونحدث القائمة
        print("⚠️ جميع المنتجات مكررة، سيتم إرسال عشوائيات وإعادة تعيين القائمة.")
        selected_deals = random.sample(all_deals, min(6, len(all_deals)))
        # حفظ الروابط الجديدة
        save_last_deals([d['link'] for d in selected_deals])
    else:
        # نأخذ أول 6 منتجات جديدة (أو أقل)
        selected_deals = new_deals[:6]
        # تحديث قائمة الروابط المرسلة (نحتفظ بآخر 20 رابطاً)
        updated_links = last_links + [d['link'] for d in selected_deals]
        save_last_deals(updated_links[-20:])  # نحتفظ بآخر 20 رابط فقط
    
    message_text = build_message(selected_deals)
    if not message_text:
        print("لا توجد منتجات لعرضها.")
        return
    
    # إرسال الرسالة إلى تيليجرام
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False  # تظهر معاينة للمنتج الأول أحياناً
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ تم إرسال قائمة العروض بنجاح!")
        else:
            print(f"❌ فشل الإرسال: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ في الإرسال: {e}")

if __name__ == "__main__":
    post_to_telegram()
