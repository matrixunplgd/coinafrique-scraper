import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Créer dossier data s'il n'existe pas
os.makedirs("data", exist_ok=True)

# URLs à scraper avec leur type et nombre de pages exact
urls = [
    {"url": "https://sn.coinafrique.com/categorie/vetements-homme", "type": "habits", "pages": 10, "filename": "vetements_homme.csv"},
    {"url": "https://sn.coinafrique.com/categorie/chaussures-homme", "type": "chaussures", "pages": 10, "filename": "chaussures_homme.csv"},
    {"url": "https://sn.coinafrique.com/categorie/vetements-enfants", "type": "habits", "pages": 10, "filename": "vetements_enfants.csv"},
    {"url": "https://sn.coinafrique.com/categorie/chaussures-enfants", "type": "chaussures", "pages": 8, "filename": "chaussures_enfants.csv"},
]

# Fonction de scraping
def scrape_page(url, type_article, max_pages):
    all_data = []
    for page in range(1, max_pages + 1):
        full_url = f"{url}?page={page}"
        print(f"Scraping: {full_url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36"
            }
            response = requests.get(full_url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            cards = soup.select("div.m4")

            for card in cards:
                try:
                    prix = card.select_one("p.ad__card-price").text.strip()
                except:
                    prix = None
                try:
                    adresse = card.select_one(".ad__card-location span").text.strip()
                except:
                    adresse = None
                try:
                    image = card.select_one("img")["src"]
                except:
                    image = None

                all_data.append({
                    "type": type_article,
                    "prix": prix,
                    "adresse": adresse,
                    "image_lien": image
                })
            time.sleep(1)

        except Exception as e:
            print(f"Erreur lors du scraping de {full_url} : {e}")
    return all_data

# Scraping par fichier
for u in urls:
    print(f"\n🔄 Début du scraping de {u['filename']}")
    data = scrape_page(u["url"], u["type"], u["pages"])
    df = pd.DataFrame(data)
    filepath = f"data/{u['filename']}"
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"✅ Données enregistrées dans {filepath}")
    print(f"Scraping de {u['filename']} terminé.\n")
    time.sleep(2)  # Pause entre les fichiers pour éviter les blocages  