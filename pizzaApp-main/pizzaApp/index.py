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
