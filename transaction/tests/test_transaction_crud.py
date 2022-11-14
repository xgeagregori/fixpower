from fastapi.testclient import TestClient

from app.transaction_controller import app

import os
import requests

client = TestClient(app)


class ValueStorageTransactionCRUD:
    user_ids = []
    access_token_admin = None
    access_token = None
    product_listing_id = None
    transaction_id = None


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

    # def test_create_product_listing(self):
    #     response = requests.post(
    #         os.getenv("AWS_API_GATEWAY_URL")
    #         + "/product-listing-api/v1/product-listings",
    #         json={
    #             "id": "testProductListingID",
    #             "seller": {"id": ValueStorageTransactionCRUD.user_ids[0]},
    #             "product": {
    #                 "name": "Surface Pro 7",
    #                 "brand": "Surface",
    #                 "category": "REFURBISHED_PRODUCT",
    #                 "sub_category": "LAPTOP",
    #             },
    #             "listed_price": 319.99,
    #         },
    #         headers={
    #             "Authorization": "Bearer "
    #             + ValueStorageTransactionCRUD.access_token_admin
    #         },
    #     )
    #     assert response.status_code == 201
    #     assert "id" in response.json()
    #     ValueStorageTransactionCRUD.product_listing_id = response.json()["id"]

    # def test_create_transaction(self):
    #     response = client.post(
    #         "/transactions",
    #         json={
    #             "product_listing": {
    #                 "id": ValueStorageTransactionCRUD.product_listing_id
    #             },
    #             "final_price": 319.99,
    #         },
    #         headers={
    #             "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
    #         },
    #     )
    #     assert response.status_code == 201
    #     assert "id" in response.json()
    #     ValueStorageTransactionCRUD.transaction_id = response.json()["id"]

    # def test_get_transactions(self):
    #     response = client.get(
    #         "/transactions",
    #         headers={
    #             "Authorization": "Bearer "
    #             + ValueStorageTransactionCRUD.access_token_admin
    #         },
    #     )
    #     assert response.status_code == 200
    #     assert len(response.json()) >= 1

    # def test_get_transaction_by_id(self):
    #     response = client.get(
    #         f"/transactions/{ValueStorageTransactionCRUD.transaction_id}",
    #         headers={
    #             "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
    #         },
    #     )
    #     assert response.status_code == 200
    #     assert response.json()["id"] == ValueStorageTransactionCRUD.transaction_id
    #     assert response.json()["state"] == "PAID"
    #     assert response.json()["product_listing"]["id"] == "testProductListingID"
    #     assert response.json()["final_price"] == 319.99
    #     assert "created_at" in response.json()

    # def test_get_transaction_not_found(self):
    #     response = client.get(
    #         "/transactions/notFoundID",
    #         headers={
    #             "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
    #         },
    #     )
    #     assert response.status_code == 404
    #     assert response.json() == {"detail": "Transaction not found"}

    # def test_update_transaction_by_id(self):
    #     response = client.patch(
    #         f"/transactions/{ValueStorageTransactionCRUD.transaction_id}",
    #         json={
    #             "state": "SHIPPED",
    #         },
    #         headers={
    #             "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
    #         },
    #     )
    #     assert response.status_code == 200
    #     assert response.json()["id"] == ValueStorageTransactionCRUD.transaction_id
    #     assert response.json()["state"] == "SHIPPED"
    #     assert response.json()["product_listing"]["id"] == "testProductListingID"
    #     assert response.json()["final_price"] == 319.99
    #     assert "created_at" in response.json()

    # def test_delete_transaction_by_id(self):
    #     response = client.delete(
    #         f"/transactions/{ValueStorageTransactionCRUD.transaction_id}",
    #         headers={
    #             "Authorization": "Bearer " + ValueStorageTransactionCRUD.access_token
    #         },
    #     )
    #     assert response.status_code == 200
    #     assert "id" in response.json()

    # def delete_product_listing_by_id(self):
    #     response = requests.delete(
    #         os.getenv("AWS_API_GATEWAY_URL")
    #         + f"/product-listing-api/v1/product-listings/{ValueStorageTransactionCRUD.product_listing_id}",
    #         headers={
    #             "Authorization": "Bearer "
    #             + ValueStorageTransactionCRUD.access_token_admin
    #         },
    #     )
    #     assert response.status_code == 200
    #     assert "id" in response.json()

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
