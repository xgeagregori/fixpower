from abc import ABC, abstractmethod


class PaymentService(ABC):
    @abstractmethod
    def create_payment_strategy(self, payment_method):
        pass


class PaymentStrategyFactory(ABC):
    @abstractmethod
    def create_payment_strategy(self, payment_method):
        pass
