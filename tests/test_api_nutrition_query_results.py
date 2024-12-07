import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from unittest.mock import patch
from src.app import app
from src.database.create_tables import SavedRecipe  
from mock_data import mock_saved_recipes_query_all

class NutritionQueryResultsTestCase(unittest.TestCase):

    # Set up the app for testing
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
    def test_nutrition_query_results(self, mock_saved_recipes):
        mock_saved_recipes.return_value = mock_saved_recipes_query_all
        
        form_data = {
            "age": "25",
            "gender": "male",
            "height": "180",
            "weight": "75",
            "activityLevel": "moderate"
        }

        # Send a post request to nutrition_query that will redirect to nutrition_query_results
        response = self.app.post("/nutrition_query", data=form_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        self.assertIn(b"25", response.data)  
        self.assertIn(b"male", response.data) 
        self.assertIn(b"180", response.data)  
        self.assertIn(b"75", response.data)  
        self.assertIn(b'Nutrition Query Results', response.data)
      
if __name__ == "__main__":
    unittest.main()
