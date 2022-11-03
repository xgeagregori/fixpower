from fastapi import FastAPI
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

app = FastAPI(
    root_path="/prod/shopping-cart-api/v1",
    title="Shopping Cart API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/shopping-cart-api/v1")
router = InferringRouter()


@cbv(router)
class ShoppingCartController:
    @app.get("/shopping-carts")
    def get_shopping_carts():
        """Get shopping carts."""
        return {"message": "Welcome to the Shopping Cart Service!"}


app.include_router(router)
