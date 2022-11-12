from fastapi.testclient import TestClient

from app.user_controller import app

client = TestClient(app)


class ValueStorageFavouriteCRUD:
    user_id = None
    favourite_id = None
    access_token = None


class TestSuiteFavouriteCRUD:
    def test_create_user(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsernameFavourite",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageFavouriteCRUD.user_id = response.json()["id"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameFavourite", "password": "testPassword"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        ValueStorageFavouriteCRUD.access_token = response.json()["access_token"]

    def test_create_favourite(self):
        response = client.post(
            f"/users/{ValueStorageFavouriteCRUD.user_id}/favourites",
            json={"id": "testProductListingID"},
            headers={
                "Authorization": f"Bearer {ValueStorageFavouriteCRUD.access_token}"
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageFavouriteCRUD.favourite_id = response.json()["id"]

    def test_get_favourites_by_user_id(self):
        response = client.get(
            f"/users/{ValueStorageFavouriteCRUD.user_id}/favourites",
            headers={
                "Authorization": f"Bearer {ValueStorageFavouriteCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_delete_favourite_by_id(self):
        response = client.delete(
            f"/users/{ValueStorageFavouriteCRUD.user_id}/favourites/{ValueStorageFavouriteCRUD.favourite_id}",
            headers={
                "Authorization": f"Bearer {ValueStorageFavouriteCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageFavouriteCRUD.favourite_id}

    def test_delete_user_by_id(self):
        response = client.delete(
            f"/users/{ValueStorageFavouriteCRUD.user_id}",
            headers={
                "Authorization": f"Bearer {ValueStorageFavouriteCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageFavouriteCRUD.user_id}
