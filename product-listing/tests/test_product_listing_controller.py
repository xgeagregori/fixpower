from fastapi.testclient import TestClient

from app.product_listing_controller import app

client = TestClient(app)


def test_get_product_listings():
    response = client.get("/product-listings")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Product Listing Service!"}

def test_get_product_listing_by_id():
    response = client.get("/product-listings/123")
    assert response.status_code == 200
    assert response.json() == {"id": "123","listed_price": 12.3}

def test_create_product_listing():
    response = client.get("/product-listings")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Product Listing Service!"}

def test_upadte_product_listing_by_id():
    response = client.get("/product-listings")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Product Listing Service!"}

def test_delete_product_listing_by_id():
    response = client.post(
            "/product-listings",
            json={
                "username": "test",
                "email": "test@example.com",
                "password": "test",
            },
        )
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Product Listing Service!"}    