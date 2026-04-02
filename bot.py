import requests
import os
import random

# الإعدادات الأساسية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def post_to_telegram():
    # مخزن الصيدات بروابط كاملة ومباشرة لضمان العمل 100%
    deals = [
        {
            "title": "🔥 سماعة آبل إيربودز برو (الجيل الثاني) مع علبة شحن USB-C",
            "link": "https://www.amazon.sa/-/en/Apple-AirPods-Pro-2nd-generation-with-MagSafe-Case-USB-C/dp/B0CHX56W98"
        },
        {
            "title": "🚀 قلاية فيليبس الهوائية سعة 4.1 لتر - تقنية Rapid Air لطهي صحي",
            "link": "https://www.amazon.sa/-/en/Philips-Essential-Airfryer-Technology-Black-HD9200-90/dp/B08XWWPNC6"
        },
        {
            "title": "⚡️ ماكينة حلاقة فيليبس مالتي جروم سلسلة 7000 (14 في 1) للوجه والشعر",
            "link": "https://www.amazon.sa/-/en/Philips-Multigroom-Series-Trimmer-MG7720-15/dp/B071RZMB4B"
        },
        {
            "title": "📱 هاتف سامسونج جالكسي S24 الترا - ذاكرة 256 جيجابايت",
            "link": "https://www.amazon.sa/-/en/Samsung-Galaxy-S24-Ultra-256GB/dp/B0CSB24PTP"
        }
    ]
    
    # اختيار صيدة عشوائية
    deal = random.choice(deals)
    
    # ربط كود الأرباح بالرابط الكامل بطريقة صحيحة
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    
    # نص الرسالة المباشر
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
            print(f"✅ تم الإرسال بنجاح! الرابط الآن يعمل 100%.")
        else:
            print(f"❌ فشل: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    post_to_telegram()
    
