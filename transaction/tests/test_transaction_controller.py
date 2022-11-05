from fastapi.testclient import TestClient

from app.transaction_controller import app

client = TestClient(app)


def test_get_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Transaction Service!!!"}