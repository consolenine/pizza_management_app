from fastapi.testclient import TestClient

from api.main import app
from api.schemas.pizza import PizzaResponse as Pizza

# Create a test client
client = TestClient(app)

# Test cases for each route
def test_get_pizzas():
    headers = {
        "Content-Type": "application/json"
    }
    response = client.get("/api/v1/pizzas/all", headers=headers)
    assert response.status_code == 200
    
    # Validate the response data against the Pizza schema
    pizzas_data = response.json()
    
    pizza_data = pizzas_data[0]
    pizza = Pizza(**pizza_data)
    assert pizza.id >= 0
    assert isinstance(pizza.type, str)
    assert pizza.price >= 0
    assert isinstance(pizza.description, str)

if __name__ == "__main__":
    import pytest
    pytest.main()