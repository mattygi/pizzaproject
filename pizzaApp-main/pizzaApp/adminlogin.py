from flask import Flask, render_template, request, redirect, url_for, session, flash
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Temporary key for development

# Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Airtable Connection
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
            return redirect(url_for('admin_menu'))  # Redirect to admin dashboard

        records = airtable.get_all(formula=f"{{Username}}='{username}'")
        if records:
            stored_password = records[0]['fields'].get('Password')
            role = records[0]['fields'].get('Role')

            if stored_password == password:
                session['role'] = role
                session['username'] = username
                flash("Login successful!", "success")
                return redirect(url_for('login'))  # Stay on the login page with success message
        
        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')

        if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Login successful!", "success")
            return redirect(url_for('admin_menu'))  # Redirect to admin menu
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for('admin_login'))

    return render_template('adminLogin.html')

@app.route('/admin_menu')
def admin_menu():
    if not session.get('admin_logged_in'):
        flash("Unauthorized access. Please log in.", "error")
        return redirect(url_for('admin_login'))
    
    return render_template('adminMenu.html', message="Welcome Admin! Manage your menu here.")

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

