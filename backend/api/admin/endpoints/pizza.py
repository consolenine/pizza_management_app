from fastapi import APIRouter, Depends
from api.config.db import get_session
from sqlalchemy.orm import Session
from api.models.pizza import Pizza
from api.schemas.pizza import *
from api.utils.auth import *

router = APIRouter()

@router.post("/add")
async def add_pizza(
    current_user: Annotated[User, Depends(is_user_admin)],
    pizza_data: PizzaCreate,
    db: Session = Depends(get_session)
) -> PizzaResponse:
    '''
    ## Add a new pizza.
    ## Required roles - `admin`
    ## Headers:
    - **Authorization**: Bearer `access_token`
    - **Content-Type**: application/json
    '''
    
    if db.query(Pizza).filter(Pizza.type == pizza_data.type).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Similar pizza already exists")
    
    try:
        new_pizza = Pizza(**pizza_data.model_dump())
        db.add(new_pizza)
        db.commit()
        db.refresh(new_pizza)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str("Unable to add pizza"))
    return new_pizza    
