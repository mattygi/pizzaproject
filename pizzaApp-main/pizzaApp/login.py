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

