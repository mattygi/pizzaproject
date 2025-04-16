
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Replace in production for security

# Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Account Management'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Hardcoded for school project

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate input fields
        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for('login'))

        # Check if the user is the hardcoded admin
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = username
            session['role'] = 'admin'
            session.permanent = True  # Keep the session active
            flash("Admin login successful!", "success")
            return redirect(url_for('customize_pizza'))

        # Authenticate non-admin users via Airtable
        records = airtable.get_all(formula=f"AND({{Username}}='{username}')")
        if records:
            stored_password = records[0]['fields'].get('Password')
            role = records[0]['fields'].get('Role')

            if stored_password == password:
                session['username'] = username
                session['role'] = role
                session.permanent = True
                flash("Login successful!", "success")
                return redirect(url_for('customize_pizza'))

        flash("Invalid username or password.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')  # Ensure register.html exists

@app.route('/customize_pizza')
def customize_pizza():
    if 'username' in session:
        return render_template('customize_pizza.html', username=session['username'])
    flash("Please log in first.", "error")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
