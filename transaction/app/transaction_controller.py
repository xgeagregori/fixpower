from fastapi import FastAPI, Depends, status, HTTPException
from mangum import Mangum

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.dependencies.auth import (
    get_current_user,
    check_user_permissions,
    check_user_is_admin,
)
from app.dependencies.transaction import TransactionDep
from app.schemas.transaction import TransactionCreate, TransactionUpdate

import os
import requests

app = FastAPI(
    root_path="/prod/transaction-api/v1",
    title="Transaction API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/transaction-api/v1")
router = InferringRouter()


@cbv(router)
class TransactionController:
    @app.post("/login", tags=["auth"])
    def login(form_data: OAuth2PasswordRequestForm = Depends()):
        token_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/login",
            data=dict(username=form_data.username, password=form_data.password),
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_response.json()

    @app.post(
        "/transactions", status_code=status.HTTP_201_CREATED, tags=["transactions"]
    )
    def create_transaction(
        transaction_create: TransactionCreate,
        self=Depends(TransactionDep),
        current_user=Depends(get_current_user),
    ):
        """Create transaction."""
        transaction_id = self.transaction_service.create_transaction(transaction_create)
        if transaction_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Transaction not created",
            )
        return {"id": transaction_id}

    @app.get("/transactions", tags=["transactions"])
    def get_transactions(
        current_user=Depends(get_current_user), self=Depends(TransactionDep)
    ):
        """Get all transactions"""
        check_user_is_admin(current_user)
        transactions = self.transaction_service.get_transactions()
        return [transactions.attribute_values for transactions in transactions]

    @app.get("/transactions/{transaction_id}", tags=["transactions"])
    def get_transaction_by_id(
        transaction_id: str,
        current_user=Depends(get_current_user),
        self=Depends(TransactionDep),
    ):
        """Get transaction by id."""
        transaction = self.transaction_service.get_transaction_by_id(transaction_id)
        return {"id": transaction.id, **transaction.attribute_values}

    @app.patch("/transactions/{transaction_id}", tags=["transactions"])
    def update_transaction_by_id(
        transaction_id: str,
        transaction_update: TransactionUpdate,
        current_user=Depends(get_current_user),
        self=Depends(TransactionDep),
    ):
        """Update transaction by id"""
        transaction = self.transaction_service.update_transaction_by_id(
            transaction_id, transaction_update
        )
        return transaction.attribute_values

    @app.delete("/transactions/{transaction_id}", tags=["transactions"])
    def delete_transaction_by_id(
        transaction_id: str,
        current_user=Depends(get_current_user),
        self=Depends(TransactionDep),
    ):
        """Delete transaction by id."""
        transaction_id = self.transaction_service.delete_transaction_by_id(
            transaction_id
        )

        return {"id": transaction_id}


app.include_router(router)
