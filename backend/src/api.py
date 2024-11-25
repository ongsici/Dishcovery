from fastapi import FastAPI
from data_models import IngredientsInput
from get_spoonacular import get_recipe_by_ingredients

app = FastAPI()

@app.post("/ingredients_search")
def ingredients_search(item: IngredientsInput):
    ingredients_list = item.ingredients
    results = get_recipe_by_ingredients(ingredients_list)
    return results
    


