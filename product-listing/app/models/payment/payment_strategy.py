from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def process(self):
        pass
