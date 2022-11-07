from pydantic import BaseModel
from typing import Optional


class SettingsCreate(BaseModel):
    sms_notifications: Optional[bool] = True
    email_notifications: Optional[bool] = True


class SettingsUpdate(BaseModel):
    sms_notifications: Optional[bool]
    email_notifications: Optional[bool]


class SettingsInDB(BaseModel):
    sms_notifications: bool
    email_notifications: bool


class SettingsOut(BaseModel):
    sms_notifications: bool
    email_notifications: bool
