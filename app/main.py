import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI environments

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import os
import numpy as np
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from prometheus_client import Counter, generate_latest, Gauge, Histogram
import psutil
from time import time


app = Flask(__name__,static_folder='/app/static') ##remove static_folder for local run
app.secret_key = 'your_secret_key'


# Initialize the database
def init_db():
    conn = sqlite3.connect('configurations.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            stock1 TEXT,
            start_date TEXT,
            end_date TEXT,
            timestep TEXT,
            color1 TEXT,
            stock2 TEXT,
            color2 TEXT,
            bestfit INTEGER
        )
    ''')
    conn.commit()
    conn.close()


# Save the configuration into the database
def save_configuration(name, stock1, start_date, end_date, timestep, color1, stock2, color2, bestfit):
    conn = sqlite3.connect('configurations.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO configurations (name, stock1, start_date, end_date, timestep, color1, stock2, color2, bestfit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, stock1, start_date, end_date, timestep, color1, stock2, color2, int(bestfit)))
    conn.commit()
    conn.close()


# Load all saved configurations from the database
def load_configurations():
    conn = sqlite3.connect('configurations.db')
    c = conn.cursor()
    c.execute('SELECT name FROM configurations')
    configs = c.fetchall()
    conn.close()
    return configs


# Load a specific configuration from the database
def get_configuration(name):
    conn = sqlite3.connect('configurations.db')
    c = conn.cursor()
    c.execute('SELECT * FROM configurations WHERE name = ?', (name,))
    config = c.fetchone()
    conn.close()
    return config


# Initialize the database on application start
init_db()
# Define a Prometheus Counter to track the number of times the generate button is clicked
generate_counter = Counter('generate_button_clicks', 'Number of times the Generate button has been clicked')
total_requests = Counter('http_requests_total', 'Total HTTP requests made to the application')
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage')
memory_usage = Gauge('memory_usage_percent', 'Memory usage percentage')
best_fit_usage = Counter('best_fit_usage', 'Number of times the line of best fit was selected')
total_graph_generations = Counter('total_graph_generations', 'Total number of graph generations')
best_fit_percentage = Gauge('best_fit_percentage', 'Percentage of graphs generated with best fit selected')
compare_usage = Counter('compare_function_usage', 'Number of times the compare function was used')
compare_percentage = Gauge('compare_function_percentage', 'Percentage of graphs generated with compare function')
api_fetch_errors = Counter('api_fetch_errors', 'Number of API errors while fetching stock data')
http_500_errors = Counter('http_500_errors', 'Number of HTTP 500 errors (internal server errors)')
request_latency = Histogram('request_latency_seconds', 'Request latency in seconds', buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0])
graph_generation_latency = Histogram('graph_generation_latency_seconds', 'Latency of graph generation in seconds', buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0])



@app.before_request
def before_request():
    request.start_time = time()
    total_requests.inc()
    cpu_usage.set(psutil.cpu_percent(interval=1))
    memory_usage.set(psutil.virtual_memory().percent)



# After each request, calculate the elapsed time and record it in the histogram
@app.after_request
def record_latency(response):
    request_latency.observe(time() - request.start_time)
    return response


@app.errorhandler(500)
def handle_500_error(error):
    http_500_errors.inc()  # Increment the 500 error counter
    return render_template('500.html'), 500




@app.route('/', methods=['GET', 'POST'])
def index():
    configurations = load_configurations()  # Load configurations from the database
    selected_config = None
    filename = None  # Initialize filename as None for debugging

    if request.method == 'POST':
        action = request.form.get('action')

        # Handle saving configuration
        if action == 'save':
            print("Saving configuration")  # Debugging line
            name = request.form['config_name']
            stock1 = request.form['stockname']
            start_date = request.form['start']
            end_date = request.form['end']
            time_step = request.form['timestep']
            color1 = request.form.get('color1', 'blue')  # Default to 'blue' if color1 is not provided
            stock2 = request.form['stockname2']
            color2 = request.form.get('color2', 'red')  # Default to 'red' if color2 is not provided
            bestfit = 'bestfit' in request.form

            save_configuration(name, stock1, start_date, end_date, time_step, color1, stock2, color2, bestfit)
            flash(f"Configuration '{name}' saved successfully.")

            # Pass back the form data to retain after saving
            return render_template('index.html',
                                   configurations=configurations,
                                   selected_config=selected_config,
                                   stockname=stock1,
                                   stockname2=stock2,
                                   start=start_date,
                                   end=end_date,
                                   color1=color1,
                                   color2=color2,
                                   time_step=time_step,
                                   bestfit_checked=bestfit,
                                   filename=filename)

        # Handle loading configuration
        elif action == 'load':
            print(f"Loading configuration: {request.form['load_config']}")  # Debugging line
            selected_config = get_configuration(request.form['load_config'])
            print(f"Loaded configuration: {selected_config}")  # Debugging line
            flash(f"Configuration '{request.form['load_config']}' loaded.")

            # After loading, update the form with the loaded configuration values
            if selected_config:
                # If a configuration is loaded, populate the form with its values
                return render_template('index.html',
                                       configurations=configurations,
                                       selected_config=selected_config,
                                       stockname=selected_config[2],  # stock1
                                       start=selected_config[3],  # start_date
                                       end=selected_config[4],  # end_date
                                       time_step=selected_config[5],  # timestep
                                       color1=selected_config[6],  # color1
                                       stockname2=selected_config[7],  # stock2
                                       color2=selected_config[8],  # color2
                                       bestfit_checked=bool(selected_config[9]),
                                       filename=filename)
            else:
                # If no configuration is loaded, use default values
                return render_template('index.html',
                                       configurations=configurations,
                                       selected_config=None,
                                       stockname='AAPL',  # Default stock name
                                       start='2020-01-01',  # Default start date
                                       end='2023-01-01',  # Default end date
                                       time_step='1 day',  # Default time step
                                       color1='blue',  # Default color1
                                       stockname2='',  # Default no second stock
                                       color2='red',  # Default color2
                                       bestfit_checked=False,
                                       filename=filename)
        # Handle downloading configuration as JSON
        elif action == 'download':
            print("Downloading configuration")  # Debugging line
            config = {
                'stock1': request.form['stockname'],
                'start_date': request.form['start'],
                'end_date': request.form['end'],
                'timestep': request.form['timestep'],
                'color1': request.form['color1'],
                'stock2': request.form['stockname2'],
                'color2': request.form['color2'],
                'bestfit': 'bestfit' in request.form
            }
            return jsonify(config)

        # Handle graph generation
        elif action == 'generate':
            generate_counter.inc()# Increment the Prometheus counter
            total_graph_generations.inc()

            # Check if the best fit option is selected and increment the best fit usage counter
            show_best_fit = 'bestfit' in request.form
            if show_best_fit:
                best_fit_usage.inc()



            print("Generating graph")  # Debugging line
            with graph_generation_latency.time():
                stock1 = request.form['stockname']
                start_date = request.form['start']
                end_date = request.form['end']
                time_step = request.form['timestep']
                color1 = request.form.get('color1', 'blue').lower()  # Default to 'blue' if color1 is not provided
                stock2 = request.form.get('stockname2', None)
                color2 = request.form.get('color2', 'red')
                show_best_fit = 'bestfit' in request.form

                # Parse start and end dates
                try:
                    start_date_parsed = pd.to_datetime(start_date.strip())
                    end_date_parsed = pd.to_datetime(end_date.strip())
                    current_date = pd.to_datetime(datetime.now())

                    # Check if the start date is after the end date, and swap them if necessary
                    if start_date_parsed > end_date_parsed:
                        start_date_parsed, end_date_parsed = end_date_parsed, start_date_parsed
                        flash("Start date was after the end date, so the dates have been swapped.")
                    # Clip the end date to the current date if it's in the future
                    if end_date_parsed > current_date:
                        end_date_parsed = current_date
                        flash(f"End date was after the current date and has been clipped to {current_date.strftime('%Y-%m-%d')}.")
                except ValueError:
                    flash("Invalid date format. Please use the date picker.")
                    return redirect(url_for('index'))

                # Ensure the start and end dates are valid
                if pd.isna(start_date_parsed) or pd.isna(end_date_parsed):
                    flash("Please enter valid start and end dates.")
                    return redirect(url_for('index'))

                print(f"Downloading data for {stock1} from {start_date_parsed} to {end_date_parsed}")  # Debugging line
                # Download stock1 data from yfinance

                try:
                    data1 = yf.download(stock1, start=start_date_parsed, end=end_date_parsed)
                    if data1.empty:
                        api_fetch_errors.inc()  # Increment the API fetch error counter
                        flash(f"Failed to fetch data for {stock1}.")
                        return render_template('index.html')  # Handle the error case
                except Exception as e:
                    api_fetch_errors.inc()  # Increment the API fetch error counter
                    flash(f"Error fetching stock data: {e}")
                    return render_template('index.html')
                    # Check if data1 has at least 2 points

                if len(data1) < 2:
                    flash(f"Not enough data points to generate the graph for {stock1}. At least 2 data points are required.")
                    return redirect(url_for('index'))

                # Resample data based on time_step
                if time_step == "1 week":
                    data1 = data1.resample('W').ffill()

                # Download and process second stock data (if provided)
                data2 = None
                if stock2:
                    compare_usage.inc()
                    print(f"Downloading data for second stock {stock2}")  # Debugging line

                    try:
                        data2 = yf.download(stock2, start=start_date_parsed, end=end_date_parsed)
                        if data2.empty:
                            api_fetch_errors.inc()  # Increment the API fetch error counter
                            flash(f"Failed to fetch data for {stock2}.")
                            return render_template('index.html')  # Handle the error case
                    except Exception as e:
                        api_fetch_errors.inc()  # Increment the API fetch error counter
                        flash(f"Error fetching stock data: {e}")
                        return render_template('index.html')

                        # Check if data2 has at least 2 points
                    if len(data2) < 2:
                        flash(f"Not enough data points to generate the graph for {stock2}. At least 2 data points are required.")
                        return redirect(url_for('index'))

                    if time_step == "1 week":
                        data2 = data2.resample('W').ffill()

                # Create the plot
                fig, ax = plt.subplots(figsize=(10, 5))
                print("Plotting data")  # Debugging line

                # Plot stock 1
                ax.plot(data1.index, data1['Close'], color=color1, label=stock1)

                # Add line of best fit for stock 1 if checkbox is selected
                if show_best_fit:
                    print(f"Adding best fit line for {stock1}")  # Debugging line
                    x_values = np.arange(len(data1))
                    y_values = data1['Close'].values

                    if len(x_values) > 1 and len(np.unique(y_values)) > 1 and np.all(np.isfinite(y_values)):
                        try:
                            coeffs = np.polyfit(x_values, y_values, 1)
                            best_fit_line = np.polyval(coeffs, x_values)
                            ax.plot(data1.index, best_fit_line, color='orange', linestyle='--', label=f'{stock1} Best Fit')
                        except np.linalg.LinAlgError:
                            flash(f"Could not generate a line of best fit for {stock1} due to data issues.")
                    else:
                        flash(f"Insufficient data to generate a best fit line for {stock1}.")

                # Plot stock 2 (if selected)
                if data2 is not None:
                    print(f"Plotting second stock {stock2}")  # Debugging line
                    ax.plot(data2.index, data2['Close'], color=color2, label=stock2)

                    # Add line of best fit for stock 2 if checkbox is selected
                    if show_best_fit:
                        print(f"Adding best fit line for {stock2}")  # Debugging line
                        x_values2 = np.arange(len(data2))
                        y_values2 = data2['Close'].values

                        if len(x_values2) > 1 and len(np.unique(y_values2)) > 1 and np.all(np.isfinite(y_values2)):
                            try:
                                coeffs2 = np.polyfit(x_values2, y_values2, 1)
                                best_fit_line2 = np.polyval(coeffs2, x_values2)
                                ax.plot(data2.index, best_fit_line2, color='purple', linestyle='--', label=f'{stock2} Best Fit')
                            except np.linalg.LinAlgError:
                                flash(f"Could not generate a line of best fit for {stock2} due to data issues.")
                        else:
                            flash(f"Insufficient data to generate a best fit line for {stock2}.")
                if total_graph_generations._value.get() > 0:  # Avoid division by zero
                    percentage_compare = (compare_usage._value.get() / total_graph_generations._value.get()) * 100
                    compare_percentage.set(percentage_compare)
                    percentage = (best_fit_usage._value.get() / total_graph_generations._value.get()) * 100
                    best_fit_percentage.set(percentage)
                # Customize the graph
                ax.set_xlabel("Date", fontsize=9)
                ax.set_ylabel("Price", fontsize=9)
                ax.tick_params(axis='both', which='major', labelsize=9)
                ax.grid(True)
                ax.legend()

                # Set the title
                ax.set_title(f"Stock Prices from {start_date_parsed.strftime('%Y-%m-%d')} to {end_date_parsed.strftime('%Y-%m-%d')}")

                # Save the plot
                plot_path = os.path.join('static', 'plot.png')

                if not os.path.exists('static'):
                    os.makedirs('static')



                print(f"Saving plot to {plot_path}")  # Debugging line
                fig.savefig(plot_path)
                plt.close(fig)  # Close the figure to free memory
                filename = 'plot.png'
                print(f"Plot saved successfully to {filename}")  # Debugging line

            # Pass back the form data to retain in the form after submission
            return render_template('index.html',
                                   start=start_date,
                                   end=end_date,
                                   stockname=stock1,
                                   stockname2=stock2,
                                   color1=request.form.get('color1', 'blue'),  # Ensure color1 exists
                                   color2=request.form.get('color2', 'red'),  # Ensure color2 exists
                                   time_step=time_step,
                                   filename=filename,
                                   bestfit_checked=show_best_fit,
                                   configurations=configurations)


    return render_template('index.html', configurations=configurations, selected_config=selected_config)

@app.route('/metrics')
def metrics():
        return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
if __name__ == "__main__":
    app.run(debug=True)
