from fastapi import HTTPException, status
from pynamodb.exceptions import DoesNotExist, DeleteError

from app.models.transaction import Transaction
from app.models.commands.paid_command import PaidCommand
from app.models.commands.shipped_command import ShippedCommand
from app.models.commands.delivered_command import DeliveredCommand
from app.models.commands.returned_command import ReturnedCommand
from app.models.commands.cancelled_command import CancelledCommand
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.transaction_service import TransactionService

from uuid import uuid4


class TransactionServiceImpl(TransactionService):
    def __init__(self) -> None:
        super().__init__()
        self.commands = {
            "PAID": PaidCommand(),
            "SHIPPED": ShippedCommand(),
            "DELIVERED": DeliveredCommand(),
            "RETURNED": ReturnedCommand(),
            "CANCELLED": CancelledCommand(),
        }

    def create_transaction(self, transaction_create: TransactionCreate):
        generated_id = str(uuid4())

        transaction = Transaction(id=generated_id, **transaction_create.dict())
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
        if transaction_update.state and transaction.state != transaction_update.state:
            transaction = self.commands[transaction_update.state].execute(transaction)

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
