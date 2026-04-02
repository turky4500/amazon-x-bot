import requests
import os
import re

# الإعدادات الأساسية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
# هوية الأرباح الخاصة بك يا أبو علي
ASSOCIATE_TAG = "tkwin-21" 

def post_photo_to_telegram(photo_url, caption_text):
    # رابط API التلجرام لإرسال الصورة مع النص
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": photo_url,
        "caption": caption_text,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except:
        return False

def get_amazon_deals_with_photo():
    # رابط قسم العروض اليومية في أمازون السعودية
    base_url = "https://www.amazon.sa/-/en/gp/goldbox"
    # تحويل الرابط إلى رابط أرباح خاص بك
    affiliate_url = f"{base_url}?tag={ASSOCIATE_TAG}"
    
    # --- كلام تسويقي جذاب من إنشائي (أبو علي) ---
    marketing_messages = [
        f"<b>🚀 لا تفوتك صيدات الساعة من أمازون! 🇸🇦</b>\n\nلقينا لك خصومات خرافية على قسم العروض اليومية.. 🔥\n🛍️ <b>اقتنص الفرصة قبل نفاذ الكمية:</b>\n{affiliate_url}\n\n<i>⚡️ الحق على اللي يعجبك!</i>",
        
        f"<b>🚨 عروض أمازون السعودية ولعت! 🔥</b>\n\nصيدات قوية وخصومات كبرى بانتظارك الآن.. 👇\n🛍️ <b>تصفح كافة العروض من هنا:</b>\n{affiliate_url}\n\n<i>💸 وفّر فلوسك واشتر بذكاء!</i>",
        
        f"<b>📢 بدأت أقوى عروض اليوم في أمازون! 🇸🇦</b>\n\nجهزنا لك أبرز الخصومات على منتجات مختارة.. 😍\n🛍️ <b>تصفح العروض من هنا:</b>\n{affiliate_url}\n\n<i>💡 النصيحة: العروض تتغير بسرعة!</i>",
        
        f"<b>🔥 صيدات تركي وصلت! لا تفوتها.. 🚀</b>\n\nعروض أمازون السعودية جارية الآن بأسعار مجنونة.. 🔥\n🛍️ <b>تصفح كافة العروض من هنا:</b>\n{affiliate_url}\n\n<i>اشترك في القناة لتوصلك التنبيهات فوراً! ⚡️</i>"
    ]
    
    # اختيار رسالة عشوائية لتنويع الكلام التسويقي
    import random
    selected_message = random.choice(marketing_messages)
    
    # --- جلب صورة العرض الافتراضية ---
    # نستخدم صورة عامة لعروض أمازون لضمان الاستقرار (لاحقاً يمكن جلب صور منتجات محددة)
    default_photo_url = "https://m.media-amazon.com/images/I/71R2oVwM5lL._AC_SL1500_.jpg" # مثال لصورة احترافية من أمازون

    if post_photo_to_telegram(default_photo_url, selected_message):
        print("✅ تم إرسال العرض الاحترافي مع الصورة والكلام التسويقي بنجاح يا مدير!")
    else:
        # إذا فشل إرسال الصورة، أرسل النص فقط لضمان النشر
        print("⚠️ حدث خطأ في إرسال الصورة، جاري إرسال النص فقط.")
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": selected_message,
            "parse_mode": "HTML",
        }
        requests.post(url, json=payload)

if __name__ == "__main__":
    get_amazon_deals_with_photo()
