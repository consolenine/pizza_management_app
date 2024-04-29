from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.config.db import get_session
from sqlalchemy.orm import Session
from api.models.user import User
from api.utils.auth import create_access_token, authenticate_user, verify_password
from api.schemas.user import *
from api.schemas.token import Token
from api.utils.auth import *

router = APIRouter()

@router.post("/signup")
def signup(
    user_data: UserCreate, 
    db: Session = Depends(get_session)
) -> UserCreateResponse:
    '''
    ## Endpoint to create a new customer user
    
    Use login endpoint to obtain access token after registration.
    '''
    
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    
    try:
        # Create new user
        new_user = User(name=user_data.name, email=user_data.email, password=hashed_password, address=user_data.address)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str("Unable to add user"))
    
    return {"message": "Registered successfully"}

@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(get_session)
) -> Token:
    '''
    ## Endpoint to login existing user
    
    Takes email and password as input and returns access token.
    '''
    
    # Authenticate user
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    # Generate access token
    access_token = create_access_token(db, data={"email": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}
