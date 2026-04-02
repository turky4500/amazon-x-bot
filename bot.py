import requests
import os
import random

# الإعدادات الأساسية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def post_to_telegram():
    # مخزن الصيدات المختارة
    deals = [
        {
            "title": "🔥 سماعة آبل إيربودز برو (الجيل الثاني) الأصلية",
            "link": "https://www.amazon.sa/dp/B0BDHWDR12"
        },
        {
            "title": "🚀 قلاية فيليبس الهوائية سعة 4.1 لتر - الأكثر مبيعاً",
            "link": "https://www.amazon.sa/dp/B08XWWPNC6"
        },
        {
            "title": "⚡️ ماكينة حلاقة فيليبس مالتي جروم (14 في 1)",
            "link": "https://www.amazon.sa/dp/B071RZMB4B"
        }
    ]
    
    # اختيار صيدة عشوائية
    deal = random.choice(deals)
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    
    # نص الرسالة المختصر والمباشر
    message_text = (
        f"<b>{deal['title']}</b>\n\n"
        f"🔗 <b>رابط الصيدة مباشرة:</b>\n{final_link}\n\n"
        f"✅ <b>تم الرصد بواسطة بوت صيدات تركي</b>"
    )
    
    # استخدام sendMessage بدلاً من sendPhoto لتجنب أخطاء الروابط
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False  # هذا السطر سيجعل التلجرام يجلب صورة المنتج تلقائياً
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ تم بنجاح! تفقد القناة الآن.")
        else:
            print(f"❌ فشل: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    post_to_telegram()
    
