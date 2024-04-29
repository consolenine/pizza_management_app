from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from typing import Annotated, Union

from sqlalchemy.orm import Session
from api.config.db import get_session
from api.utils.auth import get_current_user
from api.schemas.order import *
from api.models.order import Order
from api.models.pizza import Pizza
from api.models.user import User

# Create A FastAPI Router instance
router = APIRouter()

class OrderNotCancellableException(HTTPException):
    def __init__(self):
        detail = "The order is delivered and cannot be updated or cancelled."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

@router.get("/")
async def get_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_session)
) -> list[OrderBase]:
    '''
    ## Get all orders for currently logged in user.
    ## Headers:
    - **Authorization**: Bearer `access_token`
    - **Content-Type**: application/json
    '''
    orders = db.query(User).filter(User.id == current_user.id).first().orders
    return [OrderBase.model_validate(order) for order in orders]

@router.get("/{order_id}")
async def get_order(
    current_user: Annotated[User, Depends(get_current_user)],
    order_id: int = Path(..., description="Order ID"),
    db: Session = Depends(get_session)
) -> OrderBase:
    '''
    ## Get order information specified by Order ID.
    ## Headers:
    - **Authorization**: Bearer `access_token`
    - **Content-Type**: application/json
    '''
    order = db.query(Order).filter(Order.id == order_id).first()
    return OrderBase.model_validate(order)


@router.post("/")
async def add_order(
    current_user: Annotated[User, Depends(get_current_user)],
    order_data: OrderCreate,
    db: Session = Depends(get_session)
) -> OrderCreateResponse:
    '''
    ## Place a new order.
    ## Headers:
    - **Authorization**: Bearer `access_token`
    - **Content-Type**: application/json
    '''
    
    # Calculate total price of the order
    pizza_rate = db.query(Pizza).filter(Pizza.id == order_data.pizza_id).first().price
    order_price = order_data.quantity * pizza_rate
    
    new_order = Order(
        user_id = current_user.id,
        pizza_id = order_data.pizza_id,
        quantity = order_data.quantity,
        address = order_data.address,
        total_price = order_price,
        status = "Accepted"
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return OrderCreateResponse(order_id=new_order.id, message=f"Order created successfully. Will be delivered to {new_order.address}")

@router.put("/{order_id}")
async def update_order(
    current_user: Annotated[User, Depends(get_current_user)],
    order_data: OrderCreate,
    order_id: int = Path(..., description="Order ID"),
    db: Session = Depends(get_session)
) -> OrderCreateResponse:
    '''
    ## Update an order.
    ### Order can only be updated if it is in the "Accepted" state (not delivered).
    ## Headers:
    - **Authorization**: Bearer `access_token`
    - **Content-Type**: application/json
    '''
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this order")
    if order.status != "Accepted":
        raise OrderNotCancellableException()
    
    order.pizza_id = order_data.pizza_id
    order.quantity = order_data.quantity
    order.address = order_data.address
    order.total_price = order_data.quantity * db.query(Pizza).filter(Pizza.id == order_data.pizza_id).first().price
    order.status = "Accepted"
    
    db.commit()
    return OrderCreateResponse(order_id=order.id, message=f"Order updated successfully") 

@router.delete("/{order_id}")
async def cancel_order(
    current_user: Annotated[User, Depends(get_current_user)],
    order_data: OrderCancel,
    order_id: int = Path(..., description="Order ID"),
    db: Session = Depends(get_session)
) -> OrderCancelResponse:
    '''
    ## Cancel an order.
    ### Order can only be cancelled if it is in the "Accepted" state (not delivered).
    ## Headers:
    - **Authorization**: Bearer `access_token`
    - **Content-Type**: application/json
    '''
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to cancel this order")
    if order.status != "Accepted":
        raise OrderNotCancellableException()
    
    order.status = "Cancelled"
    
    db.commit()
    return OrderCreateResponse(order_id=order.id, message=f"Order cancelled successfully") 