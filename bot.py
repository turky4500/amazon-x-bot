import requests
import os
import json

# إعدادات الحساب (تُجلب من الخزنة الآمنة في GitHub)
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CT0 = os.getenv("CT0")
SCRAPER_ANT_KEY = "b23fbb86270742a7b4060d5077b3a76c"

def post_to_x(text):
    """دالة النشر في منصة X باستخدام الكوكيز"""
    url = "https://x.com/i/api/graph_ql/S8_t8vX0XGzS_tX0XGzS_t/CreateTweet"
    
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7p9W4tMAb6g7pSdh97sHU9b6vC0vba8abt0pKC",
        "X-Twitter-Auth-Type": "OAuth2Session",
        "X-Twitter-Active-User": "yes",
        "X-Csrf-Token": CT0,
        "Cookie": f"auth_token={AUTH_TOKEN}; ct0={CT0};",
        "Content-Type": "application/json",
    }
    
    payload = {
        "variables": {
            "tweet_text": text,
            "dark_request": False,
            "media": {"media_entities": [], "possibly_sensitive": False},
            "semantic_annotation_ids": []
        },
        "queryId": "S8_t8vX0XGzS_tX0XGzS_t"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("✅ تم نشر التغريدة بنجاح!")
        else:
            print(f"❌ فشل النشر. خطأ: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"⚠️ خطأ أثناء النشر: {e}")

def get_deal_and_post():
    target_url = "https://www.amazon.sa/-/en/gp/goldbox"
    proxy_url = f"https://api.scrapingant.com/v2/general?url={target_url}&x-api-key={SCRAPER_ANT_KEY}&browser=false"

    print("--- جاري رصد صيدة جديدة ---")
    try:
        response = requests.get(proxy_url, timeout=30)
        if "SAR" in response.text:
            # هنا سنختار نصاً ترويجياً جذاباً بشكل عشوائي كمثال للنظام الآلي
            # في التطوير القادم سنربطه بـ ChatGPT لصياغة مخصصة
            tweet_content = "🚨 صيدة جديدة من أمازون السعودية! \n\nخصومات قوية الان على قسم العروض، لا تفوتكم الفرصة قبل انتهاء الكمية ⚡️\n\nللإطلاع على العروض: https://www.amazon.sa/-/en/gp/goldbox \n\n#أمازون #عروض #صيدات"
            
            print(f"جاري النشر: {tweet_content}")
            post_to_x(tweet_content)
        else:
            print("لم يتم العثور على عروض جديدة حالياً.")
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    get_deal_and_post()
