# Stockulator Documentation

## Overview

Stockulator is a web-based application built using Flask that allows users to generate stock price graphs for one or two stocks over a selected date range. Users can save their settings as configurations, load previously saved configurations, and download the configurations as JSON files.

## Features

- **Stock Price Graph Generation**: Generate graphs for one or two stocks over a specified date range.
- **Multiple Time Steps**: Users can choose to view stock data by day or by week.
- **Best Fit Line**: Optionally add a line of best fit to the graph.
- **Configuration Management**: Save configurations with stock names, colors, date ranges, and options. Load or download saved configurations.
- **Graph Customization**: Select colors for each stock line to differentiate them.

## Setup and Installation

### Requirements

Ensure that you have the following dependencies installed:

- Python 3.x
- Flask
- Matplotlib
- Pandas
- YFinance
- SQLite (for database storage of configurations)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Stockulator.git
   cd Stockulator
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:
   ```bash
   python main.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`.

### SQLite Database Setup

The application uses an SQLite database to store configurations. On the first run, the database will be initialized automatically.

## Application Usage

### User Interface

The interface consists of a form on the left and the graph display on the right.

- **Load Configuration**: A dropdown where users can load previously saved configurations.
- **Stock Name**: Input the stock symbol (e.g., AAPL for Apple, TSLA for Tesla).
- **Start Date/End Date**: Select the start and end dates for the stock data.
- **Time Step**: Choose whether to view the data by "1 Day" or "1 Week".
- **Color Selection**: Pick a color for the stock line (for both stock 1 and stock 2, if applicable).
- **Add Line of Best Fit**: Option to add a best fit line to the graph.

After generating a graph, the form fields retain the user's input.

### Buttons

- **Generate**: Generate the graph based on the selected inputs.
- **Save Configuration**: Save the current form data as a configuration.
- **Download Configuration**: Download the current configuration as a JSON file.

### Graph

Once generated, the graph will be displayed on the right side of the interface. The graph includes:
- Stock lines (for one or two stocks).
- Optional best fit lines.
- Date range on the x-axis and stock price on the y-axis.

## Configuration Management

- **Save a Configuration**: After entering your settings in the form, you can save them with a custom name. Enter a configuration name and click "Save Configuration".
- **Load a Configuration**: Select a previously saved configuration from the "Load Configuration" dropdown and click "Load" to populate the form with the saved settings.
- **Download a Configuration**: Download the current configuration as a JSON file.

## Known Issues and Troubleshooting

- **Bad Request Error**: Ensure all required fields are filled before submitting the form. If a configuration is loaded, check that all fields are populated correctly.
- **Graph Not Displaying**: Ensure that the stock symbol is valid, and there is data available for the selected date range.
- **Line of Best Fit Errors**: If the stock data has insufficient data points or invalid values, the best fit line may not be generated.

## File Structure

```
Stockulator/
│
├── static/
│   └── plot.png            # Generated graphs
│
├── templates/
│   └── index.html          # HTML template for the application
│
├── configurations.db        # SQLite database storing saved configurations
├── main.py                  # Main Flask application
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

## Future Improvements

- **Stock Autocomplete**: Implement an autocomplete feature for stock symbols.
- **Additional Graph Customization**: Add options for more graph customizations, such as line thickness, styles, and additional annotations.
- **Performance Optimization**: Improve performance for generating graphs with large datasets.

## Contributing

If you'd like to contribute to Stockulator, please fork the repository and submit a pull request.

### License

This project is licensed under the MIT License.
