from fastapi import HTTPException, status
from pynamodb.exceptions import DoesNotExist, DeleteError

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.transaction_service import TransactionService

from uuid import uuid4


class TransactionServiceImpl(TransactionService):
    def create_transaction(self, transaction_create: TransactionCreate):
        transaction_already_exists = False

        if transaction_create.id:
            try:
                transaction_found = self.get_transaction_by_id(transaction_create.id)
                transaction_already_exists = True
            except:
                pass

            # If id already exists, raise exception
            if transaction_already_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transaction already exists",
                )
        else:
            transaction_create.id = str(uuid4())
        transaction = Transaction(**transaction_create.dict())
        transaction.save()
        return transaction.id

    def get_transactions(self):
        try:
            return Transaction.scan()
        except Transaction.ScanError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Transaction found",
            )

    def get_transaction_by_id(self, transaction_id: str):
        try:
            transaction = Transaction.get(transaction_id)
            return transaction
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
            )

    def update_transaction_by_id(
        self, transaction_id: str, transaction_update: TransactionUpdate
    ):
        transaction = self.get_transaction_by_id(transaction_id)
        for key, value in transaction_update.dict().items():
            if value:
                setattr(transaction, key, value)

        transaction.save()
        return transaction

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
