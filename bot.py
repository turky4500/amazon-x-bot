import requests
import os

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CT0 = os.getenv("CT0")

def test_connection():
    # رابط بسيط جداً فقط لجلب بيانات حسابك للتأكد من الاتصال
    url = "https://x.com/i/api/1.1/account/verify_credentials.json"
    
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7p9W4tMAb6g7pSdh97sHU9b6vC0vba8abt0pKC",
        "X-Csrf-Token": CT0,
        "Cookie": f"auth_token={AUTH_TOKEN}; ct0={CT0};"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ الاتصال ناجح! أهلاً بك يا: {user_data.get('screen_name')}")
        else:
            print(f"❌ فشل الاتصال. رمز الخطأ: {response.status_code}")
            print("تنبيه: تأكد من تحديث AUTH_TOKEN و CT0 في GitHub Secrets يدوياً.")
    except Exception as e:
        print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    test_connection()
