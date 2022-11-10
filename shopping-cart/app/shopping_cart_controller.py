from fastapi import FastAPI, HTTPException, status, Depends
from mangum import Mangum

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv


from app.dependencies.auth import (
    get_current_user,
    check_user_permissions,
    check_user_is_admin,
)
from app.dependencies.order import OrderDep
from app.schemas.order import OrderCreate, OrderUpdate, OrderOut
from app.schemas.user import UserOut


import os
import requests


app = FastAPI(
    root_path="/prod/shopping-cart-api/v1",
    title="Shopping Cart API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/shopping-cart-api/v1")
router = InferringRouter()


@cbv(router)
class ShoppingCartController:
    @app.post("/login", tags=["auth"])
    def login(form_data: OAuth2PasswordRequestForm = Depends()):
        token_response = requests.post(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/login",
            data=dict(username=form_data.username, password=form_data.password),
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_response.json()

    @app.post(
        "/shopping-carts", status_code=status.HTTP_201_CREATED, tags=["shopping-carts"]
    )
    def create_order(
        order_create: OrderCreate,
        current_user=Depends(get_current_user),
        self=Depends(OrderDep),
    ):
        """Create order"""
        order_id = self.order_service.create_order(order_create)
        if order_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Order not created",
            )
        return {"id": order_id}

    @app.get("/shopping-carts", tags=["shopping-carts"])
    def get_orders(current_user=Depends(get_current_user), self=Depends(OrderDep)):
        """Get orders"""
        orders = self.order_service.get_orders()

        formatted_orders = []
        for order in orders:

            order.user = UserOut(**order.user.attribute_values)
            formatted_order = OrderOut(**order.attribute_values)
            formatted_orders.append(formatted_order)

        return formatted_orders

    @app.get("/shopping-carts/{order_id}", tags=["shopping-carts"])
    def get_order_by_id(
        order_id: str, current_user=Depends(get_current_user), self=Depends(OrderDep)
    ):
        """Get Order by id"""
        order = self.order_service.get_order_by_id(order_id)
        order.user = UserOut(**order.user.attribute_values)
        formatted_order = OrderOut(**order.attribute_values)
        return formatted_order

    @app.patch("/shopping-carts/{order_id}", tags=["shopping-carts"])
    def update_order_by_id(
        order_id: str,
        order_update: OrderUpdate,
        current_user=Depends(get_current_user),
        self=Depends(OrderDep),
    ):
        """Update order by id"""
        order = self.order_service.update_order_by_id(order_id, order_update)
        return order.attribute_values

    @app.delete("/shopping-carts/{order_id}", tags=["shopping-carts"])
    def delete_order_by_id(
        order_id: str, current_user=Depends(get_current_user), self=Depends(OrderDep)
    ):
        """Delete order by id"""
        order_id = self.order_service.delete_order_by_id(order_id)

        return {"id": order_id}


app.include_router(router)
