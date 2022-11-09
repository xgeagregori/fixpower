from abc import ABC, abstractmethod


class ProductListingService(ABC):
    @abstractmethod
    def create_product_listing(self, product_listing):
        pass

    @abstractmethod
    def get_product_listings(self):
        pass

    @abstractmethod
    def get_product_listing_by_id(self, id):
        pass

    @abstractmethod
    def update_product_listing_by_id(self, id, product_listing):
        pass

    @abstractmethod
    def delete_product_listing_by_id(self, id):
        pass

