import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from src.utils.data_models import IngredientsInput
from src.utils.get_spoonacular import get_nutrition_by_id, get_recipe_by_id, get_recipe_by_ingredients
from src.utils.get_nutrition_intake import get_daily_nutrition_intake
from src.database.create_tables import SavedRecipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dishcovery:dishcovery@localhost/dishcovery'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

results = {}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recipe_search")
def recipe_search():
    return render_template("recipe_search.html")


@app.route("/ingredients_search", methods=["POST"])
def ingredients_search():

    results = {}
    
    print("************** got the POST ******************")

    search_query = request.form['ingredients']
    print(search_query)

    ingredients_list = [search_query]

    # ingredient_list could contain commas, so maybe need to split to form the list

    

    # filter_option = data.get("filter", "default1")
    # sort_option = data.get("sort", "default")
    
    # Get the list of recipes based on the ingredients list
    recipe_ingredients = get_recipe_by_ingredients(ingredients_list)
    
    # Initialize an empty dictionary to store the organized recipe details
    
    # Loop through each recipe in the list and fetch the details and nutrition info
    for recipe in recipe_ingredients:
        print("recipe!!!!!", recipe)
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
            "instructions": recipe_details.get('instructions'),
            "extended_ingredients": extended_ingredients,  # Include ingredients from the details
            "missed_ingredients": missed_ingredients,  # Only names of missed ingredients
            "used_ingredients": used_ingredients,  # Only names of used ingredients
            "ready_in_minutes": recipe_details.get('readyInMinutes'),
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

        # Add the recipe to the results dictionary with recipe_id as the key
        results[recipe_id] = organized_recipe

        print(used_ingredients)

    return render_template("recipe_search_results.html", recipes=results)


@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    recipe = results.get(recipe_id)
    success =  request.args.get('success')
    toast_message = request.args.get('toast_message')
    if not recipe:
        return "Recipe not found", 404
    return render_template('recipe_details.html', recipe=recipe, success=success, toast_message=toast_message)


# For debugging
# if __name__ == "__main__":
#     app.run(debug=True)


@app.route("/nutrition_tracker")
def nutrition_tracker():
    return render_template("nutrition_tracker.html")


@app.route("/nutrition_query", methods=["POST"])
def nutrition_query():
    age = request.form.get("age")
    gender = request.form.get("gender")
    height = request.form.get("height")
    weight = request.form.get("weight") 

    print(f'age: {age, type(age)}')
    print(gender, type(gender))
    print(height, type(height))
    print(weight, type(weight))
    rec_intake = get_daily_nutrition_intake(gender, age, height, weight)
    # print(rec_intake)

    return render_template("nutrition_tracker.html", results=rec_intake)


@app.route("/saved_recipes")
def saved_recipes(recipe_id):
    # database.session.add(results.get(recipe_id))
    # database.session.commit()
    # saved_recipes = SavedRecipe.query.all()
    return render_template("saved_recipes.html")
    # , recipes=saved_recipes


# Write saved recipe to database
@app.route('/save_recipe', methods=['POST'])
def save_recipe():
    recipe_id = request.form.get('recipe_id')
    recipe = results.get(int(recipe_id))

    if recipe:
        saved_recipe = SavedRecipe(
            recipe_id=recipe['id'],
            name=recipe['name'],
            image=recipe['image'],
            instructions=recipe['instructions'],
            calories=int(recipe['nutrition']['calories'][:-1]),
            carbohydrate=int(recipe['nutrition']['carbohydrate'][:-1]),
            fat=int(recipe['nutrition']['fat'][:-1]),
            protein=int(recipe['nutrition']['protein'][:-1]),
        )
        try:
            with app.app_context():
                db.session.add(saved_recipe)
                db.session.commit()

            return redirect(url_for('recipe_details', recipe_id=recipe_id, success='true', toast_message="Recipe Saved Successfully!"))
        
        except Exception as e:
            db.session.rollback() 
            return redirect(url_for('recipe_details', recipe_id=recipe_id, success='false', toast_message="Failed to save recipe: Recipe ID already exists"))
