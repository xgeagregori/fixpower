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

    def test_add_offer(self):
        response = client.post(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/offers",
            json={"sender": "123",
                  "recipient": "432",
                  "price": 12.3},
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageOfferCRUD.offer_id = response.json()["id"]

    def test_accept_offer(self):
        response = client.get(f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/accept_offer")
        assert response.status_code == 200
        assert response.json()["state"] == "Accepted"
    
    def test_decline_offer(self):
        response = client.get(f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/decline_offer")
        assert response.status_code == 200
        assert response.json()["state"] == "Declined"

    def test_counter_offer(self):
        response = client.post(
            f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}/counter_offer",
            json={"sender": "123",
                  "recipient": "432",
                  "price": 123},
        )
        assert response.status_code == 201
        assert len(response.json()["offers"]) == 2
        assert response.json()["offers"][-1]["attribute_values"]["state"] == "Pending"
        

    def test_delete_product_listing_by_id(self):
        response = client.delete(f"/product-listings/{ValueStorageOfferCRUD.product_listing_id}")
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageOfferCRUD.product_listing_id}