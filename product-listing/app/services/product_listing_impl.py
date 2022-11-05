from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.models.product_listing import ProductListing
from app.schemas.product_listing import ProductListingCreate 
from app.services.product_listing_service import Product_listingService

from uuid import uuid4


class ProductListingServiceImpl(Product_listingService):
    def create_product_listing(self, product_listing_create:ProductListingCreate):
        # If id is not provided, generate one
        if not product_listing_create.id:
            product_listing_create.id = str(uuid4())
        product_listing = ProductListing(**product_listing_create)
        product_listing.save()

        return product_listing.id


    def get_product_listing_by_product_id(self, id: str):
        
        return "hello world"