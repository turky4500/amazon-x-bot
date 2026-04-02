import requests
import os

# الإعدادات الأساسية
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
# هوية الأرباح الخاصة بك يا أبو علي
ASSOCIATE_TAG = "tkwin-21" 

def post_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except:
        return False

def get_amazon_deals():
    # رابط قسم العروض اليومية في أمازون السعودية
    base_url = "https://www.amazon.sa/-/en/gp/goldbox"
    
    # تحويل الرابط إلى رابط أرباح خاص بك
    affiliate_url = f"{base_url}?tag={ASSOCIATE_TAG}"
    
    message = (
        "<b>🔥 عروض الساعة من أمازون السعودية! 🇸🇦</b>\n\n"
        "دخلنا قسم الصيدات ولقينا خصومات قوية الآن.. 👇\n\n"
        "🛍️ <b>تصفح كافة العروض من هنا:</b>\n"
        f" {affiliate_url} \n\n"
        "<i>💡 نصيحة: العروض تنتهي بسرعة، الحق على اللي يعجبك!</i>\n"
        "ــــــــــــــــــــــــــــــــــــــــ\n"
        "✅ <b>تم الرصد بواسطة بوت صيدات تركي</b>"
    )
    
    if post_to_telegram(message):
        print("✅ تم إرسال عروض الأرباح بنجاح يا مدير!")
    else:
        print("❌ حدث خطأ في الإرسال.")

if __name__ == "__main__":
    get_amazon_deals()
