from pynamodb.attributes import (
    MapAttribute,
    UnicodeSetAttribute
)

class UserAttribute(MapAttribute):
    id = UnicodeSetAttribute()