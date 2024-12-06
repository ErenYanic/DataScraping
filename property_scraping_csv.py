import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GeckoDriver yolunu belirt
driver_path = "C:/Users/ereny/Downloads/Compressed/geckodriver/geckodriver.exe"  # Buraya kendi GeckoDriver yolunuzu yazın
service = Service(driver_path)

# Firefox WebDriver başlat
driver = webdriver.Firefox(service=service)

# Hedef URL'nin temel yapısı
base_url = "https://www.century21global.com/en/l/homes-for-sale/turkey?page={}&max=40"

# Verileri tutacak bir liste
all_listings = []

# İlk 10 sayfa boyunca scraping işlemi
for page in range(1, 10):  # Sayfalar 1'den 2'ye kadar (örnek olarak ayarlandı)
    url = base_url.format(page)
    print(f"Sayfa {page} işleniyor: {url}")
    driver.get(url)

    try:
        # Tüm JSON-LD script etiketlerini seç
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "script"))
        )
        scripts = driver.find_elements(By.TAG_NAME, "script")

        for script in scripts:
            if 'application/ld+json' in script.get_attribute("type"):
                json_data = json.loads(script.get_attribute("innerHTML"))

                # İlan bilgilerini ekle
                all_listings.append({
                    "Title": json_data.get("name"),
                    "Description": json_data.get("description"),
                    "Image URL": json_data.get("image"),
                    "Address": json_data.get("address", {}).get("addressLocality"),
                    "Country": json_data.get("address", {}).get("addressCountry"),
                    "Number of Bedrooms": json_data.get("numberOfBedrooms"),
                    "Number of Bathrooms": json_data.get("numberOfBathroomsTotal"),
                    "Floor Size (m2)": json_data.get("floorSize", {}).get("value"),
                    "Price (USD)": json_data.get("offers", [{}])[0].get("price"),
                    "Property URL": json_data.get("url")
                })
    except Exception as e:
        print(f"Sayfa {page} yüklenirken hata oluştu: {e}")

    # Bekleme süresi
    time.sleep(20)

# Tarayıcıyı kapat
driver.quit()

# Verileri DataFrame'e çevir ve CSV'ye kaydet
df = pd.DataFrame(all_listings)
df.to_csv("century21_property.csv", index=False, encoding="utf-8")
print("Tüm veriler başarıyla 'century21_property.csv' dosyasına kaydedildi!")
