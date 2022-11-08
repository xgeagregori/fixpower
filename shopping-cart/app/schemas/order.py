from pydantic import BaseModel
from typing import Optional

from app.schemas.user import UserCreate


class OrderCreate(BaseModel):
    user: UserCreate
    price: int


class OrderUpdate(BaseModel):
    price: Optional[str]
