import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from unittest.mock import patch
from flask import json
from src.app import app
from src.database.create_tables import SavedRecipe  
from mock_data import mock_saved_recipes_query_all

class SavedRecipesTestCase(unittest.TestCase):

    def setUp(self):
        with patch.dict(os.environ, {
            'PG_USER': 'test_user',
            'PG_PASSWORD': 'test_password',
            'PG_HOST': 'localhost',
            'PG_PORT': '5432'
        }):
            self.app = app.test_client()
            self.app.testing = True
            self.app_context = app.app_context()
            self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("src.app.SavedRecipe.query.all")
    def test_default_sorting(self, mock_saved_recipes):
        mock_saved_recipes.return_value = mock_saved_recipes_query_all

        response = self.app.get("/saved_recipes")

        self.assertEqual(response.status_code, 200)

        self.assertIn(b"Japanese Gyoza Pot Stickers", response.data)
        self.assertIn(b"Spaghetti With Smoked Salmon and Prawns", response.data)

        # mock_saved_recipes.assert_called_once()

    @patch("src.app.SavedRecipe.query.order_by")
    def test_sort_by_protein(self, mock_order_by):
        # Send GET request with 'sort' parameter set to 'protein'
        response = self.app.get("/saved_recipes?sort=protein")

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Ensure the query was ordered by protein
        # mock_order_by.assert_called_with(SavedRecipe.protein.asc())

if __name__ == "__main__":
    unittest.main()