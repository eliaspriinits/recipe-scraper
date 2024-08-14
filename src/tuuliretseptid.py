import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def load_and_parse_page(page_number, term):
    if page_number == 1:
        url = f"https://tuuliretseptid.ee/?s={term}"
    else:
        url = f"https://tuuliretseptid.ee/page/{page_number}/?s={term}"

    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def get_pages_tr(term):
    soup = load_and_parse_page(1, term)
    pagination_links = soup.find_all("a", class_="page-numbers")
    if pagination_links:
        page_numbers = [int(link.get_text()) for link in pagination_links if link.get_text().isdigit()]
        return max(page_numbers) if page_numbers else 1
    else:
        return 1  # default to 1 if pagination not found

def fetch_recipes_from_current_site(page_number, term):
    return load_and_parse_page(page_number, term).find_all("h2", class_="cmsmasters_archive_item_title entry-title")


def populate_recipes_tr(recipes, term):
    total_pages = get_pages_tr(term)
    pool = ThreadPoolExecutor(10)
    different_pages = [pool.submit(fetch_recipes_from_current_site, page_number, term) for page_number in range(1, total_pages + 1)]
    for page in different_pages:
        recipes.extend(page.result())


def tuuliretseptid(recipes):
    for recipe in recipes:
        title = recipe.get_text()
        link = recipe.find("a")['href']
        print(f'perenaine.ee Title: {title}')
        print(f'Link: {link}')
        print('---')
