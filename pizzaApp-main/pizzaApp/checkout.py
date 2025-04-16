from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from airtable import Airtable
import re

app = Flask(__name__)

# Configure email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Replace with your email password or app password
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'  # Replace with sender email

mail = Mail(app)

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Orders'  # The Airtable table name for storing orders
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/checkout', methods=['POST'])
def process_checkout():
    try:
        # Extract form data
        pizza = request.form.get('pizza')
        quantity = request.form.get('quantity')
        size = request.form.get('size')
        price = request.form.get('price')
        delivery_method = request.form.get('delivery_method')  # 'in_store_pickup' or 'delivery'
        payment_method = request.form.get('payment_method')  # 'online' or 'in_store'
        email = request.form.get('email')  # Customer's email address

        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Invalid email address."}), 400

        # Store order details in Airtable
        order_data = {
            "Pizza": pizza,
            "Quantity": int(quantity),
            "Size": size,
            "Price": float(price),
            "Delivery Method": delivery_method,
            "Payment Method": payment_method,
            "Email": email,
            "Status": "Pending"  # Initial status
        }
        airtable.insert(order_data)

        # Payment status message
        payment_status = "Payment will be completed in-store." if payment_method == "in_store" else "Payment processed successfully!"

        # Send email receipt
        if email:
            subject = "Your Pizza Order Receipt"
            body = f"Thank you for your order!\n\nPizza: {pizza}\nQuantity: {quantity}\nSize: {size}\nPrice: ${price}\nPickup Option: {delivery_method}\nPayment Method: {payment_method}\nStatus: {payment_status}\n\nEnjoy your pizza!"
            
            msg = Message(subject, recipients=[email])
            msg.body = body
            mail.send(msg)

        return jsonify({"message": payment_status}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pickup-options', methods=['GET'])
def pickup_options():
    options = {
        "pickup_options": ["in_store_pickup", "delivery"],
        "payment_methods": ["online", "in_store"]
    }
    return jsonify(options), 200

@app.route('/checkout-form')
def checkout():
    return render_template('checkout.html')  # Ensure this file exists in your "templates" folder

if __name__ == '__main__':
    app.run(debug=True)
