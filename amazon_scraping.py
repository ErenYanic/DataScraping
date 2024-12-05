import requests
from bs4 import BeautifulSoup
import pandas as pd

# Amazon telefon kategorisi için URL
base_url = "https://www.amazon.com/s?k=phones&page={}"

# Kullanıcı aracını belirtmek için bir User-Agent ekleyelim
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

all_products = []

# 5 sayfa boyunca scraping yapalım
for page in range(1, 6):  # 1'den 5'e kadar sayfa numaraları
    url = base_url.format(page)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        for product in soup.select(".s-main-slot .s-result-item"):
            # Aynı kodla ürün bilgilerini çekiyoruz
            title = product.select_one("h2 .a-text-normal")
            price = product.select_one(".a-price-whole")
            rating = product.select_one(".a-icon-alt")
            review_count = product.select_one(".a-size-base")
            product_link = product.select_one("h2 .a-text-normal")

            if title:
                all_products.append({
                    "Ürün Adı": title.text.strip(),
                    "Fiyat": price.text.strip() if price else "Belirtilmemiş",
                    "Puan": rating.text.split(" ")[0] if rating else "Belirtilmemiş",
                    "Değerlendirme Sayısı": review_count.text.strip() if review_count else "Belirtilmemiş",
                    "Ürün Linki": f"https://www.amazon.com{product_link['href']}" if product_link else "Belirtilmemiş"
                })
    else:
        print(f"Sayfa {page} yüklenemedi, durum kodu: {response.status_code}")

# Verileri CSV'ye kaydetme
df = pd.DataFrame(all_products)
df.to_csv("amazon_telefonlar.csv", index=False, encoding="utf-8")
print("5 sayfa boyunca veriler başarıyla kaydedildi!")