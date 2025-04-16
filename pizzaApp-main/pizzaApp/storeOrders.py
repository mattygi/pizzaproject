
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management
app.permanent_session_lifetime = 3600  # Expire session after 1 hour

# Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Airtable Connection for Admin Orders Management
BASE_ID = 'appkRvP5WntxZWYOg'
ORDERS_TABLE = 'Orders'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'

orders_airtable = Airtable(BASE_ID, ORDERS_TABLE, API_TOKEN)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hardcoded admin authentication
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True  # Set session flag for admin
            session.permanent = True  # Keep session active
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_menu'))  # Redirect to adminMenu.html

        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

@app.route('/admin_menu')
def admin_menu():
    if not session.get('admin_logged_in'):
        flash("Please log in as an admin.", "error")
        return redirect(url_for('admin_login'))

    return render_template('adminMenu.html')

@app.route('/admin_orders')
def admin_orders():
    if not session.get('admin_logged_in'):
        flash("Unauthorized access.", "error")
        return redirect(url_for('admin_login'))

    try:
        records = orders_airtable.get_all()
        if not records:
            flash("No orders found.", "info")
            return redirect(url_for('admin_menu'))  # Redirect to adminMenu instead

        order_data = [
            {
                'id': rec['id'],
                'customer': rec['fields'].get('Customer', 'Unknown'),
                'items': [
                    {
                        'pizza': item.get('Pizza', 'Unknown Pizza'),
                        'quantity': item.get('Quantity', 1),
                        'price': item.get('Price', 0)
                    } for item in rec['fields'].get('Items', [])
                ],
                'status': rec['fields'].get('Status', 'Pending'),
                'total': rec['fields'].get('Total', 0)
            }
            for rec in records
        ]

        return render_template('storeOrders.html', orders=order_data)

    except Exception as e:
        flash(f"Error fetching orders: {str(e)}", "error")
        return redirect(url_for('admin_menu'))  # Redirect to adminMenu instead

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Admin has been logged out.", "info")
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
