
import os
from flask import Flask, request, jsonify, render_template, flash
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Pizzas'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Hardcoded for school project

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/editprices')
def edit_prices():
    try:
        # Fetch menu items from Airtable
        records = airtable.get_all()
        menu = {rec['fields']['Pizza']: rec['fields'].get('Price', 0.00) for rec in records}

        return render_template('editPrices.html', menu=menu)
    
    except Exception as e:
        flash(f"Error fetching menu prices: {str(e)}", "error")
        return jsonify({"error": str(e)}), 500

@app.route('/update_prices', methods=['POST'])
def update_prices():
    try:
        form_data = request.json  # Expect JSON input

        if not form_data:
            return jsonify({"error": "No data provided."}), 400

        for pizza_name, new_price in form_data.items():
            if not pizza_name or new_price is None:
                return jsonify({"error": f"Invalid data for '{pizza_name}'."}), 400
            
            try:
                new_price = float(new_price)
                if new_price < 0:
                    raise ValueError("Price must be a non-negative number.")
            except ValueError:
                return jsonify({"error": f"Invalid price format for '{pizza_name}'."}), 400

            # Fetch matching record
            record = airtable.get_all(formula=f"{{Pizza}}='{pizza_name}'")

            if record:
                airtable.update(record[0]['id'], {'Price': new_price})
            else:
                return jsonify({"error": f"Pizza '{pizza_name}' not found in Airtable."}), 404

        return jsonify({"message": "Prices updated successfully"}), 200

    except Exception as e:
        flash(f"Error updating prices: {str(e)}", "error")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
