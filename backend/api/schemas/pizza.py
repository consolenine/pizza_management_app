from pydantic import BaseModel
from typing import Optional

class PizzaCreate(BaseModel):
    type: str
    price: float
    description: str

class PizzaResponse(BaseModel):
    id: int
    type: str
    price: float
    description: str  

class PizzaDelete(BaseModel):
    id: int
