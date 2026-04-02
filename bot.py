import requests
import os
import json

# إعدادات الحساب (تُجلب من الخزنة الآمنة في GitHub)
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CT0 = os.getenv("CT0")
SCRAPER_ANT_KEY = "b23fbb86270742a7b4060d5077b3a76c"

def post_to_x(text):
    """دالة النشر في منصة X بتحديث 2026 لتفادي خطأ 404"""
    # تحديث رابط النشر ليكون الرابط العام الأكثر استقراراً
    url = "https://x.com/i/api/graphql/sn9_is9K9S9K9S9K9S9K9S9K/CreateTweet"
    
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7p9W4tMAb6g7pSdh97sHU9b6vC0vba8abt0pKC",
        "X-Twitter-Auth-Type": "OAuth2Session",
        "X-Twitter-Active-User": "yes",
        "X-Csrf-Token": CT0,
        "Cookie": f"auth_token={AUTH_TOKEN}; ct0={CT0};",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    payload = {
        "variables": {
            "tweet_text": text,
            "dark_request": False,
            "media": {"media_entities": [], "possibly_sensitive": False},
            "semantic_annotation_ids": []
        },
        "features": {
            "interactive_text_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_text_entities_to_tweet_display_text_enabled": True,
            "standardized_nudges_misinfo": True
        },
        "fieldToggles": {"withArticleRichContentState": False},
        "queryId": "sn9_is9K9S9K9S9K9S9K9S9K"
    }

    try:
        # سنحاول النشر، وإذا فشل سنطبع تفاصيل أكثر للمدير
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200 or response.status_code == 201:
            print("✅ تم بنجاح! اذهب وتحقق من حسابك في X.")
        else:
            print(f"❌ فشل النشر. رمز الحالة: {response.status_code}")
            if response.status_code == 403:
                print("تنبيه: يبدو أن الكوكيز انتهت صلاحيتها أو الـ CT0 غير دقيق.")
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

def get_deal_and_post():
    target_url = "https://www.amazon.sa/-/en/gp/goldbox"
    proxy_url = f"https://api.scrapingant.com/v2/general?url={target_url}&x-api-key={SCRAPER_ANT_KEY}&browser=false"

    print("--- جاري محاولة النشر من جديد ---")
    try:
        response = requests.get(proxy_url, timeout=30)
        if response.status_code == 200:
            tweet_content = "🚨 تجربة تشغيل الموظف الرقمي 🚨\n\nخصومات أمازون السعودية جارية الآن! ⚡️\n\nرابط العروض: https://www.amazon.sa/-/en/gp/goldbox \n\n#أمازون #عروض"
            post_to_x(tweet_content)
        else:
            print("فشل في جلب العروض من أمازون.")
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    get_deal_and_post()
