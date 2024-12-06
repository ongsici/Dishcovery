import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from unittest.mock import patch
from src.app import app 

class NutritionQueryTestCase(unittest.TestCase):

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

    @patch("src.app.get_daily_nutrition_intake")
    def test_nutrition_query_success(self, mock_get_daily_nutrition_intake):
   
        mock_get_daily_nutrition_intake.return_value = expected_result = {
            "Calories": 2277,
            "Carbohydrate": 370,  
            "Protein": 44,
            "Fat": 89 
        }

        response = self.app.post("/nutrition_query", data={
            "age": "25",
            "gender": "male",
            "height": "180",
            "weight": "75",
            "activityLevel": "active"
        })

        self.assertEqual(response.status_code, 302)  
        # check redirect URL 
        self.assertIn("/nutrition_query_results", response.location)  

    @patch("src.app.get_daily_nutrition_intake")
    def test_nutrition_query_failure(self, mock_get_daily_nutrition_intake):
        mock_get_daily_nutrition_intake.return_value = None

        response = self.app.post("/nutrition_query", data={
            "age": "25",
            "gender": "male",
            "height": "180",
            "weight": "75",
            "activityLevel": "active"
        })

        self.assertEqual(response.status_code, 200) 
        self.assertIn(b"Failed to fetch nutrition data. Please try again later.", response.data)

if __name__ == "__main__":
    unittest.main()
