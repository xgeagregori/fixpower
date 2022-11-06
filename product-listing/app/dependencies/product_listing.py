from app.services.product_listing_service import ProductListingService
from app.services.product_listing_impl import ProductListingServiceImpl


class ProductListingDep:
    def __init__(self):
        self.product_listing_service: ProductListingService = ProductListingServiceImpl()
