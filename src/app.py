import requests
from flask import Flask, render_template, request
from src.utils.data_models import IngredientsInput
from src.utils.get_spoonacular import get_nutrition_by_id, get_recipe_by_id, get_recipe_by_ingredients
from src.utils.get_nutrition_intake import get_daily_nutrition_intake
from src.database import database as db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:/username:password@db//saved_recipes.db" # TODO
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) # Set up extensions
db.create_all()
db.drop_all()

results = {}

# Define the database model
class SavedRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    calories = db.Column(db.String(50), nullable=True)
    carbohydrate = db.Column(db.String(50), nullable=True)
    fat = db.Column(db.String(50), nullable=True)
    protein = db.Column(db.String(50), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recipe_search")
def recipe_search():
    return render_template("recipe_search.html")


@app.route("/ingredients_search", methods=["POST"])
def ingredients_search():
    data = request.get_json()
    ingredients_list = data.get("ingredients", [])
    # filter_option = data.get("filter", "default1")
    # sort_option = data.get("sort", "default")
    
    # Get the list of recipes based on the ingredients list
    recipe_ingredients = get_recipe_by_ingredients(ingredients_list)
    
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

        print(results)

    return results
    

@app.route("/recipe_search_results")
def recipe_search_results():
    return render_template("recipe_search_results.html", recipes=results)


# @app.route("/recipe_details.html")
@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    recipe = results.get(recipe_id)
    if not recipe:
        return "Recipe not found", 404
    return render_template('recipe_details.html', recipe=recipe)


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
            id=recipe['id'],
            name=recipe['name'],
            image=recipe['image'],
            instructions=recipe['instructions'],
            calories=recipe['nutrition']['calories'],
            carbohydrate=recipe['nutrition']['carbohydrate'],
            fat=recipe['nutrition']['fat'],
            protein=recipe['nutrition']['protein'],
        )
        db.session.add(saved_recipe)
        db.session.commit()
        # return redirect(url_for('saved_recipes')) TODO: Fix