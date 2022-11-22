from fastapi.testclient import TestClient

from app.shopping_cart_controller import app

import os
import requests

client = TestClient(app)


class ValueStorageItemCRUD:
    user_ids = []
    access_token_admin = None
    access_token = None
    order_id = None
    item_id = None


class TestSuiteItemCRUD:
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
        ValueStorageItemCRUD.user_ids.append(user_response.json()["id"])

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
        ValueStorageItemCRUD.user_ids.append(user_response.json()["id"])

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
        ValueStorageItemCRUD.access_token_admin = response.json()["access_token"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameOrder", "password": "testPassword"},
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageItemCRUD.access_token = response.json()["access_token"]

    def test_create_order(self):
        response = client.post(
            "/shopping-carts",
            json={"user": {"id": ValueStorageItemCRUD.user_ids[1]}, "price": 10.1},
            headers={"Authorization": "Bearer " + ValueStorageItemCRUD.access_token},
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageItemCRUD.order_id = response.json()["id"]

    def test_create_item(self):
        response = client.post(
            f"/shopping-carts/{ValueStorageItemCRUD.order_id}/items",
            json={"id": "testID"},
            headers={"Authorization": f"Bearer {ValueStorageItemCRUD.access_token}"},
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageItemCRUD.item_id = response.json()["id"]

    def test_get_items_by_order_id(self):
        response = client.get(
            f"/shopping-carts/{ValueStorageItemCRUD.order_id}/items",
            headers={"Authorization": f"Bearer {ValueStorageItemCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_delete_item_by_id(self):
        response = client.delete(
            f"/shopping-carts/{ValueStorageItemCRUD.order_id}/items/{ValueStorageItemCRUD.item_id}",
            headers={"Authorization": f"Bearer {ValueStorageItemCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageItemCRUD.item_id}

    def test_delete_order_by_id(self):
        response = client.delete(
            f"/shopping-carts/{ValueStorageItemCRUD.order_id}",
            headers={"Authorization": "Bearer " + ValueStorageItemCRUD.access_token},
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageItemCRUD.order_id

    def test_delete_user(self):
        # Delete users starting from the last one because the first one has the access token
        for user_id in ValueStorageItemCRUD.user_ids[::-1]:
            user_response = requests.delete(
                os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/users/" + user_id,
                headers={
                    "Authorization": "Bearer " + ValueStorageItemCRUD.access_token_admin
                },
            )

            assert user_response.status_code == 200
            assert "id" in user_response.json()
