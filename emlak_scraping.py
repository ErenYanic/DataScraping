import requests
from bs4 import BeautifulSoup
import pandas as pd

# Hedef URL (örnek)
base_url = "https://www.century21global.com/en/l/homes-for-sale/turkey?page={}"

# Kullanıcı aracını belirtmek için User-Agent ekleyelim
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

# Verileri tutmak için bir liste
all_listings = []

# Kaç sayfa veri çekmek istediğimizi belirleyelim
for page in range(1, 6):  # İlk 5 sayfa
    url = base_url.format(page)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # İlanları bul
        for listing in soup.select(".listing-item"):  # Doğru sınıfı siteye göre değiştir
            title = listing.select_one(".listing-title")
            price = listing.select_one(".listing-price")
            size = listing.select_one(".listing-size")
            rooms = listing.select_one(".listing-rooms")
            link = listing.select_one("a")

            if title and price:
                all_listings.append({
                    "Başlık": title.text.strip(),
                    "Fiyat": price.text.strip(),
                    "Metrekare": size.text.strip() if size else "Belirtilmemiş",
                    "Oda Sayısı": rooms.text.strip() if rooms else "Belirtilmemiş",
                    "Link": f"https://www.example.com{link['href']}" if link else "Belirtilmemiş"
                })
    else:
        print(f"Sayfa {page} yüklenemedi, durum kodu: {response.status_code}")

# Verileri CSV'ye kaydetme
df = pd.DataFrame(all_listings)
df.to_csv("emlak_ilanlari.csv", index=False, encoding="utf-8")
print("Veriler başarıyla kaydedildi!")
