from perenaine import populate_recipes_pn
from tuuliretseptid import populate_recipes_tr
from retseprisahtel_requests import populate_recipes_rs
from naminami import populate_recipes_nn

recipes = []
term = "juust+muna+jahu+kukeseen"
populate_recipes_tr(recipes, term)
populate_recipes_rs(recipes, term)
populate_recipes_pn(recipes, term)

for recipe in recipes:
    title = recipe.get_text()
    link = recipe.find("a")['href']
    print(f'Title: {title.strip()}')
    print(f'Link: {link}')
    print('---')
