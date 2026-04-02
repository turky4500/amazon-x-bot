import tweepy
import os
import requests

# جلب المفاتيح الرسمية من خزنة GitHub
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_secret = os.getenv("TWITTER_ACCESS_SECRET")
SCRAPER_ANT_KEY = "b23fbb86270742a7b4060d5077b3a76c"

def post_to_x(text):
    try:
        # الاتصال الرسمي بمنصة X عبر API V2
        client = tweepy.Client(
            consumer_key=api_key, 
            consumer_secret=api_secret,
            access_token=access_token, 
            access_token_secret=access_secret
        )
        response = client.create_tweet(text=text)
        print(f"✅ تم النشر بنجاح! معرف التغريدة: {response.data['id']}")
    except Exception as e:
        print(f"❌ فشل النشر الرسمي: {e}")

def get_deal_and_post():
    target_url = "https://www.amazon.sa/-/en/gp/goldbox"
    proxy_url = f"https://api.scrapingant.com/v2/general?url={target_url}&x-api-key={SCRAPER_ANT_KEY}&browser=false"

    print("--- جاري فحص صيدات أمازون الجديدة ---")
    try:
        response = requests.get(proxy_url, timeout=30)
        if response.status_code == 200:
            # نص التغريدة الافتتاحي للمشروع
            tweet_content = "🚨 عروض أمازون السعودية جارية الآن! 🇸🇦\n\nصيدات قوية وخصومات خرافية على قسم العروض اليومية.. لا تفوتكم قبل نفاد الكمية! ⚡️\n\nتفقد العروض من هنا 👇\nhttps://www.amazon.sa/-/en/gp/goldbox \n\n#أمازون #عروض #صيدات #السعودية"
            post_to_x(tweet_content)
        else:
            print("فشل في الوصول لموقع أمازون حالياً.")
    except Exception as e:
        print(f"حدث خطأ في الرصد: {e}")

if __name__ == "__main__":
    get_deal_and_post()
