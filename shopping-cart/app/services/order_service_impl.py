from fastapi import HTTPException, status

# from pynamodb.exception import DoesNotExists, DeleteError

from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.order_service import OrderService

from uuid import uuid4


class OrderServiceImpl(OrderService):
    def create_order(self, order_create: OrderCreate):
        generated_id = str(uuid4())
        order = Order(id=generated_id, **order_create.dict())
        order.save()

        return order.id
