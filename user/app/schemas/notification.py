from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class NotificationCreate(BaseModel):
    title: str
    message: str
    type: str


class NotificationUpdate(BaseModel):
    type: Optional[str]
    title: Optional[str]
    message: Optional[str]


class NotificationOut(BaseModel):
    id: str
    type: str
    title: str
    message: str
    created_at: datetime
