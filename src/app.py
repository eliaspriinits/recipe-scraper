from flask import Flask, render_template, request
from perenaine import populate_recipes_pn
from tuuliretseptid import populate_recipes_tr
from retseprisahtel_requests import populate_recipes_rs

app = Flask(__name__)

# home route to render the form
@app.route('/')
def home():
    return render_template('index.html')

# route to handle the form submission and display results
@app.route('/results', methods=['POST'])
def results():
    term = request.form['term']
    recipes = []

    # populate recipes from different sources
    populate_recipes_tr(recipes, term)
    populate_recipes_rs(recipes, term)
    populate_recipes_pn(recipes, term)

    # pass the results to the template for rendering
    return render_template('results.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)