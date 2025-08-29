import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd
import argparse
import re

BASE_URL = "http://books.toscrape.com/"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def clean_price_text(txt: str):
    if not txt:
        return None
    cleaned = re.sub(r"[^\d.]", "", txt)
    try:
        return float(cleaned)
    except:
        return None

def fetch_description(product_url):
    try:
        res = requests.get(product_url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        desc_tag = soup.select_one("#product_description ~ p")
        return desc_tag.get_text(strip=True) if desc_tag else "No description"
    except Exception as e:
        print(f"Error fetching description: {e}")
        return "No description"

def parse_list_page(soup, base_url):
    products = []
    articles = soup.select("article.product_pod")

    for art in articles:
        title = art.h3.a["title"]
        product_link = requests.compat.urljoin(base_url, art.h3.a["href"])

        price_tag = art.select_one("p.price_color")
        price = clean_price_text(price_tag.get_text()) if price_tag else None

        rating_tag = art.select_one("p.star-rating")
        rating = 0
        if rating_tag:
            classes = rating_tag.get("class", [])
            for c in classes:
                if c in RATING_MAP:
                    rating = RATING_MAP[c]
                    break

        desc = fetch_description(product_link)

        products.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Description": desc,
            "Link": product_link,
        })
    return products

def scrape_books(pages):
    all_products = []
    url = BASE_URL

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        products = parse_list_page(soup, url)
        all_products.extend(products)

        next_page = soup.select_one("li.next a")
        if next_page:
            url = requests.compat.urljoin(url, next_page["href"])
        else:
            break

    return all_products

def save_to_db_and_excel(products):
    df = pd.DataFrame(products)
    df['Rating'] = df['Rating'].fillna(0).astype(int)

    conn = sqlite3.connect("Products.db")
    df.to_sql("Products", conn, if_exists="replace", index=False)
    conn.close()

    df.to_excel("Products.xlsx", index=False)

    print("Data saved to Products.db and Products.xlsx")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape")
    args = parser.parse_args()

    products = scrape_books(args.pages)
    save_to_db_and_excel(products)
    print(f"Scraping finished. Total products: {len(products)}")


