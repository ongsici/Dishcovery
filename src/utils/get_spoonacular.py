import os
import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_recipe_by_ingredients(ingredients_list: List):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    ingredients = ", ".join(ingredients_list)
    params ={
        "ingredients": ingredients,
        "apiKey": API_KEY,
        "number": 10
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    return data


def get_recipe_by_id(recipeID: int):
    url = f'https://api.spoonacular.com/recipes/{recipeID}/information'
    params = {
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


def get_nutrition_by_id(recipeID: int):
    url = f'https://api.spoonacular.com/recipes/{recipeID}/nutritionWidget.json'
    params = {
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data
