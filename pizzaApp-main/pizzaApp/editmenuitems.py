from flask import Flask, render_template, request, redirect, url_for
from airtable import Airtable

app = Flask(__name__)

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'  # Your Airtable Base ID
TABLE_NAME = 'Pizzas'  # Ensure this matches your Airtable table name
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Your Airtable PAT

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

# Route: Display and Manage Menu Items
@app.route('/editMenuItems', methods=['GET', 'POST'])
def edit_menu_items():
    if request.method == 'POST':
        action = request.form.get('action')
        item_name = request.form.get('item')
        price = request.form.get('price')
        item_id = request.form.get('item_id')

        if action == 'add':
            new_item = {'Item': item_name, 'Price': float(price)}
            airtable.insert(new_item)

        elif action == 'update':
            updated_item = {'Item': item_name, 'Price': float(price)}
            airtable.update(item_id, updated_item)

        elif action == 'delete':
            airtable.delete(item_id)

        return redirect(url_for('edit_menu_items'))

    # Fetch Menu Items
    records = airtable.get_all()
    menu = [{'id': rec['id'], 'item': rec['fields'].get('Item', ''), 'price': rec['fields'].get('Price', 0)} for rec in records]

    return render_template('editMenuItems.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)

