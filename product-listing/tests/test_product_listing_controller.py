from fastapi.testclient import TestClient

from app.product_listing_controller import app

client = TestClient(app)


def test_get_product_listings():
    response = client.get("/product-listings")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Product Listing Service!"}
