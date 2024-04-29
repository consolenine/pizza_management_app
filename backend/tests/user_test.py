from fastapi.testclient import TestClient

from api.main import app
from api.models.user import User
from api.schemas.user import UserCreate, UserCreateResponse

# Create a test client
client = TestClient(app)

# # Test cases for each route
# def test_register_user():
#     user_data = {
#         "name": "Test User",
#         "email": "test@example.com",
#         "password": "testtest",
#         "address": "Test Address"
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = client.get("/api/v1/user/signup", headers=headers)
#     assert response.status_code == 200
    
#     # Validate the response data against the UserCreateResponse schema

def test_login_user():
    user_data = {
        "email": "test@gmail.com",
        "password": "testtest"
    }



if __name__ == "__main__":
    import pytest
    pytest.main()