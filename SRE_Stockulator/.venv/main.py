import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI environments

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock = request.form['stockname']

        # Attempt to parse start and end dates
        try:
            start_date = pd.to_datetime(request.form['start'].strip(), format="%d/%m/%Y")
            end_date = pd.to_datetime(request.form['end'].strip(), format="%d/%m/%Y")
            print(f"Parsed start date: {start_date}, Parsed end date: {end_date}")  # Debugging line
        except ValueError:
            flash("Invalid date format. Please use DD/MM/YYYY.")
            return redirect(url_for('index'))

        time_step = request.form['timestep']
        color = request.form['color'].lower()

        # Ensure the start and end dates are valid
        if pd.isna(start_date) or pd.isna(end_date):
            flash("Please enter valid start and end dates.")
            return redirect(url_for('index'))

        # Download stock data
        data = yf.download(stock, start=start_date, end=end_date)

        # Resample data based on time_step
        if time_step == "1 hour":
            data = data.resample('H').ffill()
        elif time_step == "1 week":
            data = data.resample('W').ffill()

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data['Close'], color=color)
        ax.set_title(f"{stock} Price from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")

        # Save the plot
        plot_path = os.path.join('static', 'plot.png')

        # Ensure the 'static' directory exists
        if not os.path.exists('static'):
            os.makedirs('static')

        fig.savefig(plot_path)
        plt.close(fig)  # Close the figure to free memory

        return redirect(url_for('index', filename='plot.png'))

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
