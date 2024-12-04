import os
import requests
from typing import List
from src.config import API_KEY

def get_api_key():
    return API_KEY

def get_recipe_by_ingredients(ingredients_list: List):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    ingredients = ", ".join(ingredients_list)
    params ={
        "ingredients": ingredients,
        "apiKey": get_api_key(),
        "number": 2
    }
    response = requests.get(url, params=params)
    if response.status_code==200:
        return response.json()
    else:
        return None


def get_recipe_by_id(recipeID: int):
    url = f'https://api.spoonacular.com/recipes/{recipeID}/information'
    params = {
        "apiKey": get_api_key()
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_nutrition_by_id(recipeID: int):
    url = f'https://api.spoonacular.com/recipes/{recipeID}/nutritionWidget.json'
    params = {
        "apiKey": get_api_key()
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
