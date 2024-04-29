from fastapi import APIRouter, Depends, HTTPException, status, Path
from api.config.db import get_session
from sqlalchemy.orm import Session
from api.models.user import User
from api.schemas.user import *
from api.schemas.token import Token
from api.utils.auth import *

import os

router = APIRouter()

@router.post("/admincreate")
def admin_create(
    user_data: AdminCreate, 
    db: Session = Depends(get_session)
) -> UserCreateResponse:
    '''
    ## Endpoint to create a new admin user
    - requires app secret
    
    Use login endpoint to obtain access token after registration.
    '''
    
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    try:
        # Create new user
        new_user = User(name=user_data.name, email=user_data.email, password=hashed_password, address=user_data.address, role="admin")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str("Unable to add user"))
    
    return {"message": "Registered successfully"}

@router.delete("/{email}")
async def user_delete(
    admin_user: Annotated[User, Depends(is_user_admin)],
    email: str = Path(..., description="Order ID"),
    db: Session = Depends(get_session)
):
    '''
    ## Endpoint to delete existing user
    
    Takes user email as parameter.
    - Required role: admin
    '''
    
    # Check if the user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin user cannot be deleted")
    
    db.query(User).filter(User.email == email).delete()
    db.commit()
    
    return {"message": f"User with associated email - {email} deleted successfully"}
