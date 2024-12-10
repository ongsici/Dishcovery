from unittest.mock import patch, MagicMock
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.get_nutrition_intake import get_api_key, get_daily_nutrition_intake


mock_success_response = {
        'BMI_EER': {'BMI': '19.5', 'Estimated Daily Caloric Needs': '2,277 kcal/day'},
        'macronutrients_table': {'macronutrients-table': [
            ['Macronutrient', 'Recommended Intake Per Day'],
            ['Carbohydrate', '256 - 370 grams'],
            ['Protein', '44 grams'],
            ['Fat', '51 - 89 grams']
        ]}
    }

mock_failure_response = None

@patch('src.utils.get_nutrition_intake.get_api_key', return_value="fake_api_key")
@patch('requests.get')
def test_get_daily_nutrition_intake_success(mock_get, mock_get_api_key):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_success_response

    gender = 'male'
    age = 25
    height = 180
    weight = 75
    activity_level = 'active'

    result = get_daily_nutrition_intake(gender, age, height, weight, activity_level)

    expected_result = {
        "Calories": 2277,
        "Carbohydrate": 370,  
        "Protein": 44,
        "Fat": 89 
    }

    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    mock_get.assert_called_with(
        "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info",
        headers={
            "x-rapidapi-key": "fake_api_key",
            "x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
        },
        params={
            "measurement_units": "met",
            "sex": 'male',
            "age_value": '25',
            "age_type": "yrs",
            "cm": '180',
            "kilos": '75',
            "activity_level": 'active'
        }, 
        timeout=15
    )

@patch('src.utils.get_nutrition_intake.get_api_key', return_value="fake_api_key")
@patch('requests.get')
def test_get_daily_nutrition_intake_failure(mock_get, mock_get_api_key):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = mock_failure_response

    gender = 'female'
    age = 30
    height = 165
    weight = 60
    activity_level = 'low'

    result = get_daily_nutrition_intake(gender, age, height, weight, activity_level)

    assert result == None, f"Expected an empty dictionary, but got {result}"

    mock_get.assert_called_with(
        "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info",
        headers={
            "x-rapidapi-key": "fake_api_key", 
            "x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
        },
        params={
            "measurement_units": "met",
            "sex": 'female',
            "age_value": '30',
            "age_type": "yrs",
            "cm": '165',
            "kilos": '60',
            "activity_level": 'low'
        }, 
        timeout=15
    )