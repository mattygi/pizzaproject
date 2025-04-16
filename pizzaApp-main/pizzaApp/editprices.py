from flask import Flask, request, jsonify, render_template
from airtable import Airtable

app = Flask(__name__)

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Pizzas'  # Updated table name
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable Personal Access Token

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/editprices')
def edit_prices():
    return render_template('editPrices.html')  # Ensure the file is in the "templates" folder

@app.route('/update_prices', methods=['POST'])
def update_prices():
    try:
        # Extract form data (assuming JSON format)
        form_data = request.json

        # Loop through each item and update the price in the **Pizzas** table
        for pizza_name, new_price in form_data.items():
            record = airtable.get_all(formula=f"{{Pizza}}='{pizza_name}'")

            if record:
                airtable.update(record[0]['id'], {'Price': float(new_price)})
            else:
                return jsonify({"error": f"Pizza '{pizza_name}' not found in Airtable."}), 404

        return jsonify({"message": "Prices updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    app.run(debug=True)
