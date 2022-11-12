from pydantic import BaseModel
from typing import Optional

from app.schemas.profile import ProfileCreate, ProfileInDB, ProfileOut

from datetime import datetime


class UserCreate(BaseModel):
    id: Optional[str]
    username: str
    email: str
    password: str
    profile: Optional[ProfileCreate] = {
        "picture": None,
        "address": "",
        "settings": {
            "sms_notifications": True,
            "email_notifications": True,
        },
    }
    is_admin: Optional[bool] = False
    is_banned: Optional[bool] = False


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]
    is_banned: Optional[bool]


class UserInDB(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str
    is_admin: bool
    is_banned: bool
    profile: ProfileInDB


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool
    is_banned: bool
    profile: ProfileOut
    created_at: datetime


class UserOutCurrent(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool
    is_banned: bool
    profile: ProfileOut
    notifications: list
    created_at: datetime
