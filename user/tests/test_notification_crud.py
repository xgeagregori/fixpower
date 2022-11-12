from fastapi.testclient import TestClient

from app.user_controller import app

client = TestClient(app)


class ValueStorageNotificationCRUD:
    user_id = None
    notification_id = None
    access_token = None


class TestSuiteNotificationCRUD:
    def test_create_user(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsernameNotification",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageNotificationCRUD.user_id = response.json()["id"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameNotification", "password": "testPassword"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        ValueStorageNotificationCRUD.access_token = response.json()["access_token"]

    def test_create_notification(self):
        response = client.post(
            f"/users/{ValueStorageNotificationCRUD.user_id}/notifications",
            json={"type": "testType", "title": "testTitle", "message": "testMessage"},
            headers={
                "Authorization": f"Bearer {ValueStorageNotificationCRUD.access_token}"
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageNotificationCRUD.notification_id = response.json()["id"]

    def test_get_notifications_by_user_id(self):
        response = client.get(
            f"/users/{ValueStorageNotificationCRUD.user_id}/notifications",
            headers={
                "Authorization": f"Bearer {ValueStorageNotificationCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_notification_by_id(self):
        response = client.get(
            f"/users/{ValueStorageNotificationCRUD.user_id}/notifications/{ValueStorageNotificationCRUD.notification_id}",
            headers={
                "Authorization": f"Bearer {ValueStorageNotificationCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageNotificationCRUD.notification_id

    def test_get_notification_by_id_not_found(self):
        response = client.get(
            f"/users/{ValueStorageNotificationCRUD.user_id}/notifications/notFoundID",
            headers={
                "Authorization": f"Bearer {ValueStorageNotificationCRUD.access_token}"
            },
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Notification not found"}

    def test_update_notification_by_id(self):
        response = client.patch(
            f"/users/{ValueStorageNotificationCRUD.user_id}/notifications/{ValueStorageNotificationCRUD.notification_id}",
            json={"title": "testTitleUpdated", "message": "testMessageUpdated"},
            headers={
                "Authorization": f"Bearer {ValueStorageNotificationCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageNotificationCRUD.notification_id
        assert response.json()["type"] == "testType"
        assert response.json()["title"] == "testTitleUpdated"
        assert response.json()["message"] == "testMessageUpdated"

    def test_delete_notification_by_id(self):
        response = client.delete(
            f"/users/{ValueStorageNotificationCRUD.user_id}/notifications/{ValueStorageNotificationCRUD.notification_id}",
            headers={
                "Authorization": f"Bearer {ValueStorageNotificationCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageNotificationCRUD.notification_id}

    def test_delete_user_by_id(self):
        response = client.delete(
            f"/users/{ValueStorageNotificationCRUD.user_id}",
            headers={
                "Authorization": f"Bearer {ValueStorageNotificationCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageNotificationCRUD.user_id}
