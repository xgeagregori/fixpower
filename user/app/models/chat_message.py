from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, MapAttribute

import datetime


class ChatMessage(MapAttribute):
    id = UnicodeAttribute()
    sender_id = UnicodeAttribute()
    recipient_id = UnicodeAttribute()
    message = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now)
