from flask import Flask, render_template, request, jsonify
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Pizzas'  # Correct table name for retrieving menu data
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/')
def index():
    """Fetch menu data dynamically from Airtable and serve the customization page."""
    records = airtable.get_all()
    menu = {rec['fields'].get('Item'): {'price': rec['fields'].get('Price', 0), 'size': rec['fields'].get('Size', 'Medium')} for rec in records}

    return render_template('customize_pizza.html', menu=menu)  # Pass menu data to template

@app.route('/customize_pizza', methods=['POST'])
def customize_pizza():
    """Handle pizza customization and store selections in Airtable."""
    data = request.json

    pizza_type = data.get("pizzaType")
    size = data.get("size")
    quantity = data.get("quantity", 1)

    # Fetch price and size dynamically from Airtable
    records = airtable.get_all(formula=f"{{Item}}='{pizza_type}'")
    if records:
        price_per_pizza = records[0]['fields'].get('Price', 0)
        ingredients = records[0]['fields'].get('Ingredients', 'No ingredients listed')
        available_size = records[0]['fields'].get('Size', 'Medium')  # Default to "Medium" if not listed
    else:
        return jsonify({"error": "Pizza not found in menu."}), 404

    total_price = price_per_pizza * int(quantity)

    # Store order in Airtable
    order_data = {
        "Item": pizza_type,
        "Size": size if size else available_size,  # Use the selected size or the default one
        "Ingredients": ingredients,
        "Quantity": quantity,
        "Price": total_price,
        "Status": "Pending"
    }
    airtable.insert(order_data)

    response_message = f"{quantity} {size.capitalize()} {pizza_type.capitalize()} Pizza(s) with ingredients: {ingredients}, for ${total_price:.2f}"

    return jsonify({"message": response_message})

if __name__ == '__main__':
    app.run(debug=True)
