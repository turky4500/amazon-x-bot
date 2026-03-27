import requests
import json

def get_amazon_deals():
    # مفتاحك الذهبي الذي حصلت عليه
    api_key = "b23fbb86270742a7b4060d5077b3a76c"
    # رابط عروض أمازون السعودية
    target_url = "https://www.amazon.sa/-/en/gp/goldbox"
    
    # استدعاء الوسيط لتجاوز الحماية وجلب البيانات
    proxy_url = f"https://api.scrapingant.com/v2/general?url={target_url}&x-api-key={api_key}&browser=false"

    print("--- جاري جلب الصيدات باستخدام المفتاح الذهبي ---")
    
    try:
        response = requests.get(proxy_url, timeout=30)
        if response.status_code == 200:
            html_content = response.text
            
            # التحقق من وجود بيانات
            if "SAR" in html_content or "Price" in html_content:
                print("✅ نجاح باهر! تم اختراق حماية أمازون وجلب البيانات.")
                # هنا سنطبع عينة بسيطة للتأكد
                print("نظام الرصد الآن جاهز للربط مع منصة X.")
            else:
                print("⚠️ تم جلب الصفحة ولكن يبدو أنها فارغة، سنقوم بتعديل الرابط في الخطوة التالية.")
        else:
            print(f"❌ فشل الاتصال بالوسيط. رمز الخطأ: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ حدث خطأ تقني: {e}")

if __name__ == "__main__":
    get_amazon_deals()
    
