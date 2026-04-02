import requests
from bs4 import BeautifulSoup
import os
import random

# الإعدادات الأساسية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def get_real_deal():
    # رابط العروض المباشرة
    url = "https://www.amazon.sa/-/en/gp/goldbox"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # البحث عن كروت المنتجات
        items = soup.find_all('div', {'data-testid': 'grid-desktop-card'})
        if not items:
            items = soup.select('.octopus-pc-item-content')

        if items:
            item = random.choice(items)
            
            # 1. جلب العنوان
            title_tag = item.find(['h2', 'span'], class_=True)
            title = title_tag.get_text().strip() if title_tag else "عرض خاص من أمازون"
            
            # 2. جلب الصورة
            img_tag = item.find('img')
            img_url = img_tag['src'] if img_tag else ""
            
            # 3. جلب الرابط وإضافة كودك tkwin-21
            link_tag = item.find('a', href=True)
            raw_link = link_tag['href']
            if not raw_link.startswith('http'):
                raw_link = "https://www.amazon.sa" + raw_link
            final_link = raw_link.split('?')[0] + f"?tag={ASSOCIATE_TAG}"
            
            return title, img_url, final_link
    except:
        pass
    return None, None, None

def post_to_telegram():
    title, img, link = get_real_deal()
    
    if title and img and link:
        # نص الرسالة: اسم المنتج + الرابط (بدون فلسفة زايدة)
        caption = (
            f"<b>{title}</b>\n\n"
            f"🔗 <b>رابط العرض:</b>\n{link}\n\n"
            f"✅ <b>تم الرصد بواسطة بوت صيدات تركي</b>"
        )
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "photo": img,
            "caption": caption,
            "parse_mode": "HTML"
        }
        
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("✅ تم إرسال الصيدة بنجاح!")
            return

    print("❌ فشل في جلب منتج محدد.")

if __name__ == "__main__":
    post_to_telegram()
    
