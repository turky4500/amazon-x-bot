import requests
import os
import random

# الإعدادات
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"

def post_to_telegram():
    # رابط العروض العام مع كود الأرباح الخاص بك
    affiliate_url = f"https://www.amazon.sa/-/en/gp/goldbox?tag={ASSOCIATE_TAG}"
    
    # نصوص تسويقية جذابة ومختصرة لضمان الوصول
    messages = [
        f"<b>🚀 صيدات الساعة من أمازون وصلت! 🇸🇦</b>\n\nلقينا لك خصومات خرافية في قسم العروض اليومية.. 🔥\n\n🛍️ <b>تصفح العروض واقتنص الفرصة:</b>\n{affiliate_url}\n\n<i>⚡️ الحق قبل نفاذ الكمية!</i>",
        f"<b>🚨 عروض أمازون السعودية ولعت! 🔥</b>\n\nصيدات قوية بانتظارك الآن بأسعار مجنونة.. 👇\n\n🛍️ <b>تصفح كافة العروض من هنا:</b>\n{affiliate_url}\n\n<i>💸 وفر قروشك واشتر بذكاء!</i>",
        f"<b>🔥 جديد صيدات تركي! لا تفوتها.. 🚀</b>\n\nأقوى خصومات اليوم في أمازون صارت جاهزة.. 😍\n\n🛍️ <b>للتصفح والشراء المباشر:</b>\n{affiliate_url}\n\n<i>✅ تم الرصد بواسطة بوت صيدات تركي</i>"
    ]
    
    selected_message = random.choice(messages)
    
    # رابط الإرسال (نص فقط لضمان النجاح 100%)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": selected_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False # لإظهار معاينة بسيطة للرابط
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ تم الإرسال بنجاح! تفقد القناة الآن.")
        else:
            print(f"❌ فشل الإرسال. السبب: {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

if __name__ == "__main__":
    post_to_telegram()
    
