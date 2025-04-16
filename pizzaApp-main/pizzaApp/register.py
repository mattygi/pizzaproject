
from flask import Flask, render_template, request, redirect, url_for, flash
from airtable import Airtable
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Account Management'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'

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
            return redirect(url_for('register'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.", "error")
            return redirect(url_for('register'))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for('register'))

        # Check if user exists in Airtable
        try:
            existing_users = airtable.get_all(formula=f"OR( {{Username}} = '{username}', {{Email}} = '{email}' )")
            if existing_users:
                flash("Username or email already exists.", "error")
                return redirect(url_for('register'))
        except Exception as e:
            flash(f"Error checking existing users: {str(e)}", "error")
            return redirect(url_for('register'))

        # Hash password before storing
        hashed_password = generate_password_hash(password)
        user_data = {'Username': username, 'Email': email, 'Password': hashed_password}
        airtable.insert(user_data)

        flash("Account created successfully!", "success")
        return redirect(url_for('login'))  # Redirect to login after registration

    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
