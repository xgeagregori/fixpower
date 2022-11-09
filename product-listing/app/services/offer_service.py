from abc import ABC, abstractmethod


class OfferService(ABC):
    @abstractmethod
    def create_offer(self, id, offer):
        pass

    @abstractmethod
    def get_offers_by_product_listing_id(self, id):
        pass

    @abstractmethod
    def get_offer_by_id(self, id):
        pass

    @abstractmethod
    def update_offer_by_id(self, id, offer):
        pass

    @abstractmethod
    def delete_offer_by_id(self, id):
        pass
