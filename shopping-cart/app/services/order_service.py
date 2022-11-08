from abc import ABC, abstractmethod
from app.schemas.order import OrderCreate, OrderUpdate


class OrderService(ABC):
    @abstractmethod
    def create_order(self, order_create: OrderCreate):
        pass
