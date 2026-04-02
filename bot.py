import requests
from bs4 import BeautifulSoup
import os
import random
import time

# الإعدادات الأساسية (تأكد أن الـ Token في الـ Secrets)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def get_amazon_deal():
    # رابط قسم العروض اليومية في أمازون السعودية
    url = "https://www.amazon.sa/-/en/gp/goldbox"
    
    # محاكاة متصفح حقيقي لتجنب الحظر
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # البحث عن كروت المنتجات في الصفحة
        items = soup.select('div[data-testid="grid-desktop-card"]')
        
        if not items:
            # إذا لم يجد شبكة العروض، نبحث بتنسيق بديل
            items = soup.select('.a-section.octopus-pc-item-content')

        if items:
            # اختيار منتج عشوائي من القائمة
            item = random.choice(items)
            
            # 1. استخراج الاسم
            title_tag = item.select_one('h2') or item.select_one('.a-truncate-full') or item.select_one('.octopus-pc-dotd-title')
            title = title_tag.text.strip() if title_tag else "عرض مميز من أمازون السعودية"
            
            # 2. استخراج الصورة
            img_tag = item.find('img')
            img_url = img_tag['src'] if img_tag else "https://m.media-amazon.com/images/G/01/AmazonExports/Fuji/2020/May/Hero/Fuji_TallHero_Home_v2_en_US_1x._CB429090084_.jpg"
            
            # 3. استخراج الرابط وتحويله لأرباح
            link_tag = item.find('a', href=True)
            if link_tag:
                raw_link = link_tag['href']
                if not raw_link.startswith('http'):
                    raw_link = "https://www.amazon.sa" + raw_link
                # تنظيف الرابط وإضافة كود الأرباح tkwin-21
                clean_link = raw_link.split('?')[0] + f"?tag={ASSOCIATE_TAG}"
            else:
                clean_link = f"https://www.amazon.sa/-/en/gp/goldbox?tag={ASSOCIATE_TAG}"
            
            return title, img_url, clean_link
            
    except Exception as e:
        print(f"Error: {e}")
    
    return None, None, None

def post_to_telegram():
    title, img, link = get_amazon_deal()
    
    if not title:
        print("⚠️ لم يتم العثور على منتج محدد، سأرسل العرض العام.")
        title = "عروض الصيدات اليومية في أمازون 🇸🇦"
        img = "https://m.media-amazon.com/images/G/01/AmazonExports/Fuji/2020/May/Hero/Fuji_TallHero_Home_v2_en_US_1x._CB429090084_.jpg"
        link = f"https://www.amazon.sa/-/en/gp/goldbox?tag={ASSOCIATE_TAG}"

    # نصوص تسويقية جذابة
    marketing_texts = [
        f"<b>🔥 لقطة اليوم من أمازون! 🇸🇦</b>\n\n📦 <b>المنتج:</b> {title[:120]}...\n\n🔗 <b>اطلبه الآن قبل نفاذ الكمية:</b>\n{link}\n\n<i>⚡️ صيدات تركي - وفّر قروشك!</i>",
        f"<b>🚨 عرض محدود لا يفوتك! 🔥</b>\n\n✅ <b>لقينا لك هذا العرض:</b>\n{title[:120]}\n\n💰 <b>رابط الشراء مباشرة:</b>\n{link}\n\n<i>💡 تفقد العرض الآن، الخصم قوي!</i>",
        f"<b>📢 عروض الساعات من أمازون وصلت! 😍</b>\n\n🛍️ <b>شف وش جبنا لك:</b>\n{title[:120]}\n\n🔗 <b>رابط العرض والحجز:</b>\n{link}\n\n<i>✅ تم الرصد بواسطة بوت صيدات تركي</i>"
    ]
    
    caption = random.choice(marketing_texts)
    
    # إرسال الصورة مع النص للتلجرام
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": img,
        "caption": caption,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"✅ تم النشر بنجاح: {title[:30]}")
    else:
        print(f"❌ فشل النشر: {response.text}")

if __name__ == "__main__":
    post_to_telegram()
    
