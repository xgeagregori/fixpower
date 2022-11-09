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
                "username": "testUsernameOrder32",
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
            json={"user": {"id": ValueStorageOrderCRUD.user_id}, "price": 10.1},
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageOrderCRUD.order_id = response.json()["id"]

    # def test_create_order_with_existing_id(self):
    #     response = client.post(
    #         "/shopping-carts",
    #         json={"user": {"id": ValueStorageOrderCRUD.user_id}, "price": "10"},
    #     )
    #     assert response.status_code == 422
    #     assert response.json()=={"detail":"Order id already exists"}

    def test_get_orders(self):
        response = client.get("/shopping-carts/")
        assert response.status_code == 200

    def test_get_order_by_id(self):
        response = client.get(f"/shopping-carts/{ValueStorageOrderCRUD.order_id}")
        assert response.status_code == 200
        assert "user" in response.json()
        assert "price" in response.json()
        assert "created_at" in response.json()

    def test_get_order_not_found(self):
        response = client.get("/shopping-carts/notFoundID")
        assert response.status_code == 404
        assert response.json() == {"detail": "Order not found"}

    def test_update_order_by_id(self):
        response = client.patch(
            f"/shopping-carts/{ValueStorageOrderCRUD.order_id}", json={"price": 20.0}
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageOrderCRUD.order_id
        assert response.json()["price"] == 20.0
        assert "user" in response.json()
        assert "created_at" in response.json()

    def test_update_order_by_id_not_found(self):
        response = client.patch(f"/shopping-carts/xyz", json={"price": 20.4})
        assert response.status_code == 404
        assert response.json() == {"detail": "Order not found"}

    def test_delete_order_by_id(self):
        response = client.delete(f"/shopping-carts/{ValueStorageOrderCRUD.order_id}")
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageOrderCRUD.order_id

    def test_delete_order_not_found(self):
        response = client.delete(f"/shopping-carts/idNotFound")
        assert response.status_code == 404
        assert response.json() == {"detail": "Order not found"}

    # def test_delete_user(self):
    #     user_response = requests.delete(
    #         os.getenv("API_GATEWAY_URL")
    #         + f"/user-api/v1/users/{ValueStorageOrderCRUD.user_id}"
    #     )
    #     assert user_response.status_code == 200
    #     assert "id" in user_response.json()
