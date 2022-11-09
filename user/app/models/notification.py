from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, MapAttribute

import datetime


class Notification(MapAttribute):
    id = UnicodeAttribute()
    type = UnicodeAttribute()
    title = UnicodeAttribute()
    message = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now)
