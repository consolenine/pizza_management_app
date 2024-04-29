from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from typing import Annotated

from sqlalchemy.orm import Session
from api.config.db import get_session
from api.config.settings import SECRET_KEY, ALGORITHM
from api.models.user import User

from datetime import datetime, timedelta


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    '''
    Create SHA256 encoded password hash.
    '''
    return pwd_context.hash(password)

def create_access_token(
    db: Session, 
    data: dict, 
    expires_delta: 
    timedelta = None
) -> str:
    '''
    Create access token for a specific user
    '''
    user = db.query(User).filter(User.email == data["email"]).first()
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    user.token = encoded_jwt
    
    db.add(user)
    db.commit()
    
    return encoded_jwt

def authenticate_user(
    db: Session, 
    email: str, 
    password: str
) -> User:
    '''
    Authenticates a user after verifying received email and password.
    '''
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    '''
    Validates user info trying to log in
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        # Check if token has expired
        expiration_timestamp = payload.get("exp")
        if expiration_timestamp is not None:
            current_timestamp = datetime.now().timestamp()
            if current_timestamp > expiration_timestamp:
                raise credentials_exception  # Token has expired
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    # Check if token matches the token stored in the database
    
    
    return user

async def is_user_admin(
    current_user: Annotated[User, Depends(get_current_user)],
):
    '''
    Checks if currently logged in user has admin role.
    - Raises HTTPException if not
    '''
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user
