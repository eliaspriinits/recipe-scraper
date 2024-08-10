import requests
from bs4 import BeautifulSoup


def load_and_parse_page(page_number, term):
    if page_number == 1:
        url = f"https://retseptisahtel.ee/?s={term}"
    else:
        url = f"https://retseptisahtel.ee/page/{page_number}/?s={term}"

    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


# Parse the initial page to determine the number of pages
def get_pages_rs(term):
    soup = load_and_parse_page(1, term)
    pagination = soup.find("span", class_="pages")
    if pagination:
        return int(pagination.get_text().split()[-1])
    else:
        return 1  # Default to 1 if pagination not found


# Iterate over all pages
def populate_recipes_rs(recipes, term):
    total_pages = get_pages_rs(term)
    for page_number in range(1, total_pages + 1):
        soup = load_and_parse_page(page_number, term)
        current_recipes = soup.find_all("h3", class_="entry-title")
        recipes.extend(current_recipes)

def retseprisahtel(recipes):
    for recipe in recipes:
        title = recipe.get_text()  # Extract the text (title) of the recipe
        link = recipe.find("a")['href']  # Extract the href (link) of the recipe
        print(f'retseptisahtel.ee Title: {title}')
        print(f'Link: {link}')
        print('---')
