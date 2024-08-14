from flask import Flask, render_template, request
from perenaine import populate_recipes_pn
from tuuliretseptid import populate_recipes_tr
from retseprisahtel_requests import populate_recipes_rs
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# home route to render the form
@app.route('/')
def home():
    return render_template('index.html')

# route to handle the form submission and display results
@app.route('/results', methods=['POST'])
def results():
    term = request.form.get("term", "").lower()
    term = term.replace(" ", "+")
    recipes = []

    print(term)
    # populate recipes from different sources
    pool = ThreadPoolExecutor(3)
    tasks = [
        pool.submit(populate_recipes_tr, recipes, term),
        pool.submit(populate_recipes_rs, recipes, term),
        pool.submit(populate_recipes_pn, recipes, term)
    ]
    for task in tasks:
        print("task done")
        task.result()

    # pass the results to the template for rendering
    return render_template('results.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)