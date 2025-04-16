from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global login status (Replaces session-based authentication)
login_status = {'admin': False}

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')

        # Hardcoded admin credentials (simplified for school project)
        if admin_username == "admin" and admin_password == "admin":
            login_status['admin'] = True
            return redirect(url_for('admin_menu'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('adminLogin.html')

@app.route('/admin_menu')
def admin_menu():
    if login_status['admin']:  # Check login state
        return render_template('adminMenu.html')  # Render Admin Menu
    else:
        return "Access denied. Only admins can access this page.", 403

@app.route('/store_orders', methods=['GET'])
def store_orders():
    if not login_status['admin']:  # Check login state
        return "Access denied. Only admins can review store orders.", 403

    # Placeholder data for store orders (since Airtable is removed)
    orders = [
        {"order_id": 1, "items": ["Pizza", "Soda"], "total": "$15.99"},
        {"order_id": 2, "items": ["Salad", "Juice"], "total": "$9.99"}
    ]
    
    return render_template('storeOrders.html', orders=orders)  # Render orders in HTML

@app.route('/edit_menu_items', methods=['GET', 'POST'])
def edit_menu_items():
    if not login_status['admin']:  # Check login state
        return "Access denied. Only admins can edit menu items.", 403

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        action = request.form.get('action')  # e.g., add/remove/edit
        return f"Menu item '{item_name}' has been {action}d."
    
    return render_template('editMenuItems.html')  # Render menu editing page

@app.route('/edit_prices', methods=['GET', 'POST'])
def edit_prices():
    if not login_status['admin']:  # Check login state
        return "Access denied. Only admins can edit menu prices.", 403

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        new_price = request.form.get('new_price')
        return f"Price for '{item_name}' has been updated to {new_price}."

    return render_template('editPrices.html')  # Render price editing page

@app.route('/admin_logout')
def admin_logout():
    login_status['admin'] = False  # Reset login state
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
