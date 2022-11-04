from fastapi.testclient import TestClient

from app.user_controller import app

client = TestClient(app)


class ValueStorageUserCRUD:
    user_ids = []
    access_token = None


class TestSuiteUserCRUD:
    def test_register_with_id(self):
        response = client.post(
            "/register",
            json={
                "id": "test",
                "username": "test",
                "email": "test@example.com",
                "password": "test",
            },
        )
        assert response.status_code == 201
        assert response.json() == {"id": "test"}
        ValueStorageUserCRUD.user_ids.append("test")

    def test_register_without_id(self):
        response = client.post(
            "/register",
            json={
                "username": "test2",
                "email": "test2@example.com",
                "password": "test2",
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageUserCRUD.user_ids.append(response.json()["id"])

    def test_register_user_already_exists(self):
        response = client.post(
            "/register",
            json={
                "username": "test",
                "email": "test@example.com",
                "password": "test",
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "User already exists"}

    def test_get_authenticated_user_not_authenticated(self):
        response = client.get("/users/me")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_login_invalid_credentials(self):
        response = client.post(
            "/login",
            data={"username": "wrong", "password": "wrong"},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid username or password"}

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "test", "password": "test"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageUserCRUD.access_token = response.json()["access_token"]

    def test_get_authenticated_user(self):
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == "test"
        assert response.json()["username"] == "test"
        assert response.json()["email"] == "test@example.com"
        assert "password" not in response.json()
        assert "hashed_password" in response.json()
        assert "created_at" in response.json()
