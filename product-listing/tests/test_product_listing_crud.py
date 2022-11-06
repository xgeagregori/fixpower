from fastapi.testclient import TestClient

from app.product_listing_controller import app

client = TestClient(app)


class ValueStorageProductListingCRUD:
    ids = []
    listed_price = None


class TestSuiteProductListingCRUD:
    def test_create_product_listing(self):
        response = client.post(
            "/product-listings", json={"id": "123", "listed_price": "12.3"},
        )
        assert response.status_code == 201
        assert response.json() == {"id": "123"}
        ValueStorageProductListingCRUD.ids.append(response.json()["id"])

    def test_create_product_listing_without_id(self):
        response = client.post("/product-listings",
                               json={"listed_price": "3.45"},)
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageProductListingCRUD.ids.append(response.json()["id"])

    def test_create_product_listing_already_exists_same_id(self):
        response = client.post(
            "/product-listings", json={"id": "123", "listed_price": 12.3},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Product-listing already exists"}

    def test_get_product_listing_by_id(self):
        response = client.get("/product-listings/123")
        assert response.status_code == 200
        assert response.json() == {"id": "123", "listed_price": 12.3}

    def test_upadte_product_listing_by_id(self):
        response = client.patch("/product-listings/123",
                                json={"id": "123",
                                      "listed_price": 1200
                                      }
                                )
        assert response.status_code == 200
        assert response.json()["id"] == "123"
        assert response.json()["listed_price"] == 1200.0

    def test_delete_product_listing_by_id(self):
        for id in ValueStorageProductListingCRUD.ids:
            response = client.delete(
                f'/product-listings/{id}'
            )
            assert response.status_code == 200
            assert response.json() == {"id": id}

    # def test_delete_product_listing_by_id_not_found():
    #     for id in ValueStorageProductListingCRUD.ids:
    #         response = client.delete(
    #             f'/product-listings/{id}'
    #         )
    #         assert response.status_code == 200
    #         assert response.json() == {"id": id}
