from fastapi.testclient import TestClient

from app.transaction_controller import app

import os
import requests

client = TestClient(app)


class ValueStorageTransactionCRUD:
    transaction_ids = []
    user_ids = []
    access_token_admin = None
    access_token = None


class TestSuiteTransactionCRUD:
    def test_create_user_admin(self):
        user_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameTransactionAdmin",
                "email": "test@example.com",
                "password": "testPassword",
                "is_admin": True,
            },
        )

        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageTransactionCRUD.user_ids.append(user_response.json()["id"])

    def test_create_user(self):
        user_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameTransaction",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )

        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageTransactionCRUD.user_ids.append(user_response.json()["id"])

    def test_login_admin(self):
        response = client.post(
            "/login",
            data={
                "username": "testUsernameTransactionAdmin",
                "password": "testPassword",
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageTransactionCRUD.access_token_admin = response.json()["access_token"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameTransaction", "password": "testPassword"},
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageTransactionCRUD.access_token = response.json()["access_token"]

    def test_create_transaction_with_id(self):
        response = client.post(
            "/transactions",
            json={
                "id": "testID",
                "state": "testState",
            },
            headers={
                "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
            },
        )
        assert response.status_code == 201
        assert response.json()["id"] == "testID"
        ValueStorageTransactionCRUD.transaction_ids.append("testID")

    def test_create_transaction_without_id(self):
        response = client.post(
            "/transactions",
            json={
                "state": "testState",
            },
            headers={
                "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageTransactionCRUD.transaction_ids.append(response.json()["id"])

    def test_create_transaction_with_existing_id(self):
        response = client.post(
            "/transactions",
            json={
                "id": "testID",
                "state": "testState",
            },
            headers={
                "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Transaction already exists"}

    def test_get_transactions(self):
        response = client.get(
            "/transactions",
            headers={
                "Authorization": "Bearer "
                + ValueStorageTransactionCRUD.access_token_admin
            },
        )
        assert response.status_code == 200
        assert len(response.json()) >= 2

    def test_get_transaction_by_id(self):
        response = client.get(
            "/transactions/testID",
            headers={
                "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
            },
        )
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert "state" in response.json()
        assert "created_at" in response.json()

    def test_get_transaction_not_found(self):
        response = client.get(
            "/transactions/notFoundID",
            headers={
                "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
            },
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Transaction not found"}

    def test_update_transaction_by_id(self):
        response = client.patch(
            "/transactions/testID",
            json={
                "state": "testStateUpdated",
            },
            headers={
                "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
            },
        )
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert response.json()["state"] == "testStateUpdated"
        assert "created_at" in response.json()

    def test_delete_transaction_by_id(self):
        for transaction_id in ValueStorageTransactionCRUD.transaction_ids:
            response = client.delete(
                f"/transactions/{transaction_id}",
                headers={
                    "Authorization": "Bearer "
                    + ValueStorageTransactionCRUD.access_token
                },
            )
            assert response.status_code == 200
            assert "id" in response.json()

    def test_delete_user(self):
        # Delete users starting from the last one because the first one has the access token
        for user_id in ValueStorageTransactionCRUD.user_ids[::-1]:
            user_response = requests.delete(
                os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/users/" + user_id,
                headers={
                    "Authorization": "Bearer "
                    + ValueStorageTransactionCRUD.access_token_admin
                },
            )

            assert user_response.status_code == 200
            assert "id" in user_response.json()
