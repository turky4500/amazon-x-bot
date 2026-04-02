import requests
import os
import random

# الإعدادات الأساسية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def post_to_telegram():
    # هنا نضع "مخزن الصيدات" - يمكنك إضافة أي رابط منتج أعجبك هنا مستقبلاً
    # البوت سيختار واحد منها عشوائياً في كل مرة ليرسله بصورته
    deals = [
        {
            "title": "سماعة آبل إيربودز برو (الجيل الثاني) مع علبة شحن MagSafe",
            "img": "https://m.media-amazon.com/images/I/61f1Yf71HeL._AC_SL1500_.jpg",
            "link": "https://www.amazon.sa/dp/B0BDHWDR12"
        },
        {
            "title": "قلاية فيليبس الهوائية سعة 4.1 لتر - تقنية Rapid Air",
            "img": "https://m.media-amazon.com/images/I/61S9df6yS8L._AC_SL1500_.jpg",
            "link": "https://www.amazon.sa/dp/B08XWWPNC6"
        },
        {
            "title": "ماكينة حلاقة فيليبس مالتي جروم سلسلة 7000 (14 في 1)",
            "img": "https://m.media-amazon.com/images/I/81S7H8O0K5L._AC_SL1500_.jpg",
            "link": "https://www.amazon.sa/dp/B071RZMB4B"
        }
    ]
    
    # اختيار صيدة عشوائية
    deal = random.choice(deals)
    
    # إضافة كود الأرباح للرابط
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    
    # نص الرسالة (بدون تفاصيل مملة)
    caption = (
        f"<b>🔥 {deal['title']}</b>\n\n"
        f"🔗 <b>رابط الصيدة:</b>\n{final_link}\n\n"
        f"✅ <b>تم الرصد بواسطة بوت صيدات تركي</b>"
    )
    
    # رابط الإرسال للتلجرام (صورة + نص)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": deal['img'],
        "caption": caption,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ تم إرسال الصيدة بنجاح: {deal['title'][:20]}")
        else:
            print(f"❌ فشل الإرسال. السبب: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

if __name__ == "__main__":
    post_to_telegram()
    
