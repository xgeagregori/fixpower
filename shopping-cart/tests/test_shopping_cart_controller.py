from fastapi.testclient import TestClient

from app.shopping_cart_controller import app

client = TestClient(app)


def test_get_shopping_carts():
    response = client.get("/shopping-carts")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Shopping Cart Service!"}
