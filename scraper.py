import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import re
from urllib.parse import urljoin

BASE_URL = "https://sn.coinafrique.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'fr-FR,fr;q=0.9'
}
DELAY = 2  # Pause entre les requêtes
RETRIES = 2  # Tentatives max en cas d’échec

# ----------------------
# Requête avec tentatives
# ----------------------
def fetch_page(url):
    for i in range(RETRIES):
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            res.raise_for_status()
            return res
        except Exception as e:
            print(f"[{i+1}] Échec : {url} -> {e}")
            time.sleep(DELAY)
    return None

# ----------------------
# Nettoyage du prix
# ----------------------
def clean_price(text):
    text = re.sub(r'[^\d,]', '', text.replace(' ', ''))
    return float(text.replace(',', '.')) if text else None

# ----------------------
# Extraction d’un produit
# ----------------------
def extract_product(card, category):
    try:
        title = card.select_one('h2.card-title, [class*="title"]')
        price = card.select_one('.price, [class*="price"]')
        location = card.select_one('.location, [class*="location"]')
        image = card.select_one('img[src], img[data-src]')

        return {
            'type': category,
            'titre': title.get_text(strip=True) if title else None,
            'prix': clean_price(price.get_text()) if price else None,
            'adresse': location.get_text(strip=True) if location else None,
            'image_lien': urljoin(BASE_URL, image.get('src') or image.get('data-src')) if image else None,
            'date_scraping': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Erreur produit : {e}")
        return None

# ----------------------
# Scraping d’une catégorie
# ----------------------
def scrape_category(path, category, pages=3):
    data, seen = [], set()
    for page in range(1, pages + 1):
        url = f"{BASE_URL}{path}?page={page}"
        print(f"Scraping : {url}")
        res = fetch_page(url)
        if not res:
            continue

        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.select('div.card, div[class*="product"]')

        if not cards:
            print("Aucun produit trouvé")
            break

        for card in cards:
            item = extract_product(card, category)
            if item:
                uid = hash(item['titre'] + str(item['image_lien']))
                if uid not in seen:
                    seen.add(uid)
                    data.append(item)

        time.sleep(DELAY)

    return pd.DataFrame(data)

# ----------------------
# Sauvegarde CSV
# ----------------------
def save_csv(df, filename):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Sauvegardé : {filename}")
        return True
    except Exception as e:
        print(f"Erreur sauvegarde : {e}")
        return False

# ----------------------
# Programme principal
# ----------------------
def main():
    categories = [
        ('/categorie/vetements-homme', 'habits'),
        ('/categorie/chaussures-homme', 'chaussures'),
        ('/categorie/vetements-enfants', 'habits'),
        ('/categorie/chaussures-enfants', 'chaussures')
    ]

    all_data = []

    for url, cat in categories:
        print(f"\nCatégorie : {cat.upper()}")
        df = scrape_category(url, cat)
        if not df.empty:
            if save_csv(df, f"data/{cat}.csv"):
                all_data.append(df)
                print(f"{len(df)} produits trouvés.")

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True).dropna(subset=['titre', 'prix'], how='all')
        save_csv(final_df, "data/coinafrique_final.csv")
        print(f"\nTotal produits : {len(final_df)}")
    else:
        print("Aucune donnée récupérée.")

if __name__ == "__main__":
    main()
