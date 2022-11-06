from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.models.product_listing import ProductListing
from app.schemas.product_listing import ProductListingCreate, ProductListingUpdate
from app.services.product_listing_service import ProductListingService

from uuid import uuid4


class ProductListingServiceImpl(ProductListingService):
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
                    detail="Product-listing already exists",
                )
        else:
            # If id is not provided, generate one
            product_listing_create.id = str(uuid4())

        # If product_listing_name already exists, raise exception
        try:
            product_listing_found = self.get_product_listing_by_id(
                product_listing_create.id
            )
            if product_listing_found:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Product-listing already exists",
                )
        except:
            pass

        product_listing = ProductListing(**product_listing_create.dict())
        product_listing.save()
        return product_listing.id

    def get_product_listing_by_id(self, id: str):
        try:
            return ProductListing.get(id)
        except ProductListing.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product-listing not found",
            )

    def update_product_listing_by_id(
        self, id: str, product_listing_update: ProductListingUpdate
    ):
        product_listing = self.get_product_listing_by_id(id)
        for key, value in product_listing_update.dict().items():
            if value:
                setattr(product_listing, key, value)

        product_listing.save()
        return product_listing

    def delete_product_listing_by_id(self, id: str):
        product_listing = self.get_product_listing_by_id(id)
        product_listing.delete()
        return id
