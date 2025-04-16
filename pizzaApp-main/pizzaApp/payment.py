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
