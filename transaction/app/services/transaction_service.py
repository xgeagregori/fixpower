from abc import ABC, abstractmethod
from app.schemas.transaction import TransactionCreate


class TransactionService(ABC):
    @abstractmethod
    def create_transaction(self, transaction_create: TransactionCreate):
        pass

    @abstractmethod
    def get_transaction_by_id(self, transaction_id: str):
        pass

    @abstractmethod
    def delete_transaction_by_id(self, transaction_id: str):
        pass
