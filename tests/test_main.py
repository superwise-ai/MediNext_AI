"""
Test file for MediNext AI main application

This module contains basic tests for the main application functionality.
"""

import unittest
import sys
import os

# Add the app directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

class TestEHRDemoPortal(unittest.TestCase):
    """Test cases for MediNext AI application."""
    
    def test_imports(self):
        """Test that all required modules can be imported."""
        try:
            from components.header import create_header
            from components.sidebar import create_sidebar
            from components.dashboard_cards import create_dashboard_cards
            from components.patient_table import create_patient_table
            from components.activity_feed import create_activity_feed
            from components.analytics_charts import create_analytics_charts
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import required modules: {e}")
    
    def test_config_import(self):
        """Test that configuration can be imported."""
        try:
            from config.settings import APP_NAME, APP_VERSION
            self.assertEqual(APP_NAME, "MediNext AI")
            self.assertEqual(APP_VERSION, "1.0.0")
        except ImportError as e:
            self.fail(f"Failed to import configuration: {e}")
    
    def test_utils_import(self):
        """Test that utility functions can be imported."""
        try:
            from utils.data_generator import generate_patient_data
            self.assertTrue(callable(generate_patient_data))
        except ImportError as e:
            self.fail(f"Failed to import utility functions: {e}")

if __name__ == '__main__':
    unittest.main()
