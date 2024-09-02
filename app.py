# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database of stock prices
stock_prices = {
    'AAPL': 150.0,
    'GOOGL': 2800.0,
    'AMZN': 3500.0,
    'TSLA': 700.0,
    'MSFT': 300.0,
    'WLMRT': 225.0 
}

@app.route('/calculate', methods=['GET'])
def calculate_stock_value():
    stock_index = request.args.get('stock_index')
    shares = request.args.get('shares', type=int)

    if not stock_index or not shares:
        return jsonify({'error': 'Please provide both stock_index and shares parameters'}), 400

    stock_price = stock_prices.get(stock_index.upper())

    if stock_price is None:
        return jsonify({'error': f'Stock index {stock_index} not found in the database'}), 404

    total_value = stock_price * shares
    return jsonify({'stock_index': stock_index.upper(), 'shares': shares, 'total_value': total_value})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

