from sqlalchemy import Column, Integer, String
from api.config.db import Base

class User(Base):
    '''
    Model for the users table in the database.
    '''
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String, default="customer")
    email = Column(String, unique=True, index=True)
    password = Column(String)
    address = Column(String)
    token = Column(String)