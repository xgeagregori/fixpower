from pynamodb.attributes import MapAttribute, UnicodeAttribute


class ProductListing(MapAttribute):
    id = UnicodeAttribute()
