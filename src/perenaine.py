import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
recipes = []


def load_and_parse_page(page_number, term):
    if page_number == 1:
        url = f"https://perenaine.ee/?s={term}"
    else:
        url = f"https://perenaine.ee/page/{page_number}/?s={term}"

    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


# Parse the initial page to determine the number of pages
def get_pages(term):
    soup = load_and_parse_page(1, term)
    pagination_links = soup.find_all("a", class_="page-numbers")
    if pagination_links:
        if pagination_links[-1].get_text() == "Järgmine":
            return int(pagination_links[-2].get_text())
        return int(pagination_links[-1].get_text())
    else:
        return 1  # Default to 1 if pagination not found

def fetch_recipes_from_current_site(page_number, term):
    return load_and_parse_page(page_number, term).find_all("h3", class_="entry-title")

def populate_recipes_pn(recipes, term):
    total_pages = get_pages(term)
    pool = ThreadPoolExecutor(10)
    different_pages = [pool.submit(fetch_recipes_from_current_site, page_number, term) for page_number in range(1, total_pages + 1)]
    for page in different_pages:
        recipes.extend(page.result())
"""
for recipe in recipes:
    title = recipe.get_text()
    link = recipe.find("a")['href']
    print(f'Title: {title}')
    print(f'Link: {link}')
    print('---')
"""