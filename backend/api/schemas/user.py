from pydantic import BaseModel

class UserCreate(BaseModel):
    '''
    Accepts Parameters:
    - name: str
    - email: str
    - password: str
    - address: str
    '''
    name: str
    email: str
    password: str
    address: str

class UserCreateResponse(BaseModel):
    message: str
    
class UserLogin(BaseModel):
    email: str
    password: str

class AdminCreate(UserCreate):
    app_secret: str
