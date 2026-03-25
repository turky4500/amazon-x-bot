from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_amazon_deals():
    print("--- جاري تشغيل المتصفح المتخفي لرصد الصيدات ---")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") # تشغيل بدون نافذة (سحابي)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # الدخول لأمازون السعودية - قسم العروض
        driver.get("https://www.amazon.sa/-/en/gp/goldbox")
        time.sleep(5) # انتظار تحميل الصفحة بالكامل
        
        print("--- تم دخول الموقع، جاري البحث عن المنتجات ---")
        
        # البحث عن كروت المنتجات
        products = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="grid-desktop-card"]')
        
        if not products:
            print("تنبيه: أمازون ما زال يخفي العروض. سنحاول مرة أخرى.")
        else:
            for idx, product in enumerate(products[:5], 1):
                try:
                    name = product.find_element(By.CSS_SELECTOR, '.a-size-base').text
                    price = product.find_element(By.CSS_SELECTOR, '.a-price-whole').text
                    print(f"{idx}. صيدة: {name[:50]}... | السعر: {price} ريال")
                except:
                    continue
                    
    except Exception as e:
        print(f"خطأ تقني: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    get_amazon_deals()
    
