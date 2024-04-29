from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from api.config.db import Base
from api.models.user import User
from api.models.pizza import Pizza

class Order(Base):
    '''
    Model for the orders table in the database.
    '''
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    pizza_id = Column(Integer, ForeignKey("pizzas.id"))
    pizza = relationship("Pizza", back_populates="orders")
    quantity = Column(Integer)
    address = Column(String)
    status = Column(String)
    total_price = Column(Float)

User.orders = relationship("Order", back_populates="user")
Pizza.orders = relationship("Order", back_populates="pizza")
