from flask import Flask, render_template, request, redirect, url_for, session, flash
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Account Management'
API_TOKEN = 'YOUR_SECURE_API_TOKEN_HERE'

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password required!", "error")
            return redirect(url_for('login'))

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['role'] = 'store_owner'
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('login'))  # Redirects to login.html

        records = airtable.get_all(formula=f"{{Username}}='{username}'")
        if records:
            stored_password = records[0]['fields'].get('Password')
            role = records[0]['fields'].get('Role')

            if stored_password == password:
                session['role'] = role
                session['username'] = username
                flash("Login successful!", "success")
                return redirect(url_for('login'))  # Redirects to login.html
        
        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

@app.route('/editMenuItems', methods=['GET', 'POST'])
def edit_menu_items():
    if session.get('role') != 'store_owner':
        flash("Access denied. Store owners only.", "error")
        return redirect(url_for('login'))  # Redirects to login.html

    if request.method == 'POST':
        action = request.form.get('action')
        item_name = request.form.get('item')
        price = request.form.get('price')
        item_id = request.form.get('item_id')

        try:
            if action == 'add':
                airtable.insert({'Item': item_name, 'Price': float(price)})
            elif action == 'update':
                airtable.update(item_id, {'Item': item_name, 'Price': float(price)})
            elif action == 'delete':
                airtable.delete(item_id)
            flash("Menu item updated!", "success")
        except Exception as e:
            flash(f"Error updating item: {str(e)}", "error")

        return redirect(url_for('edit_menu_items'))

    records = airtable.get_all()
    menu = [{'id': rec['id'], 'item': rec['fields'].get('Item', ''), 'price': rec['fields'].get('Price', 0)} for rec in records]
    
    return render_template('editMenuItems.html', menu=menu)

@app.route('/editPrices', methods=['POST'])
def edit_prices():
    if session.get('role') != 'store_owner':
        flash("Access denied. Store owners only.", "error")
        return redirect(url_for('login'))  # Redirects to login.html

    role = request.form.get('role')
    return render_template('editPrices.html', role=role)

if __name__ == '__main__':
    app.run(debug=True)
