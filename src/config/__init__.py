import os
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv()

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY')
API_KEY = os.getenv('API_KEY')