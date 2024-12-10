import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.database.create_tables import SavedRecipe

mock_recipes_by_ingredients = [
    {
        "id": 655573,
        "title": "Penne Arrabiata",
        "image": "https://img.spoonacular.com/recipes/655573-312x231.jpg",
        "imageType": "jpg",
        "usedIngredientCount": 3,
        "missedIngredientCount": 2,
        "missedIngredients": [
            {"id": 10511297, "amount": 3.0, "unit": "tablespoons", "name": "parsley"},
            {"id": 11821, "amount": 2.0, "unit": "", "name": "peppers"}
        ],
        "usedIngredients": [
            {"id": 10011531, "amount": 14.5, "unit": "oz", "name": "tomato"},
            {"id": 11215, "amount": 2.0, "unit": "Cloves", "name": "garlic"}
        ],
    },
    {
        "id": 637327,
        "title": "Cavatelli With Red and Green Chard",
        "image": "https://img.spoonacular.com/recipes/637327-312x231.jpg",
        "imageType": "jpg",
        "usedIngredientCount": 3,
        "missedIngredientCount": 2,
        "missedIngredients": [
            {"id": 6172, "amount": 0.5, "unit": "cup", "name": "chicken stock"},
            {"id": 11147, "amount": 1.0, "unit": "large bunch", "name": "swiss chard"}
        ],
        "usedIngredients": [
            {"id": 12220420, "amount": 13.0, "unit": "ounces", "name": "cavatelli"},
            {"id": 11215, "amount": 2.0, "unit": "cloves", "name": "garlic"}
        ],
    }
]

mock_nutrition_by_id = {
    'calories': '466',
    'carbs': '82g',
    'fat': '8g',
    'protein': '14g',
    'bad': [
        {'amount': '466', 'indented': False, 'title': 'Calories', 'percentOfDailyNeeds': 23.31},
        {'amount': '8g', 'indented': False, 'title': 'Fat', 'percentOfDailyNeeds': 13.6},
        {'amount': '82g', 'indented': False, 'title': 'Carbohydrates', 'percentOfDailyNeeds': 27.49},
    ],
    'good': [
        {'amount': '14g', 'indented': False, 'title': 'Protein', 'percentOfDailyNeeds': 28.0},
    ]
}

mock_recipe_by_id = {
    # 'vegetarian': True,
    # 'vegan': True,
    # 'glutenFree': False,
    # 'lowFodmap': False,
    # 'sustainable': False,
    # 'readyInMinutes': 45,
    'image': 'https://img.spoonacular.com/recipes/655573-556x370.jpg',
    'extendedIngredients': [
        {'id': 10011531, 'name': 'tomato', 'amount': 14.5, 'unit': 'oz', 'image': 'tomatoes-canned.png'},
        {'id': 10511297, 'name': 'parsley', 'amount': 3.0, 'unit': 'tablespoons', 'image': 'parsley.jpg'},
        {'id': 11215, 'name': 'garlic', 'amount': 2.0, 'unit': 'Cloves', 'image': 'garlic.png'},
        {'id': 4053, 'name': 'olive oil', 'amount': 2.0, 'unit': 'tablespoons', 'image': 'olive-oil.jpg'},
        {'id': 11120420, 'name': 'penne', 'amount': 14.0, 'unit': 'oz', 'image': 'penne-pasta.jpg'}
    ]
}

mock_saved_recipes_query_all = [
            SavedRecipe(
                recipe_id=648475, 
                name="Japanese Gyoza Pot Stickers", 
                image="https://img.spoonacular.com/recipes/648475-556x370.jpg", 
                instructions="<ol><li>Chop cabbage fine, place in colander and pour boiling water over the cabbage. Cool to touch, then squeeze cabbage well to get the water out. In a bowl mix cabbage, chopped green onions, chopped mushrooms and grated ginger. Mix ground beef, wine, soy sauce, sesame oil and black pepper together with vegetables; mix well. Place a small amount of filling (about 1 teaspoon) in center of gyoza wrapping and fold in half. Pleat edge to seal. If edges won't stick together, dampen the inside edge with a little water, then pleat. Put 2 tablespoon salad oil in </li></ol>", 
                calories=463.0, 
                carbohydrate=8.0, 
                fat=31.0, 
                protein=13.0
            ),
            SavedRecipe(
                recipe_id=660837, 
                name="Spaghetti With Smoked Salmon and Prawns", 
                image="https://img.spoonacular.com/recipes/660837-556x370.jpg", 
                instructions="<ol><li>Cook spaghetti as per packet instructions. Dish up and put in a large bowl.</li><li>Use fork to loosen the smoked salmon and set aside.</li><li>Heat frying pan at medium heat, add olive oil and throw in garlic and saute for a while.</li><li>Then add in prawns and fry till cooked, lower heat and pour in the smoked salmon and fresh dills ~ stir fry well and off heat.</li><li>Lastly pour all the ingredients on the cooked spaghetti and toss well with some pepper then serve into individual plate.</li><li>Enjoy!</li></ol>", 
                calories=61.0, 
                carbohydrate=60.0, 
                fat=6.0, 
                protein=2.0
            )
        ]