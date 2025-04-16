from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global variable for login status
login_status = {'admin': False}

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')

        # Hardcoded credentials
        if admin_username == "admin" and admin_password == "admin":
            login_status['admin'] = True  # Update global login state
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if login_status['admin']:  # Check login state
        return "Welcome Admin! You can manage users, view reports, and configure the system."
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin_logout')
def admin_logout():
    login_status['admin'] = False  # Reset login state
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

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

    return render_template('admin_login.html')

@app.route('/admin_menu')
def admin_menu():
    if login_status['admin']:  # Check login state
        return render_template('adminmenu.html')  # Render Admin Menu
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

from flask import Flask, render_template, request, redirect, url_for
from airtable import Airtable

app = Flask(__name__)

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Orders'  # The Airtable table name for storing orders
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/cart', methods=['GET'])
def cart():
    # Fetch cart data dynamically from Airtable
    records = airtable.get_all()
    cart = [{'id': rec['id'], 'pizza': rec['fields'].get('Pizza'), 'quantity': rec['fields'].get('Quantity'),
             'size': rec['fields'].get('Size'), 'price': rec['fields'].get('Price')} for rec in records]

    return render_template('cart.html', cart=cart)

@app.route('/proceed', methods=['POST'])
def proceed():
    # Retrieve delivery method from the form
    delivery_method = request.form.get('method')
    
    if not delivery_method:
        return "Please select a delivery method.", 400  # Bad request if no method is selected

    # Update delivery method in Airtable for all pending orders
    records = airtable.get_all()
    for record in records:
        airtable.update(record['id'], {'Delivery Method': delivery_method})

    # Redirect user based on delivery selection
    if delivery_method == "delivery":
        return redirect(url_for('checkout'))
    elif delivery_method == "pickup":
        return redirect(url_for('payment'))
    else:
        return "Invalid delivery method selected.", 400

@app.route('/checkout', methods=['GET'])
def checkout():
    # Mark orders as "Completed" in Airtable
    records = airtable.get_all()
    for record in records:
        airtable.update(record['id'], {'Status': 'Completed'})

    return render_template('orderPlaced.html')

@app.route('/payment', methods=['GET'])
def payment():
    return "This is the payment page for pickup. Replace this with a proper template."

