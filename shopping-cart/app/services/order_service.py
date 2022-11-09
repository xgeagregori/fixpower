from abc import ABC, abstractmethod
from app.schemas.order import OrderCreate, OrderUpdate


class OrderService(ABC):
    @abstractmethod
    def create_order(self, order_create: OrderCreate):
        pass

    @abstractmethod
    def get_orders(self):
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: str):
        pass

    @abstractmethod
    def update_order_by_id(self, order_id: str, order_update: OrderUpdate):
        pass

    @abstractmethod
    def delete_order_by_id(self, order_id: str):
        pass
