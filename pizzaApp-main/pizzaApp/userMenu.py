import os
from flask import Flask, render_template, session, redirect, url_for, flash
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'
ORDERS_TABLE = 'Orders'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'

orders_airtable = Airtable(BASE_ID, ORDERS_TABLE, API_TOKEN)

@app.route('/')
def index():
    """Render the user menu page."""
    return render_template('userMenu.html')

@app.route('/review_order', methods=['GET'])
def review_order():
    """Fetch the logged-in user's orders from Airtable."""
    try:
        user = session.get('username', 'Guest')  # Get logged-in username
        records = orders_airtable.get_all(formula=f"{{User}}='{user}'")

        if not records:
            flash("No orders found.", "info")
            return redirect(url_for('index'))

        order_data = [
            {
                'id': rec['id'],
                'user': user,
                'items': [
                    {
                        'pizza': rec['fields'].get('Pizza', 'Unknown Pizza'),
                        'quantity': rec['fields'].get('Quantity', 1),
                        'size': rec['fields'].get('Size', 'Medium'),
                        'price': rec['fields'].get('Price', 0)
                    }
                ],
                'status': rec['fields'].get('Status', 'Pending')
            }
            for rec in records
        ]

        return render_template('reviewOrder.html', orders=order_data)

    except Exception as e:
        flash(f"Error fetching orders: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/customize_pizza', methods=['GET'])
def customize_pizza():
    """Render the pizza customization page."""
    return render_template('customize_pizza.html')

@app.route('/logout')
def logout():
    """Clear the user session and redirect to the homepage."""
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
