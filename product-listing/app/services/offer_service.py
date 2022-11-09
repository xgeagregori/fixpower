from abc import ABC, abstractmethod


class OfferService(ABC):
    @abstractmethod
    def add_offer(self, id ,offer):
        pass

    @abstractmethod
    def accept_offer(self, id):
        pass

    @abstractmethod
    def decline_offer(self, id):
        pass

    @abstractmethod
    def counter_offer(self, id, offer):
        pass
