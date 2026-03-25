import requests
from bs4 import BeautifulSoup
import os

def get_amazon_deals():
    # الرابط المستهدف (أمازون السعودية - قسم العروض)
    url = "https://www.amazon.sa/-/en/gp/goldbox"
    
    # تعريف المتصفح (لكي لا يكتشف أمازون أننا برنامج) - تم تحديثه ليعمل بشكل أفضل
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    print("--- جاري البدء في رصد الصيدات من أمازون ---")
    
    try:
        session = requests.Session() # استخدام جلسة مستمرة لزيادة الموثوقية
        response = session.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # محاولة العثور على المنتجات بأكثر من طريقة لأن أمازون يغير تصميمه
            products = soup.find_all('div', {'data-testid': 'grid-desktop-card'})
            if not products:
                 products = soup.find_all('div', {'id': 'grid-main-container'})
                 if products:
                     products = products[0].find_all('div', {'class': 'a-section'})

            deals_found = []
            
            if products:
                # سنجلب أول 5 عروض فقط للتجربة لتجنب أي مشاكل في البداية
                max_deals = 5
                count = 0
                
                for product in products:
                    if count >= max_deals:
                        break
                        
                    # محاولة استخراج الاسم
                    name_tag = product.find('div', {'class': 'p13n-sc-truncate'})
                    if not name_tag:
                         name_tag = product.find('span', {'class': 'a-size-base'})
                    
                    # محاولة استخراج السعر
                    price_tag = product.find('span', {'class': 'a-price-whole'})
                    
                    if name_tag:
                        name_text = name_tag.text.strip()
                        price_text = price_tag.text.strip() if price_tag else "غير محدد"
                        
                        deals_found.append({
                            "المنتج": name_text,
                            "السعر": price_text
                        })
                        count += 1
            
            if not deals_found:
                print("تنبيه: لم يتم العثور على منتجات في هذه الجولة. قد يكون الموقع محمي بشكل أقوى حالياً.")
            else:
                for idx, deal in enumerate(deals_found, 1):
                    # إخفاء جزء من الاسم للسرية في التقارير العامة
                    short_name = (deal['المنتج'][:40] + '..') if len(deal['المنتج']) > 40 else deal['المنتج']
                    print(f"{idx}. {short_name} - السعر: {deal['السعر']} ريال")
        else:
            print(f"فشل الوصول للموقع. رمز الخطأ: {response.status_code}")
            
    except Exception as e:
        print(f"حدث خطأ تقني في الاتصال بأمازون: {e}")

if __name__ == "__main__":
    get_amazon_deals()
  
