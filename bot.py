import requests
import os

# جلب المفتاح الرسمي من خزنة GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# رابط قناتك العامة (المعرف الرسمي)
TELEGRAM_CHAT_ID = "@amazonturky" 

def send_to_telegram(text):
    # رابط API التلجرام للإرسال
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML", # لاستخدام التنسيقات مثل العريض والروابط
        "disable_web_page_preview": False # لإظهار معاينة لرابط أمازون
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ مبروك يا أبو علي! أول صيدة وصلت للقناة بنجاح.")
        else:
            print(f"❌ فشل الإرسال. رمز الخطأ: {response.status_code}")
            print(f"السبب: {response.text}")
            print("تنبيه: تأكد أن البوت مضاف كـ Admin في قناة @amazonturky")
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

if __name__ == "__main__":
    # نص الرسالة الاحترافي الذي سيظهر للمشتركين في قناتك
    message = (
        "<b>📢 صيدات أمازون السعودية وصلت! 🇸🇦</b>\n\n"
        "بدأت الآن أقوى العروض اليومية بخصومات كبرى.. 🔥\n\n"
        "🔗 <b>تصفح العروض واقتنص الفرصة قبل النفاذ:</b>\n"
        "https://www.amazon.sa/-/en/gp/goldbox\n\n"
        "<i>اشترك في القناة لتوصلك التنبيهات فوراً! ⚡️</i>"
    )
    send_to_telegram(message)
