import requests
from bs4 import BeautifulSoup
import os
import random
import time

# الإعدادات
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def get_amazon_deal():
    # رابط العروض اليومية
    url = "https://www.amazon.sa/-/en/gp/goldbox"
    
    # محاكاة متصفح حقيقي وتغيير "البصمة الرقمية" لتجنب الحظر
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]),
        "Accept-Language": "en-US,en;q=0.9,ar-SA;q=0.8",
        "Referer": "https://www.google.com/"
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # البحث عن المنتجات بعدة طرق (لأن أمازون تغير الكود باستمرار)
        # الطريقة الأولى: شبكة العروض
        items = soup.find_all('div', {'data-testid': 'grid-desktop-card'})
        
        # الطريقة الثانية: إذا فشلت الأولى (البحث عن الروابط التي تحتوي على منتجات)
        if not items:
            items = soup.find_all('div', class_='a-section octopus-pc-item-content')

        if items:
            # فلترة المنتجات التي تحتوي على روابط صحيحة وصور
            valid_items = []
            for i in items:
                link = i.find('a', href=True)
                img = i.find('img')
                if link and img:
                    valid_items.append(i)
            
            if valid_items:
                item = random.choice(valid_items)
                
                # استخراج العنوان
                title = "عرض مميز من صيدات تركي"
                title_tag = item.find(['h2', 'span', 'div'], class_=True)
                if title_tag:
                    title = title_tag.get_text().strip()[:100]

                # استخراج الصورة
                img_url = item.find('img')['src']
                
                # استخراج الرابط وتحويله لأرباح
                raw_link = item.find('a', href=True)['href']
                if not raw_link.startswith('http'):
                    raw_link = "https://www.amazon.sa" + raw_link
                
                # تنظيف الرابط من الزوائد وإضافة كودك tkwin-21
                clean_link = raw_link.split('/ref=')[0] if '/ref=' in raw_link else raw_link
                final_link = f"{clean_link}?tag={ASSOCIATE_TAG}"
                
                return title, img_url, final_link
            
    except Exception as e:
        print(f"Error Scrapping: {e}")
    
    return None, None, None

def post_to_telegram():
    title, img, link = get_amazon_deal()
    
    # إذا فشل الرادار في سحب منتج، نرسل عرضاً "يدوياً" جذاباً
    if not title:
        title = "أقوى الصيدات والخصومات اليومية 🔥"
        img = "https://m.media-amazon.com/images/I/71R2oVwM5lL._AC_SL1500_.jpg"
        link = f"https://www.amazon.sa/-/en/gp/goldbox?tag={ASSOCIATE_TAG}"

    messages = [
        f"<b>🚨 لقطة اليوم يا مدير! 🔥</b>\n\n📦 <b>المنتج:</b> {title}\n\n🔗 <b>رابط الصيدة مباشرة:</b>\n{link}\n\n<i>⚡️ الكمية تخلص بسرعة، الحق!</i>",
        f"<b>🚀 جديد صيدات تركي من أمازون! 🇸🇦</b>\n\n🛍️ <b>شف وش لقينا لك الآن:</b>\n{title}\n\n💰 <b>رابط العرض والحجز:</b>\n{link}\n\n<i>💸 وفّر قروشك واشتر بذكاء!</i>",
        f"<b>🔥 خصم قوي بانتظارك الآن! 😍</b>\n\n✅ <b>تفاصيل المنتج:</b>\n{title}\n\n🔗 <b>تصفح العرض من هنا:</b>\n{link}\n\n<i>💡 اشترك وفعل التنبيهات لأقوى العروض!</i>"
    ]
    
    caption = random.choice(messages)
    
    # إرسال الصورة مع النص
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": img,
        "caption": caption,
        "parse_mode": "HTML"
    }
    
    requests.post(url, json=payload)
    print("✅ تم النشر بنجاح!")

if __name__ == "__main__":
    post_to_telegram()
    
