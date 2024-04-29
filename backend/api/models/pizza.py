from sqlalchemy import Column, Integer, String, Float

from api.config.db import Base

class Pizza(Base):
    '''
    Model for the pizza table in the database.
    '''
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True, key="type")
    description = Column(String)
    price = Column(Float, nullable=False)