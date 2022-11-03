from fastapi.testclient import TestClient

from app.user_controller import app

client = TestClient(app)


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the User Service!"}
