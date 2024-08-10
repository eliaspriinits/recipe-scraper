from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver_path = "C:\\Users\\Arvuti\\geckodriver-v0.34.0-win64\\geckodriver.exe"
driver = webdriver.Firefox()

term = "juust+muna"
recipes = []


def load_and_parse_page(page_number):
    if page_number == 1:
        driver.get(f"https://retseptisahtel.ee/?s={term}")
    else:
        driver.get(f"https://retseptisahtel.ee/page/{page_number}/?s={term}")
    time.sleep(0.5)  # Wait for the new content to load (adjust as necessary)
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')


soup = load_and_parse_page(1)
pagination = soup.find("span", class_="pages")  # last part is the count of pages
if pagination:
    total_pages = int(pagination.get_text().split()[-1])
else:
    total_pages = 1  # default to 1 if pagination not found

for page_number in range(1, total_pages + 1):
    if page_number < total_pages:
        soup = load_and_parse_page(page_number)
        current_recipes = soup.find_all(lambda tag: tag.name == "a" and tag.get("rel") == ["bookmark"] and not tag.find("img"))
        recipes.extend(current_recipes)
        print(recipes)

driver.quit()

number_of_recipes = len(recipes)
print(number_of_recipes)
# Process and print the recipes
for recipe in recipes:
    title = recipe.get_text()  # Adjust the selector as needed
    link = recipe['href']
    print(f'Title: {title}')
    print(f'Link: {link}')
    print('---')
