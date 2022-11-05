from fastapi import HTTPException, status
from pynamodb.exceptions import DoesNotExist, DeleteError

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import TransactionService

from uuid import uuid4


class TransactionServiceImpl(TransactionService):
    def create_transaction(self, transaction_create: TransactionCreate):
        if transaction_create.id:

            try:
                transaction_found = self.get_transaction_by_id(transaction_create.id)
            except:
                pass
            if transaction_found is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transaction already exists",
                )
        else:
            transaction_create.id = str(uuid4())
        transaction = Transaction(**transaction_create.dict())
        transaction.save()
        return transaction.id

    def get_transaction_by_id(self, transaction_id: str):
        try:
            transaction = Transaction.get(transaction_id)
            return transaction
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
            )

    def delete_transaction_by_id(self, transaction_id: str):
        transaction = self.get_transaction_by_id(transaction_id)

        if transaction is not None:
            try:
                # Delete operation
                transaction.delete()
                return transaction.id
            except DeleteError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error on deletion",
                )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
