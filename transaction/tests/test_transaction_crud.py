from fastapi.testclient import TestClient

from app.transaction_controller import app

client = TestClient(app)

class ValueStorageTransactionCRUD:
    transaction_ids = []


class TestSuiteTransactionCRUD:
    

    def test_create_transaction_with_id(self):
        response = client.post(
            "/transactions", json={"id": "test", "state": "test_state",},
        )
        assert response.status_code == 201
        assert response.json()["id"] == "test"
        ValueStorageTransactionCRUD.transaction_ids.append("test")
        
        # Create all the test cases for creation
        #test without id
        
        
    
    
       

    def test_get_transactions_by_id(self):
        response = client.get("/transactions/{id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Transaction Service!!!"}

    def test_delete_transaction_by_id(self):
        response = client.delete("/transactions/{id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Transaction deleted successfully!!!"}
