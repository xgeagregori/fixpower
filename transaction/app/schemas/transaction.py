from pydantic import BaseModel
from typing import Optional
from enum import Enum

from app.schemas.product_listing import ProductListingCreate, ProductListingOut

from datetime import datetime


class TransactionState(str, Enum):
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    RETURNED = "RETURNED"
    CANCELLED = "CANCELLED"


class TransactionCreate(BaseModel):
    state: str = TransactionState.PAID
    product_listing: ProductListingCreate
    final_price: float


class TransactionUpdate(BaseModel):
    state: Optional[TransactionState]


class TransactionOut(BaseModel):
    id: str
    state: TransactionState
    product_listing: ProductListingOut
    final_price: float
    created_at: datetime
