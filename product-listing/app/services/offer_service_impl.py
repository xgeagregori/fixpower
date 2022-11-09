from fastapi import HTTPException, status

from app.models.offer import Offer
from app.schemas.offer import OfferCreate, OfferUpdate
from app.services.product_listing_service_impl import ProductListingServiceImpl
from app.services.offer_service import OfferService

from uuid import uuid4

class OfferServiceImpl(OfferService):
    def __init__(self):
        self.product_listing_service = ProductListingServiceImpl()

    def add_offer(self, product_listing_id, offer_create: OfferCreate):
        generated_id = str(uuid4())
        offer = Offer(id=generated_id, **offer_create.dict())
        product_listing = self.product_listing_service.get_product_listing_by_id(product_listing_id)
        product_listing.offers.append(offer)
        product_listing.save()

        return offer.id
    
    def accept_offer(self, product_listing_id):
        product_listing = self.product_listing_service.get_product_listing_by_id(product_listing_id)
        product_listing.offers[-1].state = "Accepted"
        product_listing.save()
        return product_listing.offers[-1]

    def decline_offer(self, product_listing_id):
        product_listing = self.product_listing_service.get_product_listing_by_id(product_listing_id)
        product_listing.offers[-1].state = "Declined"
        product_listing.save()
        return product_listing.offers[-1]

    
    def counter_offer(self, product_listing_id, offer_update: OfferUpdate):
        product_listing = self.product_listing_service.get_product_listing_by_id(product_listing_id)
        product_listing.offers[-1].state = "Declined"
        generated_id = str(uuid4())
        offer = Offer(id=generated_id, **offer_update.dict())
        product_listing.offers.append(offer)
        product_listing.save()
        return product_listing