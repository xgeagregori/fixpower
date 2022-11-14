from fastapi import HTTPException, status

from app.models.offer import Offer
from app.schemas.offer import OfferCreate, OfferUpdate, OfferState
from app.services.product_listing_service_impl import ProductListingServiceImpl
from app.services.offer_service import OfferService

from uuid import uuid4


class OfferServiceImpl(OfferService):
    def __init__(self):
        self.product_listing_service = ProductListingServiceImpl()

    def create_offer(self, product_listing_id, offer_create: OfferCreate):
        generated_id = str(uuid4())
        offer = Offer(id=generated_id, **offer_create.dict())
        product_listing = self.product_listing_service.get_product_listing_by_id(
            product_listing_id
        )
        product_listing.offers.append(offer)
        product_listing.save()

        return offer.id

    def get_offers_by_product_listing_id(self, product_listing_id):
        product_listing = self.product_listing_service.get_product_listing_by_id(
            product_listing_id
        )

        return product_listing.offers

    def get_offer_by_id(self, product_listing_id, offer_id):
        product_listing = self.product_listing_service.get_product_listing_by_id(
            product_listing_id
        )
        for offer in product_listing.offers:
            if offer.id == offer_id:
                return offer
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found"
        )

    def update_offer_by_id(
        self, product_listing_id, offer_id, offer_update: OfferUpdate
    ):
        product_listing = self.product_listing_service.get_product_listing_by_id(
            product_listing_id
        )
        for offer in product_listing.offers:
            if offer.id == offer_id:
                if offer_update.state == OfferState.ACCEPTED:
                    if product_listing.sold:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Product already sold",
                        )
                    else:
                        offer.state = offer_update.state
                        product_listing.sold = True
        product_listing.save()
        return offer

    def delete_offer_by_id(self, product_listing_id, offer_id):
        product_listing = self.product_listing_service.get_product_listing_by_id(
            product_listing_id
        )
        for offer in product_listing.offers:
            if offer.id == offer_id:
                product_listing.offers.remove(offer)
                product_listing.save()
                return offer.id
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found"
        )
