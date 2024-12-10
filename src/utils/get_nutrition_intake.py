import re
import requests
from src.config import NUTRITION_API_KEY

def get_api_key():
    return NUTRITION_API_KEY

def get_daily_nutrition_intake(gender, age, height, weight, activity_level):
    url = "https://nutrition-calculator.p.rapidapi.com/api/nutrition-info"

    querystring = {"measurement_units":"met",
                    "sex":str(gender),
                    "age_value":str(age),
                    "age_type":"yrs",
                    "cm":str(height),
                    "kilos":str(weight),
                    "activity_level":str(activity_level)}

    headers = {
        "x-rapidapi-key": get_api_key(),
        "x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)

        if response.status_code ==200:
            data = response.json()
        
            caloric_needs = int(re.sub(r'\D', '', data['BMI_EER']['Estimated Daily Caloric Needs']))
            results = {}
            
            macronutrients = data['macronutrients_table']['macronutrients-table']

            for row in macronutrients[1:]: 
                if row[0] in ['Carbohydrate', 'Protein', 'Fat']:
                    if 'Carbohydrate' in row[0]:
                        value = row[1].split(' - ')[1]  
                    elif 'Fat' in row[0]:
                        value = row[1].split(' - ')[1] 
                    else:
                        value = row[1]  
                    results[row[0]] = int(re.sub(r'\D', '', value)) 

            results["Calories"] = caloric_needs

            return results
        else:
            return None
    except Exception as e:
        print(f"Error fetching nutrition data: {e}")
        return None
