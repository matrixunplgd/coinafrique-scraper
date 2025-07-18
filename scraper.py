import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_category(url, type_article, page_count=5):
    all_data = []

    for page in range(1, page_count + 1):
        page_url = f"{url}?page={page}"
        print(f"Scraping {page_url}...")

        response = requests.get(page_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="sc-c0c5e0d3-0")

        for product in products:
            title = product.find("p", class_="sc-d1ede7e3-0").text.strip()
            price = product.find("span", class_="sc-3ef5a5d2-0").text.strip()
            location = product.find("span", class_="sc-e0f5a8b3-0").text.strip()
            image = product.find("img")["src"]

            all_data.append({
                "type": type_article,
                "nom": title,
                "prix": price,
                "adresse": location,
                "image_lien": image
            })

    df = pd.DataFrame(all_data)
    return df
