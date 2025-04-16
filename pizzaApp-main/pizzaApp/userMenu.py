from flask import Flask, render_template
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
ORDERS_TABLE = 'Orders'  # Correct table name for fetching order data
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

orders_airtable = Airtable(BASE_ID, ORDERS_TABLE, API_TOKEN)

@app.route('/')
def index():
    return render_template('userMenu.html')

@app.route('/review_orders', methods=['GET'])
def review_orders():
    """Fetch order details dynamically from Airtable."""
    records = orders_airtable.get_all()

    if records:
        order_data = [
            {
                'id': rec['id'],  # Use Airtable record ID as order ID
                'user': rec['fields'].get('User', 'Unknown'),  # Updated to use "User" field
                'items': [{'pizza': rec['fields'].get('Pizza'), 'quantity': rec['fields'].get('Quantity'), 'size': rec['fields'].get('Size'), 'price': rec['fields'].get('Price')}],
                'status': rec['fields'].get('Status', 'Pending')
            }
            for rec in records
        ]
    else:
        order_data = []

    return render_template('reviewOrder.html', orders=order_data)

@app.route('/customize_pizza', methods=['GET'])
def customize_pizza():
    return render_template('customize_pizza.html')

if __name__ == '__main__':
    app.run(debug=True)
