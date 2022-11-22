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
from app.schemas.item import ItemCreate, ItemOut
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
    # Shopping Cart routes
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
        check_user_permissions(current_user, order_create.user.id)

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
        check_user_is_admin(current_user)

        orders = self.order_service.get_orders()

        formatted_orders = []
        for order in orders:
            order.items = [ItemOut(**item.attribute_values) for item in order.items]
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
        check_user_permissions(current_user, order.user.id)

        order.items = [ItemOut(**item.attribute_values) for item in order.items]
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
        check_user_permissions(current_user, order.user.id)

        order.items = [ItemOut(**item.attribute_values) for item in order.items]
        order.user = UserOut(**order.user.attribute_values)
        formatted_order = OrderOut(**order.attribute_values)
        return formatted_order

    @app.delete("/shopping-carts/{order_id}", tags=["shopping-carts"])
    def delete_order_by_id(
        order_id: str, current_user=Depends(get_current_user), self=Depends(OrderDep)
    ):
        """Delete order by id"""
        order = self.order_service.get_order_by_id(order_id)
        check_user_permissions(current_user, order.user.id)

        order_id = self.order_service.delete_order_by_id(order_id)

        return {"id": order_id}

    # Item routes
    @app.post(
        "/shopping-carts/{order_id}/items",
        status_code=status.HTTP_201_CREATED,
        tags=["items"],
    )
    def create_item(
        order_id: str,
        item_create: ItemCreate,
        current_user=Depends(get_current_user),
        self=Depends(OrderDep),
    ):
        """Create item for order"""
        order = self.order_service.get_order_by_id(order_id)
        check_user_permissions(current_user, order.user.id)

        item_id = self.item_service.create_item(order_id, item_create)
        return {"id": item_id}

    @app.get("/shopping-carts/{order_id}/items", tags=["items"])
    def get_items_by_order_id(
        order_id: str,
        current_user=Depends(get_current_user),
        self=Depends(OrderDep),
    ):
        """Get items for order"""
        order = self.order_service.get_order_by_id(order_id)
        check_user_permissions(current_user, order.user.id)

        items = self.item_service.get_items_by_order_id(order_id)
        return [ItemOut(**item.attribute_values) for item in items]

    @app.delete("/shopping-carts/{order_id}/items/{item_id}", tags=["items"])
    def delete_item_by_id(
        order_id: str,
        item_id: str,
        current_user=Depends(get_current_user),
        self=Depends(OrderDep),
    ):
        """Delete item by id for order"""
        order = self.order_service.get_order_by_id(order_id)
        check_user_permissions(current_user, order.user.id)

        item_id = self.item_service.delete_item_by_id(order_id, item_id)
        return {"id": item_id}


app.include_router(router)
