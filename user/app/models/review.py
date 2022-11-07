from pynamodb.attributes import (
    MapAttribute,
    UnicodeAttribute,
    NumberAttribute,
    UTCDateTimeAttribute,
)

import datetime


class Review(MapAttribute):
    id = UnicodeAttribute()
    sender_id = UnicodeAttribute()
    rating = NumberAttribute()
    message = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now)
