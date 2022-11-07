from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class ReviewCreate(BaseModel):
    sender_id: str
    rating: int
    message: Optional[str]


class ReviewUpdate(BaseModel):
    rating: Optional[int]
    message: Optional[str]


class ReviewInDB(BaseModel):
    id: str
    sender_id: str
    rating: int
    message: Optional[str]


class ReviewOut(BaseModel):
    id: str
    sender_id: str
    rating: int
    message: Optional[str]
    created_at: datetime
