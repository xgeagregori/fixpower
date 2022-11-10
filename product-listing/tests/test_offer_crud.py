from fastapi.testclient import TestClient

from app.product_listing_controller import app

client = TestClient(app)


class ValueStorageOfferCRUD:
    product_listing_id = None
    offer_id = None


class TestSuiteOfferCRUD:
    def test_create_product_listing_with_id(self):
        response = client.post(
            "/product-listings",
            json={"id": "testID", "listed_price": 12.3},
        )
        assert response.status_code == 201
        assert response.json() == {"id": "testID"}
        ValueStorageOfferCRUD.product_listing_id = response.json()["id"]

    def test_create_offer(self):
        response = client.post(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers",
            json={"sender": "123", "recipient": "432", "price": 12.3},
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageOfferCRUD.offer_id = response.json()["id"]

    def get_offers_by_product_listing_id(self):
        response = client.get(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers"
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_offer_by_id(self):
        response = client.get(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers/{ValueStorageOfferCRUD.offer_id}"
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageOfferCRUD.offer_id
        assert response.json()["sender"] == "123"
        assert response.json()["recipient"] == "432"
        assert response.json()["price"] == 12.3

    def test_get_offer_by_id_not_found(self):
        response = client.get(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers/notFoundID"
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Offer not found"}

    def test_update_offer_by_id(self):
        response = client.patch(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers/{ValueStorageOfferCRUD.offer_id}",
            json={"state": "ACCEPTED"},
        )
        assert response.status_code == 200
        print(response.json())
        assert response.json()["id"] == ValueStorageOfferCRUD.offer_id
        assert response.json()["state"] == "ACCEPTED"

    def test_delete_offer_by_id(self):
        response = client.delete(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers/{ValueStorageOfferCRUD.offer_id}"
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageOfferCRUD.offer_id}

    def test_delete_product_listing_by_id(self):
        response = client.delete(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}"
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageOfferCRUD.product_listing_id}
