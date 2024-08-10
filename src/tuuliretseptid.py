import requests
from bs4 import BeautifulSoup


def load_and_parse_page(page_number, term):
    if page_number == 1:
        url = f"https://tuuliretseptid.ee/?s={term}"
    else:
        url = f"https://tuuliretseptid.ee/page/{page_number}/?s={term}"

    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


# Parse the initial page to determine the number of pages
def get_pages_tr(term):
    soup = load_and_parse_page(1, term)
    pagination_links = soup.find_all("a", class_="page-numbers")
    if pagination_links:
        page_numbers = [int(link.get_text()) for link in pagination_links if link.get_text().isdigit()]
        return max(page_numbers) if page_numbers else 1
    else:
        return 1  # Default to 1 if pagination not found


def populate_recipes_tr(recipes, term):
    total_pages = get_pages_tr(term)
    for page_number in range(1, total_pages + 1):
        soup = load_and_parse_page(page_number, term)
        current_recipes = soup.find_all("h2", class_="cmsmasters_archive_item_title entry-title")
        recipes.extend(current_recipes)


def tuuliretseptid(recipes):
    for recipe in recipes:
        title = recipe.get_text()
        link = recipe.find("a")['href']
        print(f'perenaine.ee Title: {title}')
        print(f'Link: {link}')
        print('---')
