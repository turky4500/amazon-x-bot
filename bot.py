import requests
import os

# نستخدم الأسرار التي وضعناها سابقاً (تأكد أن قيمها صحيحة من المتصفح)
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CT0 = os.getenv("CT0")

def post_tweet_free(text):
    url = "https://x.com/i/api/graphql/nS_S2vX_0eS68F9S8F9S8F/CreateTweet" # رابط النشر المباشر
    
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7p9W4tMAb6g7pSdh97sHU9b6vC0vba8abt0pKC",
        "X-Csrf-Token": CT0,
        "Cookie": f"auth_token={AUTH_TOKEN}; ct0={CT0};",
        "Content-Type": "application/json"
    }

    # بيانات التغريدة بتنسيق X الحديث
    payload = {
        "variables": {
            "tweet_text": text,
            "reply": {"exclude_reply_user_ids": []},
            "media": {"media_entities": [], "possibly_sensitive": False}
        },
        "queryId": "nS_S2vX_0eS68F9S8F9S8F"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("✅ تم النشر مجاناً وبنجاح يا مدير!")
        else:
            print(f"❌ فشل النشر. رمز الخطأ: {response.status_code}")
            print("ملاحظة: تأكد من نسخ AUTH_TOKEN و CT0 من المتصفح الخفي (Incognito).")
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

if __name__ == "__main__":
    post_tweet_free("🚀 تجربة النشر المجاني عبر النظام المطور.. صيدات أمازون قادمة!")
