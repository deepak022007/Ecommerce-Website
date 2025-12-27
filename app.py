from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)


PRODUCTS_FILE = 'product.json'
ORDERS_FILE = 'orders.json'


def load_products():
    if not os.path.exists(PRODUCTS_FILE): return []
    with open(PRODUCTS_FILE, 'r') as f:
        return json.load(f)

def save_order(order_data):
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'w') as f: json.dump([], f)
    
    with open(ORDERS_FILE, 'r') as f:
        orders = json.load(f)
    

    order_data['id'] = len(orders) + 1
    order_data['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    orders.append(order_data)
    
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=4)
    return order_data


@app.route('/')
def home(): return render_template('index.html')

@app.route('/product')
def product_page(): return render_template('product.html')

@app.route('/cart')
def cart_page(): return render_template('cart.html')

@app.route('/checkout')
def checkout_page(): return render_template('checkout.html')

@app.route('/invoice')
def invoice_page(): return render_template('invoice.html')



@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(load_products())

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    return jsonify(product) if product else ('', 404)

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    saved_order = save_order(data)
    print(f"💰 New Order Received: {saved_order['total']} INR")
    return jsonify({"status": "success", "order_id": saved_order['id']})

if __name__ == '__main__':
    app.run(debug=True, port=5001)