from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class OfferBase(BaseModel):
    sender: str
    recipient: str
    price: Optional[float]


class OfferCreate(OfferBase):
    pass


class OfferUpdate(OfferCreate):
    pass
