from fastapi.testclient import TestClient
from app.shopping_cart_controller import app
import requests
import os

client = TestClient(app)


class ValueStorageOrderCRUD:
    order_id = None
    user_id = None


class TestSuiteOrderCRUD:
    def test_create_user(self):
        user_response = requests.post(
            os.getenv("API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameOrder1",
                "email": "testOrder@example.com",
                "password": "testPasswordOrder",
            },
        )
        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageOrderCRUD.user_id = user_response.json()["id"]

    def test_create_order_with_id(self):
        response = client.post(
            "/shopping-carts",
            json={"user": {"id": ValueStorageOrderCRUD.user_id}, "price": "10"},
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageOrderCRUD.order_id = response.json()["id"]

    # def test_delete_user(self):
    #     user_response = requests.delete(
    #         os.getenv("API_GATEWAY_URL")
    #         + f"/user-api/v1/users/{ValueStorageOrderCRUD.user_id}"
    #     )
    #     assert user_response.status_code == 200
    #     assert "id" in user_response.json()
