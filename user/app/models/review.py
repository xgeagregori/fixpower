from pynamodb.attributes import MapAttribute, UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute

class Review(MapAttribute):
    id = UnicodeAttribute()
    rating = NumberAttribute()
    message = UnicodeAttribute()
    created_at = UTCDateTimeAttribute()