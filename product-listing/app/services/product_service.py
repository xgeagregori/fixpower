from abc import ABC, abstractmethod

class ProductService(ABC):
    @abstractmethod
    def create_Product(self, id, product, catorgory):
        pass

class ProductFactory(ABC):
    @abstractmethod
    def create_Product(self, product):
        pass