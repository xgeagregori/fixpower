from fastapi.testclient import TestClient

from app.shopping_cart_controller import app


import os
import requests


client = TestClient(app)


class ValueStorageOrderCRUD:
    order_ids = []
    user_ids = []
    access_token_admin = None
    access_token = None


class TestSuiteOrderCRUD:
    def test_create_user_admin(self):
        user_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameOrderAdmin",
                "email": "test@example.com",
                "password": "testPassword",
                "is_admin": True,
            },
        )

        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageOrderCRUD.user_ids.append(user_response.json()["id"])

    def test_create_user(self):
        user_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameOrder",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )

        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageOrderCRUD.user_ids.append(user_response.json()["id"])

    def test_login_admin(self):
        response = client.post(
            "/login",
            data={
                "username": "testUsernameOrderAdmin",
                "password": "testPassword",
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageOrderCRUD.access_token_admin = response.json()["access_token"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameOrder", "password": "testPassword"},
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageOrderCRUD.access_token = response.json()["access_token"]

    def test_get_orders(self):
        response = client.get(
            "/shopping-carts",
            headers={
                "Authorization": "Bearer " + ValueStorageOrderCRUD.access_token_admin
            },
        )

        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Shopping Cart Service!"}

    def test_create_order_with_id(self):
        response = client.post(
            "/shopping-carts",
            json={"user": {"id": ValueStorageOrderCRUD.user_ids[1]}, "price": 10.1},
            headers={"Authorization": "Bearer " + ValueStorageOrderCRUD.access_token},
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageOrderCRUD.order_id = response.json()["id"]

    def test_get_orders(self):
        response = client.get(
            "/shopping-carts",
            headers={
                "Authorization": "Bearer " + ValueStorageOrderCRUD.access_token_admin
            },
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_order_by_id(self):
        response = client.get(
            f"/shopping-carts/{ValueStorageOrderCRUD.order_id}",
            headers={"Authorization": "Bearer " + ValueStorageOrderCRUD.access_token},
        )
        assert response.status_code == 200
        assert "user" in response.json()
        assert "price" in response.json()
        assert "created_at" in response.json()

    def test_get_order_not_found(self):
        response = client.get(
            "/shopping-carts/notFoundID",
            headers={"Authorization": "Bearer " + ValueStorageOrderCRUD.access_token},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Order not found"}

    def test_update_order_by_id(self):
        response = client.patch(
            f"/shopping-carts/{ValueStorageOrderCRUD.order_id}",
            json={"price": 20.0},
            headers={"Authorization": "Bearer " + ValueStorageOrderCRUD.access_token},
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageOrderCRUD.order_id
        assert response.json()["price"] == 20.0
        assert "user" in response.json()
        assert "created_at" in response.json()

    def test_delete_order_by_id(self):
        response = client.delete(
            f"/shopping-carts/{ValueStorageOrderCRUD.order_id}",
            headers={"Authorization": "Bearer " + ValueStorageOrderCRUD.access_token},
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageOrderCRUD.order_id

    def test_delete_user(self):
        # Delete users starting from the last one because the first one has the access token
        for user_id in ValueStorageOrderCRUD.user_ids[::-1]:
            user_response = requests.delete(
                os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/users/" + user_id,
                headers={
                    "Authorization": "Bearer "
                    + ValueStorageOrderCRUD.access_token_admin
                },
            )

            assert user_response.status_code == 200
            assert "id" in user_response.json()
