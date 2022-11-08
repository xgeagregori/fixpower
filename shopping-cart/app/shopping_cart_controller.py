from fastapi import FastAPI, Depends, status, HTTPException
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv


from app.dependencies.order import OrderDep
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.order_service import OrderService
from app.services.order_service_impl import OrderServiceImpl

app = FastAPI(
    # root_path="/prod/shopping-cart-api/v1",
    title="Shopping Cart API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/shopping-cart-api/v1")
router = InferringRouter()


@cbv(router)
class ShoppingCartController:
    @app.post("/shopping-carts", status_code=status.HTTP_201_CREATED)
    def create_order(order_create: OrderCreate, self=Depends(OrderDep)):
        """Create an order"""
        order_id = self.order_service.create_order(order_create)
        if order_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Order not created",
            )
        return {"id": order_id}

    @app.get("/shopping-carts")
    def get_orders(self=Depends(OrderDep)):
        """Get all orders"""
        orders = self.order_service.get_orders()
        return [orders.attribute_values for orders in orders]

    @app.get("/shopping-carts/{order_id}")
    def get_order_by_id(order_id: str, self=Depends(OrderDep)):
        """Get Order by id."""
        order = self.order_service.get_order_by_id(order_id)
        # return order
        return {"id": order.id, **order.attribute_values}


app.include_router(router)
