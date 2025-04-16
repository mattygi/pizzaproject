
from flask import Flask, render_template, request, redirect, url_for
from airtable import Airtable

app = Flask(__name__)

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Orders'  # The Airtable table name for storing orders
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/cart', methods=['GET'])
def cart():
    # Fetch cart data dynamically from Airtable
    records = airtable.get_all()
    cart = [{'id': rec['id'], 'pizza': rec['fields'].get('Pizza'), 'quantity': rec['fields'].get('Quantity'),
             'size': rec['fields'].get('Size'), 'price': rec['fields'].get('Price')} for rec in records]

    return render_template('cart.html', cart=cart)

@app.route('/proceed', methods=['POST'])
def proceed():
    # Retrieve delivery method from the form
    delivery_method = request.form.get('method')
    
    if not delivery_method:
        return "Please select a delivery method.", 400  # Bad request if no method is selected

    # Update delivery method in Airtable for all pending orders
    records = airtable.get_all()
    for record in records:
        airtable.update(record['id'], {'Delivery Method': delivery_method})

    # Redirect user based on delivery selection
    if delivery_method == "delivery":
        return redirect(url_for('checkout'))
    elif delivery_method == "pickup":
        return redirect(url_for('payment'))
    else:
        return "Invalid delivery method selected.", 400

@app.route('/checkout', methods=['GET'])
def checkout():
    # Mark orders as "Completed" in Airtable
    records = airtable.get_all()
    for record in records:
        airtable.update(record['id'], {'Status': 'Completed'})

    return render_template('orderPlaced.html')

@app.route('/payment', methods=['GET'])
def payment():
    return "This is the payment page for pickup. Replace this with a proper template."

@app.route('/store_orders', methods=['GET'])
def store_orders():
    # Fetch completed orders from Airtable
    records = airtable.get_all(formula="{Status}='Completed'")
    orders = [{'pizza': rec['fields'].get('Pizza'), 'quantity': rec['fields'].get('Quantity'),
               'size': rec['fields'].get('Size'), 'price': rec['fields'].get('Price'), 
               'delivery_method': rec['fields'].get('Delivery Method')} for rec in records]

    return render_template('storeOrders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
