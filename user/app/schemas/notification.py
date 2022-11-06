from pydantic import BaseModel
from typing import Optional


class NotificationBase(BaseModel):
    title: str
    message: str


class NotificationCreate(NotificationBase):
    type: str


class NotificationUpdate(BaseModel):
    type: Optional[str]
    title: Optional[str]
    message: Optional[str]
