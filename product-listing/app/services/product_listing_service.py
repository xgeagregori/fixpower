from abc import ABC, abstractmethod


class Product_listingService(ABC):
    @abstractmethod
    def create_product_listing(self, product_listing):
        pass

    @abstractmethod
    def get_product_listing_by_product_id(self, product_listingname):
        pass