@app.route('/store_orders', methods=['GET'])
def store_orders():
    # Fetch completed orders from Airtable
    records = airtable.get_all(formula="{Status}='Completed'")
    orders = [{'pizza': rec['fields'].get('Pizza'), 'quantity': rec['fields'].get('Quantity'),
               'size': rec['fields'].get('Size'), 'price': rec['fields'].get('Price'), 
               'delivery_method': rec['fields'].get('Delivery Method')} for rec in records]

    return render_template('storeOrders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)



from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from airtable import Airtable
import re

app = Flask(__name__)

# Configure email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Replace with your email password or app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # Replace with sender email

mail = Mail(app)

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Orders'  # The Airtable table name for storing orders
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/checkout', methods=['POST'])
def process_checkout():
    try:
        # Extract form data
        pizza = request.form.get('pizza')
        quantity = request.form.get('quantity')
        size = request.form.get('size')
        price = request.form.get('price')
        delivery_method = request.form.get('delivery_method')  # 'in_store_pickup' or 'delivery'
        payment_method = request.form.get('payment_method')  # 'online' or 'in_store'
        email = request.form.get('email')  # Customer's email address

        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Invalid email address."}), 400

        # Store order details in Airtable
        order_data = {
            "Pizza": pizza,
            "Quantity": int(quantity),
            "Size": size,
            "Price": float(price),
            "Delivery Method": delivery_method,
            "Payment Method": payment_method,
            "Email": email,
            "Status": "Pending"  # Initial status
        }
        airtable.insert(order_data)

        # Payment status message
        payment_status = "Payment will be completed in-store." if payment_method == "in_store" else "Payment processed successfully!"

        # Send email receipt
        if email:
            subject = "Your Pizza Order Receipt"
            body = f"Thank you for your order!\n\nPizza: {pizza}\nQuantity: {quantity}\nSize: {size}\nPrice: ${price}\nPickup Option: {delivery_method}\nPayment Method: {payment_method}\nStatus: {payment_status}\n\nEnjoy your pizza!"
            
            msg = Message(subject, recipients=[email])
            msg.body = body
            mail.send(msg)

        return jsonify({"message": payment_status}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pickup-options', methods=['GET'])
def pickup_options():
    options = {
        "pickup_options": ["in_store_pickup", "delivery"],
        "payment_methods": ["online", "in_store"]
    }
    return jsonify(options), 200

@app.route('/checkout-form')
def checkout():
    return render_template('checkout.html')  # Ensure this file exists in your "templates" folder

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
from airtable import Airtable

app = Flask(__name__)

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Pizzas'  # Ensure this matches your Airtable table name
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable PAT

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

# Route: Display and Manage Menu Items
@app.route('/editMenuItems', methods=['GET', 'POST'])
def edit_menu_items():
    if request.method == 'POST':
        action = request.form.get('action')
        item_name = request.form.get('item')
        price = request.form.get('price')
        item_id = request.form.get('item_id')

        if action == 'add':
            new_item = {'Item': item_name, 'Price': float(price)}
            airtable.insert(new_item)

        elif action == 'update':
            updated_item = {'Item': item_name, 'Price': float(price)}
            airtable.update(item_id, updated_item)

        elif action == 'delete':
            airtable.delete(item_id)

        return redirect(url_for('edit_menu_items'))

    # Fetch Menu Items
    records = airtable.get_all()
    menu = [{'id': rec['id'], 'item': rec['fields'].get('Item', ''), 'price': rec['fields'].get('Price', 0)} for rec in records]

    return render_template('editMenuItems.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from airtable import Airtable

app = Flask(__name__)

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Pizzas'  # Updated table name
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/editprices')
def edit_prices():
    return render_template('editPrices.html')  # Ensure the file is in the "templates" folder

@app.route('/update_prices', methods=['POST'])
def update_prices():
    try:
        # Extract form data (assuming JSON format)
        form_data = request.json

        # Loop through each item and update the price in the **Pizzas** table
        for pizza_name, new_price in form_data.items():
            record = airtable.get_all(formula=f"{{Pizza}}='{pizza_name}'")

            if record:
                airtable.update(record[0]['id'], {'Price': float(new_price)})
            else:
                return jsonify({"error": f"Pizza '{pizza_name}' not found in Airtable."}), 404

        return jsonify({"message": "Prices updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Account Management'  # Updated table name
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user is the hardcoded admin
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['role'] = 'store_owner'  # Admin is always the store owner
            return redirect(url_for('dashboard'))

        # Otherwise, check Airtable for user authentication
        records = airtable.get_all(formula=f"{{Username}}='{username}'")
        if records:
            stored_password = records[0]['fields'].get('Password')
            role = records[0]['fields'].get('Role')
            if stored_password == password:
                session['role'] = role  # Save user role in session
                return redirect(url_for('dashboard'))

        return "Invalid username or password. Please try again."

    return render_template('login.html')  # Ensure this template exists

@app.route('/dashboard')
def dashboard():
    role = session.get('role')
    if role == 'store_owner':
        return "Welcome Admin! You can manage pizzas, menus, and prices."
    elif role == 'user':
        return "Welcome User! You can customize pizzas and browse the menu."
    elif role == 'guest':
        return "Welcome Guest! Feel free to browse and customize pizzas."
    else:
        return redirect(url_for('login'))  # Redirect to login if no role is set

@app.route('/logout')
def logout():
    session.pop('role', None)  # Clear user session
    return redirect(url_for('index'))

@app.route('/customize_pizza', methods=['GET'])
def customize_pizza():
    preset = request.args.get('preset')
    return f"Customize pizza as {preset}"  # Replace with proper logic

@app.route('/editMenuItems', methods=['GET'])
def edit_menu_items():
    # Restrict access to store_owner role (hardcoded admin)
    if session.get('role') != 'store_owner':
        return "Access denied. Only store owners can edit menu items.", 403
    preset = request.args.get('preset')
    return f"Edit Menu Items for {preset}"  # Replace with proper logic

@app.route('/editPrices', methods=['POST'])
def edit_prices():
    # Restrict access to store_owner role (hardcoded admin)
    if session.get('role') != 'store_owner':
        return "Access denied. Only store owners can edit prices.", 403
    role = request.form.get('role')
    return f"Edit Prices as {role}"  # Replace with proper logic

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Account Management'  # Correct table name
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the user is the hardcoded admin
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = username
            session['role'] = 'admin'  # Admin has full access
            return redirect(url_for('dashboard'))

        # Authenticate non-admin users via Airtable
        records = airtable.get_all(formula=f"{{Username}}='{username}'")
        if records:
            stored_password = records[0]['fields'].get('Password')
            role = records[0]['fields'].get('Role')
            if stored_password == password:
                session['username'] = username
                session['role'] = role
                return redirect(url_for('dashboard'))

        return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome {session['username']}! Your role is {session['role']}."
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Orders'  # Airtable table for storing orders
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/order_placed', methods=['GET'])
def order_placed():
    # Fetch order details from Airtable (assuming orders have a status "Pending")
    records = airtable.get_all(formula="{Status}='Pending'")

    if records:
        order_data = {
            'user': records[0]['fields'].get('User', 'Guest'),  # Updated to retrieve User field
            'email': records[0]['fields'].get('Email', 'No Email Provided'),
            'delivery_method': records[0]['fields'].get('Delivery Method', 'Delivery'),
            'payment_method': records[0]['fields'].get('Payment Method', 'Credit Card'),
            'items': [{'quantity': rec['fields'].get('Quantity'), 
                      'size': rec['fields'].get('Size'),
                      'pizza': rec['fields'].get('Pizza'), 
                      'price': rec['fields'].get('Price')} for rec in records],
            'total': sum(float(rec['fields'].get('Price', 0)) * int(rec['fields'].get('Quantity', 1)) for rec in records)
        }
    else:
        order_data = {"message": "No pending orders found."}

    return render_template('orderPlaced.html', order=order_data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Orders'  # Airtable table for storing orders
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Get the selected payment method
        payment_method = request.form.get('method')

        if not payment_method:
            return "Please choose a payment method.", 400

        # Store payment method in Airtable for pending orders
        records = airtable.get_all(formula="{Status}='Pending'")
        for record in records:
            airtable.update(record['id'], {'Payment Method': payment_method})

        # Redirect based on the selection
        if payment_method == "credit":
            return redirect(url_for('checkout'))
        elif payment_method == "in_store":
            return redirect(url_for('order_placed'))
        else:
            return "Invalid payment method selected.", 400

    return render_template('payment.html')

@app.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout.html')

@app.route('/order_placed', methods=['GET'])
def order_placed():
    # Fetch the latest order with pending status
    records = airtable.get_all(formula="{Status}='Pending'")
    if records:
        order_data = {
            'user': records[0]['fields'].get('User', 'Guest'),
            'email': records[0]['fields'].get('Email', 'No Email Provided'),
            'delivery_method': records[0]['fields'].get('Delivery Method', 'Delivery'),
            'payment_method': records[0]['fields'].get('Payment Method', 'Credit Card'),
            'items': [{'quantity': rec['fields'].get('Quantity'), 
                      'size': rec['fields'].get('Size'),
                      'pizza': rec['fields'].get('Pizza'), 
                      'price': rec['fields'].get('Price')} for rec in records],
            'total': sum(float(rec['fields'].get('Price', 0)) * int(rec['fields'].get('Quantity', 1)) for rec in records)
        }
        # Update order status to "Completed"
        for record in records:
            airtable.update(record['id'], {'Status': 'Completed'})
    else:
        order_data = {"message": "No pending orders found."}

    return render_template('orderPlaced.html', order=order_data)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Pizzas'  # Correct table name for retrieving menu data
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/')
def index():
    """Fetch menu data dynamically from Airtable and serve the customization page."""
    records = airtable.get_all()
    menu = {rec['fields'].get('Item'): {'price': rec['fields'].get('Price', 0), 'size': rec['fields'].get('Size', 'Medium')} for rec in records}

    return render_template('customize_pizza.html', menu=menu)  # Pass menu data to template

@app.route('/customize_pizza', methods=['POST'])
def customize_pizza():
    """Handle pizza customization and store selections in Airtable."""
    data = request.json

    pizza_type = data.get("pizzaType")
    size = data.get("size")
    quantity = data.get("quantity", 1)

    # Fetch price and size dynamically from Airtable
    records = airtable.get_all(formula=f"{{Item}}='{pizza_type}'")
    if records:
        price_per_pizza = records[0]['fields'].get('Price', 0)
        ingredients = records[0]['fields'].get('Ingredients', 'No ingredients listed')
        available_size = records[0]['fields'].get('Size', 'Medium')  # Default to "Medium" if not listed
    else:
        return jsonify({"error": "Pizza not found in menu."}), 404

    total_price = price_per_pizza * int(quantity)

    # Store order in Airtable
    order_data = {
        "Item": pizza_type,
        "Size": size if size else available_size,  # Use the selected size or the default one
        "Ingredients": ingredients,
        "Quantity": quantity,
        "Price": total_price,
        "Status": "Pending"
    }
    airtable.insert(order_data)

    response_message = f"{quantity} {size.capitalize()} {pizza_type.capitalize()} Pizza(s) with ingredients: {ingredients}, for ${total_price:.2f}"

    return jsonify({"message": response_message})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from airtable import Airtable
import re

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Simplified key for school use

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Account Management'  # Correct table name for storing user accounts
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Basic validation
        if not username or not email or not password:
            flash("All fields are required.", "error")
            return render_template('register.html')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.", "error")
            return render_template('register.html')

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template('register.html')

        # Check if the user already exists in Airtable
        existing_users = airtable.get_all(formula=f"OR({{Username}}='{username}', {{Email}}='{email}')")
        if existing_users:
            flash("Username or email already exists.", "error")
            return render_template('register.html')

        # Save the new user in Airtable
        user_data = {'Username': username, 'Email': email, 'Password': password}
        airtable.insert(user_data)

        flash("Account created successfully!", "success")
        return redirect(url_for('login'))  # Redirect to login page after registration

    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

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

    return render_template('adminOrders.html', orders=order_data)

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)

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
    return render_template('adminPanel.html')

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

    return render_template('reviewOrders.html', orders=order_data)

@app.route('/customize_pizza', methods=['GET'])
def customize_pizza():
    return render_template('customize_pizza.html')

if __name__ == '__main__':
    app.run(debug=True)
