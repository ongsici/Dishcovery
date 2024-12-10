import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import requests
from typing import List
from src.config import API_KEY
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_api_key():
    return API_KEY

def get_recipe_by_ingredients(ingredients_list: List):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    ingredients = ", ".join(ingredients_list)
    params ={
        "ingredients": ingredients,
        "apiKey": get_api_key(),
        "number": 5
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        logger.debug(f'Get recipe by ingredients external API call returned response status code: {response.status_code}')
        if response.status_code==200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None


def get_recipe_by_id(recipeID: int):
    url = f'https://api.spoonacular.com/recipes/{recipeID}/information'
    params = {
        "apiKey": get_api_key()
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        logger.debug(f'Get recipe by ID external API call returned response status code: {response.status_code}')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None


def get_nutrition_by_id(recipeID: int):
    url = f'https://api.spoonacular.com/recipes/{recipeID}/nutritionWidget.json'
    params = {
        "apiKey": get_api_key()
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        logger.debug(f'Get nutrition by ID external API call returned response status code: {response.status_code}')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None
