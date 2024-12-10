import os
import sys
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.get_spoonacular import get_recipe_by_ingredients, get_recipe_by_id, get_nutrition_by_id
from tests.mock_data import mock_recipes_by_ingredients, mock_nutrition_by_id, mock_recipe_by_id


@patch('src.utils.get_spoonacular.get_api_key', return_value="fake_api_key")
@patch('requests.get')
def test_get_recipe_by_ingredients_success(mock_get, mock_get_api_key):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_recipes_by_ingredients

    ingredients = ["tomato", "garlic", "pasta"]
    response = get_recipe_by_ingredients(ingredients)

    required_fields = {"id", "title", "image", "usedIngredients", "missedIngredients"}

    assert mock_get.called
    for recipe in response:
        assert required_fields.issubset(recipe.keys()), f"Missing fields in recipe: {recipe}"

    mock_get.assert_called_with(
        "https://api.spoonacular.com/recipes/findByIngredients",
        params={
            "ingredients": "tomato, garlic, pasta",
            "apiKey": "fake_api_key",
            "number": 5
        }, 
        timeout=15
    )

@patch('src.utils.get_spoonacular.get_api_key', return_value="fake_api_key")
@patch('requests.get')
def test_get_recipe_by_ingredients_failure(mock_get, mock_get_api_key):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {"error": "Internal Server Error"}

    ingredients = ["tomato", "garlic", "pasta"]
    response = get_recipe_by_ingredients(ingredients)

    assert mock_get.called
    assert response is None, "Expected None when the API call fails"

    mock_get.assert_called_with(
        "https://api.spoonacular.com/recipes/findByIngredients",
        params={
            "ingredients": "tomato, garlic, pasta",
            "apiKey": "fake_api_key",
            "number": 5
        },
        timeout=15
    )

@patch('src.utils.get_spoonacular.get_api_key', return_value="fake_api_key")
@patch('requests.get')
def test_get_recipe_by_id_success(mock_get,  mock_get_api_key):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_recipe_by_id

    recipe_id = 655573
    response = get_recipe_by_id(recipe_id)

    # required_fields = {
    #     "extendedIngredients", "readyInMinutes", "vegan", "vegetarian", 
    #     "glutenFree", "lowFodmap", "sustainable", "image"
    # }

    required_fields = {
        "extendedIngredients", "image"
    }

    assert mock_get.called
    assert required_fields.issubset(response.keys()), f"Missing fields in response: {response}"
    mock_get.assert_called_with(
        f"https://api.spoonacular.com/recipes/{recipe_id}/information",
        params={"apiKey": "fake_api_key"}, 
        timeout=15
    )

@patch('src.utils.get_spoonacular.get_api_key', return_value="fake_api_key")
@patch('requests.get')
def test_get_recipe_by_id_failure(mock_get, mock_get_api_key):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {"error": "Internal Server Error"}

    recipe_id = 655573
    response = get_recipe_by_id(recipe_id)

    assert mock_get.called
    assert response is None, "Expected None when the API call fails"

    mock_get.assert_called_with(
        f"https://api.spoonacular.com/recipes/{recipe_id}/information",
        params={"apiKey": "fake_api_key"}, 
        timeout=15
    )

@patch('src.utils.get_spoonacular.get_api_key', return_value="fake_api_key")
@patch('requests.get')
def test_get_nutrition_by_id_success(mock_get,  mock_get_api_key):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_nutrition_by_id

    recipe_id = 655573
    response = get_nutrition_by_id(recipe_id)

    required_fields = {"calories", "carbs", "fat", "protein"}

    assert mock_get.called
    assert required_fields.issubset(response.keys()), f"Missing fields in response: {response}"
    mock_get.assert_called_with(
        f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json",
        params={"apiKey": "fake_api_key"}, 
        timeout=15
    )

@patch('src.utils.get_spoonacular.get_api_key', return_value="fake_api_key")
@patch('requests.get')
def test_get_nutrition_by_id_failure(mock_get, mock_get_api_key):
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {"error": "Internal Server Error"}

    recipe_id = 655573
    response = get_nutrition_by_id(recipe_id)

    assert mock_get.called
    assert response is None, "Expected None when the API call fails"

    mock_get.assert_called_with(
        f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json",
        params={"apiKey": "fake_api_key"}, 
        timeout=15
    )