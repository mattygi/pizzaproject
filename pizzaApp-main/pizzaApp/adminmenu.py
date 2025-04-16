from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Replace with a secure key in production

# Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')

        if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Login successful!", "success")
            return redirect(url_for('admin_menu'))  # Redirects to Admin Menu
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for('admin_login'))

    return render_template('adminLogin.html')

@app.route('/admin_menu')
def admin_menu():
    if not session.get('admin_logged_in'):  # Secure the menu page
        flash("Unauthorized access. Please log in.", "error")
        return redirect(url_for('admin_login'))

    return render_template('adminMenu.html', message="Welcome Admin! Manage store orders and menu items.")

@app.route('/store_orders')
def store_orders():
    if not session.get('admin_logged_in'):  # Secure admin-only pages
        flash("Access denied. Only admins can review store orders.", "error")
        return redirect(url_for('admin_login'))

    orders = [
        {"order_id": 1, "items": ["Pizza", "Soda"], "total": "$15.99"},
        {"order_id": 2, "items": ["Salad", "Juice"], "total": "$9.99"}
    ]
    
    return render_template('storeOrders.html', orders=orders)

@app.route('/edit_menu_items', methods=['GET', 'POST'])
def edit_menu_items():
    if not session.get('admin_logged_in'):
        flash("Access denied. Only admins can edit menu items.", "error")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        action = request.form.get('action')
        flash(f"Menu item '{item_name}' has been {action}d.", "success")
        return redirect(url_for('edit_menu_items'))

    return render_template('editMenuItems.html')

@app.route('/edit_prices', methods=['GET', 'POST'])
def edit_prices():
    if not session.get('admin_logged_in'):
        flash("Access denied. Only admins can edit prices.", "error")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        new_price = request.form.get('new_price')
        flash(f"Price for '{item_name}' has been updated to {new_price}.", "success")
        return redirect(url_for('edit_prices'))

    return render_template('editPrices.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)  # Clear session upon logout
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

