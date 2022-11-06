from fastapi import FastAPI, Depends, status, HTTPException
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.dependencies.product_listing import ProductListingDep
from app.schemas.product_listing import ProductListingCreate, ProductListingUpdate

app = FastAPI(
    # root_path="/prod/product-listing-api/v1",
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

    @app.get("/product-listings/{product_listing_id}")
    def get_product_listing_by_id(product_listing_id: str, self=Depends(ProductListingDep)):
        """Get product listing by id"""
        product_listing = self.product_listing_service.get_product_listing_by_id(product_listing_id)
        return product_listing.attribute_values

    @app.post("/product-listings", status_code=status.HTTP_201_CREATED)
    def create_product_listing(product_listing: ProductListingCreate, self=Depends(ProductListingDep)):
        """Create product listing"""
        product_listing_id = self.product_listing_service.create_product_listing(product_listing)
        if product_listing_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Product listing not created"
            )

        return {"id" : product_listing_id}

    @app.patch("/product-listings/{product_listing_id}")
    def update_product_listing_by_id(product_listing_id: str, product_listing: ProductListingUpdate, self=Depends(ProductListingDep)):
        """Update product listing by id"""
        product_listing = self.product_listing_service.update_product_listing_by_id(product_listing_id, product_listing)
        return product_listing.attribute_values

    @app.delete("/product-listings/{product_listing_id}")
    def create_product_listing(product_listing_id: str, product_listing: ProductListingUpdate, self=Depends(ProductListingDep)):
        product_listing_id = self.product_listing_service.delete_product_listing_by_id(product_listing_id)
        return {"id" : product_listing_id}

app.include_router(router)
