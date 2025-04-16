from flask import Flask, request, render_template
from pizzaApp.checkout import process_checkout  # Import functionality from checkout.py
from pizzaApp.editmenuitems import edit_menu_items  # Import functionality from editMenuItems.py
from pizzaApp.editprices import edit_prices  # Import functionality from editPrices.py
from pizzaApp.pizzacreate import customize_pizza  # Import functionality from pizzacreate.py
from index import index  # Import the index function from index.py

app = Flask(__name__)

# Route: Home page
@app.route('/')
def index_route():
    return index()  # Calls the `index` function from index.py

# Route: Checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')  # Serve the checkout HTML file
    return process_checkout()  # Call the functionality from checkout.py

# Route: Edit Menu Items
@app.route('/editmenuitems', methods=['GET', 'POST'])
def edit_menu():
    if request.method == 'GET':
        return render_template('editMenuItems.html')  # Serve the editMenuItems HTML file
    return edit_menu_items()

# Route: Edit Prices
@app.route('/editprices', methods=['GET', 'POST'])
def edit_prices_route():
    if request.method == 'GET':
        return render_template('editPrices.html')  # Serve the editPrices HTML file
    return edit_prices()

# Route: Customize Pizza
@app.route('/customize_pizza', methods=['GET', 'POST'])
def pizza_creator():
    if request.method == 'GET':
        return render_template('customize_pizza.html')  # Serve the customize_pizza HTML file
    return customize_pizza()

if __name__ == '__main__':
    app.run(debug=True)
