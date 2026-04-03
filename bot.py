import requests
import os
import random
import json
from bs4 import BeautifulSoup

# ========== الإعدادات الأساسية ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"  # ضع معرف قناتك هنا
ASSOCIATE_TAG = "tkwin-21"         # ضع معرف الشريك الخاص بك هنا
LAST_DEAL_FILE = "last_deal.json"  # ملف لحفظ آخر منتج تم إرساله لمنع التكرار

# ========== قائمة العبارات التسويقية الجذابة ==========
MARKETING_PHRASES = [
    "🔥 عرض لمدة 24 ساعة فقط",
    "⚡ خصم يصل إلى 50%",
    "🎁 شامل ضمان لمدة سنتين",
    "🚀 الشحن المجاني اليوم فقط",
    "💎 الأكثر مبيعاً في أمازون",
    "🏆 أفضل سعر خلال 30 يوماً",
    # ... يمكنك إضافة المزيد هنا
]

def add_marketing_phrase(title):
    """تضيف عبارة تسويقية عشوائية قبل عنوان المنتج"""
    phrase = random.choice(MARKETING_PHRASES)
    return f"{phrase}\n\n{title}"

# ========== دوال منع التكرار ==========
def save_last_deal(deal):
    """حفظ بيانات آخر منتج تم إرساله"""
    try:
        with open(LAST_DEAL_FILE, "w", encoding="utf-8") as f:
            json.dump(deal, f, ensure_ascii=False, indent=2)
        print("📝 تم حفظ آخر منتج بنجاح.")
    except Exception as e:
        print(f"⚠️ خطأ أثناء حفظ آخر منتج: {e}")

def get_last_deal():
    """قراءة آخر منتج تم إرساله من الملف"""
    try:
        with open(LAST_DEAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("ℹ️ لا يوجد ملف سابق. سيتم إرسال أول منتج.")
        return None
    except Exception as e:
        print(f"⚠️ خطأ أثناء قراءة آخر منتج: {e}")
        return None

def select_unique_deal(deals, last_deal):
    """تختار منتجاً مختلفاً عن آخر منتج تم إرساله"""
    if not deals:
        return None
    if last_deal is None:
        return random.choice(deals)
    unique_deals = [d for d in deals if d["link"] != last_deal.get("link")]
    if not unique_deals:
        print("⚠️ جميع المنتجات الحالية مكررة. سيتم إرسال المنتج الأول.")
        return deals[0]
    return random.choice(unique_deals)

# ========== دالة جلب المنتجات من صفحة عروض أمازون ==========
def fetch_amazon_deals():
    """تجلب قائمة بأحدث العروض من صفحة العروض (Today's Deals) في أمازون السعودية"""
    print("🔄 جاري جلب العروض من أمازون...")
    deals_url = "https://www.amazon.sa/deals"  # صفحة العروض الرئيسية
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(deals_url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ فشل الاتصال بصفحة العروض: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    
    # البحث عن عناصر المنتجات داخل الصفحة (مع التحديث لأحدث بنية)
    # نستخدم محدداً بحثاً يجد العناوين داخل روابط المنتجات
    product_items = soup.select("div[data-testid='product-card'] a.a-link-normal[href*='/dp/']")
    
    if not product_items:
        print("⚠️ لم يتم العثور على منتجات. ربما تغيرت بنية الصفحة.")
        # إذا تغيرت الصفحة، نستخدم عروض احتياطية كحل بديل
        return []
    
    deals = []
    for item in product_items[:10]:  # نأخذ أول 10 منتجات فقط
        link = item.get('href')
        if not link.startswith("http"):
            link = "https://www.amazon.sa" + link
        
        title_element = item.find('span', recursive=False)
        title = title_element.get_text(strip=True) if title_element else "منتج مميز"
        
        deals.append({
            "title": title,
            "link": link
        })
    
    return deals

# ========== دالة بناء وإرسال الرسالة ==========
def post_to_telegram():
    """الوظيفة الرئيسية: جلب المنتجات، اختيار واحد عشوائي، وإرساله مع عبارة تسويقية"""
    deals = fetch_amazon_deals()
    
    # استخدام قائمة احتياطية في حالة فشل جلب العروض
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
    
    # إضافة كود الأرباح للرابط
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    
    # إضافة العبارة التسويقية للعنوان
    title_with_phrase = add_marketing_phrase(deal['title'])
    
    # بناء نص الرسالة مع التنبيه إلى أن العرض من صفحة العروض
    message_text = (
        f"<b>{title_with_phrase}</b>\n\n"
        f"<i>✨ هذا العرض مُستورد من صفحة عروض أمازون الحصرية ✨</i>\n\n"
        f"🔗 <b>رابط الشراء المباشر:</b>\n{final_link}\n\n"
        f"💡 <i>تذكر: العروض لفترة محدودة، فلا تتردد!</i>"
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
            print("✅ تم الإرسال بنجاح مع عرض من صفحة العروض!")
            save_last_deal(deal)
        else:
            print(f"❌ فشل الإرسال: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ في الإرسال: {e}")

# ========== تشغيل البوت ==========
if __name__ == "__main__":
    post_to_telegram()
