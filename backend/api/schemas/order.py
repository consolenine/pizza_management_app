from pydantic import BaseModel, Field

class OrderBase(BaseModel):
    id: int
    user_id: int
    pizza_id: int
    quantity: int
    address: str
    status: str
    total_price: float
    
    class Config:
        """
        Pydantic model configuration.
        """
        use_enum_values = True  # Use enum values for enumerations
        populated_by_name = True  # Allow population by field name
        from_attributes = True  # Enable ORM mode for SQLAlchemy models

class OrderCreate(BaseModel):
    pizza_id: int
    quantity: int
    address: str

class OrderCreateResponse(BaseModel):
    order_id: int
    message: str
    
class OrderCancel(BaseModel):
    order_id: int

class OrderCancelResponse(BaseModel):
    message: str