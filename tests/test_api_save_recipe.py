import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from unittest.mock import patch
from src.app import app

class RecipeRoutesTestCase(unittest.TestCase):

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

    @patch("src.app.global_results")
    @patch("src.app.db.session.commit")
    @patch("src.app.db.session.add")
    def test_save_recipe_success(self, mock_add, mock_commit, mock_global_results):
        mock_global_results.get.return_value = {
            'id': 1,
            'name': 'Test Recipe',
            'image': 'image_url',
            'instructions': 'Step by step instructions',
            'nutrition': {
                'calories': 200,
                'carbohydrate': '20g',
                'fat': '10g',
                'protein': '15g'
            }
        }

        with app.test_client() as client:
            response = client.post('/save_recipe', data={'recipe_id': '1'})

        expected_redirect_url = '/recipe/1?success=true&toast_message=Recipe+Saved+Successfully!'
        self.assertEqual(response.location, expected_redirect_url) 

        self.assertEqual(response.status_code, 302)  

        mock_add.assert_called_once()
        mock_commit.assert_called_once()

    @patch("src.app.global_results")
    def test_save_recipe_not_found(self, mock_global_results):
        mock_global_results.get.return_value = None

        with app.test_client() as client:
            response = client.post('/save_recipe', data={'recipe_id': '1'})

        expected_redirect_url = '/recipe/1?success=false&toast_message=Recipe+not+found'

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, expected_redirect_url)

    @patch("src.app.global_results")
    @patch("src.app.db.session.commit")
    @patch("src.app.db.session.add")
    def test_save_recipe_duplicate(self, mock_add, mock_commit, mock_global_results):
        mock_global_results.get.return_value = {
            'id': 1,
            'name': 'Test Recipe',
            'image': 'image_url',
            'instructions': 'Step by step instructions',
            'nutrition': {
                'calories': 200,
                'carbohydrate': '20g',
                'fat': '10g',
                'protein': '15g'
            }
        }
        mock_commit.side_effect = Exception("Duplicate recipe ID")

        with app.test_client() as client:
            response = client.post('/save_recipe', data={'recipe_id': '1'})

        expected_redirect_url = '/recipe/1?success=false&toast_message=Failed+to+save+recipe:+Recipe+ID+already+exists'

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, expected_redirect_url)

if __name__ == "__main__":
    unittest.main()