from fastapi import FastAPI, HTTPException, status, Depends
from mangum import Mangum

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.dependencies.auth import get_current_user, check_user_permissions, check_user_is_admin

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
        token_response = requests.post(os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/login", data=dict(username=form_data.username, password=form_data.password))

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_response.json()

    @app.get("/shopping-carts", tags=["shopping-carts"])
    def get_shopping_carts(current_user=Depends(get_current_user)):
        """Get shopping carts."""
        return {"message": "Welcome to the Shopping Cart Service!"}


app.include_router(router)
