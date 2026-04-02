import requests
import os

def check_secrets():
    auth = os.getenv("AUTH_TOKEN")
    ct0 = os.getenv("CT0")
    
    print(f"--- فحص الأسرار (المدير التقني) ---")
    if not auth or not ct0:
        print("❌ خطأ: لم يتم العثور على AUTH_TOKEN أو CT0 في إعدادات GitHub!")
        return
    
    print(f"طول auth_token المكتشف: {len(auth)} حرف")
    print(f"طول ct0 المكتشف: {len(ct0)} حرف")
    
    url = "https://x.com/i/api/1.1/account/verify_credentials.json"
    headers = {
        "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7p9W4tMAb6g7pSdh97sHU9b6vC0vba8abt0pKC",
        "X-Csrf-Token": ct0,
        "Cookie": f"auth_token={auth}; ct0={ct0};"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"✅ مبروك يا مدير! تم الاتصال بنجاح.")
            print(f"الحساب المرتبط: {response.json().get('screen_name')}")
        else:
            print(f"❌ فشل (خطأ {response.status_code})")
            print("السبب المحتمل: الكوكيز منتهية أو تم نسخها بشكل خاطئ.")
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

if __name__ == "__main__":
    check_secrets()
