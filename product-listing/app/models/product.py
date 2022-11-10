from pynamodb.attributes import (
    UnicodeAttribute,
    MapAttribute,
)


class Product(MapAttribute):
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    brand = UnicodeAttribute()

class Component(Product):
    category = UnicodeAttribute()

class DamageProduct(Product):
    category = UnicodeAttribute()
    issue = UnicodeAttribute()

class RefurbishedProduct(Product):
    category = UnicodeAttribute()