import requests
import os
import random

# الإعدادات الأساسية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21" 

def post_to_telegram(photo_url, caption_text):
    # محاولة إرسال الصورة أولاً
    url_photo = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload_photo = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": photo_url,
        "caption": caption_text,
        "parse_mode": "HTML",
    }
    
    try:
        response = requests.post(url_photo, json=payload_photo)
        if response.status_code == 200:
            print("✅ تم إرسال العرض الاحترافي مع الصورة بنجاح!")
            return True
        else:
            # إذا فشلت الصورة لأي سبب، نرسل النص كرسالة عادية لضمان النشر
            print(f"⚠️ فشل إرسال الصورة (Error: {response.status_code}), جاري إرسال النص فقط...")
            url_msg = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload_msg = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": caption_text,
                "parse_mode": "HTML",
            }
            requests.post(url_msg, json=payload_msg)
            return True
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")
        return False

def run_smart_bot():
    affiliate_url = f"https://www.amazon.sa/-/en/gp/goldbox?tag={ASSOCIATE_TAG}"
    
    # قائمة الرسائل التسويقية بلهجة جذابة
    messages = [
        f"<b>🚀 صيدات الساعة من أمازون وصلت! 🇸🇦</b>\n\nلقينا لك خصومات خرافية في قسم العروض اليومية.. 🔥\n\n🛍️ <b>اقتنص الفرصة من هنا:</b>\n{affiliate_url}\n\n<i>⚡️ الحق قبل نفاذ الكمية!</i>",
        f"<b>🚨 عروض أمازون السعودية ولعت! 🔥</b>\n\nصيدات قوية بانتظارك الآن بأسعار مجنونة.. 👇\n\n🛍️ <b>تصفح كافة العروض:</b>\n{affiliate_url}\n\n<i>💸 وفر فلوسك واشتر بذكاء!</i>",
        f"<b>🔥 جديد صيدات تركي! لا تفوتها.. 🚀</b>\n\nأقوى خصومات اليوم في أمازون صارت جاهزة.. 😍\n\n🛍️ <b>للتصفح والشراء:</b>\n{affiliate_url}\n\n<i>اشترك بالقناة لتوصلك التنبيهات فوراً! ⚡️</i>"
    ]
    
    # رابط صورة عروض مستقر جداً (رابط مباشر من خادم موثوق)
    image_url = "https://images-na.ssl-images-amazon.com/images/G/01/AmazonExports/Fuji/2020/May/Hero/Fuji_TallHero_Home_v2_en_US_1x._CB429090084_.jpg"

    post_to_telegram(image_url, random.choice(messages))

if __name__ == "__main__":
    run_smart_bot()
