from app.services.offer_service import OfferService
from app.services.offer_service_impl import OfferServiceImpl


class OfferDep:
    def __init__(self):
        self.offer_service: OfferService = (
            OfferServiceImpl()
        )
