from fastapi import HTTPException, status
from pynamodb.exceptions import DoesNotExist, DeleteError

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

    def get_orders(self):
        try:
            return Order.scan()
        except Order.ScanError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Order found",
            )

    def get_order_by_id(self, order_id: str):
        try:
            order = Order.get(order_id)
            return order
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

    def update_order_by_id(self, order_id: str, order_update: OrderUpdate):
        order = self.get_order_by_id(order_id)
        for key, value in order_update.dict().items():
            if value:
                setattr(order, key, value)

        order.save()
        return order

    def delete_order_by_id(self, order_id: str):
        order = self.get_order_by_id(order_id)

        if order is not None:
            try:
                order.delete()
                return order.id
            except DeleteError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error on deletion",
                )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
