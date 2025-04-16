
import os
from flask import Flask, render_template, session, redirect, url_for, flash
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Orders'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/review_order', methods=['GET'])
def review_order():
    """Fetch processing order details dynamically from Airtable."""
    try:
        records = airtable.get_all(formula="AND({Status}='Processing')")

        if not records:
            flash("No orders found.", "info")
            return redirect(url_for('index'))

        order_data = {
            'id': records[0]['id'],  # Use Airtable record ID as order ID
            'user': session.get('username', 'Guest'),  # Retrieve logged-in username
            'method': records[0]['fields'].get('Delivery Method', 'Delivery'),
            'status': records[0]['fields'].get('Status', 'Processing'),
            'items': [
                {
                    'quantity': rec['fields'].get('Quantity', 1),
                    'size': rec['fields'].get('Size', 'Medium'),
                    'pizza': rec['fields'].get('Pizza', 'Unknown Pizza'),
                    'price': rec['fields'].get('Price', 0)
                }
                for rec in records
            ],
            'total': sum(float(rec['fields'].get('Price', 0)) * int(rec['fields'].get('Quantity', 1)) for rec in records)
        }

        return render_template('reviewOrder.html', order=order_data)

    except Exception as e:
        flash(f"Error retrieving order details: {str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
