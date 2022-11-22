from app.services.item_service import ItemService
from app.services.item_service_impl import ItemServiceImpl
from app.services.order_service import OrderService
from app.services.order_service_impl import OrderServiceImpl


class OrderDep:
    def __init__(self):
        self.order_service: OrderService = OrderServiceImpl()

        self.item_service: ItemService = ItemServiceImpl()
