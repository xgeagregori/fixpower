from abc import ABC, abstractmethod
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService(ABC):
    @abstractmethod
    def create_transaction(self, transaction_create: TransactionCreate):
        pass

    @abstractmethod
    def get_transactions(self):
        pass

    @abstractmethod
    def get_transaction_by_id(self, transaction_id: str):
        pass

    @abstractmethod
    def update_transaction_by_id(
        self, transaction_id: str, transaction_create=TransactionUpdate
    ):
        pass

    @abstractmethod
    def delete_transaction_by_id(self, transaction_id: str):
        pass
