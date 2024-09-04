import json
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import pandas as pd
from io import BytesIO
import os

from app.main import app, init_db, save_configuration, load_configurations, get_configuration

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database and test client before each test."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['DATABASE'] = self.db_path
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Initialize the database schema
        with app.app_context():
            init_db()

    def tearDown(self):
        """Close and remove the temporary database after each test."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_save_configuration(self):
        """Test saving a configuration to the database."""
        save_configuration('Test Config', 'AAPL', '2020-01-01', '2021-01-01', '1d', 'blue', 'GOOGL', 'red', True)
        configs = load_configurations()
        self.assertIn(('Test Config',), configs, "The configuration should be saved and retrievable from the database.")

    def test_load_configurations(self):
        """Test loading configurations from the database."""
        save_configuration('Test Config', 'AAPL', '2020-01-01', '2021-01-01', '1d', 'blue', 'GOOGL', 'red', True)
        configs = load_configurations()
        self.assertGreater(len(configs), 0, "There should be at least one configuration loaded from the database.")

    def test_get_configuration(self):
        """Test retrieving a specific configuration from the database."""
        save_configuration('Test Config', 'AAPL', '2020-01-01', '2021-01-01', '1d', 'blue', 'GOOGL', 'red', True)
        config = get_configuration('Test Config')
        self.assertIsNotNone(config, "The configuration should be retrievable from the database by name.")
        self.assertEqual(config[1], 'Test Config', "The retrieved configuration should match the saved one.")

    def test_index_page(self):
        """Test if the index page loads correctly with a GET request."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_save_configuration_route(self):
        """Test the save configuration functionality via POST request."""
        response = self.app.post('/', data=dict(
            action='save',
            config_name='Test Config',
            stockname='AAPL',
            start='2020-01-01',
            end='2021-01-01',
            timestep='1d',
            color1='blue',
            stockname2='GOOGL',
            color2='red',
            bestfit='on'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_load_configuration_route(self):
        """Test the load configuration functionality via POST request."""
        save_configuration('Test Config', 'AAPL', '2020-01-01', '2021-01-01', '1d', 'blue', 'GOOGL', 'red', True)
        response = self.app.post('/', data=dict(
            action='load',
            load_config='Test Config'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_generate_graph_route(self):
        """Test the generate graph functionality via POST request."""
        response = self.app.post('/', data=dict(
            action='generate',
            stockname='AAPL',
            start='2020-01-01',
            end='2021-01-01',
            timestep='1d',
            color1='blue',
            stockname2='GOOGL',
            color2='red',
            bestfit='on'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_download_configuration_route(self):
        """Test the download configuration functionality via POST request."""
        response = self.app.post('/', data=dict(
            action='download',
            stockname='AAPL',
            start='2020-01-01',
            end='2021-01-01',
            timestep='1d',
            color1='blue',
            stockname2='GOOGL',
            color2='red',
            bestfit='on'
        ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['stock1'], 'AAPL', "The JSON response should contain the correct stock1 value.")
        self.assertEqual(data['stock2'], 'GOOGL', "The JSON response should contain the correct stock2 value.")

if __name__ == '__main__':
    unittest.main()