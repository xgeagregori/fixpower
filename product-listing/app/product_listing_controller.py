from fastapi import FastAPI, Depends, status, HTTPException
from mangum import Mangum

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from app.dependencies.auth import (
    get_current_user,
    check_user_permissions,
    check_user_is_admin,
)
from app.dependencies.product_listing import ProductListingDep
from app.dependencies.offer import OfferDep
from app.schemas.product_listing import ProductListingCreate, ProductListingUpdate
from app.schemas.offer import OfferCreate, OfferUpdate


import os
import requests

app = FastAPI(
    # root_path="/prod/product-listing-api/v1",
    title="Product Listing API",
    version="1.0.0",
)
handler = Mangum(app, api_gateway_base_path="/product-listing-api/v1")
router = InferringRouter()


@cbv(router)
class ProductListingController:
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
        "/product-listings",
        status_code=status.HTTP_201_CREATED,
        tags=["product-listings"],
    )
    def create_product_listing(
        product_listing_create: ProductListingCreate,
        current_user=Depends(get_current_user),
        self=Depends(ProductListingDep),
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

    @app.get("/product-listings", tags=["product-listings"])
    def get_product_listings(
        current_user=Depends(get_current_user), self=Depends(ProductListingDep)
    ):
        """Get all product listings"""
        product_listings = self.product_listing_service.get_product_listings()
        return [
            product_listing.attribute_values for product_listing in product_listings
        ]

    @app.get("/product-listings/{product_listing_id}", tags=["product-listings"])
    def get_product_listing_by_id(
        product_listing_id: str,
        current_user=Depends(get_current_user),
        self=Depends(ProductListingDep),
    ):
        """Get product listing by id"""
        product_listing = self.product_listing_service.get_product_listing_by_id(
            product_listing_id
        )
        return product_listing.attribute_values

    @app.patch("/product-listings/{product_listing_id}", tags=["product-listings"])
    def update_product_listing_by_id(
        product_listing_id: str,
        product_listing_update: ProductListingUpdate,
        current_user=Depends(get_current_user),
        self=Depends(ProductListingDep),
    ):
        """Update product listing by id"""
        product_listing = self.product_listing_service.update_product_listing_by_id(
            product_listing_id, product_listing_update
        )
        return product_listing.attribute_values

    @app.delete("/product-listings/{product_listing_id}", tags=["product-listings"])
    def delete_product_listing_by_id(
        product_listing_id: str,
        current_user=Depends(get_current_user),
        self=Depends(ProductListingDep),
    ):
        """Delete product listing by id"""
        product_listing_id = self.product_listing_service.delete_product_listing_by_id(
            product_listing_id
        )
        return {"id": product_listing_id}

    @app.post(
        "/product-listings/{product_listing_id}/offers",
        status_code=status.HTTP_201_CREATED,
        tags=["offers"],
    )
    def create_offer(
        product_listing_id: str, offer_create: OfferCreate, self=Depends(OfferDep)
    ):
        """Create offer"""
        offer_id = self.offer_service.create_offer(product_listing_id, offer_create)
        return {"id": offer_id}

    @app.get("/product-listings/{product_listing_id}/offers", tags=["offers"])
    def get_offers_by_product_listing_id(
        product_listing_id: str, self=Depends(OfferDep)
    ):
        """Get offers by product listing id"""
        offers = self.offer_service.get_offers_by_product_listing_id(product_listing_id)
        return [offer.attribute_values for offer in offers]

    @app.get(
        "/product-listings/{product_listing_id}/offers/{offer_id}", tags=["offers"]
    )
    def get_offer_by_id(product_listing_id: str, offer_id: str, self=Depends(OfferDep)):
        """Get offer by id"""
        offer = self.offer_service.get_offer_by_id(product_listing_id, offer_id)
        return offer.attribute_values

    @app.patch(
        "/product-listings/{product_listing_id}/offers/{offer_id}", tags=["offers"]
    )
    def update_offer_by_id(
        product_listing_id: str,
        offer_id: str,
        offer_update: OfferUpdate,
        self=Depends(OfferDep),
    ):
        """Update offer"""
        offer = self.offer_service.update_offer_by_id(
            product_listing_id, offer_id, offer_update
        )
        return offer.attribute_values

    @app.delete(
        "/product-listings/{product_listing_id}/offers/{offer_id}", tags=["offers"]
    )
    def delete_offer_by_id(
        product_listing_id: str, offer_id: str, self=Depends(OfferDep)
    ):
        """Delete offer"""
        offer_id = self.offer_service.delete_offer_by_id(product_listing_id, offer_id)
        return {"id": offer_id}


app.include_router(router)
