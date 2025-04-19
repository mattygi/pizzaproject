import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Keep this secure in production

# ✅ Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ✅ Hardcoded Menu Items (No Database Needed)
MENU_ITEMS = {
    "Cheese Pizza": "$10.00",
    "Pepperoni Pizza": "$12.00",
    "Supreme Pizza": "$14.00",
    "Veggie Pizza": "$13.00"
}

# ✅ JSON Files for Persistent User & Order Storage
USERS_FILE = "users.json"
ORDERS_FILE = "orders.json"

# ✅ Helper Functions for JSON Storage
def load_json(file):
    """Load data from JSON file."""
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Initialize empty list if file not found
    except json.JSONDecodeError:
        return []  # Handle empty or corrupted JSON file

def save_json(file, data):
    """Save data to JSON file."""
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving to {file}: {e}")
        flash("Failed to save data. Please try again.", "error")  # Inform the user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    return render_template('adminLogin.html')

@app.route('/edit_menu_items', methods=['GET', 'POST'])
def edit_menu_items():
    return render_template('editMenuItems.html')

@app.route('/proceed', methods=['POST'])
def proceed():
    """Handle the submission of checkout details."""
    # Example logic for processing checkout details
    delivery_method = request.form.get('method')  # Get the delivery method (e.g., 'delivery' or 'pickup')

    if not delivery_method:
        flash("Please choose a delivery method.", "error")
        return redirect(url_for('checkout'))

    # Redirect to the payment page after processing
    flash(f"Proceeding with {delivery_method} option.", "success")
    return redirect(url_for('payment'))

@app.route('/customize_pizza', methods=['GET', 'POST'])
def customize_pizza():
    if request.method == 'POST':
        pizza = request.form.get('pizza')
        size = request.form.get('size')
        quantity = request.form.get('quantity')
        username = session.get('username')

        # Create order data
        order_data = {
            "order_id": len(load_json(ORDERS_FILE)) + 1,
            "username": username,
            "items": [  # Ensure this is a list
                {
                    "Item": pizza,
                    "Size": size,
                    "Quantity": int(quantity),
                    "Price": float(MENU_ITEMS[pizza].replace("$", "")) * int(quantity)
                }
            ],
            "status": "Pending",
            "total": float(MENU_ITEMS[pizza].replace("$", "")) * int(quantity)
        }

        # Load orders and append new order
        orders = load_json(ORDERS_FILE)  # Ensure orders is a list
        orders.append(order_data)  # Append new order to the list
        save_json(ORDERS_FILE, orders)  # Save updated orders

        flash(f"{quantity}x {size} {pizza} added to cart!", "success")
        return redirect(url_for('cart'))

    return render_template('customize_pizza.html', menu=MENU_ITEMS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["role"] = "store_owner"
            session["username"] = username
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_menu'))

        users = load_json(USERS_FILE)
        user = next((u for u in users if u["username"] == username and u["password"] == password), None)

        if user:
            session["role"] = "customer"
            session["username"] = username
            session["user_id"] = user.get("user_id", os.urandom(8).hex())  # Set user_id
            flash("Login successful!", "success")
            return redirect(url_for('user_menu'))

        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_json(USERS_FILE)

        if any(u["username"] == username for u in users):
            flash("Username already exists!", "error")
            return redirect(url_for('register'))

        user_id = os.urandom(8).hex()  # Generate user_id
        users.append({"username": username, "password": password, "role": "customer", "user_id": user_id})
        save_json(USERS_FILE, users)
        session["user_id"] = user_id  # Set user_id
        session["username"] = username  # Set username
        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/cart', methods=['GET'])
def cart():
    """Show the cart contents, or indicate if the cart is empty."""
    orders = load_json(ORDERS_FILE)
    username = session.get("username")

    # Filter pending orders for the logged-in user
    pending_orders = [order for order in orders if order["username"] == username and order["status"] == "Pending"]

    if not pending_orders:
        flash("Your cart is empty!", "info")
        # Render the cart page even if it is empty
        return render_template('cart.html', cart=pending_orders)

    # Render the cart page with pending orders
    return render_template('cart.html', cart=pending_orders)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    """Handle payment process."""
    if request.method == 'POST':
        # Process payment here (e.g., mock payment for now)
        flash("Payment successful! Thank you for your order.", "success")
        return redirect(url_for('store_orders'))  # Redirect to order history after payment

    return render_template('payment.html')  # Render payment page

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Handle checkout process for pending orders."""
    # Load all orders
    orders = load_json(ORDERS_FILE)
    username = session.get("username")

    # Filter pending orders for the logged-in user
    pending_orders = [order for order in orders if order["username"] == username and order["status"] == "Pending"]

    if request.method == 'POST':
        # Handle form submission for delivery method
        delivery_method = request.form.get('method')  # "delivery" or "pickup"

        if not delivery_method:  # Ensure a delivery method is selected
            flash("Please choose a delivery method.", "error")
            return render_template('checkout.html', cart=pending_orders)

        # Mark all pending orders for the user as "Complete"
        for order in orders:
            if order["username"] == username and order["status"] == "Pending":
                order["status"] = "Complete"

        # Save the updated orders to the JSON file
        save_json(ORDERS_FILE, orders)

        # Redirect to the payment page
        flash(f"Order placed successfully with {delivery_method} option! Redirecting to payment.", "success")
        return redirect(url_for('payment'))

    # Handle GET requests to render the checkout page
    return render_template('checkout.html', cart=pending_orders)

@app.route('/store_orders', methods=['GET'])
def store_orders():
    """Show completed orders for the logged-in user."""
    orders = load_json(ORDERS_FILE)
    username = session.get("username")
    completed_orders = [order for order in orders if order["username"] == username and order["status"] == "Complete"]
    return render_template('storeOrders.html', orders=completed_orders)

@app.route('/admin_menu')
def admin_menu():
    if session.get('role') != 'store_owner':
        flash("Access denied. Store owners only.", "error")
        return redirect(url_for('login'))
    return render_template('adminMenu.html')

@app.route('/user_menu')
def user_menu():
    return render_template('userMenu.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)