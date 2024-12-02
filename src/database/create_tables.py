import sqlalchemy.orm
from sqlalchemy.dialects.postgresql import ARRAY, JSON, JSONB
from sqlalchemy import create_engine, inspect, String, Integer, Float, Column, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('postgresql://dishcovery:dishcovery@localhost/dishcovery')
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