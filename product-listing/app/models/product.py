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

# class ComponentAttribute(ProductAttribute):

# class DamagedProduct(ProductAttribute):
#     category = UnicodeAttribute()

# class RefurbishedProductAttribute(ProductAttribute):
#     category = UnicodeAttribute()