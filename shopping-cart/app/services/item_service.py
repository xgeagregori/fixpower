from abc import ABC, abstractmethod

from app.schemas.item import ItemCreate


class ItemService(ABC):
    @abstractmethod
    def create_item(self, order_id: str, item_create: ItemCreate):
        pass

    @abstractmethod
    def get_items_by_order_id(self, order_id):
        pass

    @abstractmethod
    def delete_item_by_id(self, id):
        pass
