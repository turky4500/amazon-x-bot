import requests
from bs4 import BeautifulSoup
import os
import random

# الإعدادات
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def get_random_amazon_deal():
    url = "https://www.amazon.sa/-/en/gp/goldbox"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # البحث عن المنتجات في الصفحة (أمازون تغير الكلاسات أحياناً، نستخدم بحثاً مرناً)
        items = soup.select('div[data-testid="grid-desktop-card"]')
        
        if not items:
            return None, None, None

        # اختيار منتج عشوائي من القائمة
        item = random.choice(items)
        
        # استخراج الاسم
        title = item.select_one('h2') or item.select_one('.a-truncate-full')
        title_text = title.text.strip() if title else "عرض مميز من أمازون"
        
        # استخراج الصورة
        img = item.find('img')
        img_url = img['src'] if img else "https://m.media-amazon.com/images/I/71R2oVwM5lL._AC_SL1500_.jpg"
        
        # استخراج الرابط وتحويله لأرباح
        link_tag = item.find('a', href=True)
        raw_link = "https://www.amazon.sa" + link_tag['href'] if link_tag else url
        # تنظيف الرابط وإضافة كود الأرباح
        clean_link = raw_link.split('?')[0] + f"?tag={ASSOCIATE_TAG}"
        
        return title_text, img_url, clean_link
    except Exception as e:
        print(f"Error fetching deals: {e}")
        return None, None, None

def post_to_telegram():
    title, img, link = get_random_amazon_deal()
    
    if not title:
        print("❌ لم يتم العثور على منتجات حالياً، سأحاول لاحقاً.")
        return

    # عبارات تسويقية منوعة
    marketing_phrases = [
        f"<b>🔥 صيدة اليوم من أمازون! 🇸🇦</b>\n\n📦 <b>المنتج:</b> {title[:100]}...\n\n💰 <b>الحق على العرض من هنا:</b>\n{link}\n\n<i>⚡️ الكمية محدودة، اطلب الآن!</i>",
        f"<b>🚨 لقطة لا تفوتك يا مدير! 🔥</b>\n\n✅ <b>وصلنا هذا العرض الآن:</b>\n{title[:100]}\n\n🔗 <b>رابط الشراء مباشرة:</b>\n{link}\n\n<i>💸 وفر قروشك واقتنص الصيدات!</i>",
        f"<b>📢 عرض حصري في أمازون السعودية! 😍</b>\n\n🛍️ <b>شف وش لقينا لك:</b>\n{title[:100]}\n\n🔗 <b>رابط العرض:</b>\n{link}\n\n<i>💡 اشترك وفعل التنبيهات لأقوى العروض!</i>"
    ]
    
    caption = random.choice(marketing_phrases)
    
    # إرسال الصورة مع النص
    url_photo = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": img,
        "caption": caption,
        "parse_mode": "HTML"
    }
    
    requests.post(url_photo, json=payload)
    print(f"✅ تم نشر منتج عشوائي بنجاح: {title[:30]}...")

if __name__ == "__main__":
    post_to_telegram()
    
