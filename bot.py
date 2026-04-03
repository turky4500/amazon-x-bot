import requests
import os
import random
from bs4 import BeautifulSoup

# ========== الإعدادات الأساسية ==========
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"   # يمكنك لاحقاً جعلها متغير بيئة
ASSOCIATE_TAG = "tkwin-21"

# ========== دالة جلب العروض الحقيقية من أمازون ==========
def fetch_amazon_deals():
    """
    تجلب منتجات من صفحة "أفضل مبيعاً" في أمازون السعودية.
    تعيد قائمة من القواميس، كل قاموس يحتوي على title و link.
    """
    url = "https://www.amazon.sa/gp/bestsellers"  # صفحة الأكثر مبيعاً
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # يتوقف إذا كان هناك خطأ في الاتصال
    except Exception as e:
        print(f"❌ فشل الاتصال بأمازون: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "lxml")
    
    # نبحث عن عناصر المنتجات داخل الصفحة
    # ملاحظة: أمازون تغير الكلاسات أحياناً، هذه الكلاسات تعمل حالياً
    product_items = soup.select("div.p13n-sc-truncate-desktop-type2")  # عناوين المنتجات
    
    if not product_items:
        print("⚠️ لم يتم العثور على منتجات. ربما تغيرت بنية الصفحة.")
        return []
    
    deals = []
    for item in product_items[:10]:  # نأخذ أول 10 منتجات فقط
        title_element = item
        title = title_element.get_text(strip=True)
        
        # نحاول إيجاد الرابط (قد يكون موجوداً في العنصر الأب)
        parent_link = item.find_parent("a")
        if parent_link and parent_link.get("href"):
            link = parent_link["href"]
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link
        else:
            continue  # إذا لم نجد رابط، نتخطى هذا المنتج
        
        deals.append({
            "title": title,
            "link": link
        })
    
    return deals

# ========== دالة الإرسال إلى تيليجرام ==========
def post_to_telegram():
    print("🔄 جاري جلب العروض من أمازون...")
    deals = fetch_amazon_deals()
    
    if not deals:
        print("❌ لا توجد عروض متاحة. سيتم استخدام العروض الاحتياطية.")
        # عروض احتياطية في حال فشل السكراب
        deals = [
            {"title": "🔥 سماعة آبل إيربودز برو (الجيل الثاني) الأصلية", "link": "https://www.amazon.sa/dp/B0CHX56W98"},
            {"title": "🚀 قلاية فيليبس الهوائية سعة 4.1 لتر", "link": "https://www.amazon.sa/dp/B08XWWPNC6"},
            {"title": "⚡️ ماكينة حلاقة فيليبس مالتي جروم سلسلة 7000", "link": "https://www.amazon.sa/dp/B071RZMB4B"},
        ]
    
    # اختيار صيدة عشوائية من العروض التي جلبناها
    deal = random.choice(deals)
    
    # إضافة كود الأرباح
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    
    # نص الرسالة
    message_text = (
        f"<b>{deal['title']}</b>\n\n"
        f"🔗 <b>رابط الشراء المباشر:</b>\n{final_link}\n\n"
        f"✅ <b>تم الرصد بواسطة بوت صيدات تركي</b>"
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
            print("✅ تم الإرسال بنجاح مع عروض حقيقية من أمازون!")
        else:
            print(f"❌ فشل الإرسال: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ في الإرسال: {e}")

# ========== تشغيل البوت ==========
if __name__ == "__main__":
    post_to_telegram()
