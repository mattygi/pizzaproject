from flask import Flask, render_template, request, redirect, url_for, flash, session
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Keep this secure in production

# Airtable Connection with Hardcoded API Token
BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Orders'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/cart', methods=['GET'])
def cart():
    try:
        records = airtable.get_all()
        cart = [{'id': rec['id'], 'pizza': rec['fields'].get('Pizza'), 'quantity': rec['fields'].get('Quantity'),
                 'size': rec['fields'].get('Size'), 'price': rec['fields'].get('Price')} for rec in records]

        if not cart:
            flash("Your cart is empty!", "info")

        return render_template('cart.html', cart=cart)
    except Exception as e:
        flash(f"Error fetching cart data: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/proceed', methods=['POST'])
def proceed():
    delivery_method = request.form.get('method')

    if not delivery_method:
        flash("Please select a delivery method!", "error")
        return redirect(url_for('cart'))

    try:
        records = airtable.get_all()
        for record in records:
            airtable.update(record['id'], {'Delivery Method': delivery_method})

        session['delivery_method'] = delivery_method  # Store method in session for tracking

        return redirect(url_for('checkout' if delivery_method == "delivery" else 'payment'))
    except Exception as e:
        flash(f"Error processing order: {str(e)}", "error")
        return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET'])
def checkout():
    try:
        records = airtable.get_all()
        for record in records:
            airtable.update(record['id'], {'Status': 'Completed'})

        flash("Order placed successfully!", "success")
        return render_template('orderPlaced.html')
    except Exception as e:
        flash(f"Error completing order: {str(e)}", "error")
        return redirect(url_for('cart'))

@app.route('/payment', methods=['GET'])
def payment():
    delivery_method = session.get('delivery_method', 'pickup')  # Default to pickup if missing
    return render_template('payment.html', delivery_method=delivery_method)

@app.route('/store_orders', methods=['GET'])
def store_orders():
    try:
        records = airtable.get_all(formula="AND({Status}='Completed')")
        orders = [{'pizza': rec['fields'].get('Pizza'), 'quantity': rec['fields'].get('Quantity'),
                   'size': rec['fields'].get('Size'), 'price': rec['fields'].get('Price'),
                   'delivery_method': rec['fields'].get('Delivery Method')} for rec in records]

        if not orders:
            flash("No completed orders found!", "info")

        return render_template('storeOrders.html', orders=orders)
    except Exception as e:
        flash(f"Error fetching store orders: {str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

