import requests
from bs4 import BeautifulSoup
import time

# Base URL
base_url = "https://nami-nami.ee/otsi/"

# Search term
term = "juustukook"
recipes = []


# Function to load and parse the page
def load_and_parse_page(page_number):
    if page_number == 1:
        url = f"{base_url}{term}?recipe_page=1&news_page=1&string=&type=&occasion=&country=&method="
    else:
        url = f"{base_url}{term}?recipe_page={page_number}&news_page=1&string=&type=&occasion=&country=&method="

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return BeautifulSoup(response.text, 'html.parser')


def parse_recipes(soup):
    articles_div = soup.find('div', id='grid')
    if articles_div:
        return articles_div.find_all(lambda tag: tag.name == "a" and tag.get("href")
                                  and "comments" not in tag['href']
                                  and "rating" not in tag['href'])
    return []


def populate_recipes_nn(recipes):
    soup = load_and_parse_page(1)
    recipes.extend(parse_recipes(soup))

    page_number = 1
    while True:
        try:
            soup = load_and_parse_page(page_number)
            new_recipes = parse_recipes(soup)
            if not new_recipes:
                print("No more recipes found.")
                break
            recipes.extend(new_recipes)
            print(f"Loaded page {page_number} with {len(new_recipes)} recipes.")

            page_number += 1
            time.sleep(0.5)

        except Exception as e:
            print(f"Error loading more recipes: {e}")
            break
"""
# Process and print the recipes
for recipe in recipes:
    title = recipe.find("div", class_="intro").get_text().lstrip()
    link = recipe['href']
    print(f'Title: {title}')
    print(f'Link: https://nami-nami.ee{link}')
    print('---')
"""
