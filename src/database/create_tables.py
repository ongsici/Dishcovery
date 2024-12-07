import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from sqlalchemy import create_engine, String, Integer, Float, Column, Text
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from src.config import PG_HOST, PG_PASSWORD, PG_USER, PG_PORT


# Base = declarative_base()
db = SQLAlchemy()
Base = db.Model

engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/dishcovery_app_db')
Session = sessionmaker(bind=engine)
session = Session()

class SavedRecipe(Base):
    __tablename__ = 'saved_recipes'
    recipe_id = Column(Integer(), primary_key=True)
    name = Column(String(150), nullable=False)
    image = Column(String(200), nullable=False)
    instructions = Column(Text(), nullable=False)
    calories = Column(Float, nullable=False)
    carbohydrate = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)


if __name__ == '__main__':

    try:
        Base.metadata.create_all(engine)
        session.close()
    except Exception as e:
        print(e)