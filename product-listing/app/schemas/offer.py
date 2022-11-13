from pydantic import BaseModel
from enum import Enum
from app.schemas.user import UserCreate



class OfferState(str, Enum):
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    PENDING = "PENDING"


class OfferCreate(BaseModel):
    state:OfferState = OfferState.PENDING
    sender: UserCreate
    recipient: UserCreate
    price: float


class OfferUpdate(BaseModel):
    state: OfferState
