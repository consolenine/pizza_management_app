from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import user, order, pizza
from api.admin.endpoints import pizza as admin_pizza
from api.admin.endpoints import user as admin_user

app = FastAPI(
    title="Pizza Order Management System API",
    description='''RESTful API service for pizza order management.
        \nIncludes endpoints for user registration, login, and order management.
    '''
)

# Allow all origins, methods, and headers (for development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the Pizza Order Management System API"}

# Customer Routes
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(pizza.router, prefix="/api/v1/pizzas", tags=["Pizza"])
app.include_router(order.router, prefix="/api/v1/orders", tags=["Order"])

# Admin Routes
app.include_router(admin_pizza.router, prefix="/api/v1/admin/pizzas", tags=["Admin"])
app.include_router(admin_user.router, prefix="/api/v1/admin/user", tags=["Admin"])