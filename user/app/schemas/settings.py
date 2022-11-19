from pydantic import BaseModel
from typing import Optional
from enum import Enum


class PaymentMethod(str, Enum):
    APPLE_PAY = "APPLE_PAY"
    CREDIT_CARD = "CREDIT_CARD"
    GOOGLE_PAY = "GOOGLE_PAY"
    PAYPAL = "PAYPAL"


class SettingsCreate(BaseModel):
    sms_notifications: Optional[bool] = True
    email_notifications: Optional[bool] = True
    payment_method: Optional[PaymentMethod] = None


class SettingsUpdate(BaseModel):
    sms_notifications: Optional[bool]
    email_notifications: Optional[bool]
    payment_method: Optional[PaymentMethod]


class SettingsInDB(BaseModel):
    sms_notifications: bool
    email_notifications: bool
    payment_method: Optional[PaymentMethod]


class SettingsOut(BaseModel):
    sms_notifications: bool
    email_notifications: bool
    payment_method: Optional[PaymentMethod]
