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

    return render_template('adminLogin.html')

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

