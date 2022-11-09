from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, MapAttribute, NumberAttribute

import datetime



class Offer(MapAttribute):
    id = UnicodeAttribute(hash_key=True)
    state = UnicodeAttribute(default="Pending")
    sender = UnicodeAttribute()
    recipient = UnicodeAttribute()
    price = NumberAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now)
