import requests
from bs4 import BeautifulSoup
import time

def scrape_category(url, type_article, max_pages):
    all_data = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for page in range(1, max_pages + 1):
        full_url = f"{url}?page={page}"
        print(f"Scraping: {full_url}")
        res = requests.get(full_url, headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        cards = soup.select("div.m4")

        for card in cards:
            prix = card.select_one("p.ad__card-price")
            adresse = card.select_one(".ad__card-location span")
            image = card.select_one("img")

            all_data.append({
                "type": type_article,
                "prix": prix.text.strip() if prix else None,
                "adresse": adresse.text.strip() if adresse else None,
                "image_lien": image["src"] if image and image.has_attr("src") else None
            })

        time.sleep(1)

    return all_data
