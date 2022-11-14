from app.services.product_service import ProductService
from app.services.product_service_impl import ProductServiceImpl
from app.services.product_listing_service import ProductListingService
from app.services.product_listing_service_impl import ProductListingServiceImpl
from app.services.offer_service import OfferService
from app.services.offer_service_impl import OfferServiceImpl


class ProductListingDep:
    def __init__(self):
        self.product_listing_service: ProductListingService = (
            ProductListingServiceImpl()
        )

        self.product_service: ProductService = ProductServiceImpl()
        self.offer_service: OfferService = OfferServiceImpl()
