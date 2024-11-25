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
        "apiKey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    return data


get_recipe_by_ingredients(["apples, sugar, flour"])

