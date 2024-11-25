from pydantic import BaseModel
from typing import List

class IngredientsInput(BaseModel):
    ingredients: List[str]