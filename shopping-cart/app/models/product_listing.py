from pynamodb.attributes import UnicodeAttribute, MapAttribute


class ProductListing(MapAttribute):
    id = UnicodeAttribute()
