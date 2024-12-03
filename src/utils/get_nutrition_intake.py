import os
import re
import requests
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") is None:  
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
    load_dotenv(dotenv_path)

def get_api_key():
    return os.getenv("NUTRITION_API_KEY")

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
        "x-rapidapi-key": get_api_key(),
        "x-rapidapi-host": "nutrition-calculator.p.rapidapi.com"
    }
    # print(f'api: {NUTRITION_API_KEY}') 

    response = requests.get(url, headers=headers, params=querystring)
    # print(f'response:{response.status_code}')

    data = response.json()
    # print(data)

    print(f'Response Status Code: {response.status_code}')  # Debugging line
    print(f'API Response: {response.json()}')
    if response.status_code ==200:
    
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
    else:
        return {}

# print(get_daily_nutrition_intake("female", "30", "168", "55"))