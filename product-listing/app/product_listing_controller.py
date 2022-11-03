from fastapi import FastAPI
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

app = FastAPI(
    root_path="/prod/product-listing-api/v1",
    title="Product Listing API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/product-listing-api/v1")
router = InferringRouter()


@cbv(router)
class ProductListingController:
    @app.get("/product-listings")
    def get_product_listings():
        """Get product listings."""
        return {"message": "Welcome to the Product Listing Service!"}


app.include_router(router)
