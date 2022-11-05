from fastapi.testclient import TestClient

from app.transaction_controller import app

client = TestClient(app)


class ValueStorageTransactionCRUD:
    transaction_ids = []


class TestSuiteTransactionCRUD:
    def test_create_transaction_with_id(self):
        response = client.post(
            "/transactions", json={"id": "testID", "state": "test_state",},
        )
        assert response.status_code == 201
        assert response.json()["id"] == "testID"
        ValueStorageTransactionCRUD.transaction_ids.append("testID")

    def test_create_transaction_without_id(self):
        response = client.post("/transactions", json={"state": "test_state1",},)
        assert response.status_code == 201
        assert "id" in response.json()
        ValueStorageTransactionCRUD.transaction_ids.append(response.json()["id"])

    def test_create_transaction_with_existing_id(self):
        response = client.post(
            "/transactions", json={"id": "testID", "state": "testState",},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Transaction already exists"}

    def test_get_transactions_by_id(self):
        response = client.get("/transactions/testID")
        assert response.status_code == 200
        assert response.json()["id"] == "testID"
        assert "state" in response.json()
        assert "created_at" in response.json()

    def test_get_transaction_not_found(self):
        response = client.get("/transactions/testIDNotFound")
        assert response.status_code == 404
        assert response.json() == {"detail": "Transaction not found"}

    def test_delete_transaction_by_id(self):
            response = client.delete("/transactions/testID")
            assert response.status_code == 200
            assert response.json()["id"] == "testID"
        
           
                
        

    def test_delete_transaction_not_found(self):
        response = client.delete("/transactions/testIDNotFound")
        assert response.status_code == 404
        assert response.json() == {"detail": "Transaction not found"}
