from pynamodb.attributes import MapAttribute, UnicodeAttribute


class UserAttribute(MapAttribute):
    id = UnicodeAttribute()
