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
    'vegetarian': True,
    'vegan': True,
    'glutenFree': False,
    'lowFodmap': False,
    'sustainable': False,
    'readyInMinutes': 45,
    'image': 'https://img.spoonacular.com/recipes/655573-556x370.jpg',
    'extendedIngredients': [
        {'id': 10011531, 'name': 'tomato', 'amount': 14.5, 'unit': 'oz', 'image': 'tomatoes-canned.png'},
        {'id': 10511297, 'name': 'parsley', 'amount': 3.0, 'unit': 'tablespoons', 'image': 'parsley.jpg'},
        {'id': 11215, 'name': 'garlic', 'amount': 2.0, 'unit': 'Cloves', 'image': 'garlic.png'},
        {'id': 4053, 'name': 'olive oil', 'amount': 2.0, 'unit': 'tablespoons', 'image': 'olive-oil.jpg'},
        {'id': 11120420, 'name': 'penne', 'amount': 14.0, 'unit': 'oz', 'image': 'penne-pasta.jpg'}
    ]
}
