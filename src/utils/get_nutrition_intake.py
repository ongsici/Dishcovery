import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()
NUTRITION_API_KEY = os.getenv("NUTRITION_API_KEY")

def get_daily_nutrition_intake(gender, age, height, weight, activity_level="Active"):
    url = "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info"

    querystring = {"measurement_units":"met",
                    "sex":str(gender),
                    "age_value":str(age),
                    "age_type":"yrs",
                    "cm":str(height),
                    "kilos":str(weight),
                    "activity_level":activity_level}

    headers = {
        "x-rapidapi-key": NUTRITION_API_KEY,
        "x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
    }
    # print(f'api: {NUTRITION_API_KEY}') 

    response = requests.get(url, headers=headers, params=querystring)
    print(f'response:{response.status_code}')

    data = response.json()
    print(data)
    
    caloric_needs = int(re.sub(r'\D', '', data['BMI_EER']['Estimated Daily Caloric Needs']))
    results = {}
    
    macronutrients = data['macronutrients_table']['macronutrients-table']

    for row in macronutrients[1:]: 
        if row[0] in ['Carbohydrate', 'Protein', 'Fat']:
            # Split the range and get the upper limit (second value) for Carbohydrate and Fat
            if 'Carbohydrate' in row[0]:
                value = row[1].split(' - ')[1]  # Get the upper limit
            elif 'Fat' in row[0]:
                value = row[1].split(' - ')[1]  # Get the upper limit
            else:
                value = row[1]  # For Protein, there's only a single value
            results[row[0]] = int(re.sub(r'\D', '', value)) 

    results["Calories"] = caloric_needs

    return results

print(get_daily_nutrition_intake("female", "30", "168", "55"))