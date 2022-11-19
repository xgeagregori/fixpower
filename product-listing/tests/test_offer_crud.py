from fastapi.testclient import TestClient

from app.product_listing_controller import app

import os
import requests

client = TestClient(app)


class ValueStorageOfferCRUD:
    product_listing_id = None
    offer_id = None
    user_ids = []
    access_token_admin = None
    access_token = None


class TestSuiteOfferCRUD:
    def test_create_user_admin(self):
        user_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameOfferAdmin",
                "email": "test@example.com",
                "password": "testPassword",
                "is_admin": True,
            },
        )

        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageOfferCRUD.user_ids.append(user_response.json()["id"])

    def test_create_user(self):
        user_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/register",
            json={
                "username": "testUsernameOffer",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )

        assert user_response.status_code == 201
        assert "id" in user_response.json()
        ValueStorageOfferCRUD.user_ids.append(user_response.json()["id"])

    def test_login_admin(self):
        response = client.post(
            "/login",
            data={
                "username": "testUsernameOfferAdmin",
                "password": "testPassword",
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageOfferCRUD.access_token_admin = response.json()["access_token"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameOffer", "password": "testPassword"},
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageOfferCRUD.access_token = response.json()["access_token"]

    def test_create_product_listing_with_id(self):
        response = client.post(
            "/product-listings",
            json={
                "id": "testID",
                "seller": {"id": ValueStorageOfferCRUD.user_ids[0]},
                "listed_price": 319.99,
                "product": {
                    "name": "Surface Pro 7",
                    "brand": "Surface",
                    "category": "REFURBISHED_PRODUCT",
                    "sub_category": "LAPTOP",
                },
            },
            headers={"Authorization": f"Bearer {ValueStorageOfferCRUD.access_token}"},
        )
        assert response.status_code == 201
        assert response.json() == {"id": "testID"}
        ValueStorageOfferCRUD.product_listing_id = response.json()["id"]

    def test_create_offer(self):
        response = client.post(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers",
            json={"sender": {"id": "123"}, "recipient": {"id": "432"}, "price": 299.99},
            headers={"Authorization": f"Bearer {ValueStorageOfferCRUD.access_token}"},
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageOfferCRUD.offer_id = response.json()["id"]

    def get_offers_by_product_listing_id(self):
        response = client.get(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers",
            headers={"Authorization": f"Bearer {ValueStorageOfferCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_offer_by_id(self):
        response = client.get(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers/{ValueStorageOfferCRUD.offer_id}",
            headers={"Authorization": f"Bearer {ValueStorageOfferCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageOfferCRUD.offer_id
        assert response.json()["sender"]["id"] == "123"
        assert response.json()["recipient"]["id"] == "432"
        assert response.json()["price"] == 299.99
        assert response.json()["state"] == "PENDING"

    def test_get_offer_by_id_not_found(self):
        response = client.get(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers/notFoundID",
            headers={"Authorization": f"Bearer {ValueStorageOfferCRUD.access_token}"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Offer not found"}

    # def test_update_offer_by_id(self):
    #     response = client.patch(
    #         f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers/{ValueStorageOfferCRUD.offer_id}",
    #         json={"state": "ACCEPTED"},
    #         headers={"Authorization": f"Bearer {ValueStorageOfferCRUD.access_token}"},
    #     )
    #     assert response.status_code == 200
    #     assert response.json()["id"] == ValueStorageOfferCRUD.offer_id
    #     assert response.json()["state"] == "ACCEPTED"

    def test_delete_offer_by_id(self):
        response = client.delete(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers/{ValueStorageOfferCRUD.offer_id}",
            headers={"Authorization": f"Bearer {ValueStorageOfferCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageOfferCRUD.offer_id}

    def test_delete_product_listing_by_id(self):
        response = client.delete(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}",
            headers={"Authorization": f"Bearer {ValueStorageOfferCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageOfferCRUD.product_listing_id}

    def test_delete_user(self):
        # Delete users starting from the last one because the first one has the access token
        for user_id in ValueStorageOfferCRUD.user_ids[::-1]:
            user_response = requests.delete(
                os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/users/" + user_id,
                headers={
                    "Authorization": "Bearer "
                    + ValueStorageOfferCRUD.access_token_admin
                },
            )

            assert user_response.status_code == 200
            assert "id" in user_response.json()
