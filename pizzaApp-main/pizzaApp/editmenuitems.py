import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from airtable import Airtable

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# Airtable Connection
BASE_ID = 'appkRvP5WntxZWYOg'
TABLE_NAME = 'Pizzas'
API_TOKEN = 'patHZ6VyGi7miB6sg.3f9a3211d1cf0d5dda1139ea34247c0e19ac2b45cce40e104d800b36da12cac2'  # Hardcoded for school project

airtable = Airtable(BASE_ID, TABLE_NAME, API_TOKEN)

@app.route('/editMenuItems', methods=['GET', 'POST'])
def edit_menu_items():
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            item_name = request.form.get('item')
            price = request.form.get('price')
            item_id = request.form.get('item_id')

            # Validate input
            if action in ['add', 'update'] and (not item_name or not price):
                flash("Item name and price are required!", "error")
                return redirect(url_for('edit_menu_items'))

            try:
                price = float(price)
                if price < 0:
                    raise ValueError("Price must be non-negative.")
            except ValueError:
                flash("Invalid price format!", "error")
                return redirect(url_for('edit_menu_items'))

            if action == 'add':
                airtable.insert({'Item': item_name, 'Price': price})
                flash(f"Added new item: {item_name}", "success")

            elif action == 'update':
                airtable.update(item_id, {'Item': item_name, 'Price': price})
                flash(f"Updated item: {item_name}", "success")

            elif action == 'delete':
                airtable.delete(item_id)
                flash(f"Deleted item: {item_name}", "success")

            return redirect(url_for('edit_menu_items'))

        # Fetch Menu Items
        records = airtable.get_all()
        menu = [{'id': rec['id'], 'item': rec['fields'].get('Item', ''), 
                 'price': rec['fields'].get('Price', 0.00)} for rec in records]

        return render_template('editMenuItems.html', menu=menu)

    except Exception as e:
        flash(f"Error processing menu request: {str(e)}", "error")
        return redirect(url_for('index'))  # Redirect to homepage in case of failure

if __name__ == '__main__':
    app.run(debug=True)

