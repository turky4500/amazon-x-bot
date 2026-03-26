from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_amazon_deals():
    print("--- جاري تفعيل وضع التخفي الاحترافي (iPhone User Agent) ---")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # انتحال شخصية متصفح بشري حقيقي (مهم جداً)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # سنغير الرابط لصفحة العروض المباشرة لسهولة القراءة
        url = "https://www.amazon.sa/-/en/gp/goldbox"
        driver.get(url)
        
        print("--- تم الوصول للموقع، جاري فحص الصفحة ---")
        time.sleep(10) # انتظار أطول لضمان تحميل الصور والبيانات
        
        # محاولة رصد العروض باستخدام معرفات (Classes) أكثر دقة
        items = driver.find_elements(By.CSS_SELECTOR, ".a-list-item")
        
        if not items:
            # محاولة بديلة إذا فشلت الأولى
            items = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'grid-desktop-card')]")

        deals_found = []
        if items:
            for idx, item in enumerate(items[:5], 1):
                try:
                    # استخراج النصوص
                    full_text = item.text.replace("\n", " ")
                    if "SAR" in full_text: # للتأكد أنه عرض سعري
                        deals_found.append(f"صيدة {idx}: {full_text[:60]}...")
                except:
                    continue

        if not deals_found:
            # إذا فشل الرصد التلقائي، سنطبع "كود الصفحة" لنعرف ماذا يرى البوت (للتحليل فقط)
            print("تنبيه: لم تظهر العروض بشكل مباشر. جاري فحص هيكل الصفحة...")
            # سنقوم بطباعة أسماء الأقسام كاختبار
            elements = driver.find_elements(By.TAG_NAME, "h1")
            for e in elements:
                print(f"عنوان الصفحة المكتشف: {e.text}")
        else:
            for deal in deals_found:
                print(deal)
                    
    except Exception as e:
        print(f"حدث خطأ غير متوقع: {e}")
    finally:
        driver.quit()
        print("--- انتهت جولة المراقبة بنجاح ---")

if __name__ == "__main__":
    get_amazon_deals()
    
