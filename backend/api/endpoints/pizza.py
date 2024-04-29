from fastapi import APIRouter, Depends, Path

from sqlalchemy.orm import Session
from api.config.db import get_session
from api.models.pizza import Pizza
from api.schemas.pizza import PizzaResponse

router = APIRouter()

@router.get("/all")
async def fetch_pizzas(
    db: Session = Depends(get_session)
) -> list[PizzaResponse]:
    '''
    ## Fetch data for all pizzas.
    '''
    
    return db.query(Pizza).all()