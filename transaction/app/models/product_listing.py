from pynamodb.attributes import MapAttribute, UnicodeAttribute

class ProductListingAttribute(MapAttribute):
    id = UnicodeAttribute()