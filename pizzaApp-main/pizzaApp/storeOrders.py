
from flask import Flask, render_template, request, session, redirect, url_for
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Airtable Connection for Non-Admin Users
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
ORDERS_TABLE = 'Orders'  # Airtable table for admin order management
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

orders_airtable = Airtable(BASE_ID, ORDERS_TABLE, API_TOKEN)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hardcoded admin authentication
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True  # Set session flag for admin
            return redirect(url_for('admin_panel'))

        return render_template('admin_login.html', error="Invalid credentials. Please try again.")

    return render_template('admin_login.html')

@app.route('/admin_panel')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    return render_template('adminPanel.html')

@app.route('/admin_orders')
def admin_orders():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Fetch orders dynamically from Airtable
    records = orders_airtable.get_all()
    order_data = [
        {
            'id': rec['id'],
            'customer': rec['fields'].get('Customer', 'Unknown'),
            'items': [{'pizza': rec['fields'].get('Pizza'), 'quantity': rec['fields'].get('Quantity'), 'price': rec['fields'].get('Price')}],
            'status': rec['fields'].get('Status', 'Pending'),
            'total': rec['fields'].get('Total', 0)
        }
        for rec in records
    ]

    return render_template('storeOrders.html', orders=order_data)

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
