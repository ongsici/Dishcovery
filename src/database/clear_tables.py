from sqlalchemy import create_engine
from src.config import PG_HOST, PG_PASSWORD, PG_USER, PG_PORT

engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/dishcovery_app_db')

try:
    # connect to database
    with engine.connect() as connection:
        connection.execute("DELETE FROM saved_recipes;")
except Exception as e:
    print(e)