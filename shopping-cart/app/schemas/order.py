from pydantic import BaseModel
from typing import Optional

from app.schemas.user import UserCreate, UserOut

from datetime import datetime


class OrderCreate(BaseModel):
    user: UserCreate
    price: float


class OrderUpdate(BaseModel):
    price: Optional[float]


class OrderOut(BaseModel):
    id: str
    user: UserOut
    items: list
    price: float
    created_at: datetime
