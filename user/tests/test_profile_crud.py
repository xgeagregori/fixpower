from fastapi.testclient import TestClient

from app.user_controller import app

client = TestClient(app)

class ValueStorageProfileCRUD:
    user_id = None
    access_token = None

class TestSuiteProfileCRUD:
    def test_create_user(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsernameProfile",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageProfileCRUD.user_id = response.json()["id"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameProfile", "password": "testPassword"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        ValueStorageProfileCRUD.access_token = response.json()["access_token"]

    def test_update_profile_by_user_id(self):
        response = client.patch(
            f"/users/{ValueStorageProfileCRUD.user_id}/profile",
            json={
                "address": "testAddress",
                "settings": {"sms_notifications": False},
            },
            headers={
                "Authorization": f"Bearer {ValueStorageProfileCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json()["address"] == "testAddress"
        assert response.json()["settings"]["sms_notifications"] == False
        assert response.json()["settings"]["email_notifications"] == True

    def test_get_profile_by_user_id(self):
        response = client.get(
            f"/users/{ValueStorageProfileCRUD.user_id}/profile",
            headers={
                "Authorization": f"Bearer {ValueStorageProfileCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json()["address"] == "testAddress"
        assert response.json()["settings"]["sms_notifications"] == False
        assert response.json()["settings"]["email_notifications"] == True

    def test_delete_user(self):
        response = client.delete(
            f"/users/{ValueStorageProfileCRUD.user_id}",
            headers={
                "Authorization": f"Bearer {ValueStorageProfileCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageProfileCRUD.user_id}
        

    