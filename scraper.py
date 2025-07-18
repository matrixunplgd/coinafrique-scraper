import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from urllib.parse import urljoin
import re

# Configuration
BASE_URL = "https://sn.coinafrique.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9'
}
DELAY = 2  # Délai entre les requêtes en secondes
MAX_RETRIES = 2  # Nombre de tentatives en cas d'échec

# Création du dossier data s'il n'existe pas
os.makedirs('data', exist_ok=True)

def make_request(url):
    """Effectue une requête HTTP avec gestion des erreurs"""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Tentative {attempt + 1} échouée pour {url}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY * (attempt + 1))
    return None

def extract_product_data(product, category):
    """Extrait les données d'un produit avec des sélecteurs robustes"""
    try:
        # Titre
        title = product.select_one('h2.card-title, [class*="title"], h2')
        title = title.get_text(strip=True) if title else None
        
        # Prix
        price = product.select_one('.price, [class*="price"], .ad__card-price')
        price = clean_price(price.get_text()) if price else None
        
        # Adresse
        location = product.select_one('.location, [class*="location"], .ad__card-location')
        location = location.get_text(strip=True) if location else None
        
        # Image
        img = product.select_one('img[src], img[data-src]')
        img_url = urljoin(BASE_URL, img['src' if img.has_attr('src') else 'data-src']) if img else None
        
        return {
            'type': category,
            'titre': title,
            'prix': price,
            'adresse': location,
            'image_lien': img_url,
            'date_scraping': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Erreur extraction produit: {e}")
        return None

def clean_price(price_str):
    """Nettoie et convertit le prix en nombre"""
    if not price_str:
        return None
    # Supprime tous les caractères non numériques sauf les virgules/décimales
    cleaned = re.sub(r'[^\d,]', '', price_str.replace(' ', ''))
    # Gère les nombres avec virgule décimale
    if ',' in cleaned:
        cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return None

def scrape_category(category_url, category_name, max_pages=3):
    """Scrape une catégorie complète avec gestion des doublons"""
    products = []
    seen_products = set()  # Pour éviter les doublons
    
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}{category_url}?page={page}" if 'http' not in category_url else f"{category_url}?page={page}"
        print(f"Scraping {url}")
        
        response = make_request(url)
        if not response:
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        product_cards = soup.select('div.card, div.listing-card, div.m4, div[class*="product"]')
        
        if not product_cards:
            print("Aucun produit trouvé - structure HTML peut-être changée")
            break
            
        for card in product_cards:
            product_data = extract_product_data(card, category_name)
            if product_data:
                # Crée un identifiant unique pour éviter les doublons
                product_id = hash(f"{product_data['titre']}{product_data['image_lien']}")
                if product_id not in seen_products:
                    seen_products.add(product_id)
                    products.append(product_data)
        
        time.sleep(DELAY)
    
    return pd.DataFrame(products)

def save_to_csv(df, filename):
    """Sauvegarde les données avec vérification du dossier"""
    try:
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Données sauvegardées dans {filename}")
        return True
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")
        return False

def main():
    """Fonction principale avec gestion des erreurs améliorée"""
    categories = [
        ('/categorie/vetements-homme', 'habits'),
        ('/categorie/chaussures-homme', 'chaussures'),
        ('/categorie/vetements-enfants', 'habits'),
        ('/categorie/chaussures-enfants', 'chaussures')
    ]
    
    all_data = []
    
    for url, cat_type in categories:
        print(f"\nScraping catégorie: {cat_type.upper()}")
        try:
            df = scrape_category(url, cat_type)
            if not df.empty:
                # Sauvegarde intermédiaire par catégorie
                cat_file = f"data/coinafrique_{cat_type}.csv"
                if save_to_csv(df, cat_file):
                    all_data.append(df)
                    print(f"{len(df)} produits valides trouvés")
        except Exception as e:
            print(f"Échec catégorie {cat_type}: {e}")
            continue
    
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        # Nettoyage final
        final_df = final_df.dropna(subset=['titre', 'prix'], how='all')
        final_file = "data/coinafrique_final.csv"
        if save_to_csv(final_df, final_file):
            print(f"\nScraping terminé. {len(final_df)} produits sauvegardés dans {final_file}")
    else:
        print("Aucune donnée valide à sauvegarder")

if __name__ == "__main__":
    main()