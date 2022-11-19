from fastapi import HTTPException, status

from app.models.payment.payment_processor import PaymentProcessor
from app.models.product_listing import ProductListing
from app.schemas.product_listing import ProductListingCreate, ProductListingUpdate
from app.services.payment_service import PaymentService
from app.services.payment_service_impl import PaymentServiceImpl
from app.services.product_service import ProductService
from app.services.product_service_impl import ProductServiceImpl
from app.services.product_listing_service import ProductListingService

import os
import requests
from uuid import uuid4


class ProductListingServiceImpl(ProductListingService):
    def __init__(self):
        self.payment_service: PaymentService = PaymentServiceImpl()
        self.product_service: ProductService = ProductServiceImpl()

    def create_product_listing(self, product_listing_create: ProductListingCreate):
        product_listing_already_exists = False

        if product_listing_create.id:
            try:
                product_listing_found = self.get_product_listing_by_id(
                    product_listing_create.id
                )
                product_listing_already_exists = True
            except:
                pass
            # If id already exists, raise exception
            if product_listing_already_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product listing already exists",
                )
        else:
            # If id is not provided, generate one
            product_listing_create.id = str(uuid4())

        # Apply the proper create schema based on the product category
        try:
            product_listing_create.product = self.product_service.create_product(
                product_listing_create.product
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The specified details are not valid for this product category",
            )

        product_listing = ProductListing(**product_listing_create.dict())
        product_listing.save()
        return product_listing.id

    def get_product_listings(self):
        try:
            return ProductListing.scan()
        except ProductListing.ScanError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No product listings found",
            )

    def get_product_listing_by_id(self, id: str):
        try:
            return ProductListing.get(id)
        except ProductListing.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product listing not found",
            )

    def update_product_listing_by_id(
        self, id: str, product_listing_update: ProductListingUpdate
    ):
        product_listing = self.get_product_listing_by_id(id)
        for key, value in product_listing_update.dict().items():
            if key == "buyer":
                self.process_payment(value["id"])

                product_listing.sold = True
            if value:
                setattr(product_listing, key, value)

        product_listing.save()
        return product_listing

    def delete_product_listing_by_id(self, id: str):
        product_listing = self.get_product_listing_by_id(id)
        product_listing.delete()
        return id

    def process_payment(self, user_id):
        user = requests.get(
            os.getenv("AWS_API_GATEWAY_URL") + "/user-api/v1/users/" + user_id
        ).json()
        if user["settings"]["payment_method"]:
            payment_method = user["settings"]["payment_method"]
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has no payment method",
            )

        payment_strategy = self.payment_service.create_payment_strategy(payment_method)
        payment_processor = PaymentProcessor(payment_strategy)

        try:
            payment_processor.process()
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment failed",
            )
