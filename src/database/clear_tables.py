import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.create_tables import SavedRecipe
from src.config import PG_HOST, PG_PASSWORD, PG_USER, PG_PORT

engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/dishcovery')
Session = sessionmaker(bind=engine)
session = Session()

try:
    session.query(SavedRecipe).delete()  
    session.commit()
except Exception as e:
    print(e)