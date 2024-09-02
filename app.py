from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database of stock prices
stock_prices = {
    'AAPL': 150.0,
    'GOOGL': 2800.0,
    'AMZN': 3500.0,
    'TSLA': 700.0,
    'MSFT': 300.0,
    'WMT': 225.0  
}

# Simulated user portfolio
user_portfolio = {}

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

@app.route('/buy', methods=['POST'])
def buy_stock():
    data = request.json
    stock_index = data.get('stock_index')
    shares = data.get('shares', type=int)

    if not stock_index or not shares:
        return jsonify({'error': 'Please provide both stock_index and shares in the request body'}), 400

    stock_index = stock_index.upper()
    stock_price = stock_prices.get(stock_index)

    if stock_price is None:
        return jsonify({'error': f'Stock index {stock_index} not found in the database'}), 404

    if stock_index in user_portfolio:
        user_portfolio[stock_index] += shares
    else:
        user_portfolio[stock_index] = shares

    return jsonify({'message': f'Successfully bought {shares} shares of {stock_index}', 'portfolio': user_portfolio})

@app.route('/sell', methods=['POST'])
def sell_stock():
    data = request.json
    stock_index = data.get('stock_index')
    shares = data.get('shares', type=int)

    if not stock_index or not shares:
        return jsonify({'error': 'Please provide both stock_index and shares in the request body'}), 400

    stock_index = stock_index.upper()

    if stock_index not in user_portfolio or user_portfolio[stock_index] < shares:
        return jsonify({'error': f'Not enough shares of {stock_index} to sell'}), 400

    user_portfolio[stock_index] -= shares

    if user_portfolio[stock_index] == 0:
        del user_portfolio[stock_index]

    return jsonify({'message': f'Successfully sold {shares} shares of {stock_index}', 'portfolio': user_portfolio})

@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    portfolio_value = 0.0

    for stock_index, shares in user_portfolio.items():
        stock_price = stock_prices.get(stock_index, 0)
        portfolio_value += shares * stock_price

    return jsonify({'portfolio': user_portfolio, 'total_value': portfolio_value})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
