# Flask Application Unit Testing Documentation

## Overview

This document provides detailed instructions and explanations for the unit tests created for a Flask application. The application involves configurations and operations related to stock data, such as saving configurations, loading configurations, and generating graphs. The unit tests ensure that these functionalities work correctly and as expected.

## Test Structure

The unit tests are written using Python's built-in `unittest` framework. Each test case is designed to verify a specific part of the Flask application's functionality, including database operations, route handling, and application logic.

### Files Involved

* **main.py** : Contains the Flask application and the `init_db`, `save_configuration`, `load_configurations`, and `get_configuration` functions.
* **unit_test.py** : Contains the unit tests for the Flask application.

## Test Case Overview

### 1. **Test Setup and Teardown**

The `setUp` and `tearDown` methods ensure that each test runs in a clean, isolated environment with a temporary SQLite database.

* **setUp** :
* Creates a temporary database using `tempfile.mkstemp()`.
* Patches the Flask application's database to use the temporary database.
* Initializes the database schema by calling `init_db()` within the app's context.
* **tearDown** :
* Closes and removes the temporary database file after each test to ensure isolation between tests.

### 2. **Test Cases**

Each test case verifies a specific functionality of the Flask application.

#### a. **test_save_configuration**

* **Purpose** : Verifies that a configuration can be saved to the database.
* **Steps** :
* Saves a test configuration to the database.
* Loads configurations from the database.
* Asserts that the saved configuration is present in the database.

#### b. **test_load_configurations**

* **Purpose** : Tests that configurations can be loaded from the database.
* **Steps** :
* Saves a configuration.
* Loads all configurations.
* Asserts that there is at least one configuration in the database.

#### c. **test_get_configuration**

* **Purpose** : Ensures that a specific configuration can be retrieved by name.
* **Steps** :
* Saves a test configuration.
* Retrieves the saved configuration by name.
* Asserts that the retrieved configuration matches the saved one.

#### d. **test_index_page**

* **Purpose** : Verifies that the index page loads correctly.
* **Steps** :
* Makes a GET request to the index page (`/`).
* Asserts that the response status code is `200`.

#### e. **test_save_configuration_route**

* **Purpose** : Tests the save configuration functionality via a POST request.
* **Steps** :
* Submits a POST request to the save route with configuration data.
* Asserts that the response status code is `200`.

#### f. **test_load_configuration_route**

* **Purpose** : Verifies that a saved configuration can be loaded via a POST request.
* **Steps** :
* Saves a configuration.
* Submits a POST request to the load route.
* Asserts that the response status code is `200`.

#### g. **test_generate_graph_route**

* **Purpose** : Tests the graph generation functionality via a POST request.
* **Steps** :
* Submits a POST request to generate a graph using configuration data.
* Asserts that the response status code is `200`.

#### h. **test_download_configuration_route**

* **Purpose** : Tests the download configuration functionality via a POST request.
* **Steps** :
* Submits a POST request to download the configuration as JSON.
* Asserts that the response status code is `200`.
* Asserts that the returned JSON data matches the expected configuration values.

## Notes

* The `sqlite3.connect` method is patched within the test cases to ensure that each test uses a temporary database file. This approach isolates the tests from the main application's database, ensuring that the tests do not affect the production environment.
* Ensure that `main.py` is correctly importing and using the `init_db`, `save_configuration`, `load_configurations`, and `get_configuration` functions.

## Conclusion

These unit tests are designed to thoroughly verify the functionality of the Flask application. By running these tests, you can confidently make changes to the application, knowing that core features will be automatically validated against potential regressions.
