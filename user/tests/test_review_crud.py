from fastapi.testclient import TestClient

from app.user_controller import app

client = TestClient(app)


class ValueStorageReviewCRUD:
    user_id_sender = None
    user_id_recipient = None
    review_id = None
    access_token = None


class TestSuiteReviewCRUD:
    def test_create_user_sender(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsernameReview",
                "email": "test@example.com",
                "password": "testPassword",
                "is_admin": True,
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageReviewCRUD.user_id_sender = response.json()["id"]

    def test_create_user_recipient(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsernameReview2",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageReviewCRUD.user_id_recipient = response.json()["id"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameReview", "password": "testPassword"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        ValueStorageReviewCRUD.access_token = response.json()["access_token"]

    def test_create_review(self):
        response = client.post(
            f"/users/{ValueStorageReviewCRUD.user_id_recipient}/reviews",
            json={
                "sender_id": ValueStorageReviewCRUD.user_id_sender,
                "rating": 5,
                "message": "testMessage",
            },
            headers={"Authorization": f"Bearer {ValueStorageReviewCRUD.access_token}"},
        )
        assert response.status_code == 201
        ValueStorageReviewCRUD.review_id = response.json()["id"]

    def test_get_reviews_by_user_id(self):
        response = client.get(
            f"/users/{ValueStorageReviewCRUD.user_id_recipient}/reviews",
            headers={"Authorization": f"Bearer {ValueStorageReviewCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_review_by_id(self):
        response = client.get(
            f"/users/{ValueStorageReviewCRUD.user_id_recipient}/reviews/{ValueStorageReviewCRUD.review_id}",
            headers={"Authorization": f"Bearer {ValueStorageReviewCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageReviewCRUD.review_id

    def test_update_review_by_id(self):
        response = client.patch(
            f"/users/{ValueStorageReviewCRUD.user_id_recipient}/reviews/{ValueStorageReviewCRUD.review_id}",
            json={"rating": 4, "message": "testMessageUpdated"},
            headers={"Authorization": f"Bearer {ValueStorageReviewCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageReviewCRUD.review_id
        assert response.json()["rating"] == 4
        assert response.json()["message"] == "testMessageUpdated"

    def test_delete_review_by_id(self):
        response = client.delete(
            f"/users/{ValueStorageReviewCRUD.user_id_recipient}/reviews/{ValueStorageReviewCRUD.review_id}",
            headers={"Authorization": f"Bearer {ValueStorageReviewCRUD.access_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageReviewCRUD.review_id

    def test_delete_user(self):
        # Delete users starting from the last one because the first one has the access token
        for user_id in [
            ValueStorageReviewCRUD.user_id_recipient,
            ValueStorageReviewCRUD.user_id_sender,
        ]:
            response = client.delete(
                f"/users/{user_id}",
                headers={
                    "Authorization": f"Bearer {ValueStorageReviewCRUD.access_token}"
                },
            )
            assert response.status_code == 200
            assert response.json()["id"] == user_id
