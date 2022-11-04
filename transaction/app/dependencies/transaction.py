from app.services.transaction_service import TransactionService
from app.services.transaction_service_impl import TransactionServiceImpl


class TransactionDep:
    def __init__(self):
        self.transaction_service: TransactionService = TransactionServiceImpl()