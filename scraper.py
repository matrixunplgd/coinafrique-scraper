import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Configuration du scraper
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9'
}
BASE_DELAY = 3  # Délai de base entre les requêtes en secondes
MAX_RETRIES = 2  # Nombre de tentatives en cas d'échec

# Liste des URLs à scraper avec leurs types
CATEGORIES = [
    {
        'url': 'https://sn.coinafrique.com/categorie/vetements-homme',
        'type': 'habits',
        'pages': 3  # Nombre de pages à scraper
    },
    {
        'url': 'https://sn.coinafrique.com/categorie/chaussures-homme',
        'type': 'chaussures',
        'pages': 3
    },
    {
        'url': 'https://sn.coinafrique.com/categorie/vetements-enfants',
        'type': 'habits',
        'pages': 3
    },
    {
        'url': 'https://sn.coinafrique.com/categorie/chaussures-enfants',
        'type': 'chaussures',
        'pages': 3
    }
]

def make_request(url, retry=0):
    """Effectue une requête HTTP avec gestion des erreurs"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        if retry < MAX_RETRIES:
            print(f"Tentative {retry + 1} échouée pour {url}. Nouvel essai...")
            time.sleep(BASE_DELAY * (retry + 1))
            return make_request(url, retry + 1)
        print(f"Échec après {MAX_RETRIES} tentatives pour {url}: {e}")
        return None

def parse_product(product, category_type):
    """Extrait les données d'un produit"""
    try:
        # Titre
        title_elem = product.find('h2', class_=lambda x: x and 'title' in x.lower())
        title = title_elem.get_text(strip=True) if title_elem else 'N/A'
        
        # Prix
        price_elem = product.find('div', class_=lambda x: x and 'price' in x.lower())
        price = clean_price(price_elem.get_text()) if price_elem else None
        
        # Adresse
        location_elem = product.find('div', class_=lambda x: x and 'location' in x.lower())
        location = location_elem.get_text(strip=True) if location_elem else 'N/A'
        
        # Image
        img_elem = product.find('img')
        img_url = img_elem['src'] if img_elem and img_elem.has_attr('src') else 'N/A'
        
        return {
            'type': category_type,
            'titre': title,
            'prix': price,
            'adresse': location,
            'image_lien': img_url
        }
    except Exception as e:
        print(f"Erreur lors de l'extraction d'un produit: {e}")
        return None

def clean_price(price_str):
    """Nettoie et convertit le prix en nombre"""
    if not price_str:
        return None
    # Supprime tous les caractères non numériques sauf les virgules/décimales
    cleaned = re.sub(r'[^\d,]', '', price_str.replace('.', '').replace(' ', ''))
    # Remplace la virgule décimale par un point
    cleaned = cleaned.replace(',', '.')
    try:
        return float(cleaned)
    except:
        return None

def scrape_category(category_url, category_type, pages_to_scrape):
    """Scrape une catégorie complète"""
    products = []
    
    for page in range(1, pages_to_scrape + 1):
        current_url = f"{category_url}?page={page}"
        print(f"Scraping {current_url}...")
        
        response = make_request(current_url)
        if not response:
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        product_cards = soup.find_all('div', class_=lambda x: x and 'card' in x.lower())
        
        for card in product_cards:
            product_data = parse_product(card, category_type)
            if product_data:
                products.append(product_data)
        
        # Délai aléatoire entre 2 et 5 secondes
        time.sleep(max(BASE_DELAY, min(5, BASE_DELAY + (0.5 * page))))
    
    return pd.DataFrame(products)

def main():
    """Fonction principale"""
    all_data = []
    
    for category in CATEGORIES:
        print(f"\n=== Début du scraping pour {category['type']} ===")
        df = scrape_category(category['url'], category['type'], category['pages'])
        print(f"{len(df)} produits trouvés pour {category['type']}")
        all_data.append(df)
    
    # Fusion de toutes les données
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Sauvegarde en CSV
    output_file = 'data/coinafrique_produits.csv'
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nScraping terminé. Données sauvegardées dans {output_file}")
    print(f"Total: {len(final_df)} produits")

if __name__ == "__main__":
    main()