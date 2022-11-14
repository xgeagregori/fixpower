from fastapi.testclient import TestClient

from app.product_listing_controller import app

client = TestClient(app)


class ValueStorageProductListingCRUD:
    product_listing_ids = []
    listed_price = None


class TestSuiteProductListingCRUD:
    def test_create_product_listing_with_id(self):
        response = client.post(
            "/product-listings",
            json={
                "id": "testID",
                "listed_price": 319.99,
                "product": {
                    "name": "Surface Pro 7",
                    "brand": "Surface",
                    "category": "REFURBISHED_PRODUCT",
                    "sub_category": "LAPTOP",
                },
            },
        )
        assert response.status_code == 201
        assert response.json() == {"id": "testID"}
        ValueStorageProductListingCRUD.product_listing_ids.append(response.json()["id"])

    def test_create_product_listing_without_id(self):
        response = client.post(
            "/product-listings",
            json={
                "listed_price": 319.99,
                "product": {
                    "name": "Surface Pro 7",
                    "brand": "Surface",
                    "category": "REFURBISHED_PRODUCT",
                    "sub_category": "LAPTOP",
                },
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageProductListingCRUD.product_listing_ids.append(response.json()["id"])

    def test_create_product_listing_already_exists_same_id(self):
        response = client.post(
            "/product-listings",
            json={
                "id": "testID",
                "listed_price": 319.99,
                "product": {
                    "name": "Surface Pro 7",
                    "brand": "Surface",
                    "category": "REFURBISHED_PRODUCT",
                    "sub_category": "LAPTOP",
                },
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Product listing already exists"}

    def test_get_product_listings(self):
        response = client.get(
            "/product-listings",
        )
        assert response.status_code == 200
        assert len(response.json()) >= 2

    def test_get_product_listing_by_id(self):
        response = client.get("/product-listings/testID")
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert response.json()["listed_price"] == 319.99
        assert response.json()["product"]["name"] == "Surface Pro 7"
        assert response.json()["product"]["brand"] == "Surface"
        assert response.json()["product"]["category"] == "REFURBISHED_PRODUCT"
        assert response.json()["product"]["sub_category"] == "LAPTOP"

    def test_get_product_listing_by_id_not_found(self):
        response = client.get(
            f"/product-listings/notFoundID",
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Product listing not found"}

    def test_update_product_listing_by_id(self):
        response = client.patch(
            "/product-listings/testID", json={"listed_price": 349.99}
        )
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert response.json()["listed_price"] == 349.99
        assert response.json()["product"]["name"] == "Surface Pro 7"
        assert response.json()["product"]["brand"] == "Surface"
        assert response.json()["product"]["category"] == "REFURBISHED_PRODUCT"
        assert response.json()["product"]["sub_category"] == "LAPTOP"

    def test_delete_product_listing_by_id(self):
        for product_listing_id in ValueStorageProductListingCRUD.product_listing_ids:
            response = client.delete(f"/product-listings/{product_listing_id}")
            assert response.status_code == 200
            assert response.json() == {"id": product_listing_id}
