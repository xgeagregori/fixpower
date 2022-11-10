from pydantic import BaseModel
from typing import Optional, List

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


class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]


class UserInDB(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str
    is_admin: bool
    profile: ProfileInDB


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool
    profile: ProfileOut
    created_at: datetime


class UserOutCurrent(BaseModel):
    id: str
    username: str
    email: str
    is_admin: bool
    profile: ProfileOut
    notifications: list
    created_at: datetime
