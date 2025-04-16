
import os
from flask import Flask, render_template, request, jsonify, session, flash
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Pizzas'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/')
def index():
    """Fetch menu data dynamically from Airtable and serve the customization page."""
    records = airtable.get_all()
    menu = {rec['fields'].get('Item'): {'price': rec['fields'].get('Price', 0), 'size': rec['fields'].get('Size', 'Medium')} for rec in records}

    username = session.get("username", "Guest")  # Retrieve logged-in username
    return render_template('customize_pizza.html', menu=menu, username=username)

@app.route('/customize_pizza', methods=['POST'])
def customize_pizza():
    """Handle pizza customization and store selections in Airtable."""
    pizza_type = request.form.get("pizza")
    size = request.form.get("size")
    quantity = request.form.get("quantity", 1)
    meats = request.form.getlist("meats[]")  # Get multiple meat selections
    veggies = request.form.getlist("veggies[]")  # Get multiple veggie selections

    # Fetch pizza details dynamically from Airtable
    records = airtable.get_all(formula=f"{{Item}}='{pizza_type}'")
    if records:
        price_per_pizza = records[0]['fields'].get('Price', 0)
        available_size = records[0]['fields'].get('Size', 'Medium')  # Default to "Medium" if not listed
    else:
        flash("Pizza not found in menu!", "error")
        return redirect(url_for('index'))

    total_price = price_per_pizza * int(quantity)

    # Store order in Airtable
    order_data = {
        "Item": pizza_type,
        "Size": size if size else available_size,
        "Meats": ", ".join(meats) if meats else "No meats",
        "Veggies": ", ".join(veggies) if veggies else "No veggies",
        "Quantity": quantity,
        "Price": total_price,
        "Status": "Pending"
    }
    airtable.insert(order_data)

    flash(f"{quantity} {size.capitalize()} {pizza_type.capitalize()} Pizza(s) added to your cart!", "success")
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
