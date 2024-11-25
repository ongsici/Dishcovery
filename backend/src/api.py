from fastapi import FastAPI
from data_models import IngredientsInput
from get_spoonacular import get_recipe_by_ingredients
from get_spoonacular import get_recipe_by_id
from get_spoonacular import get_nutrition_by_id

app = FastAPI()

@app.post("/ingredients_search")
def ingredients_search(item: IngredientsInput):
    ingredients_list = item.ingredients
    
    # Get the list of recipes based on the ingredients list
    recipe_ingredients = get_recipe_by_ingredients(ingredients_list)
    
    # Initialize an empty dictionary to store the organized recipe details
    results = {}

    # Loop through each recipe in the list and fetch the details and nutrition info
    for recipe in recipe_ingredients:
        recipe_id = recipe['id']
        recipe_name = recipe['title']

        missed_ingredients = []
        used_ingredients = []
        extended_ingredients = []

        # Extracting missedIngredients (only the names)
        for ingredient in recipe['missedIngredients']:
            missed_ingredients.append(ingredient['name'])
        
        # Extracting usedIngredients (only the names)
        for ingredient in recipe['usedIngredients']:
            used_ingredients.append(ingredient['name'])

        # Fetch recipe details and nutrition for the current recipe ID
        recipe_details = get_recipe_by_id(recipe_id)
        recipe_nutrition = get_nutrition_by_id(recipe_id)

        for ingredient in recipe_details.get('extendedIngredients'):
            name = ingredient.get('name')
            image = ingredient.get('image')
            metric = ingredient.get("measures", {}).get("metric", {})
            
            # Prepare the metric in a readable format
            if metric:
                metric_info = f"{metric.get('amount', '')} {metric.get('unitShort', '')}"
            else:
                metric_info = "No metric data available"

            extended_ingredients.append({
                "name": name,
                "image": image,
                "metric": metric_info
            })

        # Organize the response into a structured dictionary
        organized_recipe = {
            "id": recipe_id,  # Include recipe ID
            "name": recipe_name,  # Include recipe name
            "image": recipe_details.get('image'),  # Include image
            "extended_ingredients": extended_ingredients,  # Include ingredients from the details
            "missed_ingredients": missed_ingredients,  # Only names of missed ingredients
            "used_ingredients": used_ingredients,  # Only names of used ingredients
            "labels": {  # Labels for dietary preferences
                "vegan": recipe_details.get('vegan'),
                "vegetarian": recipe_details.get('vegetarian'),
                "glutenFree": recipe_details.get('glutenFree'),
                "lowFodmap": recipe_details.get('lowFodmap'),
                "sustainable": recipe_details.get('sustainable')
            },
            "nutrition": {  # Nutrition information
                "calories": recipe_nutrition.get('calories'),
                "carbohydrate": recipe_nutrition.get('carbs'),
                "fat": recipe_nutrition.get('fat'),
                "protein": recipe_nutrition.get('protein'),
            }
        }

        # Add the recipe to the results dictionary with recipe_name as the key
        results[recipe_name] = organized_recipe
    
    # Return the results in the structured JSON format
    return {"recipes": results}


ingredients_input = IngredientsInput(ingredients=["tomato", "cheese", "onion"])

# Call the ingredients_search function with the created instance
response = ingredients_search(ingredients_input)

# Print the response to check the result
print(response)
