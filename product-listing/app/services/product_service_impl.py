# from app.models.product import Component, RefurbishedProduct, DamagedProduct
# from app.schemas.product import ComponentCreate, DamagedProductCreate, RefurbishedProductCreate, ProductCategory, ProductCreate, ProductOut
from app.services.product_service import ProductService, ProductFactory
from app.services.product_listing_service_impl import ProductListingServiceImpl


class ProductServiceImpl(ProductService):
    def create_product(self, product_create):
        pass

    def create_product_out(self, product):
        pass
#     def __init__(self):
#         self.product_listing_service = ProductListingServiceImpl()

#     def create_product(self, product_create: ProductCreate):
#         category = product_create.category

#         if category == ProductCategory.component:
#             product = ComponentFactory().create_product(product_create)
#         elif category == ProductCategory.damage_product:
#             product = DamagedProductFactory().create_product(product_create)
#         elif category == ProductCategory.refurbishedproduct:
#             product = RefurbishedFactory().create_product(product_create)

#         return product


# class ComponentFactory(ProductFactory):
#     def create_product(self, product: ComponentCreate):
#         return Component(**product.dict())


# class DamagedProductFactory(ProductFactory):
#     def create_product(self, product: DamagedProductCreate):
#         return RefurbishedProduct(**product.dict())


# class RefurbishedFactory(ProductFactory):
#     def create_product(self, product: RefurbishedProductCreate):
#         return DamagedProduct(**product.dict())
