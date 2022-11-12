from pydantic import BaseModel
from typing import Optional, Union

from app.schemas.settings import (
    SettingsCreate,
    SettingsUpdate,
    SettingsInDB,
    SettingsOut,
)


class ProfileCreate(BaseModel):
    picture: Optional[bytes] = None
    address: Optional[str] = ""
    settings: Optional[SettingsCreate] = {
        "sms_notifications": True,
        "email_notifications": True,
    }


class ProfileUpdate(BaseModel):
    picture: Optional[bytes]
    address: Optional[str]
    settings: Optional[SettingsUpdate]


class ProfileInDB(BaseModel):
    picture: Union[bytes, None]
    address: str
    settings: SettingsInDB


class ProfileOut(BaseModel):
    picture: Union[bytes, None]
    address: str
    settings: SettingsOut
    reviews: list
