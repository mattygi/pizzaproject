from flask import Flask, render_template
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Orders'  # Correct table name for fetching order data
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/review_order', methods=['GET'])
def review_order():
    """Fetch order details dynamically from Airtable."""
    records = airtable.get_all(formula="{Status}='Processing'")

    if records:
        order_data = {
            'id': records[0]['id'],  # Use Airtable record ID as order ID
            'user': records[0]['fields'].get('User', 'Guest'),
            'method': records[0]['fields'].get('Delivery Method', 'Delivery'),
            'status': records[0]['fields'].get('Status', 'Processing'),
            'items': [{'quantity': rec['fields'].get('Quantity'),
                       'size': rec['fields'].get('Size'),
                       'pizza': rec['fields'].get('Pizza'),
                       'price': rec['fields'].get('Price')} for rec in records],
            'total': sum(float(rec['fields'].get('Price', 0)) * int(rec['fields'].get('Quantity', 1)) for rec in records)
        }
    else:
        order_data = {"message": "No orders found."}

    return render_template('reviewOrder.html', order=order_data)

if __name__ == '__main__':
    app.run(debug=True)
