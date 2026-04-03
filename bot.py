import requests
import os
import random
import json
import re
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = "@amazonturky"
ASSOCIATE_TAG = "tkwin-21"
LAST_DEAL_FILE = "last_deal.json"

MARKETING_PHRASES = [
    "🔥 عرض لمدة 24 ساعة فقط",
    "⚡ خصم يصل إلى 50%",
    "🎁 شامل ضمان لمدة سنتين",
    "🚀 الشحن المجاني اليوم فقط",
    "💎 الأكثر مبيعاً في أمازون",
    "🏆 أفضل سعر خلال 30 يوماً"
]

def add_marketing_phrase(title):
    return f"{random.choice(MARKETING_PHRASES)}\n\n{title}"

def save_last_deal(deal):
    with open(LAST_DEAL_FILE, "w", encoding="utf-8") as f:
        json.dump(deal, f, ensure_ascii=False)

def get_last_deal():
    try:
        with open(LAST_DEAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def fetch_deals():
    url = "https://www.amazon.sa/gp/bestsellers"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except:
        return []
    soup = BeautifulSoup(r.text, "lxml")
    products = []
    for item in soup.select("div.p13n-sc-truncate-desktop-type2"):
        title = item.get_text(strip=True)
        parent = item.find_parent("a")
        if parent and parent.get("href"):
            link = parent["href"]
            if not link.startswith("http"):
                link = "https://www.amazon.sa" + link.split('?')[0]
            if re.search(r'/dp/([A-Z0-9]{10})', link):
                products.append({"title": title, "link": link})
        if len(products) >= 10:
            break
    return products

def post_to_telegram():
    deals = fetch_deals()
    if not deals:
        print("لا توجد عروض")
        return
    last = get_last_deal()
    if last:
        deals = [d for d in deals if d["link"] != last["link"]]
    if not deals:
        deals = fetch_deals()[:1]
    deal = random.choice(deals)
    final_link = f"{deal['link']}?tag={ASSOCIATE_TAG}"
    title = add_marketing_phrase(deal['title'])
    msg = f"<b>{title}</b>\n\n🔗 {final_link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            save_last_deal(deal)
            print("تم الإرسال بنجاح")
        else:
            print("فشل الإرسال", r.text)
    except Exception as e:
        print("خطأ", e)

if __name__ == "__main__":
    post_to_telegram()
