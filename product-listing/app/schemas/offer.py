from pydantic import BaseModel
from enum import Enum
from app.schemas.user import UserCreate, UserOut



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

class OfferOut(BaseModel):
    id: str
    state: OfferState
    sender: UserOut
    recipient: UserOut
    price: float
