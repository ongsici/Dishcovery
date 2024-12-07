import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from unittest.mock import patch
from mock_data import mock_recipes_by_ingredients, mock_recipe_by_id, mock_nutrition_by_id

from src.app import app

class TestIngredientsSearch(unittest.TestCase):
    def setUp(self):
        with patch.dict(os.environ, {
            'PG_USER': 'test_user',
            'PG_PASSWORD': 'test_password',
            'PG_HOST': 'localhost',
            'PG_PORT': '5432'
        }):
            with app.test_client() as client:
                self.app = client
        self.app.testing = True

    @patch("src.app.get_recipe_by_ingredients")
    @patch("src.app.get_recipe_by_id")
    @patch("src.app.get_nutrition_by_id")
    def test_ingredients_search_success(self, mock_get_nutrition_by_id, mock_get_recipe_by_id, mock_get_recipe_by_ingredients):
        # Mock responses for dependencies
        mock_get_recipe_by_ingredients.return_value = mock_recipes_by_ingredients
        mock_get_recipe_by_id.return_value = mock_recipe_by_id
        mock_get_nutrition_by_id.return_value = mock_nutrition_by_id

        # Send POST request
        response = self.app.post("/ingredients_search", data={"ingredients": ["tomato", "garlic", "pasta"]})

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Additional Ingredients", response.data)
        self.assertIn(b"Matching Ingredients", response.data)
        self.assertIn(b"Protein", response.data)
        self.assertIn(b"Carbohydrate", response.data)
        self.assertIn(b"Calories", response.data)
        self.assertIn(b"Fat", response.data)
        self.assertIn(b"Penne Arrabiata", response.data) 
        self.assertIn(b"parsley", response.data) 
        self.assertIn(b"peppers", response.data)
        self.assertIn(b"tomato", response.data) 
        self.assertIn(b"garlic", response.data)
    

    @patch("src.app.get_recipe_by_ingredients")
    def test_ingredients_search_failure(self, mock_get_recipe_by_ingredients):
        mock_get_recipe_by_ingredients.return_value = None

        response = self.app.post("/ingredients_search", data={"ingredients": ["spaghetti"]})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Failed to fetch recipes", response.data)

    @patch("src.app.get_recipe_by_ingredients")
    @patch("src.app.get_recipe_by_id")
    def test_recipe_details_fetch_failure(self, mock_get_recipe_by_id, mock_get_recipe_by_ingredients):
        mock_get_recipe_by_ingredients.return_value = mock_recipes_by_ingredients
        mock_get_recipe_by_id.return_value = None

        response = self.app.post("/ingredients_search", data={"ingredients": ["spaghetti"]})
        print(mock_get_recipe_by_id.return_value)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Failed to fetch recipes", response.data)

    @patch("src.app.get_recipe_by_ingredients")
    @patch("src.app.get_recipe_by_id")
    @patch("src.app.get_nutrition_by_id")
    def test_nutrition_fetch_failure(self, mock_get_nutrition_by_id, mock_get_recipe_by_id, mock_get_recipe_by_ingredients):
        mock_get_recipe_by_ingredients.return_value = mock_recipes_by_ingredients
        mock_get_recipe_by_id.return_value = mock_get_recipe_by_id
        mock_get_nutrition_by_id.return_value = None

        response = self.app.post("/ingredients_search", data={"ingredients": ["spaghetti"]})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Failed to fetch recipes", response.data)

if __name__ == "__main__":
    unittest.main()
