
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Orders'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Get the selected payment method
        payment_method = request.form.get('method')

        if not payment_method:
            flash("Please choose a payment method.", "error")
            return redirect(url_for('payment'))

        # Store payment method in Airtable for all pending orders
        records = airtable.get_all(formula="AND({Status}='Pending')")
        if not records:
            flash("No pending orders found.", "info")
            return redirect(url_for('index'))

        for record in records:
            airtable.update(record['id'], {'Payment Method': payment_method})

        # Redirect based on the selection
        if payment_method == "credit":
            return redirect(url_for('checkout'))
        elif payment_method == "in_store":
            return redirect(url_for('order_placed'))
        else:
            flash("Invalid payment method selected.", "error")
            return redirect(url_for('payment'))

    return render_template('payment.html')

@app.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout.html')

@app.route('/order_placed', methods=['GET'])
def order_placed():
    try:
        records = airtable.get_all(formula="AND({Status}='Pending')")
        if not records:
            flash("No pending orders found.", "info")
            return redirect(url_for('index'))

        order_data = {
            'user': session.get('username', 'Guest'),  # Retrieve logged-in username
            'email': records[0]['fields'].get('Email', 'No Email Provided'),
            'delivery_method': records[0]['fields'].get('Delivery Method', 'Delivery'),
            'payment_method': records[0]['fields'].get('Payment Method', 'Credit Card'),
            'items': [
                {
                    'quantity': rec['fields'].get('Quantity', 1),
                    'size': rec['fields'].get('Size', 'Medium'),
                    'pizza': rec['fields'].get('Pizza', 'Unknown Pizza'),
                    'price': rec['fields'].get('Price', 0)
                }
                for rec in records
            ],
            'total': sum(float(rec['fields'].get('Price', 0)) * int(rec['fields'].get('Quantity', 1)) for rec in records)
        }

        # Mark all orders as "Completed"
        for record in records:
            airtable.update(record['id'], {'Status': 'Completed'})

        return render_template('orderPlaced.html', order=order_data)

    except Exception as e:
        flash(f"Error retrieving order details: {str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
