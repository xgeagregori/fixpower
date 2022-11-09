from fastapi.testclient import TestClient

from app.transaction_controller import app

client = TestClient(app)


class ValueStorageTransactionCRUD:
    transaction_ids = []


class TestSuiteTransactionCRUD:
    def test_create_transaction_with_id(self):
        response = client.post(
            "/transactions",
            json={
                "id": "testID",
                "state": "testState",
            },
        )
        assert response.status_code == 201
        assert response.json()["id"] == "testID"
        ValueStorageTransactionCRUD.transaction_ids.append("testID")

    def test_create_transaction_without_id(self):
        response = client.post(
            "/transactions",
            json={
                "state": "testState",
            },
        )
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageTransactionCRUD.transaction_ids.append(response.json()["id"])

    def test_create_transaction_with_existing_id(self):
        response = client.post(
            "/transactions",
            json={
                "id": "testID",
                "state": "testState",
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Transaction already exists"}

    def test_get_transactions(self):
        response = client.get("/transactions")
        assert response.status_code == 200
        assert len(response.json()) >= 2

    def test_get_transaction_by_id(self):
        response = client.get("/transactions/testID")
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert "state" in response.json()
        assert "created_at" in response.json()

    def test_get_transaction_not_found(self):
        response = client.get("/transactions/notFoundID")
        assert response.status_code == 404
        assert response.json() == {"detail": "Transaction not found"}

    def test_update_transaction_by_id(self):
        response = client.patch(
            "/transactions/testID",
            json={
                "state": "testStateUpdated",
            },
        )
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert response.json()["state"] == "testStateUpdated"
        assert "created_at" in response.json()

    def test_delete_transaction_by_id(self):
        for transaction_id in ValueStorageTransactionCRUD.transaction_ids:
            response = client.delete(f"/transactions/{transaction_id}")
            assert response.status_code == 200
            assert "id" in response.json()
