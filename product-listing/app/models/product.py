from pynamodb.attributes import (
    UnicodeAttribute,
    MapAttribute,
)


class ProductAttribute(MapAttribute):
    name = UnicodeAttribute()
    brand = UnicodeAttribute()
    category = UnicodeAttribute()
    sub_category = UnicodeAttribute()
    issue = UnicodeAttribute(null=True)
