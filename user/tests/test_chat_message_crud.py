from fastapi.testclient import TestClient

from app.user_controller import app

client = TestClient(app)


class ValueStorageChatMessageCRUD:
    user_id_sender = None
    user_id_recipient = None
    chat_message_id = None
    access_token = None


class TestSuiteChatMessageCRUD:
    def test_create_user_sender(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsernameChatMessage",
                "email": "test@example.com",
                "password": "testPassword",
                "is_admin": True,
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageChatMessageCRUD.user_id_sender = response.json()["id"]

    def test_create_user_recipient(self):
        response = client.post(
            "/register",
            json={
                "username": "testUsernameChatMessage2",
                "email": "test@example.com",
                "password": "testPassword",
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageChatMessageCRUD.user_id_recipient = response.json()["id"]

    def test_login(self):
        response = client.post(
            "/login",
            data={"username": "testUsernameChatMessage", "password": "testPassword"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()
        ValueStorageChatMessageCRUD.access_token = response.json()["access_token"]

    def test_create_chat_message(self):
        response = client.post(
            f"/users/{ValueStorageChatMessageCRUD.user_id_recipient}/chat-messages",
            json={
                "sender_id": ValueStorageChatMessageCRUD.user_id_sender,
                "recipient_id": ValueStorageChatMessageCRUD.user_id_recipient,
                "message": "testMessage",
            },
            headers={
                "Authorization": f"Bearer {ValueStorageChatMessageCRUD.access_token}"
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageChatMessageCRUD.chat_message_id = response.json()["id"]

    def test_get_chat_messages_by_user_id(self):
        response = client.get(
            f"/users/{ValueStorageChatMessageCRUD.user_id_recipient}/chat-messages",
            headers={
                "Authorization": f"Bearer {ValueStorageChatMessageCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_chat_message_by_id(self):
        response = client.get(
            f"/users/{ValueStorageChatMessageCRUD.user_id_recipient}/chat-messages/{ValueStorageChatMessageCRUD.chat_message_id}",
            headers={
                "Authorization": f"Bearer {ValueStorageChatMessageCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageChatMessageCRUD.chat_message_id
        assert (
            response.json()["sender_id"] == ValueStorageChatMessageCRUD.user_id_sender
        )
        assert (
            response.json()["recipient_id"]
            == ValueStorageChatMessageCRUD.user_id_recipient
        )
        assert response.json()["message"] == "testMessage"
        assert "created_at" in response.json()

    def test_get_chat_message_by_id_not_found(self):
        response = client.get(
            f"/users/{ValueStorageChatMessageCRUD.user_id_recipient}/chat-messages/notFoundID",
            headers={
                "Authorization": f"Bearer {ValueStorageChatMessageCRUD.access_token}"
            },
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "ChatMessage not found"}

    def test_update_chat_message_by_id(self):
        response = client.patch(
            f"/users/{ValueStorageChatMessageCRUD.user_id_recipient}/chat-messages/{ValueStorageChatMessageCRUD.chat_message_id}",
            json={"message": "testMessageUpdated"},
            headers={
                "Authorization": f"Bearer {ValueStorageChatMessageCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json()["id"] == ValueStorageChatMessageCRUD.chat_message_id
        assert (
            response.json()["sender_id"] == ValueStorageChatMessageCRUD.user_id_sender
        )
        assert (
            response.json()["recipient_id"]
            == ValueStorageChatMessageCRUD.user_id_recipient
        )
        assert response.json()["message"] == "testMessageUpdated"
        assert "created_at" in response.json()

    def test_delete_chat_message_by_id(self):
        response = client.delete(
            f"/users/{ValueStorageChatMessageCRUD.user_id_recipient}/chat-messages/{ValueStorageChatMessageCRUD.chat_message_id}",
            headers={
                "Authorization": f"Bearer {ValueStorageChatMessageCRUD.access_token}"
            },
        )
        assert response.status_code == 200
        assert response.json() == {"id": ValueStorageChatMessageCRUD.chat_message_id}

    def test_delete_user(self):
        # Delete users starting from the last one because the first one has the access token
        for user_id in [
            ValueStorageChatMessageCRUD.user_id_recipient,
            ValueStorageChatMessageCRUD.user_id_sender,
        ]:
            response = client.delete(
                f"/users/{user_id}",
                headers={
                    "Authorization": f"Bearer {ValueStorageChatMessageCRUD.access_token}"
                },
            )
            assert response.status_code == 200
            assert response.json()["id"] == user_id
