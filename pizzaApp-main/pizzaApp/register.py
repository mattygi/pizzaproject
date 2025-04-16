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
