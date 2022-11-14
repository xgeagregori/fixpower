from pydantic import BaseModel
from typing import Optional

from datetime import datetime


class ChatMessageCreate(BaseModel):
    sender_id: str
    recipient_id: str
    message: str


class ChatMessageUpdate(BaseModel):
    message: Optional[str]


class ChatMessageOut(BaseModel):
    id: str
    sender_id: str
    recipient_id: str
    message: str
    created_at: datetime
