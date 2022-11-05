from fastapi import FastAPI, Depends, status, HTTPException
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.dependencies.transaction import TransactionDep
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import TransactionService
from app.services.transaction_service_impl import TransactionServiceImpl

app = FastAPI(
    ##root_path="/prod/transaction-api/v1",
    title="Transaction API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/transaction-api/v1")
router = InferringRouter()


@cbv(router)
class TransactionController:
    @app.post("/transactions", status_code=status.HTTP_201_CREATED)
    def create_transaction(
        transaction_create: TransactionCreate, self=Depends(TransactionDep)
    ):
        """Create transaction."""
        transaction_id = self.transaction_service.create_transaction(transaction_create)
        if transaction_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Transaction not created",
            )
        return {"id": transaction_id}

    @app.get("/transactions/{transaction_id}")
    def get_transaction_by_id(transaction_id: str, self=Depends(TransactionDep)):
        """Get transaction by id."""
        transaction = self.transaction_service.get_transaction_by_id(transaction_id)
        # return transaction

        return {"id": transaction.id, **transaction.attribute_values}

    @app.delete("/transactions/{transaction_id}")
    def delete_transaction_by_id(transaction_id: str, self=Depends(TransactionDep)):
        """Delete transaction by id."""
        transaction_id = self.transaction_service.delete_transaction_by_id(
            transaction_id
        )
        
        return {"id": transaction_id}


app.include_router(router)
