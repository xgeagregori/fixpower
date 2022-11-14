from pynamodb.attributes import (
    UnicodeAttribute,
    UTCDateTimeAttribute,
    MapAttribute,
    NumberAttribute,
)

from app.models.user import UserAttribute

import datetime


class Offer(MapAttribute):
    id = UnicodeAttribute(hash_key=True)
    state = UnicodeAttribute()
    sender = UserAttribute()
    recipient = UserAttribute()
    price = NumberAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now)
