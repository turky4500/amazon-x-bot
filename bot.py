import requests
import os
import random

# الإعدادات الأساسية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def post_to_telegram():
    # مخزن صيدات بروابط مختصرة ومجربة (تفتح 100%)
    deals = [
        {
            "title": "🔥 سماعة آبل إيربودز برو (الجيل الثاني) الأصلية",
            "link": "https://www.amazon.sa/dp/B0CHX56W98"
        },
        {
            "title": "🚀 قلاية فيليبس الهوائية سعة 4.1 لتر - تقنية Rapid Air",
            "link": "https://www.amazon.sa/dp/B08XWWPNC6"
        },
        {
            "title": "⚡️ ماكينة حلاقة فيليبس مالتي جروم سلسلة 7000 (14 في 1)",
            "link": "https://www.amazon.sa/dp/B071RZMB4B"
        },
        {
            "title": "📱 هاتف سامسونج جالكسي S24 الترا - 256 جيجابايت",
            "link": "https://www.amazon.sa/dp/B0CSB24PTP"
        }
    ]
    
    # اختيار صيدة عشوائية
    deal = random.choice(deals)
    
    # ربط كود الأرباح بالرابط المختصر
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    
    # نص الرسالة المباشر والواضح
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
        "disable_web_page_preview": False  # تفعيل المعاينة لإظهار الصورة
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ تم الإرسال بنجاح! الرابط المختصر يعمل الآن.")
        else:
            print(f"❌ فشل: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    post_to_telegram()
    
