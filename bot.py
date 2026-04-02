import requests
import os

# جلب البيانات من الخزنة
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CT0 = os.getenv("CT0")
SCRAPER_ANT_KEY = "b23fbb86270742a7b4060d5077b3a76c"

def post_to_x(text):
    # الرابط العالمي والمستقر للنشر (Update 2026)
    url = "https://x.com/i/api/graphql/7t9GmuCemGZas89S_Z6pSg/CreateTweet"
    
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7p9W4tMAb6g7pSdh97sHU9b6vC0vba8abt0pKC",
        "X-Twitter-Auth-Type": "OAuth2Session",
        "X-Twitter-Active-User": "yes",
        "X-Csrf-Token": CT0,
        "Cookie": f"auth_token={AUTH_TOKEN}; ct0={CT0};",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # هيكل البيانات الجديد المطلوب من X
    payload = {
        "variables": {
            "tweet_text": text,
            "dark_request": False,
            "media": {"media_entities": [], "possibly_sensitive": False},
            "semantic_annotation_ids": []
        },
        "features": {
            "premium_content_api_read_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_text_entities_to_tweet_display_text_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_tweet_if_present": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        },
        "queryId": "7t9GmuCemGZas89S_Z6pSg"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print("✅ مبارك يا مدير! تم النشر بنجاح.")
        else:
            print(f"❌ خطأ {response.status_code}: الصلاحيات غير صحيحة.")
            print("تأكد أنك لم تسجل الخروج من حسابك في المتصفح الذي نسخت منه الكود.")
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

def get_deal_and_post():
    target_url = "https://www.amazon.sa/-/en/gp/goldbox"
    proxy_url = f"https://api.scrapingant.com/v2/general?url={target_url}&x-api-key={SCRAPER_ANT_KEY}&browser=false"

    print("--- محاولة تشغيل النظام الآلي ---")
    try:
        # جلب سريع للتأكد من الاتصال
        requests.get(proxy_url, timeout=30)
        tweet_text = "🚀 تم تشغيل الموظف الرقمي بنجاح! \n\nانتظروا أقوى عروض وصيدات أمازون السعودية هنا آلياً وبدون توقف. ⚡️\n\n#صيدات #أمازون #عروض"
        post_to_x(tweet_text)
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    get_deal_and_post()
