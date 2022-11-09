from pydantic import BaseModel
from enum import Enum
from typing import Optional


from datetime import datetime


class OfferState(str, Enum):
    accepted = "ACCEPTED"
    declined = "DECLINED"
    pending = "PENDING"


class OfferCreate(BaseModel):
    sender: str
    recipient: str
    price: float


class OfferUpdate(BaseModel):
    state: OfferState
