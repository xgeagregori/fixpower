from pynamodb.exceptions import DoesNotExist, DeleteError

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import TransactionService


class TransactionServiceImpl(TransactionService):
    def create_transaction(self, transaction_create: TransactionCreate):
        
       
        transaction = Transaction(**transaction_create.dict())
        
        
        transaction.save()
        return transaction.id