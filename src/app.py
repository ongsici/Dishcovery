import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from src.utils.data_models import IngredientsInput
from src.utils.get_spoonacular import get_nutrition_by_id, get_recipe_by_id, get_recipe_by_ingredients
from src.utils.get_nutrition_intake import get_daily_nutrition_intake
from src.database.create_tables import db, SavedRecipe
from src.config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT
import json
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/dishcovery_app_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
# db = SQLAlchemy(app)

global_results = {}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recipe_search")
def recipe_search():
    return render_template("recipe_search.html")


@app.route("/ingredients_search", methods=["POST"])
def ingredients_search():

    results = {}

    search_query = request.form['ingredients']
    ingredients_list = [search_query]

    # ingredient_list could contain commas, so maybe need to split to form the list

    

    # filter_option = data.get("filter", "default1")
    # sort_option = data.get("sort", "default")
    
    # Get the list of recipes based on the ingredients list
    recipe_ingredients = get_recipe_by_ingredients(ingredients_list)

    if recipe_ingredients is None:
        return render_template(
            "recipe_search_results.html", 
            recipes=None, 
            error="Failed to fetch recipes. Please try again later."
        )
    
    # Initialize an empty dictionary to store the organized recipe details
    
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

        if recipe_details is None or recipe_nutrition is None:
            return render_template(
            "recipe_search_results.html", 
            recipes=None, 
            error="Failed to fetch recipes. Please try again later."
        )

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
        global_results[recipe_id] = organized_recipe

    return render_template("recipe_search_results.html", recipes=results, error=None)


@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    recipe = global_results.get(recipe_id)
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
    activity_level = request.form.get("activityLevel")

    print(f'age: {age, type(age)}')
    print(f'gender: {gender, type(gender)}')
    print(f'height: {height, type(height)}')
    print(f'weight: {weight, type(weight)}')
    print(f'activity level: {activity_level, type(activity_level)}')

    rec_intake = get_daily_nutrition_intake(gender, age, height, weight, activity_level)
    if rec_intake:
        rec_intake_json = json.dumps(rec_intake)
        return redirect(url_for("nutrition_query_results", age=age, gender=gender, height=height, weight=weight, activity_level=activity_level, results=rec_intake_json))
    else:
        error_message = "Failed to fetch nutrition data. Please try again later."
        return render_template('nutrition_query_results.html', error_message=error_message, age=age, gender=gender, height=height, weight=weight, activity_level=activity_level)

@app.route("/nutrition_query_results")
def nutrition_query_results():
    # Retrieve data passed from the previous route
    age = request.args.get('age')
    gender = request.args.get('gender')
    height = request.args.get('height')
    weight = request.args.get('weight')
    activity_level = request.args.get('activity_level')

    # Deserialize the results from the query string
    results_json = request.args.get('results')
    results = json.loads(results_json)

    # Fetch saved recipes from the database
    saved_recipes = SavedRecipe.query.all()

    # Render the results page with form data, results, and saved recipes
    return render_template("nutrition_query_results.html", 
                           age=age, gender=gender, height=height, weight=weight, 
                           activity_level=activity_level, results=results,
                           saved_recipes=saved_recipes)

@app.route("/get_recipe_nutrition/<int:recipe_id>")
def get_recipe_nutrition(recipe_id):
    recipe = SavedRecipe.query.get_or_404(recipe_id)

    # Return nutrition data as JSON
    return jsonify({
        'calories': recipe.calories,
        'carbohydrates': recipe.carbohydrate,
        'protein': recipe.protein,
        'fat': recipe.fat
    })


@app.route("/saved_recipes")
def saved_recipes():
    # Get sort option from the saved_recipes dropbox
    sort_option = request.args.get('sort', 'default')

    # Apply sorting logic based on the sort option
    if sort_option == 'name':
        saved_recipes = SavedRecipe.query.order_by(SavedRecipe.name.asc()).all()
    # elif sort_option == 'cooking_time':
    #     saved_recipes = SavedRecipe.query.order_by(SavedRecipe.ready_in_minutes.asc()).all()
    elif sort_option == 'calories':
        saved_recipes = SavedRecipe.query.order_by(SavedRecipe.calories.asc()).all()
    # elif sort_option == 'carbohydrates':
    #     saved_recipes = SavedRecipe.query.order_by(SavedRecipe.carbohydrate.asc()).all()
    elif sort_option == 'fat':
        saved_recipes = SavedRecipe.query.order_by(SavedRecipe.fat.asc()).all()
    elif sort_option == 'protein':
        saved_recipes = SavedRecipe.query.order_by(SavedRecipe.protein.asc()).all()
    else:  # Default case
        saved_recipes = SavedRecipe.query.all()

    return render_template("saved_recipes.html", recipes=saved_recipes)


# Write saved recipe to database
@app.route('/save_recipe', methods=['POST'])
def save_recipe():
    recipe_id = request.form.get('recipe_id')
    recipe = global_results.get(int(recipe_id))

    if recipe:
        carbohydrate_in=str(recipe['nutrition']['carbohydrate'])
        fat_in=str(recipe['nutrition']['fat'])
        protein_in=str(recipe['nutrition']['protein'])

        # Function to convert string to float or None if empty
        def convert_to_float(value):
            # Check if the value is not empty and contains a valid number
            if value and value != '':  # Not empty
                # Remove 'g' if it's there and convert to float
                return float(value[:-1])
            else:
                return None  # Return None if the value is empty or invalid

        saved_recipe = SavedRecipe(
            recipe_id=recipe['id'],
            name=recipe['name'],
            image=recipe['image'],
            instructions=recipe['instructions'],
            calories=float(recipe['nutrition']['calories']),
            carbohydrate=convert_to_float(carbohydrate_in),
            fat=convert_to_float(fat_in),
            protein=convert_to_float(protein_in)
            # calories=float(recipe['nutrition']['calories'][:-1]),
            # carbohydrate=float(recipe['nutrition']['carbohydrate'][:-1]),
            # fat=float(recipe['nutrition']['fat'][:-1]),
            # protein=float(recipe['nutrition']['protein'][:-1])
        )
        try:
            with app.app_context():
                db.session.add(saved_recipe)
                db.session.commit()

            return redirect(url_for('recipe_details', recipe_id=recipe_id, success='true', toast_message="Recipe Saved Successfully!"))
        
        except Exception as e:
            print(e)
            db.session.rollback() 
            return redirect(url_for('recipe_details', recipe_id=recipe_id, success='false', toast_message="Failed to save recipe: Recipe ID already exists"))


# Delete saved recipe from database
@app.route('/unsave_recipe', methods=['POST'])
def unsave_recipe():
    recipe_id = request.form.get('recipe_id')

    try:
        with app.app_context():
            # Check if the recipe exists in the database
            saved_recipe = SavedRecipe.query.filter_by(recipe_id=recipe_id).first()

            if saved_recipe:
                db.session.delete(saved_recipe)
                db.session.commit()
                return redirect(url_for('recipe_details', recipe_id=recipe_id, success='true', toast_message="Recipe Unsaved Successfully!"))
            else:
                return redirect(url_for('recipe_details', recipe_id=recipe_id, success='false', toast_message="Failed to unsave: Recipe not found"))

    except Exception as e:
        db.session.rollback()
        return redirect(url_for('recipe_details', recipe_id=recipe_id, success='false', toast_message="An error occurred while unsaving the recipe"))
