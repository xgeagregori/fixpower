from abc import ABC, abstractmethod
from app.schemas.transaction import TransactionCreate

        
class TransactionService(ABC):
    @abstractmethod
    def create_transaction(self, transaction_create: TransactionCreate):
        pass
        