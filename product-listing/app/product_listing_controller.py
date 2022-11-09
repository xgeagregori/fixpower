from fastapi import FastAPI, Depends, status, HTTPException
from mangum import Mangum

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.dependencies.product_listing import ProductListingDep
from app.dependencies.offer import OfferDep
from app.schemas.product_listing import ProductListingCreate, ProductListingUpdate
from app.schemas.offer import OfferCreate, OfferUpdate


app = FastAPI(
    # root_path="/prod/product-listing-api/v1",
    title="Product Listing API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/product-listing-api/v1")
router = InferringRouter()


@cbv(router)
class ProductListingController:
    @app.post("/product-listings", status_code=status.HTTP_201_CREATED)
    def create_product_listing(
        product_listing_create: ProductListingCreate, self=Depends(ProductListingDep)
    ):
        """Create product listing"""
        product_listing_id = self.product_listing_service.create_product_listing(
            product_listing_create
        )
        if product_listing_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Product listing not created",
            )

        return {"id": product_listing_id}

    @app.get("/product-listings")
    def get_users(self=Depends(ProductListingDep)):
        """Get all product listings"""
        product_listings = self.product_listing_service.get_product_listings()
        return [
            product_listing.attribute_values for product_listing in product_listings
        ]

    @app.get("/product-listings/{product_listing_id}")
    def get_product_listing_by_id(
        product_listing_id: str, self=Depends(ProductListingDep)
    ):
        """Get product listing by id"""
        product_listing = self.product_listing_service.get_product_listing_by_id(
            product_listing_id
        )
        return product_listing.attribute_values

    @app.patch("/product-listings/{product_listing_id}")
    def update_product_listing_by_id(
        product_listing_id: str,
        product_listing_update: ProductListingUpdate,
        self=Depends(ProductListingDep),
    ):
        """Update product listing by id"""
        product_listing = self.product_listing_service.update_product_listing_by_id(
            product_listing_id, product_listing_update
        )
        return product_listing.attribute_values

    @app.delete("/product-listings/{product_listing_id}")
    def delete_product_listing_by_id(
        product_listing_id: str, self=Depends(ProductListingDep)
    ):
        """Delete product listing by id"""
        product_listing_id = self.product_listing_service.delete_product_listing_by_id(
            product_listing_id
        )
        return {"id": product_listing_id}

    @app.post("/product-listings/{product_listing_id}/offers", status_code=status.HTTP_201_CREATED, tags=["offers"])
    def add_offer(product_listing_id: str, offer_create: OfferCreate, self=Depends(OfferDep)):
        """add offer"""
        offer_id = self.offer_service.add_offer(
            product_listing_id, offer_create)
        return {"id": offer_id}

    @app.get("/product-listings/{product_listing_id}/accept_offer")
    def accept_offer(product_listing_id: str, self=Depends(OfferDep)):
        """accept offer"""
        offer = self.offer_service.accept_offer(
            product_listing_id)
        return offer.attribute_values

    @app.get("/product-listings/{product_listing_id}/decline_offer")
    def decline_offer(product_listing_id: str, self=Depends(OfferDep)):
        """decline offer"""
        offer = self.offer_service.decline_offer(
            product_listing_id)
        return offer.attribute_values

    @app.post("/product-listings/{product_listing_id}/counter_offer", status_code=status.HTTP_201_CREATED, tags=["offers"])
    def counter_offer(product_listing_id: str, offer_update: OfferUpdate, self=Depends(OfferDep)):
        """counter offer"""
        product_listing = self.offer_service.counter_offer(
            product_listing_id, offer_update)
        return product_listing.attribute_values


app.include_router(router)
