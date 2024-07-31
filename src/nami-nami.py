from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver_path = "C:\\Users\\Arvuti\\geckodriver-v0.34.0-win64\\geckodriver.exe"
driver = webdriver.Firefox()

term = "juustukook"

# Open the website
driver.get(f"https://nami-nami.ee/otsi/{term}?recipe_page=1&news_page=1&string={term}&type=&occasion=&country=&method=")

# nami-nami show more button is
# <a href="#" id="more_recipes" onclick="event.preventDefault(); view_more_recipes()" class="btn btn-yellow btn-block">Vaata veel</a>
while True:
    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'more_recipes'))  # Use ID to locate the button
        )
        show_more_button.click()
        print("Clicked 'Show more' button")
        time.sleep(2)  # Wait for the new content to load (adjust as necessary)
    except Exception as e:
        print(f"No more 'Show more' button found: {e}")
        break  # Exit the loop if the "show more" button is not found or not clickable
# Get the page source after loading all recipes
page_source = driver.page_source

# Close the WebDriver
driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')

recipes = soup.find_all('div', class_='intro')

# Process and print the recipes
for recipe in recipes:
    print(recipe)
