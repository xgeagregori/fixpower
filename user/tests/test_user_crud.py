from fastapi.testclient import TestClient

from app.user_controller import app
from app.services.user_service import UserService
from app.services.user_service_impl import UserServiceImpl

client = TestClient(app)


class ValueStorageUserCRUD:
    user_ids = []
    access_token = None


class TestSuiteUserCRUD:
    def test_register_with_id(self):
        response = client.post(
            "/register",
            json={
                "id": "testID",
                "username": "testUsername",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )
        assert response.status_code == 201
        assert response.json() == {"id": "testID"}
        ValueStorageUserCRUD.user_ids.append(response.json()["id"])

    def test_register_without_id(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsername2",
                "email": "test2@example.com",
                "password": "testPassword2",
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageUserCRUD.user_ids.append(response.json()["id"])

    def test_register_user_already_exists_same_id(self):
        response = client.post(
            "/register",
            json={
                "id": "testID",
                "username": "testUsername2",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "User already exists"}

    def test_register_user_already_exists_same_username(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsername",
                "email": "test@example.com",
                "password": "testPassword",
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
            data={"username": "testUsername", "password": "testPassword"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        ValueStorageUserCRUD.access_token = response.json()["access_token"]

    def test_get_users(self):
        response = client.get(
            "/users",
            headers={"Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()) >= 2

    def test_get_authenticated_user(self):
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert response.json()["username"] == "testUsername"
        assert response.json()["email"] == "test@example.com"
        assert "password" not in response.json()
        assert "hashed_password" in response.json()
        assert "created_at" in response.json()

    def test_get_user_by_username(self):
        user_service: UserService = UserServiceImpl()
        user = user_service.get_user_by_username("testUsername")
        assert user.id == "testID"
        assert user.username == "testUsername"
        assert user.email == "test@example.com"
        assert "password" not in user.attribute_values
        assert "hashed_password" in user.attribute_values
        assert "created_at" in user.attribute_values

    def test_get_user_by_username_not_found(self):
        user_service: UserService = UserServiceImpl()
        user = user_service.get_user_by_username("notFoundUsername")
        assert user is None

    def test_get_user_by_id(self):
        response = client.get(
            f"/users/testID",
            headers={"Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert response.json()["username"] == "testUsername"
        assert response.json()["email"] == "test@example.com"
        assert "password" not in response.json()
        assert "hashed_password" in response.json()
        assert "created_at" in response.json()

    def test_get_user_by_id_not_found(self):
        response = client.get(
            f"/users/notFoundID",
            headers={"Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_update_user_by_id(self):
        response = client.patch(
            f"/users/testID",
            json={
                "username": "testUsernameUpdated",
                "email": "testUpdated@example.com",
            },
            headers={"Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert response.json()["username"] == "testUsernameUpdated"
        assert response.json()["email"] == "testUpdated@example.com"
        assert "password" not in response.json()
        assert "hashed_password" in response.json()
        assert "created_at" in response.json()

    def test_update_user_by_id_not_found(self):
        response = client.patch(
            f"/users/notFoundID",
            json={
                "username": "testUsernameUpdated",
                "email": "testUpdated@example.com",
            },
            headers={"Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

    def test_delete_user_by_id(self):
        for user_id in ValueStorageUserCRUD.user_ids:
            response = client.delete(
                f"/users/{user_id}",
                headers={
                    "Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"
                },
            )
            assert response.status_code == 200
            assert response.json() == {"id": user_id}

    def test_delete_user_by_id_not_found(self):
        response = client.delete(
            f"/users/notFoundID",
            headers={"Authorization": f"Bearer {ValueStorageUserCRUD.access_token}"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
