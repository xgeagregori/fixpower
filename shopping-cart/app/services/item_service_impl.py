from fastapi import HTTPException, status

from app.models.product_listing import ProductListing
from app.schemas.item import ItemCreate
from app.services.item_service import ItemService
from app.services.order_service_impl import OrderServiceImpl

from uuid import uuid4


class ItemServiceImpl(ItemService):
    def __init__(self):
        self.order_service = OrderServiceImpl()

    def create_item(self, order_id: str, item_create: ItemCreate):
        item = ProductListing(id=item_create.id)

        order = self.order_service.get_order_by_id(order_id)
        order.items.append(item)
        order.save()

        return item.id

    def get_items_by_order_id(self, order_id):
        order = self.order_service.get_order_by_id(order_id)
        return order.items

    def delete_item_by_id(self, order_id, item_id):
        order = self.order_service.get_order_by_id(order_id)
        for item in order.items:
            if item.id == item_id:
                order.items.remove(item)
                order.save()
                return item_id
