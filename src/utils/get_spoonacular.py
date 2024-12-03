import os
import requests
from typing import List
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") is None: 
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
    load_dotenv(dotenv_path)

def get_api_key():
    return os.getenv("API_KEY")

def get_recipe_by_ingredients(ingredients_list: List):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    ingredients = ", ".join(ingredients_list)
    params ={
        "ingredients": ingredients,
        "apiKey": get_api_key(),
        "number": 2
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


def get_recipe_by_id(recipeID: int):
    url = f'https://api.spoonacular.com/recipes/{recipeID}/information'
    params = {
        "apiKey": get_api_key()
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


def get_nutrition_by_id(recipeID: int):
    url = f'https://api.spoonacular.com/recipes/{recipeID}/nutritionWidget.json'
    params = {
        "apiKey": get_api_key()
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data
