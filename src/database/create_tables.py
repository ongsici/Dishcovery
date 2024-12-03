import sqlalchemy.orm
from sqlalchemy import create_engine, String, Integer, Float, Column, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path)

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')

Base = declarative_base()

engine = create_engine(f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/dishcovery_app_db')
Session = sessionmaker(bind=engine)
session = Session()

class SavedRecipe(Base):
    __tablename__ = 'saved_recipes'
    recipe_id = Column(Integer(), primary_key=True)
    name = Column(String(150), nullable=False)
    image = Column(String(200), nullable=False)
    instructions = Column(Text(), nullable=False)
    calories = Column(Integer, nullable=False)
    carbohydrate = Column(Integer, nullable=True)
    fat = Column(Integer, nullable=True)
    protein = Column(Integer, nullable=True)


if __name__ == '__main__':

    try:
        Base.metadata.create_all(engine)
        session.close()
    except Exception as e:
        print(e)