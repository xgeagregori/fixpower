from abc import ABC, abstractmethod


class ProductService(ABC):
    @abstractmethod
    def create_product(self, product_create):
        pass


class ProductFactory(ABC):
    @abstractmethod
    def create_product(self, product_create):
        pass
