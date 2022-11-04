from fastapi.testclient import TestClient

from app.transaction_controller import app

client = TestClient(app)

class TestSuiteTransactionCRUD:

    def test_create_transaction_with_id(self):
        response = client.post(
            "/transactions",
            json={
                "id": "test",
                "state": "test_state",   
                
            },
        )
        assert response.status_code == 201
        assert response.json()["id"] == "test"
        
        
        
    def test_get_transactions(self):
        response = client.get("/transactions")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Transaction Service!!!"}

